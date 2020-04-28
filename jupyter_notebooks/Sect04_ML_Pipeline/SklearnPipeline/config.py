"""Configuration variables for pipeline"""

# ==== SETUP ====
# Import built-in modules
import sys
from pathlib import Path

# Import external modules
import pyprojroot

# Import project modules
# Allow modules to be referenced relative to the project root directory
root_dir_path = pyprojroot.here(project_files=(".git",))
if sys.path[0] != str(root_dir_path):
    sys.path.insert(0, str(root_dir_path))
# Get project configuration variables
import config_public

# ==== PATHS ====
TRAINING_DATA_FILE = str(config_public.houseprice_data_dir_path / 'train.csv')
PIPELINE_NAME = str(Path('Modelling_outputs') / 'lasso_regression')

# ==== FEATURE GROUPS ====
TARGET = 'SalePrice'

# input variables 
FEATURES = [
    'MSSubClass', 'MSZoning', 'Neighborhood',
    'OverallQual', 'OverallCond', 'YearRemodAdd',
    'RoofStyle', 'MasVnrType', 'BsmtQual', 'BsmtExposure',
    'HeatingQC', 'CentralAir', '1stFlrSF', 'GrLivArea',
    'BsmtFullBath', 'KitchenQual', 'Fireplaces', 'FireplaceQu',
    'GarageType', 'GarageFinish', 'GarageCars', 'PavedDrive',
    'LotFrontage',
    # this one is only to calculate temporal variable:
    'YrSold'
]

# this variable is to calculate the temporal variable,
# must be dropped afterwards
DROP_FEATURES = 'YrSold'

# numerical variables with NA in train set
NUMERICAL_VARS_WITH_NA = ['LotFrontage']

# categorical variables with NA in train set
CATEGORICAL_VARS_WITH_NA = [
    'MasVnrType', 'BsmtQual', 'BsmtExposure',
    'FireplaceQu', 'GarageType', 'GarageFinish'
]

TEMPORAL_VARS = 'YearRemodAdd'

# variables to log transform
NUMERICALS_LOG_VARS = ['LotFrontage', '1stFlrSF', 'GrLivArea']

# categorical variables to encode
CATEGORICAL_VARS = [
    'MSZoning', 'Neighborhood', 'RoofStyle', 'MasVnrType',
    'BsmtQual', 'BsmtExposure', 'HeatingQC', 'CentralAir',
    'KitchenQual', 'FireplaceQu', 'GarageType', 'GarageFinish',
    'PavedDrive'
]
