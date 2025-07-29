def supervised():
    return """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import warnings
warnings.filterwarnings("ignore")

# Load California Housing dataset
data = fetch_california_housing(as_frame=True)
X = data.data
y = data.target
feature_names = data.feature_names

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define models
models = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(),
    "RandomForest": RandomForestRegressor(random_state=42),
    "Lasso": Lasso(),
    "SVR": SVR(),
    "GradientBoosting": GradientBoostingRegressor(random_state=42)
}

results = {}

# Train and evaluate models
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    results[name] = {
        "MAE": mean_absolute_error(y_test, y_pred),
        "MSE": mean_squared_error(y_test, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
        "R2": r2_score(y_test, y_pred)
    }

# Convert results to DataFrame for visualization
results_df = pd.DataFrame(results).T

# Plot performance metrics
metrics = ["MAE", "MSE", "RMSE", "R2"]
plt.figure(figsize=(14, 10))
for i, metric in enumerate(metrics):
    plt.subplot(2, 2, i+1)
    sns.barplot(x=results_df.index, y=results_df[metric])
    plt.title(f'{metric} Comparison')
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Task 3: Hyperparameter Tuning for Gradient Boosting
param_grid = {
    "n_estimators": [100, 200],
    "learning_rate": [0.05, 0.1],
    "max_depth": [3, 5],
    "subsample": [0.8, 1.0]
}
gbr = GradientBoostingRegressor(random_state=42)
grid_search = GridSearchCV(gbr, param_grid, cv=5, scoring='r2')
grid_search.fit(X_train_scaled, y_train)

# Best model evaluation
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test_scaled)
print("Tuned Gradient Boosting R²:", r2_score(y_test, y_pred_best))

# Feature importance
feature_importance = pd.Series(best_model.feature_importances_, index=feature_names).sort_values(ascending=False)

# Plot feature importance
plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance.values, y=feature_importance.index, palette="viridis")
plt.title("Feature Importance (Gradient Boosting)")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()

# Learning curve: impact of number of estimators
train_r2, test_r2 = [], []
for n in range(50, 301, 50):
    gbr_n = GradientBoostingRegressor(n_estimators=n, random_state=42)
    gbr_n.fit(X_train_scaled, y_train)
    train_r2.append(gbr_n.score(X_train_scaled, y_train))
    test_r2.append(gbr_n.score(X_test_scaled, y_test))

plt.figure(figsize=(10, 5))
plt.plot(range(50, 301, 50), train_r2, label='Train R²')
plt.plot(range(50, 301, 50), test_r2, label='Test R²')
plt.xlabel("Number of Estimators")
plt.ylabel("R² Score")
plt.title("Gradient Boosting Learning Curve")
plt.legend()
plt.tight_layout()
plt.show()

# Output summary
results_df.loc["GradientBoosting_Optimized"] = {
    "MAE": mean_absolute_error(y_test, y_pred_best),
    "MSE": mean_squared_error(y_test, y_pred_best),
    "RMSE": np.sqrt(mean_squared_error(y_test, y_pred_best)),
    "R2": r2_score(y_test, y_pred_best)
}
print("Performance Comparison Table:\n", results_df)
print("\nBest Hyperparameters:", grid_search.best_params_)

"""