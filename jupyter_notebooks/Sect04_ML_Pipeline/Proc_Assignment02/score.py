"""Calculate predictions on new data"""

# ==== setup ====
import preprocessing_functions as pf
import config

# ==== scoring pipeline ====
def predict(data):
    # extract first letter from cabin
    data['cabin'] = pf.extract_cabin_letter(data, 'cabin')

    # impute NA numerical
    for var, replacement_val in config.NUMERICAL_IMPUTATION_DICT.items():
        data = pf.add_missing_indicator(data, var)
        data[var] = pf.impute_na(
            data, var, replacement=replacement_val
        )
    
    # impute NA categorical
    for var in config.CATEGORICAL_VARS:
        data[var] = pf.impute_na(data, var, replacement='Missing')

    # Group rare labels
    for var, labels_lst in config.FREQUENT_LABELS.items():
        data[var] = pf.remove_rare_labels(
            data, var, frequent_labels=labels_lst
        )
    
    # encode variables
    data = pf.encode_categorical(data, config.CATEGORICAL_VARS)

    # check all dummies were added
    data = pf.check_dummy_variables(data, config.DUMMY_VARIABLES)
    
    # scale variables
    data = pf.scale_features(data, config.OUTPUT_SCALER_PATH)
    
    # make predictions
    predictions = pf.predict(data, config.OUTPUT_MODEL_PATH)

    return predictions

# ==== automated tests ====
# small test that scripts are working ok
if __name__ == '__main__':
        
    from sklearn.metrics import accuracy_score    
    import warnings
    warnings.simplefilter(action='ignore')
    
    # Load data
    data = pf.load_data(config.PATH_TO_DATASET)
    
    X_train, X_test, y_train, y_test = pf.divide_train_test(
        data, config.TARGET
    )
    
    pred = predict(X_test)
    
    # evaluate
    # if your code reprodues the notebook, your output should be:
    # test accuracy: 0.6832
    print('test accuracy: {}'.format(accuracy_score(y_test, pred)))
    print()
