from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

import preprocessors as pp

# ==== Configuration parameters =====
# categorical variables with NA in train set
CATEGORICAL_VARS_WITH_NA = [
    'MasVnrType', 'BsmtQual', 'BsmtExposure',
    'FireplaceQu', 'GarageType', 'GarageFinish'
]

TEMPORAL_VARS = 'YearRemodAdd'

# this variable is to calculate the temporal variable,
# can be dropped afterwards
DROP_FEATURES = 'YrSold'

# variables to log transform
NUMERICALS_LOG_VARS = ['LotFrontage', '1stFlrSF', 'GrLivArea']

# numerical variables with NA in train set
NUMERICAL_VARS_WITH_NA = ['LotFrontage']

# categorical variables to encode
CATEGORICAL_VARS = ['MSZoning', 'Neighborhood', 'RoofStyle', 'MasVnrType',
                    'BsmtQual', 'BsmtExposure', 'HeatingQC', 'CentralAir',
                    'KitchenQual', 'FireplaceQu', 'GarageType', 'GarageFinish',
                    'PavedDrive']

# ==== Pipeline instance =====
price_pipe = Pipeline(
    [  # Specify each step and to which variables it applies in turn
        ('categorical_imputer',
         pp.CategoricalImputer(variables=CATEGORICAL_VARS_WITH_NA)),
        ('numerical_inputer',
         pp.NumericalImputer(variables=NUMERICAL_VARS_WITH_NA)),
        ('temporal_variable',
         pp.TemporalVariableTransformer(
             variables=TEMPORAL_VARS,
             reference_variable=TEMPORAL_VARS)),
        ('rare_label_encoder',
         pp.RareLabelCategoricalEncoder(
             tol=0.01,  # AB: Hard-coded value that could be a parameter?
             variables=CATEGORICAL_VARS)),
        ('categorical_encoder',
         pp.CategoricalEncoder(variables=CATEGORICAL_VARS)),
        ('log_transformer',
         pp.LogTransformer(variables=NUMERICALS_LOG_VARS)),
        ('drop_features',
         pp.DropUnecessaryFeatures(variables_to_drop=DROP_FEATURES)),
        ('scaler', MinMaxScaler()),
        # Last step is an Estimator to fit the model
        ('Linear_model', Lasso(alpha=0.005, random_state=0))  # AB: Hard-coded values that could be parameters?
    ]
)
