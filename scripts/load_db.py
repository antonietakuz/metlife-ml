import pandas as pd
from sqlalchemy import create_engine

# Conexión MySQL (OJOOOOO el nombre de la DB)
engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/medlife_db"
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

