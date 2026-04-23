import streamlit as st
import pandas as pd
from datetime import date

from api_call import fetch_air_quality
from database import create_tables


# --------------------------------------------------
# App setup
# --------------------------------------------------
st.set_page_config(
    page_title="Air Quality Travel App",
    page_icon="🌍",
    layout="wide",
)

st.title("Air Quality Travel App")
st.markdown(
    "Check air quality during your stay in selected cities and estimate your personal risk "
    "based on your asthma level."
)

create_tables()


# --------------------------------------------------
# Config
# --------------------------------------------------
LOCATIONS = {
    "St.Gallen": (9.375902, 47.432292),
    "Zürich": (8.541694, 47.376887),
    "Bern": (7.447447, 46.947974),
    "Genf": (6.143158, 46.204391),
}

PARAMETERS = ["o3", "pm25", "pm10"]

POLLUTANT_LABELS = {
    "o3": "O₃",
    "pm25": "PM2.5",
    "pm10": "PM10",
}


# --------------------------------------------------
# Data loading
# --------------------------------------------------
@st.cache_data(ttl=1800)
def load_air_quality_data() -> pd.DataFrame:
    results = fetch_air_quality(
        coordinates=list(LOCATIONS.values()),
        radius=5000,
        limit=5,
        parameters=PARAMETERS,
    )

    city_names = list(LOCATIONS.keys())
    rows = []

    for city_name, entry in zip(city_names, results):
        readings = entry.get("readings", {})
        station_count = entry.get("station_count", 0)
        coordinate = entry.get("coordinate")

        for parameter in PARAMETERS:
            reading = readings.get(parameter)
            if reading is not None:
                rows.append(
                    {
                        "city": city_name,
                        "parameter": parameter,
                        "parameter_label": POLLUTANT_LABELS.get(parameter, parameter.upper()),
                        "value": reading.get("value"),
                        "unit": reading.get("units", ""),
                        "station_count": station_count,
                        "coordinate": coordinate,
                        "date": date.today(),
                    }
                )

    return pd.DataFrame(rows)


# --------------------------------------------------
# Risk logic
# --------------------------------------------------
def get_asthma_factor(asthma_level: str) -> float:
    mapping = {
        "None": 0.8,
        "Mild": 1.0,
        "Moderate": 1.2,
        "Severe": 1.5,
    }
    return mapping.get(asthma_level, 1.0)


def get_thresholds(rating_type: str) -> dict:
    if rating_type == "Strict":
        return {
            "o3": {"medium": 80, "high": 100},
            "pm25": {"medium": 10, "high": 20},
            "pm10": {"medium": 20, "high": 35},
        }
    if rating_type == "Lenient":
        return {
            "o3": {"medium": 100, "high": 140},
            "pm25": {"medium": 15, "high": 30},
            "pm10": {"medium": 30, "high": 50},
        }

    return {
        "o3": {"medium": 90, "high": 120},
        "pm25": {"medium": 12, "high": 25},
        "pm10": {"medium": 25, "high": 40},
    }


def calculate_pollutant_score(parameter: str, value: float, thresholds: dict) -> int:
    if parameter not in thresholds:
        return 0

    if value >= thresholds[parameter]["high"]:
        return 2
    if value >= thresholds[parameter]["medium"]:
        return 1
    return 0


def calculate_risk(city_df: pd.DataFrame, asthma_level: str, rating_type: str):
    thresholds = get_thresholds(rating_type)
    asthma_factor = get_asthma_factor(asthma_level)

    detail_rows = []
    base_score = 0

    for _, row in city_df.iterrows():
        parameter = row["parameter"]
        value = row["value"]

        pollutant_score = calculate_pollutant_score(parameter, value, thresholds)
        base_score += pollutant_score

        detail_rows.append(
            {
                "Pollutant": row["parameter_label"],
                "Measured value": round(float(value), 2),
                "Unit": row["unit"],
                "Pollutant score": pollutant_score,
            }
        )

    adjusted_score = base_score * asthma_factor

    if adjusted_score >= 4:
        risk_level = "High"
    elif adjusted_score >= 2:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return risk_level, adjusted_score, pd.DataFrame(detail_rows)


def get_recommendation(risk_level: str) -> str:
    if risk_level == "High":
        return (
            "Today’s air quality may be risky for you. Try to reduce time outdoors, "
            "avoid intense activity outside, and take your inhaler or medication with you."
        )
    if risk_level == "Medium":
        return (
            "The situation is manageable, but be careful. Pay attention to your symptoms, "
            "avoid long intense outdoor activity, and keep medication nearby."
        )
    return (
        "Current conditions suggest a relatively low risk. Outdoor activity should usually be fine, "
        "but still listen to your body."
    )


def format_city_summary(city_df: pd.DataFrame) -> str:
    if city_df.empty:
        return "No current data available."

    station_count = int(city_df["station_count"].iloc[0])
    coordinate = city_df["coordinate"].iloc[0]
    return f"Using current measurements near {coordinate} from {station_count} station(s)."


# --------------------------------------------------
# Main data fetch
# --------------------------------------------------
try:
    df = load_air_quality_data()
except Exception as e:
    st.error(f"Error while fetching API data: {e}")
    st.stop()

if df.empty:
    st.warning("No air quality data could be loaded.")
    st.stop()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.header("Your inputs")

selected_city = st.sidebar.selectbox(
    "Choose a city",
    options=sorted(df["city"].unique().tolist()),
)

asthma_level = st.sidebar.selectbox(
    "How severe is your asthma?",
    options=["None", "Mild", "Moderate", "Severe"],
    index=1,
)

rating_type = st.sidebar.selectbox(
    "Risk rating type",
    options=["Lenient", "Standard", "Strict"],
    index=1,
)

today = date.today()

start_date = st.sidebar.date_input(
    "Travel start date",
    value=today,
    min_value=today,
    max_value=today,
)

end_date = st.sidebar.date_input(
    "Travel end date",
    value=today,
    min_value=today,
    max_value=today,
)

st.sidebar.info(
    "Currently only today's API data is available. "
    "Forecast and future dates can be added later."
)

view_mode = st.sidebar.radio(
    "Display mode",
    options=["Chart", "Table"],
)


# --------------------------------------------------
# Selected city
# --------------------------------------------------
city_df = df[df["city"] == selected_city].copy()

st.subheader(f"Current air quality for {selected_city}")
st.caption(format_city_summary(city_df))

if city_df.empty:
    st.warning("No data available for the selected city.")
    st.stop()


# --------------------------------------------------
# Metrics + recommendation
# --------------------------------------------------
risk_level, risk_score, risk_details_df = calculate_risk(
    city_df=city_df,
    asthma_level=asthma_level,
    rating_type=rating_type,
)

recommendation = get_recommendation(risk_level)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Asthma level", asthma_level)

with col2:
    st.metric("Risk rating", risk_level)

with col3:
    st.metric("Risk score", f"{risk_score:.1f}")

if risk_level == "High":
    st.error(recommendation)
elif risk_level == "Medium":
    st.warning(recommendation)
else:
    st.success(recommendation)


# --------------------------------------------------
# Pollutant display
# --------------------------------------------------
st.subheader("Pollutant data")

display_df = city_df[["parameter_label", "value", "unit"]].copy()
display_df.columns = ["Pollutant", "Value", "Unit"]

if view_mode == "Table":
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    chart_df = city_df[["parameter_label", "value"]].copy()
    chart_df.columns = ["Pollutant", "Value"]
    st.bar_chart(chart_df.set_index("Pollutant"))


# --------------------------------------------------
# Detail table
# --------------------------------------------------
st.subheader("Detailed risk evaluation")
st.dataframe(risk_details_df, use_container_width=True, hide_index=True)


# --------------------------------------------------
# Raw data
# --------------------------------------------------
with st.expander("Show raw API-based data"):
    st.dataframe(city_df, use_container_width=True, hide_index=True)