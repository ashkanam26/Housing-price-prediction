"""
Train and save the XGBoost model for California Housing dataset
"""
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import joblib
import numpy as np

print("Loading California Housing dataset...")
housing = fetch_california_housing()
X = housing.data
y = housing.target

print(f"Dataset shape: {X.shape}")
print(f"Features: {housing.feature_names}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training XGBoost model...")
model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Training R² score: {train_score:.4f}")
print(f"Testing R² score: {test_score:.4f}")

# Test prediction
sample_features = np.array([[8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]])
prediction = model.predict(sample_features)
print(f"\nSample prediction: ${prediction[0] * 100000:.2f}")

# Save the model
print("\nSaving model...")
joblib.dump(model, 'xgboost-model.pkl')
print("Model saved successfully as 'xgboost-model.pkl'")
