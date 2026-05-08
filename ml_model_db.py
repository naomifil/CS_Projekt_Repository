"""
Machine Learning Module

This code was rewritten with the assistance of ChatGPT (OpenAI).

The use of AI included:
- Code structuring and refactoring
- Debugging support

Singular section generated entirely by ChatGPT indicated accordingly.

All design decisions, testing and integration were performed by the author.
"""

import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

DB_PATH = "air_quality2.db"

# Load database: imports raw data from two relevant tables in air_quality2 database for ml pipeline
def load_data(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)

    air = pd.read_sql_query("SELECT * FROM air_quality", conn)
    weather = pd.read_sql_query("SELECT * FROM weather_daily", conn)

    conn.close()
    return air, weather

# Data preparation: transforms raw data into usable daily datasets for ml
def preprocess_data(air, weather):

    air["timestamp"] = pd.to_datetime(
        air["timestamp"],
        utc=True
    )

    air["date"] = air["timestamp"].dt.date

    weather["date"] = pd.to_datetime(
        weather["date"],
        utc=True
    ).dt.date

    air["location_id"] = air["location_id"].astype(str)
    weather["location_id"] = weather["location_id"].astype(str)

    air_daily = air.groupby(["location_id", "date"]).agg({
        "pm25": "mean",
        "pm10": "mean",
        "o3": "mean"
    }).reset_index()

    return air_daily, weather

# Merge datasets: creates a single dataset containing both weather features and air pollution measurements
def merge_data(air_daily, weather):
    data = pd.merge(
        weather,
        air_daily,
        on=["location_id", "date"],
        how="inner"
    )

    if data.empty:
        raise ValueError("Merged dataset is empty. Check your DB data.")

    return data

# Features (X) and target (y): separates dataset into input variables and prediction targets for ml training
# Features selected for initial regression model: temperature and humidity (affect outcome), no other variables available in dataset
def prepare_features(data):
    X = data[["temperature_mean", "relative_humidity_mean"]]
    y = data[["pm25", "pm10", "o3"]]

    data_clean = pd.concat([X, y], axis=1).dropna()

    X = data_clean[["temperature_mean", "relative_humidity_mean"]]
    y = data_clean[["pm25", "pm10", "o3"]]

    if X.empty:
        raise ValueError("No valid data after cleaning.")

    return X, y

# Train model: teaches ml model to predict pollution levels from weather data using regression tree
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = DecisionTreeRegressor(
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model, X_test, y_test

# Evaluate model: measures how accurate pollutant predictions are compared to real historic API values
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    pred_df = pd.DataFrame(y_pred, columns=["pm25", "pm10", "o3"])

    return mae, pred_df

# Future prediction: allows model to estimate future air quality using new weather input data
def predict_future(model, temperature, humidity):
    future_weather = pd.DataFrame(
        [[temperature, humidity]],
        columns=["temperature_mean", "relative_humidity_mean"]
    )

    future_pred = model.predict(future_weather)

    return pd.DataFrame(future_pred, columns=["pm25", "pm10", "o3"])

# Full pipeline: executes the entire ml process in one step
def run_pipeline(db_path=DB_PATH):
    air, weather = load_data(db_path)
    air_daily, weather = preprocess_data(air, weather)
    data = merge_data(air_daily, weather)
    X, y = prepare_features(data)

    model, X_test, y_test = train_model(X, y)
    mae, predictions = evaluate_model(model, X_test, y_test)

    return model, mae, predictions

# --- AI-generated section (ChatGPT/OpenAI) ---: acts as the main entry point of the program and demonstrates how the model is used
if __name__ == "__main__":
    model, mae, predictions = run_pipeline()

    print("MAE:", mae)
    print("\nPredictions sample:")
    print(predictions.head())

    future = predict_future(model, 25, 70)
    print("\nFuture prediction:")
    print(future)
# --- End AI-generated section ---