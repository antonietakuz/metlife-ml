# MetLife – Medical Insurance Cost Prediction

This repository contains an end-to-end Machine Learning solution developed as part of a technical challenge.  
The objective is to predict medical insurance costs based on personal and geographic attributes.

---

## Problem Description

MetLife is an international insurance company that processes thousands of health insurance claims per year.  
Accurately estimating future medical insurance costs is crucial for financial planning and decision-making.

Using historical data, this project builds a machine learning model to predict annual medical charges based on:

- Age
- Sex
- Body Mass Index (BMI)
- Number of children
- Smoking status
- Region
- Medical charges (target variable)

---

## Modeling Approach

Two models were evaluated:

- **Linear Regression** (baseline)
- **Random Forest Regressor** (final model)

The Random Forest model was selected due to its ability to capture non-linear relationships and interactions between variables such as smoking status, age, and BMI.  
Hyperparameter tuning was performed using `GridSearchCV`.

---

## Data Persistence

- A **MySQL** database is used for data storage.
- The dataset is stored in a table named `training_dataset` within the `medlife_db` database.
- All training and scoring pipelines read directly from the database (no CSV dependency during execution).

---
## How to Run the Project

### 1️. Load data into MySQL
```bash
python scripts/load_db.py

### 2. Train the model
```bash
python scripts/training.py

###3️. Run scoring
```bash
python scripts/scoring.py

docker build -t metlife-ml .

docker run --rm -e DB_HOST=host.docker.internal metlife-ml
