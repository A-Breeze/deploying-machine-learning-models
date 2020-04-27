"""
Project configuration
Central store of variables that can be referenced throughout the project.
"""
#########
# Setup #
#########
# Import modules
import pyprojroot

# Project structure
root_dir_path = pyprojroot.here(project_files=(".git",))
houseprice_data_dir_path = (
    root_dir_path / 'packages' / 'regression_model' / 
    'regression_model' / 'datasets'
)
