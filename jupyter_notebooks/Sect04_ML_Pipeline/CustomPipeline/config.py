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
PATH_TO_DATASET = str(config_public.houseprice_data_dir_path / 'train.csv')

# ==== FEATURE GROUPS ====
TARGET = 'SalePrice'

CATEGORICAL_TO_IMPUTE = [
    'MasVnrType', 'BsmtQual', 'BsmtExposure',
    'FireplaceQu', 'GarageType', 'GarageFinish'
]

NUMERICAL_TO_IMPUTE = ['LotFrontage']

YEAR_VARIABLE = 'YearRemodAdd'

NUMERICAL_LOG = ['LotFrontage', '1stFlrSF', 'GrLivArea', 'SalePrice']

CATEGORICAL_ENCODE = [
    'MSZoning', 'Neighborhood', 'RoofStyle',
    'MasVnrType', 'BsmtQual', 'BsmtExposure',
    'HeatingQC', 'CentralAir', 'KitchenQual',
    'FireplaceQu', 'GarageType', 'GarageFinish',
    'PavedDrive'
]

FEATURES = [
    'MSSubClass', 'MSZoning', 'Neighborhood', 'OverallQual',
    'OverallCond', 'YearRemodAdd', 'RoofStyle', 'MasVnrType',
    'BsmtQual', 'BsmtExposure', 'HeatingQC', 'CentralAir',
    '1stFlrSF', 'GrLivArea', 'BsmtFullBath', 'KitchenQual',
    'Fireplaces', 'FireplaceQu', 'GarageType', 'GarageFinish',
    'GarageCars', 'PavedDrive', 'LotFrontage'
]
