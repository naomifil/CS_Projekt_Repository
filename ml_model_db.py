import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load database
conn = sqlite3.connect("air_quality.db")

air = pd.read_sql_query("SELECT * FROM air_quality", conn)
weather = pd.read_sql_query("SELECT * FROM weather_daily", conn)

print("Air shape:", air.shape)
print("Weather shape:", weather.shape)

# Data preparation
air["timestamp"] = pd.to_datetime(air["timestamp"])
air["date"] = air["timestamp"].dt.date

weather["date"] = pd.to_datetime(weather["date"]).dt.date

air["location_id"] = air["location_id"].astype(str)
weather["location_id"] = weather["location_id"].astype(str)

# Aggregate data
air_daily = air.groupby(["location_id", "date"]).agg({
    "pm25": "mean",
    "pm10": "mean",
    "o3": "mean"
}).reset_index()

print("Air daily shape:", air_daily.shape)

# Debug
common_locations = set(air_daily["location_id"]).intersection(set(weather["location_id"]))
common_dates = set(air_daily["date"]).intersection(set(weather["date"]))

print("\nCommon locations:", len(common_locations))
print("Common dates:", len(common_dates))

if len(common_locations) == 0 or len(common_dates) == 0:
    raise ValueError(
        "No overlap between air and weather data. "
        "Check location_id and date consistency in database."
    )

# Merge datasets
data = pd.merge(
    weather,
    air_daily,
    on=["location_id", "date"],
    how="inner"
)

print("\nMerged dataset shape:", data.shape)

# Final safety check
if data.shape[0] == 0:
    raise ValueError("Merge still empty after alignment.")

# Features (X) and target (y)
X = data[["temperature_mean", "relative_humidity_mean"]]
y = data[["pm25", "pm10", "o3"]]

data_clean = pd.concat([X, y], axis=1).dropna()

X = data_clean[["temperature_mean", "relative_humidity_mean"]]
y = data_clean[["pm25", "pm10", "o3"]]

print("Final X shape:", X.shape)
print("Final y shape:", y.shape)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate model
mse = mean_squared_error(y_test, y_pred)
print("\nMean Squared Error:", mse)

# Show predictions
pred_df = pd.DataFrame(y_pred, columns=["pm25", "pm10", "o3"])
print("\nPredictions (sample):")
print(pred_df.head())

# Future prediction
future_weather = pd.DataFrame(
    [[20, 60]],
    columns=["temperature_mean", "relative_humidity_mean"]
)

future_pred = model.predict(future_weather)

future_df = pd.DataFrame(future_pred, columns=["pm25", "pm10", "o3"])
print("\nFuture Prediction:")
print(future_df)