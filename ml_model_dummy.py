import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
data = pd.read_csv("dummy_data.csv")

# Features (X) and target (y)
X = data[['temperature', 'humidity', 'wind']]
y = data[['pm25', 'pm10', 'o3']]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("Predictions:", y_pred)