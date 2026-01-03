import pandas as pd
from sqlalchemy import create_engine
import joblib
import os

from sklearn.metrics import mean_squared_error, r2_score

# -----------------------------
# 1. Conexión a MySQL
# -----------------------------
# engine = create_engine(
#     "mysql+pymysql://root:123456@localhost:3306/medlife_db"
# )

import os
from sqlalchemy import create_engine

# -----------------------------
# 1. Conexión a MySQL
# -----------------------------
db_host = os.getenv("DB_HOST", "localhost")

print("DB_HOST usado:", db_host)

engine = create_engine(
    f"mysql+pymysql://root:123456@{db_host}:3306/medlife_db"
)




# -----------------------------
# 2. Crear tabla de scoring (sample de 10)
# -----------------------------
df = pd.read_sql("SELECT * FROM training_dataset", engine)

sample_df = df.sample(n=10, random_state=42)

sample_df.to_sql(
    name="scoring_dataset",
    con=engine,
    if_exists="replace",
    index=False
)

# -----------------------------
# 3. Cargar modelo entrenado
# -----------------------------
model = joblib.load("models/best_model.joblib")

# -----------------------------
# 4. Predicción
# -----------------------------
X_score = sample_df.drop(columns=["charges"])
y_true = sample_df["charges"]

y_pred = model.predict(X_score)

sample_df["predicted_charges"] = y_pred

# -----------------------------
# 5. Guardar resultados
# -----------------------------
sample_df.to_sql(
    name="scoring_results",
    con=engine,
    if_exists="replace",
    index=False
)

# -----------------------------
# 6. Métrica final
# -----------------------------
rmse = mean_squared_error(y_true, y_pred) ** 0.5
r2 = r2_score(y_true, y_pred)

os.makedirs("reports", exist_ok=True)

with open("reports/scoring_metrics.txt", "w") as f:
    f.write("Scoring Results\n")
    f.write(f"RMSE: {rmse:.2f}\n")
    f.write(f"R2: {r2:.4f}\n")

print("Scoring ejecutado correctamente.")
print(f"RMSE (sample): {rmse:.2f}")
print(f"R2 (sample): {r2:.4f}")
