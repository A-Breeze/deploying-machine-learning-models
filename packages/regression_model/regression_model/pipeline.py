from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from regression_model import preprocessors as pp
from regression_model.config import config

# ==== Pipeline instance =====
price_pipe = Pipeline(
    [  # Specify each step and to which variables it applies in turn
        ('categorical_imputer',
         pp.CategoricalImputer(variables=config.CATEGORICAL_VARS_WITH_NA)),
        ('numerical_inputer',
         pp.NumericalImputer(variables=config.NUMERICAL_VARS_WITH_NA)),
        ('temporal_variable',
         pp.TemporalVariableTransformer(
             variables=config.TEMPORAL_VARS,
             reference_variable=config.DROP_FEATURES)),
        ('rare_label_encoder',
         pp.RareLabelCategoricalEncoder(
             tol=0.01,  # AB: Hard-coded value that could be a parameter?
             variables=config.CATEGORICAL_VARS)),
        ('categorical_encoder',
         pp.CategoricalEncoder(variables=config.CATEGORICAL_VARS)),
        ('log_transformer',
         pp.LogTransformer(variables=config.NUMERICALS_LOG_VARS)),
        ('drop_features',
         pp.DropUnecessaryFeatures(variables_to_drop=config.DROP_FEATURES)),
        ('scaler', MinMaxScaler()),
        # Last step is an Estimator to fit the model
        ('Linear_model', Lasso(alpha=0.005, random_state=0))  # AB: Hard-coded values that could be parameters?
    ]
)
