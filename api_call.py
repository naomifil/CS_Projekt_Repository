"""
openaq_lib — reusable OpenAQ air-quality fetcher.

Install:
    pip install openaq python-dotenv

.env:
    OPENAQ_API_KEY=your_api_key_here

Usage:
    from openaq_lib import find_stations, fetch_readings_by_ids, fetch_air_quality
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Any
from rate_limiter import RateLimiter
from dotenv import load_dotenv
from openaq import OpenAQ


# ---------------------------------------------------------------------------
# DTOs
# ---------------------------------------------------------------------------

@dataclass
class Reading:
    """A single averaged sensor reading for one parameter."""
    value: float
    units: str | None


@dataclass
class Station:
    """A monitoring station near a queried coordinate."""
    id: int
    name: str | None
    locality: str | None
    country_code: str | None
    country_name: str | None
    provider: str | None
    latitude: float | None
    longitude: float | None


@dataclass
class AggregatedReadings:
    """Averaged readings across one or more stations."""
    station_count: int
    readings: dict[str, Reading]  # parameter name → Reading, in requested order


@dataclass
class CoordinateReadings:
    """Averaged readings for a single queried coordinate."""
    coordinate: tuple[float, float]
    station_count: int
    readings: dict[str, Reading]  # parameter name → Reading, in requested order


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_api_key() -> str:
    load_dotenv()
    key = os.getenv("OPENAQ_API_KEY")
    if not key:
        raise EnvironmentError("OPENAQ_API_KEY is not set in environment / .env file")
    return key


def _first_non_null(*values: Any) -> Any:
    for v in values:
        if v is not None:
            return v
    return None


def _normalize(name: Any) -> str | None:
    if name is None:
        return None
    return str(name).strip().lower()

def _average_by_parameter(
    rows: list[dict[str, Any]],
    params_ordered: list[str],
) -> dict[str, Reading]:
    """Average non-null values per parameter and return in requested order."""
    groups: dict[str, list[float]] = defaultdict(list)
    units_map: dict[str, str | None] = {}

    for row in rows:
        param = row.get("parameter_name")
        value = row.get("value")
        if param is None:
            continue
        if value is not None:
            groups[param].append(value)
        units_map.setdefault(param, row.get("units"))

    return {
        p: Reading(value=sum(groups[p]) / len(groups[p]), units=units_map.get(p))
        for p in params_ordered
        if groups[p]
    }


def _list_stations(
    client: OpenAQ,
    coordinate: tuple[float, float],
    radius: int,
    limit: int,
) -> list[Station]:
    lon, lat = coordinate
    resp = client.locations.list(
        coordinates=(lat, lon),
        radius=radius,
        limit=limit,
    ).dict()

    stations = []
    for loc in resp.get("results") or []:
        country = loc.get("country") or {}
        provider = loc.get("provider") or {}
        coords = loc.get("coordinates") or {}
        stations.append(Station(
            id=loc.get("id"),
            name=loc.get("name"),
            locality=loc.get("locality"),
            country_code=country.get("code"),
            country_name=country.get("name"),
            provider=provider.get("name"),
            latitude=coords.get("latitude"),
            longitude=coords.get("longitude"),
        ))
    return stations


def _aggregate_by_ids(
    client: OpenAQ,
    station_ids: list[int],
    params_ordered: list[str],
    param_set: set[str],
    limiter: RateLimiter | None = None,
) -> AggregatedReadings:

    all_rows: list[dict[str, Any]] = []
    station_count = 0

    for i, station_id in enumerate(station_ids, start=1):
        print(f"[{i}/{len(station_ids)}] Station {station_id}")

        if limiter:
            limiter.wait()

        sensors = client.locations.sensors(station_id).dict().get("results") or []

        rows = []
        for s in sensors:
            param = _normalize((s.get("parameter") or {}).get("name"))
            if param not in param_set:
                continue

            latest = s.get("latest") or {}
            value = latest.get("value")

            if value is None:
                continue

            rows.append({
                "parameter_name": param,
                "units": (s.get("parameter") or {}).get("units"),
                "value": value,
            })

        if rows:
            all_rows.extend(rows)
            station_count += 1

    return AggregatedReadings(
        station_count=station_count,
        readings=_average_by_parameter(all_rows, params_ordered),
    )

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def find_stations(
    coordinate: tuple[float, float],
    radius: int,
    limit: int,
) -> list[Station]:
    """
    Return monitoring stations within radius metres of a coordinate.

    Args:
        coordinate: (longitude, latitude) of the search centre.
        radius:     Search radius in metres.
        limit:      Maximum number of stations to return.

    Returns:
        List of Station objects. Use Station.id with fetch_readings_by_ids
        to manually select which stations to include.
    """
    with OpenAQ(api_key=_get_api_key()) as client:
        return _list_stations(client, coordinate, radius, limit)

def get_average_for_stations(
    station_ids: list[int],
    parameters: list[str],
    client: OpenAQ,
    limiter: RateLimiter | None = None,
) -> AggregatedReadings:

    if not station_ids:
        return AggregatedReadings(station_count=0, readings={})

    params_ordered = list(dict.fromkeys(_normalize(p) for p in parameters))
    param_set = set(params_ordered)

    return _aggregate_by_ids(
        client,
        station_ids,
        params_ordered,
        param_set,
        limiter,
    )

def get_aggregates_from_json(parameters: list[str]):
    with open("stations.json") as f:
        station_map = json.load(f)

    limiter = RateLimiter(min_interval=1.1)
    results = {}

    with OpenAQ(api_key=_get_api_key()) as client:
        for key, stations in station_map.items():
            lon, lat = map(float, key.split(","))

            station_ids = [
                s["id"] for s in stations if s.get("id") is not None
            ]

            agg = get_average_for_stations(
                station_ids,
                parameters,
                client,
                limiter,
            )

            results[(lon, lat)] = agg

    return results

def fetch_air_quality(
    coordinates: list[tuple[float, float]],
    radius: int,
    limit: int,
    parameters: list[str],
) -> list[CoordinateReadings]:
    """
    Fetch averaged air-quality readings near one or more coordinates.

    Combines find_stations and fetch_readings_by_ids in a single call,
    reusing one API connection across all coordinates.

    Args:
        coordinates: List of (longitude, latitude) pairs to query.
        radius:      Search radius in metres, applied to every coordinate.
        limit:       Maximum number of stations to consider per coordinate.
        parameters:  Parameter names to include, e.g. ["o3", "pm25", "pm10"].
                     Output readings follow this order; names are normalised
                     to lowercase.

    Returns:
        One CoordinateReadings per input coordinate with:
        - coordinate:    the (lon, lat) pair
        - station_count: number of stations that contributed readings
        - readings:      parameter name → Reading (value + units),
                         in the order given by parameters
    """
    params_ordered = list(dict.fromkeys(_normalize(p) for p in parameters))
    param_set = set(params_ordered)

    with OpenAQ(api_key=_get_api_key()) as client:
        results = []
        for coordinate in coordinates:
            stations = _list_stations(client, coordinate, radius, limit)
            agg = _aggregate_by_ids(client, [s.id for s in stations], params_ordered, param_set)
            results.append(CoordinateReadings(
                coordinate=coordinate,
                station_count=agg.station_count,
                readings=agg.readings,
            ))
        return results