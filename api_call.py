"""
api_call

.env:
    OPENAQ_API_KEY=your_api_key_here

Usage:
    from api_call import fetch_air_quality

    results = fetch_air_quality(
        coordinates=[(9.108883, 47.567735), (13.404954, 52.520008)],
        radius=20000,
        limit=5,
        parameters=["pm25", "o3", "pm10"],
    )

    for entry in results:
        print(entry["coordinate"])
        for loc in entry["locations"]:
            print(loc["location"]["name"], loc["readings"])
"""

from __future__ import annotations

import os
from collections import defaultdict
from typing import Any

from dotenv import load_dotenv
from openaq import OpenAQ

def _first_non_null(*values: Any) -> Any:
    """Return the first value that is not None."""
    for v in values:
        if v is not None:
            return v
    return None


def _normalize_parameter_name(name: Any) -> str | None:
    """Lowercase-strip a parameter name, or return None."""
    if name is None:
        return None
    return str(name).strip().lower()


def _format_location(loc: dict[str, Any]) -> dict[str, Any]:
    """Extract the fields we care about from a raw location dict."""
    country = loc.get("country") or {}
    provider = loc.get("provider") or {}
    coords = loc.get("coordinates") or {}
    return {
        "id": loc.get("id"),
        "name": loc.get("name"),
        "locality": loc.get("locality"),
        "country_code": country.get("code"),
        "country_name": country.get("name"),
        "provider": provider.get("name"),
        "latitude": coords.get("latitude"),
        "longitude": coords.get("longitude"),
    }


def _build_sensor_map(sensors: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    """Index sensor metadata by sensor id."""
    sensor_map: dict[int, dict[str, Any]] = {}
    for sensor in sensors:
        sensor_id = sensor.get("id")
        if sensor_id is None:
            continue
        parameter = sensor.get("parameter") or {}
        sensor_map[sensor_id] = {
            "parameter_name": _normalize_parameter_name(parameter.get("name")),
            "units": parameter.get("units"),
        }
    return sensor_map


def _label_latest_rows(
    latest: list[dict[str, Any]],
    sensor_map: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Attach parameter metadata to each raw latest-value row."""
    labeled = []
    for item in latest:
        sensor_id = _first_non_null(item.get("sensorsId"), item.get("sensors_id"))
        meta = sensor_map.get(sensor_id, {})
        labeled.append({
            "parameter_name": meta.get("parameter_name"),
            "units": meta.get("units"),
            "value": item.get("value"),
        })
    return labeled


def _filter_parameters(
    rows: list[dict[str, Any]],
    parameters: set[str],
) -> list[dict[str, Any]]:
    """Keep only rows whose parameter_name is in the requested set."""
    return [r for r in rows if r.get("parameter_name") in parameters]


def _average_by_parameter(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Group rows by parameter_name and average non-null values.

    Returns a dict like:
        {"pm25": {"value": 12.3, "units": "µg/m³"}, ...}

    Parameters with no non-null values are omitted.
    """
    groups: dict[str, list] = defaultdict(list)
    units_map: dict[str, str | None] = {}

    for row in rows:
        param = row.get("parameter_name")
        value = row.get("value")
        if param is None:
            continue
        if value is not None:
            groups[param].append(value)
        # Remember units for this parameter (last seen wins, they should all match)
        units_map.setdefault(param, row.get("units"))

    return {
        param: {"value": sum(values) / len(values), "units": units_map.get(param)}
        for param, values in groups.items()
        if values
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def fetch_air_quality(
    coordinates: list[tuple[float, float]],
    radius: int,
    limit: int,
    parameters: list[str],
) -> list[dict[str, Any]]:
    """
    Fetch averaged air-quality readings near one or more coordinates.

    Args:
        coordinates: List of (longitude, latitude) pairs to query.
        radius:      Search radius in metres, applied to every coordinate.
        limit:       Maximum number of monitoring locations per coordinate.
        parameters:  Parameter names to include, e.g. ["pm25", "o3", "pm10"].
                     Names are normalised to lowercase before matching.

    Returns:
        One entry per input coordinate::

            [
              {
                "coordinate": (lon, lat),
                "station_count": 2,
                "readings": {
                  "pm25": {"value": 12.3, "units": "µg/m³"},
                  "o3":   {"value": 45.1, "units": "µg/m³"},
                }
              },
              ...
            ]

        ``readings`` contains only parameters that had at least one non-null
        sensor value. Values are averaged across all stations within the
        radius (nulls excluded).

    Raises:
        EnvironmentError: If OPENAQ_API_KEY is not set.
        Exception:        Propagates any OpenAQ API errors.
    """
    load_dotenv()

    api_key = os.getenv("OPENAQ_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAQ_API_KEY is not set in environment / .env file")

    # Preserve input order for output; deduplicate while keeping first occurrence
    params_ordered = list(dict.fromkeys(_normalize_parameter_name(p) for p in parameters))
    param_set = set(params_ordered)
    results = []

    with OpenAQ(api_key=api_key) as client:
        for lon, lat in coordinates:
            locations_resp = client.locations.list(
                coordinates=(lat, lon),
                radius=radius,
                limit=limit,
            ).dict()

            # Collect all matching rows from every station in the radius
            all_rows: list[dict[str, Any]] = []
            station_count = 0

            for loc in locations_resp.get("results") or []:
                location_id = _format_location(loc)["id"]

                sensors = (client.locations.sensors(location_id).dict().get("results") or [])
                sensor_map = _build_sensor_map(sensors)

                latest = (client.locations.latest(location_id).dict().get("results") or [])
                rows = _label_latest_rows(latest, sensor_map)
                filtered = _filter_parameters(rows, param_set)

                if filtered:
                    all_rows.extend(filtered)
                    station_count += 1

            averaged = _average_by_parameter(all_rows)
            results.append({
                "coordinate": (lon, lat),
                "station_count": station_count,
                "readings": {p: averaged[p] for p in params_ordered if p in averaged},
            })

    return results

