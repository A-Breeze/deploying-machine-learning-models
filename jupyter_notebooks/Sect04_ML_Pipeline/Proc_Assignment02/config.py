"""Configuration variables for pipeline"""

# ==== SETUP ====
# Import modules
from pathlib import Path


# ==== PATHS ====
PATH_TO_DATASET = "titanic.csv"
OUTPUT_PATH = Path('Modelling_outputs')
OUTPUT_SCALER_PATH = str(OUTPUT_PATH / 'scaler.pkl')
OUTPUT_MODEL_PATH = str(OUTPUT_PATH / 'logistic_regression.pkl')


# ==== PARAMETERS ====
# imputation parameters
NUMERICAL_IMPUTATION_DICT = {
    'age': 28.0, 'fare': 14.4542
}

# encoding parameters
FREQUENT_LABELS = {
    'sex': ['male', 'female'],
    'cabin': ['Missing', 'C'],
    'embarked': ['S', 'C', 'Q'],
    'title': ['Mr', 'Miss', 'Mrs']
}

DUMMY_VARIABLES = [
    'sex_male',
    'cabin_Missing', 'cabin_Rare',
    'embarked_Q', 'embarked_Rare', 'embarked_S',
    'title_Mr', 'title_Mrs', 'title_Rare'
]


# ======= FEATURE GROUPS =============
TARGET = 'survived'
CATEGORICAL_VARS = ['sex', 'cabin', 'embarked', 'title']
NUMERICAL_VARS = ['pclass', 'age', 'sibsp', 'parch', 'fare']
