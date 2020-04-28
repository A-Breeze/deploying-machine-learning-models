"""Fit the model on training data data"""

# ==== SETUP ====
import numpy as np

import preprocessing_functions as pf
import config

import warnings
warnings.simplefilter(action='ignore')

# ================================================
# TRAINING STEP - IMPORTANT TO PERPETUATE THE MODEL

# Load data
data = pf.load_data(config.PATH_TO_DATASET)
print("Correct: Data has loaded")

# divide data set
X_train, X_test, y_train, y_test = pf.divide_train_test(
    data, config.TARGET
)
assert X_train.shape[0] + X_test.shape[0] == data.shape[0]
assert y_train.shape[0] + y_test.shape[0] == data.shape[0]
print("Correct: Data has been split into train and test")

# get first letter from cabin variable
X_train['cabin'] = pf.extract_cabin_letter(X_train, 'cabin')
print("\nManual check: The following should all be letters (no numbers):")
print(X_train.cabin.value_counts(dropna=True).sort_index())  # Check these are all letters
print()

# add missing indicator column and
# impute numerical variable
for var, replacement_val in config.NUMERICAL_IMPUTATION_DICT.items():
    X_train = pf.add_missing_indicator(X_train, var)
    X_train[var] = pf.impute_na(
        X_train, var, replacement=replacement_val
    )
assert X_train[config.NUMERICAL_VARS].isnull().sum().sum() == 0
assert all([
    X_train[col_name].median() == med_val 
    for col_name, med_val in config.NUMERICAL_IMPUTATION_DICT.items()
])
print("Correct: Numerical imputation: All reasonableness tests have passed")
    
# impute categorical variables
original_missing = X_train[config.CATEGORICAL_VARS].isna().sum()
for var in config.CATEGORICAL_VARS:
    X_train[var] = pf.impute_na(X_train, var, replacement='Missing')
assert X_train[config.CATEGORICAL_VARS].isnull().sum().sum() == 0
assert X_train[config.CATEGORICAL_VARS].apply(
    lambda col_sers: (col_sers == 'Missing').sum()
).equals(original_missing)
print("Correct: Categorical imputation: All reasonableness tests have passed")

# Group rare labels
original_props = {
    col_name: X_train[col_name].value_counts(normalize=True)
    for col_name in config.CATEGORICAL_VARS
}
for var, labels_lst in config.FREQUENT_LABELS.items():
    X_train[var] = pf.remove_rare_labels(
        X_train, var, frequent_labels=labels_lst
    )
new_props = {
    col_name: X_train[col_name].value_counts(normalize=True)
    for col_name in config.CATEGORICAL_VARS
}
for col_name in config.CATEGORICAL_VARS:
    assert (
        original_props[col_name].to_frame('orig').merge(
            new_props[col_name].to_frame('new'),
            how='outer', left_index=True, right_index=True
        ).fillna(0).assign(
            check=lambda df: np.select(
                [df.index == 'Rare', df.orig < 0.05], 
                [df.new == df.orig[df.orig < 0.05].sum(), True], 
                default=(df.orig == df.new)
            )
        ).rename_axis(index=col_name).check.all()
    )
print("Correct: Group rare labels: All reasonableness tests have passed")

# encode categorical variables
expected_counts = {
    col_name: X_train[col_name].value_counts().sort_index()[1:].to_frame(
    ).reset_index().rename(columns={'index': 'level'}).assign(
        index=lambda df: col_name + '_' + df.level
    ).drop(columns='level').set_index('index')[col_name]
    for col_name in config.CATEGORICAL_VARS
}
X_train = pf.encode_categorical(X_train, config.CATEGORICAL_VARS)
# Check the counts match as expected
assert all([
    X_train[counts_df.index].sum().equals(counts_df)
    for col_name, counts_df in expected_counts.items()
])
print("Correct: All counts match as expected")

# check all dummies were added
X_train = pf.check_dummy_variables(X_train, config.DUMMY_VARIABLES)

# train scaler and save
pf.train_scaler(X_train, config.OUTPUT_SCALER_PATH)

# scale train set
X_train = pf.scale_features(X_train, config.OUTPUT_SCALER_PATH)

# train model and save
pf.train_model(X_train, y_train, config.OUTPUT_MODEL_PATH)

print('Finished training')
