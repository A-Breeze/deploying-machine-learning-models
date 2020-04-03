<a name="top"></a>

[![A-Breeze](https://circleci.com/gh/A-Breeze/deploying-machine-learning-models.svg?style=shield)](https://circleci.com/gh/A-Breeze/deploying-machine-learning-models)

# Deployment of Machine Learning Models
Fork of repo for the online course Deployment of Machine Learning Models.

For the documentation, visit the [course on Udemy](https://www.udemy.com/deployment-of-machine-learning-models/).

<!--This table of contents is maintained *manually*-->
## Contents
1. [Setup](#Setup)
    - [Start Binder instance](#Start-Binder-instance)
    - [Package environment](#Package-environment)
1. [Structure of the repo and course](#Structure-of-the-repo-and-course)
    - [Other materials](#Other-materials)
1. [Tasks: Model package](#Tasks:-Model-package)
    - [Install dependencies: Model package](#Install-dependencies:-Model-package)
    - [Get data for modelling](#Get-data-for-modelling)
    - [Train the regression pipeline](#Train-the-regression-pipeline)
    - [Build the model package](#Build-the-model-package)
    - [Run automated tests: model package](#Run-automated-tests:-model-package)
1. [Tasks: API package](#Tasks:-API-package)
    - [Install dependencies: API package](#Install-dependencies:-API-package)
    - [Run the API package](#Run-the-API-package)
    - [Run automated tests: API package](#Run-automated-tests:-API-package)
1. [Tasks: CI/CD](#Tasks:-CI/CD)
    - [Run continuous integration](#Run-continuous-integration)
    - [Deploy to Heroku](#Deploy-to-Heroku)
1. [Trouble-shooting](#Trouble-shooting)
1. [Further ideas](#Further-ideas)

<p align="right"><a href="#top">Back to top</a></p>

## Setup
This document describes how to run the repo using JupyterLab on Binder. 
- Advantage: This will run it in the browser, so there is no prerequisite of software installed on your computer (other than a compatible browser). 
- Disadvantages:
    - Security is *not* guaranteed within Binder (as per [here](https://mybinder.readthedocs.io/en/latest/faq.html#can-i-push-data-from-my-binder-session-back-to-my-repository)), so I'll be pushing Git from another location, which involves some manual copy-paste.
    - The package environment has to be restored each time, which takes some time.

It *should* be possible to run the code in JupyterLab (or another IDE) from your own machine (i.e. not on Binder), but this hasn't been tested. Start the set up from [Package environment](#Package-environment) below.

All console commands are run from the root folder of this project unless otherwise stated.

### Start Binder instance
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/A-Breeze/deploying-machine-learning-models/Sect10_PaaS?urlpath=lab)

### Package environment
A conda-env has been created from `envinronment.yml` in Binder is called `notebook` by default. I will use the `venv` that is specified *within* the conda-env.

Commands for the Binder Console (in Linux) are:
```
conda activate notebook  # Or `py369` if not on Binder
python -m venv env   # Create new venv called "env"
source env/bin/activate   # Activate env (or `env\Scripts\activate` on Windows)
```

<p align="right"><a href="#top">Back to top</a></p>

## Structure of the repo and course
*Note*: The structure of the repo changes as we work through the course, so the description here may not be entirely up to date. Section numbers refer to the Udemy course. 
- `jupyter_notebooks/.` **Section 2**: Notebooks that were originally used to analyse the data and build the model, i.e. the *research environment*. Since then, the main code has been converted to the `regression_model` package (see below), so these are no longer part of the (automated) modelling pipeline. They are kept in the repo as an example of how the inspiration would be kept close to the deployment code (i.e. a *mono-repo*). To run the notebooks, you need to:
    1. Get the data for modelling, as [above](#Get-data-for-modelling)
    1. Install the dependencies for the research environment:
        ```
        pip install -r jupyter_notebooks/requirements.txt
        ```
    
    **Note**: The notebook code does **not** currently run properly. Ideally, this would be fixed.
- **Section 3**: Considerations for the architecture of the package.
- `packages/`:
    - `regression_model`  **Section 4 and 6**: A reproducible pipeline to build the model from source data, including pre-processing.
    - `ml_api` **Section 7**: Serve the model as a Flask API to be consumed.
        - `tests/differential_tests/` **Section 9**
- `scripts/`
    - `fetch_kaggle_dataset.sh`: Automatically get the data (in this case, from an online Kaggle API).
    - `publish_model.sh`: Push the model package to an online repo. \[I decided not to do this, to avoid signing up to another service.\]
- `.circleci` **Section 8**: Configure tasks to be run in Continuous Integration pipeline.
- `Procfile` **Section 10**: Configuration for the Heroku deployment.
- `.idea/runConfigurations`: I previously set this up to automate the running of common tasks in PyCharm. I'm no longer using PyCharm, so these are not maintained (but may still work).

### Other materials
The Udemy course provided slides and notes (not saved in this repo).

<p align="right"><a href="#top">Back to top</a></p>

## Tasks: Model package
In many cases, the tasks listed in this document are are carried out in an automated way by the CI integration (see [Run continuous integration](#Run-continuous-integration)).

You'll generally want to carry out the tasks in the order given in this document.

### Install dependencies: Model package
```
pip install -r packages/regression_model/requirements.txt
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

### Train the regression pipeline
Install the requirements, then run the script to train the pipeline.
```
PYTHONPATH=./packages/regression_model python packages/regression_model/regression_model/train_pipeline.py
```
Logs are printed to console, and the model object is added in  `PACKAGE_ROOT / 'trained_models'` as per `packages/regression_model/regression_model/config/config.py`.

### Build the model package
The following will create a *source* distribution and a *wheel* distribution out of a Python package that you have written (and which includes a `setup.py`), and puts the resulting files in `build/` and `dist/` folders.
```
cd packages/regression_model 
python setup.py sdist bdist_wheel
cd ../..
```

#### Development installation
While developing the package, we can install it from the local code (without needing to build and then install) as follows:
```
pip install -e packages/regression_model
```

### Run automated tests: Model package
```
pytest packages/regression_model/tests
```

<p align="right"><a href="#top">Back to top</a></p>

## Tasks: API package
### Install dependencies: API package
We can run the API package with either the *current* or *previous* version of the `regression_model` package. The chosen version must have already been built and committed to the repo (follow the steps [above](#Train-the-regression-pipeline)).
```
pip install -r packages/ml_api/requirements.txt             # For the *current* version
pip install -r packages/ml_api/diff_test_requirements.txt   # For the *previous* version
```

### Run the API package
We have a choice of server on which to run the API app:
- The basic Flask server - only appropriate while developing, not in production:
    ```
    PYTHONPATH=./packages/ml_api python packages/ml_api/run.py  
    ```
- Gunincorn server, which is run in deployment on Heroku (see [below](#Deploy-to-Heroku)):
    ```
    gunicorn --pythonpath packages/ml_api --access-logfile - --error-logfile - run:application
    ```

    This is the command specified in the `Procfile` which Heroku uses to start the *dyno* (i.e. to run Python code dynamically on the web server).

#### Running the API from JupyterLab
The resulting API will be served at: `<notebook-base>/proxy/127.0.0.1:5000`
- That is, remove `/lab` from the URL and replace it with `/proxy/127.0.0.1:5000`.
- Go to the following endpoints to check it is working:
    - `/health`
    - `/version`
- Also watch the server console as it logs your interactions with the API.
- In addition, the logs are saved (but ignored by the Git repo) to the following location: `packages/ml_api/logs/ml_api.log`
    - This location `LOG_FILE` is a configuration setting from `packages/ml_api/api/config.py`.
    - Also in the config file, we define the message level that will go to the console `console_handler.setLevel()` and to the file `file_handler.setLevel()`. Both of these should be greater than the `logger.setLevel()` within `get_logger()`.

As per: <https://jupyter-server-proxy.readthedocs.io/en/latest/arbitrary-ports-hosts.html>.

### Run automated tests: API package
To run the test for the `ml_api` package, excluding differential tests:
```
pytest packages/ml_api/tests -m "not differential"
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

<p align="right"><a href="#top">Back to top</a></p>

## Tasks: CI/CD
### Run continuous integration
This is done on [CircleCI](https://circleci.com/) (for which you need to sign up).
- See `.circleci/config.yml`. The tasks run each time you push a commit to the GitHub remote repo.
- To run the tests, you need to provide the Kaggle API Key *privtely* to CircleCI.
    - Go to the Project settings (`Jobs`, then the little gear wheel by the project name) 
    - `Build settings` - `Environment variables` - `Add variable`
    - We want to add `KAGGLE_USERNAME` and `KAGGLE_KEY`

### Deploy to Heroku
#### Setup
- You need to have a [Heroku](https://www.heroku.com) (free) account and have installed the Heroku CLI (this cannot be installed to Binder).
- Create a new app. I called mine `udemy-ml-api-ab`. 
- Add a Heroku remote Git repo to your clone of this repo:
    ```
    heroku login   # This is an alias of: heroku auth:login. Enter your details.
    cd [root folder of this project]
    heroku git: remote -a udemy-ml-api-ab  # The name of the remote will be `heroku` (as opposed to `origin`)
    ```

#### Deploy
- Deploy a particular branch to Heroku by pushing it to `master` of the `heroku` remote:
    ```
    heroku login
    git push heroku Sect10_PaaS:master
    ``` 
**NOT COMPLETE**

#### Other commands
- Docs here: <https://devcenter.heroku.com/articles/heroku-cli-commands>
- Clone a repo from Heroku (see <https://stackoverflow.com/a/32895401>):
    ```
    heroku git: clone -a YOUR_APP_NAME
    ```

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

### Heroku
Whenever I interact with Heroku CLI, I get a message saying an update (to `6.99.0`) is available. I am ignoring it, as per <https://github.com/heroku/cli/issues/1182#issue-397716857>.

<p align="right"><a href="#top">Back to top</a></p>

## Further ideas
- Add Swagger UI view for the `ml_api` using flasgger: <https://github.com/flasgger/flasgger>
- Convert `ml_api` from a Flask API to using [Flask-RESTX](https://github.com/python-restx/flask-restx) or Flask-RESTful. Not much difference, as per <https://stackoverflow.com/a/41783739>.
- Remove comments from the PyCharm lint tests (e.g. `# noinspection PyShadowingBuiltins`) and run `pylint` tests instead.
- Ensure the `jupyter_notebooks` can be run.
    - Incorporate other research code that is currently sitting in a previous repo, not in this monorepo.
- Make this an independent repo, not a fork of the train repo.
