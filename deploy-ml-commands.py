"""
Recording commands to train and build the neural_network_model package.

This script is saved in both of the following locations:
- Kaggle Kernel: To run the commands next to the data.
    - <https://www.kaggle.com/btw78jt/deploy-ml-commands>
- GitHub repo: Just for a back-up into version control of the above.
    - <https://github.com/A-Breeze/deploying-machine-learning-models>

To avoid having to download the accompanying dataset (which is 2GB),
these commands have been run on a Kaggle Kernel to build the 
neural_network_model package. The resulting package distribution can be
manually downloaded and added to the Git repo, to be deployed.
"""

print(
    '#########\n'
    '# Setup #\n'
    '#########'
)
"""
There is some additional setup needed, 
given that we are running this on Kaggle,
not in the command line of the repo.
"""

# Import built-in modules
import os
from pathlib import Path
import shutil

# Set the DATA_FOLDER env var for use in Kaggle
os.environ['DATA_FOLDER'] = "/kaggle/input/deployingmachinelearningmodelsab/packages/neural_network_model/neural_network_model/datasets/test_data"
# Alternative:  "/kaggle/input/v2-plant-seedlings-dataset"
print("Data folder configured as follows (should print twice):")
!echo $DATA_FOLDER
!python -c "import os; print(os.environ['DATA_FOLDER'])"

# Copy scripts from (read-only) dataset to output area
folder_to_copy = Path('/kaggle/input') / 'deployingmachinelearningmodelsab' / 'packages' / 'neural_network_model'
target_location = Path('.') / 'packages' / 'neural_network_model'
target_location.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(str(folder_to_copy), str(target_location))
print("\nThe package source files have been copied to the sandbox area.")

# You should have already decided the model version that will be built
vers_str = (target_location / 'neural_network_model' / 'VERSION').read_text()
print(f"\nWe are going to be fitting version:\t{vers_str}\n")

print(
    '###############\n'
    '# Train model #\n'
    '###############'
)
# Override the default for EPOCHS
os.environ['EPOCHS'] = "2"  # 1 for testing, 8 for fitting the model
print("Number of epoch to use for training (should print twice):")
!echo $EPOCHS
!python -c "import os; print(os.environ['EPOCHS'])"

print("\nStarting model fitting...")
!PYTHONPATH=./packages/neural_network_model python packages/neural_network_model/neural_network_model/train_pipeline.py
print("\nModel fitting has completed.\n")

print(
    '#######################\n'
    '# Run automated tests #\n'
    '#######################'
)
!pytest packages/neural_network_model/tests

print(
    '#####################\n'
    '# Build the package #\n'
    '#####################'
)
os.chdir(Path('.') / 'packages' / 'neural_network_model')
!python setup.py sdist bdist_wheel
os.chdir(Path('.') / '..' / '..')

print(
    '####################\n'
    '# Clean the output #\n'
    '####################'
)
# Want to store the package distribution on Kaggle, 
# so it doesn't have to be saved within the repo.
# TODO: Move ./packages/neural_network_model/dist/neural_network_model-0.1.0.tar.gz to the top level
# TODO: Delete rest of output

