# MetLife – Predicción de Costos Médicos

Este repositorio contiene una **solución de Machine Learning de punta a punta**, desarrollada como parte de un desafío técnico.  
El objetivo es **predecir el costo médico anual** de clientes de seguros de salud a partir de atributos personales y geográficos, utilizando un enfoque reproducible y orientado a producción.

El proyecto cubre todo el ciclo de vida del modelo:

- Ingesta de datos  
- Entrenamiento y evaluación de modelos  
- Scoring sobre nuevos datos  
- Persistencia en base de datos relacional  
- Ejecución containerizada con Docker  

---

## Descripción del Problema

MetLife es una compañía internacional de seguros que procesa miles de reclamos médicos por año.  
La estimación precisa de costos médicos futuros es clave para:

- Planificación financiera  
- Gestión de riesgos  
- Análisis de escenarios  
- Toma de decisiones estratégicas  

A partir de datos históricos, este proyecto construye un modelo predictivo de costos médicos utilizando las siguientes variables:

- **Edad**: edad del asegurado  
- **Sexo**: género (masculino / femenino)  
- **BMI**: índice de masa corporal  
- **Hijos**: número de dependientes  
- **Fumador**: estado de fumador  
- **Región**: zona geográfica  
- **Charges**: costo médico anual (variable objetivo)  

---

## Enfoque de Modelado

Durante la fase exploratoria se evaluaron dos modelos de regresión supervisada:

- **Regresión Lineal** (modelo base)  
- **Random Forest Regressor** (modelo final seleccionado)  

El **Random Forest Regressor** fue elegido como modelo final debido a que:

- Captura **relaciones no lineales** entre las variables  
- Modela **interacciones entre features** (por ejemplo: fumar × edad × BMI)  
- Es robusto frente a outliers  
- No requiere escalado de variables  
- Presenta un muy buen desempeño predictivo con supuestos mínimos  

El ajuste de hiperparámetros se realizó utilizando **GridSearchCV**, optimizando la métrica **RMSE**.

---

## Desempeño del Modelo (Entrenamiento)

Sobre el conjunto de test se obtuvieron los siguientes resultados:

- **RMSE**: ~4500  
- **R²**: ~0.87  

Estos valores indican una buena capacidad explicativa y predictiva para la estimación de costos médicos.

---

## Capa de Persistencia de Datos

- Se utiliza una base de datos **MySQL** como capa de persistencia.  
- El dataset se almacena en la tabla **`training_dataset`** dentro de la base **`metlife_db`**.  
- Los pipelines de entrenamiento y scoring **leen directamente desde la base de datos**, evitando dependencias directas con archivos CSV durante la ejecución.  

Este diseño replica un escenario realista de producción donde los datos provienen de un sistema centralizado.

---

## Cómo Ejecutar el Proyecto

### Opción 1: Ejecución Local (Entorno Python)

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Cargar los datos en MySQL:
```bash
python scripts/load_db.py
```

3.Entrenar el modelo:
```bash
python scripts/training.py
```

4. Ejecutar el scoring:
```bash
python scripts/scoring.py
```
---

### Opción 2: Ejecución con Docker (Pipeline Completo)

1. Construir la imagen
```bash
docker build -t metlife-ml .
```

2. Ejecutar el pipeline completo
```bash
docker run --rm -e DB_HOST=host.docker.internal metlife-ml
```
---


### Opción 3: Docker Compose

1. Ejecutar todo el sistema con un único comando
```bash
docker-compose up --build
```