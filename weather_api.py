import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


# -----------------------------
# Setup client (reuse globally)
# -----------------------------
def create_openmeteo_client():
    cache_session = requests_cache.CachedSession(
        '.cache',
        expire_after=3600
    )
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)


openmeteo = create_openmeteo_client()


# -----------------------------
# Core fetch function (single location)
# -----------------------------
def fetch_weather(lat, lon, timezone="Europe/Berlin", past_days=28, forecast_days=3):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_mean",
            "relative_humidity_2m_mean"
        ],
        "timezone": timezone,
        "past_days": past_days,
        "forecast_days": forecast_days,
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Daily data
    daily = response.Daily()

    dates = pd.date_range(
        start=pd.to_datetime(
            daily.Time() + response.UtcOffsetSeconds(),
            unit="s",
            utc=True
        ),
        end=pd.to_datetime(
            daily.TimeEnd() + response.UtcOffsetSeconds(),
            unit="s",
            utc=True
        ),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )

    daily_df = pd.DataFrame({
        "date": dates,
        "temperature_mean": daily.Variables(0).ValuesAsNumpy(),
        "relative_humidity_mean": daily.Variables(1).ValuesAsNumpy(),
    })

    return {
        "coordinates": (response.Latitude(), response.Longitude()),
        "elevation": response.Elevation(),
        "timezone": response.Timezone(),
        "timezone_abbreviation": response.TimezoneAbbreviation(),
        "utc_offset_seconds": response.UtcOffsetSeconds(),
        "daily": daily_df
    }


# -----------------------------
# Batch function (multiple locations)
# -----------------------------
def fetch_weather_batch(locations):
    """
    locations: list of dicts like:
    [
        {"name": "Zurich", "lat": 47.37, "lon": 8.54},
        {"name": "Bern", "lat": 46.95, "lon": 7.44}
    ]
    """

    results = {}

    for loc in locations:
        name = loc.get("name", f"{loc['lat']},{loc['lon']}")

        results[name] = fetch_weather(
            lat=loc["lat"],
            lon=loc["lon"]
        )

    return results