<a name="top"></a>
# Deployment of Machine Learning Models
Fork of repo for the online course Deployment of Machine Learning Models.

For the documentation, visit the [course on Udemy](https://www.udemy.com/deployment-of-machine-learning-models/?couponCode=TIDREPO).

<!--This table of contents is maintained *manually*-->
## Contents
1. [Setup](#Setup)
    - [Start Binder instance](#Start-Binder-instance)
    - [Package environment](#Package-environment)
    - [Get data for modelling](#Get-data-for-modelling)
1. [Structure of the repo](#Structure-of-the-repo)
1. [Tasks](#Tasks)
    - [Train the regression pipeline](#Train-the-regression-pipeline)
    - [Build the model package](#Build-the-model-package)
    - [Run automated tests](#Run-automated-tests)
    - [Run continuous integration](#Run-continuous-integration)
1. [Trouble-shooting](#Trouble-shooting)

<p align="right"><a href="#top">Back to top</a></p>

## Setup
The following describes how to run the repo using JupyterLab on Binder. 
- Advantage: This will run it in the browser, so there is no prerequisite of software installed on your computer (other than a compatible browser). 
- Disadvantages:
    - Security is *not* guaranteed within Binder (as per [here](https://mybinder.readthedocs.io/en/latest/faq.html#can-i-push-data-from-my-binder-session-back-to-my-repository)), so I'll be pushing Git from another location, which involves some manual copy-paste.
    - The package environment has to be restored each time, which takes some time.

It *should* be possible to run the code in JupyterLab (or another IDE) from your own machine (i.e. not on Binder), but this hasn't been tested. Start the set up from [Package environment](#Package-environment) below.

All console commands are run from the root folder of this project unless otherwise stated.

### Start Binder instance
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/A-Breeze/deploying-machine-learning-models/use_binder?urlpath=lab)

### Package environment
A conda-env has been created from `envinronment.yml` in Binder is called `notebook` by default. I will use the `venv` that is specified *within* the conda-env.

Commands for the Binder Console (in Linux) are:
```
conda activate notebook  # Or `py369` if not on Binder
python -m venv env   # Create new venv called "env"
source env/bin/activate   # Activate env (or `env\Scripts\activate` on Windows)
pip install -r requirements_binder.txt   # Requirements for the project, excluding Jupyter
# Requirements for the self-contained regression_model package
pip install -r packages/regression_model/requirements.txt 
# Requirements for the API package
pip install -r packages/ml_api/requirements.txt
```

### Get data for modelling
Data is required for fitting the model in the `regression_model` package. It is downloaded from Kaggle using the Kaggle CLI. For this we need an API key as per <https://www.kaggle.com/docs/api>.
- Get an API Key by signing in to Kaggle and go to: `My Account` - `API` section - `Create new API Token`. 
    - This downloads a `kaggle.json` which should normally be saved at `~/.kaggle/kaggle.json` (Linux) or `C:\Users<Windows-username>.kaggle\kaggle.json` (Windows).
- Create a `kaggle.json` file manually in JupyterLab in the project root directory (which is `~`). Then move it to a `.kaggle` folder by (in console since JupyterLab can't see folders that being with `.`):
    ```
    chmod 600 kaggle.json  # Advised to run this so it is not visible by other users
    mv kaggle.json .kaggle/kaggle.json
    ```
- Now run the relevant script by:
    ```
    chmod +x scripts/fetch_kaggle_dataset.sh
    scripts/fetch_kaggle_dataset.sh
    ```
- **REMEMBER** to `Expire API Token` on Kaggle (or delete the `kaggle.json` from Binder) after running (because Binder cannot be guaranteed to be secure).

<p align="right"><a href="#top">Back to top</a></p>

## Structure of the repo
**TODO**: Write this section

## Tasks
In some cases, these tasks are dependent on the previous one, so should be carried out in order.

### Train the regression pipeline
```
python packages/regression_model/regression_model/train_pipeline.py
```
Logs are printed to console, and the model object is added in   `PACKAGE_ROOT / 'trained_models'` as per `packages/regression_model/regression_model/config/config.py`.

### Build the model package
The following will create a *source* distribution and a *wheel* distribution out of a Python package that you have written (and which includes a `setup.py`), and puts the resulting files in `build/` and `dist/` folders.
```
python packages/regression_model/setup.py sdist bdist_wheel
```

Alternatively, we can install a local package as follows:
```
pip install -e packages/regression_model
```

### Run automated tests
```
pytest packages/regression_model/tests  # On the `regression_model` package
pytest packages/ml_api/tests  # On the `ml_api` package
```

### Run the API package
```
python packages/ml_api/run.py
```

### Run continuous integration
**TODO**: Write this section

<p align="right"><a href="#top">Back to top</a></p>

## Trouble-shooting
### Package environment
There were various problems installing and using `scikit-learn` specifically. 

- The line `pip install -r requirements.txt` failed, although `scikit-learn` appeared to be in the `pip list` for the venv, it was not accessible from Python.
- After various experiments, it seems that there is a limit (on my Windows machine) on the length of the path, and `scikit-learn` (or one of its dependencies) was exceeding this limit, whereas the other packages were not.  
    - Inspired by: <https://stackoverflow.com/a/56857828>...
    - ...which links to: <https://stackoverflow.com/a/1880453>

### Binder
I spent some time trying to get VSCode to work inside JupyterLab on Binder, using the potential solution from here: <https://github.com/betatim/vscode-binder>. However, I was not successful, so concluded it was sufficient to use JupyterLab only. Also see my attempts here: <https://github.com/A-Breeze/binder_tests>.

<p align="right"><a href="#top">Back to top</a></p>
