# discover_stations.py, a one time script
# update the stations every now and then :)

import json
import os
from dotenv import load_dotenv
from openaq import OpenAQ
from rate_limiter import RateLimiter

def fetch_station_ids(coordinates, radius=20000, limit=10, per_location=3):
    load_dotenv()
    api_key = os.getenv("OPENAQ_API_KEY")

    if not api_key:
        raise EnvironmentError("OPENAQ_API_KEY not set")

    limiter = RateLimiter()
    request_count = 0
    result = {}

    with OpenAQ(api_key=api_key) as client:
        for idx, (lon, lat) in enumerate(coordinates, start=1):
            print(f"\n📍 [{idx}/{len(coordinates)}] Processing {lat},{lon}")

            # --- locations.list ---
            limiter.wait()
            resp = client.locations.list(
                coordinates=(lat, lon),
                radius=radius,
                limit=limit,
            ).dict()
            request_count += 1

            station_ids = []
            for loc in resp.get("results", []):
                if len(station_ids) >= per_location:
                    break  # ✅ stop early once we have enough

                loc_id = loc.get("id")
                loc_name = loc.get("name")

                # 1. fetch sensors for this station
                limiter.wait()
                sensors = client.locations.sensors(loc_id).dict().get("results", [])
                request_count += 1

                # 2. build set of available parameters
                available = {
                    s.get("parameter", {}).get("name", "").lower()
                    for s in sensors
                }

                # 3. filter HERE (this is the key step)
                required = {"pm25", "o3", "pm10"}
                if not required.issubset(available):
                    continue  # ❌ skip this station entirely

                # 4. only reached if station is valid
                station_ids.append({
                    "id": loc_id,
                    "name": loc_name,
                })

                print(f"  ✅ Found valid station: {loc_name}")

            print(f"  ✔ Collected {len(station_ids)} stations")
            print(f"  🔢 Total API calls so far: {request_count}")

            key = f"{lon},{lat}"
            result[key] = station_ids

    return result


if __name__ == "__main__":
    # IMPORTANT: coordinates are (lon, lat)
    coords = [
        (2.3522, 48.8566),   # Paris
        (8.5417, 47.3769),   # Zürich
        (13.4050, 52.5200),  # Berlin
        (-0.1278, 51.5074),  # London
        (8.6821, 50.1109),   # Frankfurt
        (4.3517, 50.8503),   # Brussels
        (18.0686, 59.3293),  # Stockholm
    ]

    stations = fetch_station_ids(coords)

    with open("stations.json", "w") as f:
        json.dump(stations, f, indent=2)

    print("\nSaved station IDs to stations.json")