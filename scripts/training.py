import pandas as pd
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy import create_engine
import joblib
import os

# -----------------------------
# 1. Conexión a MySQL
# -----------------------------
# engine = create_engine(
#     "mysql+pymysql://root:123456@localhost:3306/medlife_db"
# )

# # -----------------------------
# # 1. Conexión a MySQL
# # -----------------------------
# db_host = os.getenv("DB_HOST", "localhost")

# print("DB_HOST usado:", db_host)

# engine = create_engine(
#     f"mysql+pymysql://root:123456@{db_host}:3306/medlife_db"
# )

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "metlife_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


df = pd.read_sql("SELECT * FROM training_dataset", engine)

# -----------------------------
# 2. Features y target
# -----------------------------
X = df.drop(columns=["charges"])
y = df["charges"]

# -----------------------------
# 3. Train / Test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 4. Preprocesamiento
# -----------------------------
numeric_features = ["age", "bmi", "children"]
categorical_features = ["sex", "smoker", "region"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(drop="first"), categorical_features)
    ]
)

# -----------------------------
# 5. Pipeline
# -----------------------------
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(random_state=42))
    ]
)

# -----------------------------
# 6. Grid Search
# -----------------------------
param_grid = {
    "model__n_estimators": [100, 200],
    "model__max_depth": [None, 10, 20],
    "model__min_samples_split": [2, 5]
}

grid_search = GridSearchCV(
    pipeline,
    param_grid=param_grid,
    cv=3,
    scoring="neg_root_mean_squared_error",
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

# -----------------------------
# 7. Evaluación
# -----------------------------
y_pred = best_model.predict(X_test)

rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

# -----------------------------
# 8. Guardar artefactos
# -----------------------------
os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

joblib.dump(best_model, "models/best_model.joblib")

with open("reports/training_metrics.txt", "w") as f:
    f.write("Random Forest Regressor - Training Results\n")
    f.write(f"Best Params: {grid_search.best_params_}\n")
    f.write(f"RMSE: {rmse:.2f}\n")
    f.write(f"R2: {r2:.4f}\n")

print("Entrenamiento finalizado correctamente.")
print(f"RMSE: {rmse:.2f}")
print(f"R2: {r2:.4f}")
