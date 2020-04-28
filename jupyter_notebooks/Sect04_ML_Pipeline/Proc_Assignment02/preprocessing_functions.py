"""
Pipeline functions, including functions to:
- Process the data
- Build the model
- Calculate predictions on new data
"""

# ==== SETUP ====
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

import joblib


# Individual pre-processing and training functions
# ================================================
def load_data(df_path):
    """Load data for training"""
    return pd.read_csv(df_path)


def divide_train_test(df, target):
    """Divide data set into train and test"""
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(columns=[target]), df[target],
        test_size=0.2, random_state=0
    )
    return X_train, X_test, y_train, y_test


def extract_cabin_letter(df, var):
    """capture the first letter"""
    return(df[var].str[0])


def add_missing_indicator(df, var):
    """add a binary missing value indicator"""
    res = df.copy()
    res[var + '_NA'] = res[var].isna() + 0
    return(res)

    
def impute_na(df, var, replacement='Missing'):
    """
    Replace NA by value entered by user
    or by string Missing (default behaviour)
    """
    return df[var].fillna(replacement)


def remove_rare_labels(df, var, frequent_labels):
    """
    Group labels that are not in the frequent list 
    into the umbrella group 'Rare'
    """
    return np.where(df[var].isin(frequent_labels), df[var], 'Rare')


def encode_categorical(df, vars_cat):
    """add ohe variables and removes original categorical variable"""
    res = df.merge(
        pd.get_dummies(df[vars_cat], prefix=vars_cat, drop_first=True),
        left_index=True, right_index=True
    ).drop(columns=vars_cat)
    return(res)


def check_dummy_variables(df, dummy_list):
    """
    check that all missing variables where added when encoding,
    otherwise add the ones that are missing
    """
    res = df.copy()
    non_dummy_list = res.columns[~res.columns.isin(dummy_list)].tolist()
    for var in dummy_list:
        if var not in res.columns:
            res[var] = 0
    return(res[non_dummy_list + dummy_list])


def train_scaler(df, output_path):
    scaler = StandardScaler()
    scaler.fit(df)
    joblib.dump(scaler, output_path)
    return scaler


def scale_features(df, scaler):
    """load scaler and transform data"""
    scaler = joblib.load(scaler)
    return pd.DataFrame(scaler.transform(df), columns=df.columns)


def train_model(df, target, output_path):
    """train and save model"""
    log_model = LogisticRegression(C=0.0005, random_state=0)
    log_model.fit(df, target)
    joblib.dump(log_model, output_path)
    return(log_model)

    
def predict(df, model):
    """load model and get predictions"""
    model = joblib.load(model)
    return model.predict(df)
