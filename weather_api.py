import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


# -----------------------------
# Setup client (reuse globally)
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
# Code adapted from API documentation
def fetch_weather(lat, lon, timezone="Europe/Berlin", past_days=28, forecast_days=14):
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

    # Daily data -> one instance for each day for 28 days in past and 14 days forecast
    # Code here from API documentation and debugged/rewritten with ChatGPT
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
    # create df with fetched data
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
# Using fetch_weather which was for one location only, tailored to match json file structure with predefined stations
# from one shot query
def fetch_weather_batch(locations):
    results = {}

    for loc in locations:
        name = loc.get("name", f"{loc['lat']},{loc['lon']}")

        # fetch_weather for each location available in locations
        results[name] = fetch_weather(
            lat=loc["lat"],
            lon=loc["lon"]
        )

    return results