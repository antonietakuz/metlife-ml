import pandas as pd
from sqlalchemy import create_engine
import os
# # Conexión MySQL (OJOOOOO el nombre de la DB)
# engine = create_engine(
#     "mysql+pymysql://root:123456@localhost:3306/medlife_db"
# )




DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "metlife_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# Leer CSV
df = pd.read_csv("data/dataset.csv")

print("Filas en CSV:", df.shape[0])

# Cargar en MySQL
df.to_sql(
    name="training_dataset",
    con=engine,
    if_exists="replace",
    index=False
)

print("Dataset cargado en medlife_db correctamente.")

