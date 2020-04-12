# The Keras model loading function does not play well with
# Pathlib at the moment, so we are using the old os module
# style

import os
from pathlib import Path

PWD = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ROOT = os.path.abspath(os.path.join(PWD, '..'))
DATASET_DIR = os.path.join(PACKAGE_ROOT, 'datasets')
TRAINED_MODEL_DIR = os.path.join(PACKAGE_ROOT, 'trained_models')
# Allows you to specify a different folder for the source data
# Useful for training the model on Kaggle
DATA_FOLDER = os.environ.get('DATA_FOLDER', os.path.join(DATASET_DIR, 'test_data'))
# Changed from: DATA_FOLDER = os.path.join(DATASET_DIR, 'v2-plant-seedlings-dataset')

# MODEL PERSISTING
MODEL_NAME = 'cnn_model'
PIPELINE_NAME = 'cnn_pipe'
CLASSES_NAME = 'classes'
ENCODER_NAME = 'encoder'

# MODEL FITTING
IMAGE_SIZE = 150  # 50 for testing, 150 for final model
BATCH_SIZE = 10
EPOCHS = int(os.environ.get('EPOCHS', 1))  # 1 for testing, 8 for final model

# FOR TESTING ON LIMITED DATA
# Normally, the following variable would be 12. However, when the training data
# set does not contain at least one of each of the 12 plant types we need to 
# change the number here. This is only for testing purposes.
NUM_OF_CLASSES = len(
    [y for y in [x.name for x in Path(DATA_FOLDER).iterdir() if x.is_dir()] if y[0] != "."]
)
# If we're just testing the code, we won't use any test data.
PROP_OF_DATA_TEST = 0.2 if NUM_OF_CLASSES == 12 else 0.

with open(os.path.join(PACKAGE_ROOT, 'VERSION')) as version_file:
    _version = version_file.read().strip()

MODEL_FILE_NAME = f'{MODEL_NAME}_{_version}.h5'
MODEL_PATH = os.path.join(TRAINED_MODEL_DIR, MODEL_FILE_NAME)

PIPELINE_FILE_NAME = f'{PIPELINE_NAME}_{_version}.pkl'
PIPELINE_PATH = os.path.join(TRAINED_MODEL_DIR, PIPELINE_FILE_NAME)

CLASSES_FILE_NAME = f'{CLASSES_NAME}_{_version}.pkl'
CLASSES_PATH = os.path.join(TRAINED_MODEL_DIR, CLASSES_FILE_NAME)

ENCODER_FILE_NAME = f'{ENCODER_NAME}_{_version}.pkl'
ENCODER_PATH = os.path.join(TRAINED_MODEL_DIR, ENCODER_FILE_NAME)
