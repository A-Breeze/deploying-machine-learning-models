<a name="top"></a>
# Deployment of Machine Learning Models
Fork of repo for the online course Deployment of Machine Learning Models.

For the documentation, visit the [course on Udemy](https://www.udemy.com/deployment-of-machine-learning-models/).

<!--This table of contents is maintained *manually*-->
## Contents
1. [Setup](#Setup)
    - [Start Binder instance](#Start-Binder-instance)
    - [Package environment](#Package-environment)
    - [Get data for modelling](#Get-data-for-modelling)
1. [Structure of the repo and course](#Structure-of-the-repo-and-course)
    - [Other materials](#Other-materials)
1. [Tasks](#Tasks)
    - [Train the regression pipeline](#Train-the-regression-pipeline)
    - [Build the model package](#Build-the-model-package)
    - [Run automated tests](#Run-automated-tests)
    - [Run the API package](#Run-the-API-package)
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
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/A-Breeze/deploying-machine-learning-models/Sect_09_Diff_Tests?urlpath=lab)

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
    mkdir .kaggle
    mv kaggle.json .kaggle/kaggle.json
    ```
- Now run the relevant script by:
    ```
    chmod +x scripts/fetch_kaggle_dataset.sh
    scripts/fetch_kaggle_dataset.sh
    ```
- **REMEMBER** to `Expire API Token` on Kaggle (or delete the `kaggle.json` from Binder) after running (because Binder cannot be guaranteed to be secure).

<p align="right"><a href="#top">Back to top</a></p>

## Structure of the repo and course
*Note*: The structure of the repo changes as we work through the course, so the description here may not be entirely up to date. Section numbers refer to the Udemy course. 
- `jupyter_notebooks/.` **Section 2**: Notebooks that were originally used to analyse the data and build the model, i.e. the *research environment*. Since then, the main code has been converted to the `regression_model` package (see below), so these are no longer part of the (automated) modelling pipeline. They are kept in the repo as an example of how the inspiration would be kept close to the deployment code (i.e. a *mono-repo*). 
    - However, the notebook code does not currently run, because the dependencies are not part of the environment specification and the data is not included in the repo.
- **Section 3**: Considerations for the architecture of the package.
- `packages/`:
    - `regression_model`  **Section 4 and 6**: A reproducible pipeline to build the model from source data, including pre-processing.
    - `ml_api` **Section 7**: Serve the model as a Flask API to be consumed.
        - `tests/differential_tests/` **Section 9**: **NOT COMPLETE**
- `scripts/`
    - `fetch_kaggle_dataset.sh`: Automatically get the data (in this case, from an online Kaggle API).
    - `publish_model.sh`: Push the model package to an online repo. \[I decided not to do this, to avoid signing up to another service.\]
- `.circleci` **Section 8**: Configure tasks to be run in Continuous Integration pipeline.
- `.idea/runConfigurations`: I previously set this up to automate the running of common tasks in PyCharm. I'm no longer using PyCharm, so these are not maintained (but may still work).

### Other materials
The Udemy course provided slides and notes (not saved in this repo).

<p align="right"><a href="#top">Back to top</a></p>

## Tasks
In some cases, these tasks are dependent on the previous one, so should be carried out in order. Note that many of these tasks are carried out in a similar way by the CI integration (see [Run continuous integration](#Run-continuous-integration)).

### Train the regression pipeline
```
PYTHONPATH=./packages/regression_model python packages/regression_model/regression_model/train_pipeline.py
```
Logs are printed to console, and the model object is added in   `PACKAGE_ROOT / 'trained_models'` as per `packages/regression_model/regression_model/config/config.py`.

### Build the model package
The following will create a *source* distribution and a *wheel* distribution out of a Python package that you have written (and which includes a `setup.py`), and puts the resulting files in `build/` and `dist/` folders.
```
cd packages/regression_model 
python setup.py sdist bdist_wheel
cd ../..
```

Alternatively, we can install a local package (without needing to build and then install) as follows:
```
pip install -e packages/regression_model
```

### Run automated tests
```
pytest packages/regression_model/tests  # On the `regression_model` package
pytest packages/ml_api/tests -m "not differential"  # On the `ml_api` package, excluding differential tests
```

To run the *differential* tests, we need a previous version of the model package to compare against. In the course, each package build version was hosted externally, but we can include them in the Git repo (to save signing up to another external provider). So, to run the differential tests:
- You need to have built a previous version of the `regression_model` package and committed it to the repo. I've saved the *wheel* distribution in `packages/regression_model/dist/<package_name>-<version>.tar.gz`.
- You need to include this version as a package requirement for the differential tests, as per: `packages/ml_api/diff_test_requirements.txt`...
- ...and you need to install it (overwriting the usual `ml_api` requirements).

You can then load the previous model, capture predictions, load the current model, and compare the predictions as follows:
```
pip install -r packages/ml_api/diff_test_requirements.txt
PYTHONPATH=./packages/ml_api python3 packages/ml_api/tests/capture_model_predictions.py
pip install -r packages/ml_api/requirements.txt
pytest packages/ml_api/tests -m differential
```

### Run the API package
```
PYTHONPATH=./packages/ml_api python packages/ml_api/run.py  
```

#### Running the API from JupyterLab
The resulting API will be served at: `<notebook-base>/proxy/127.0.0.1:5000`
- That is, remove `/lab` from the URL and replace it with `/proxy/127.0.0.1:5000`.
- Go to the following endpoints to check it is working:
    - `/health`
    - `/version`
- Also watch the server console as it logs your interactions with the API.

As per: <https://jupyter-server-proxy.readthedocs.io/en/latest/arbitrary-ports-hosts.html>.

### Run continuous integration
This is done on [CircleCI](https://circleci.com/) (for which you need to sign up).
- See `.circleci/config.yml`. The tasks run each time you push a commit to the GitHub remote repo.
- To run the tests, you need to provide the Kaggle API Key *privtely* to CircleCI.
    - Go to the Project settings (`Jobs`, then the little gear wheel by the project name) 
    - `Build settings` - `Environment variables` - `Add variable`
    - We want to add `KAGGLE_USERNAME` and `KAGGLE_KEY`

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
