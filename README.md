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
1. [Tasks: Research notebooks](#Tasks-Research-notebooks)
    - [Install dependencies: Research notebooks](#Install-dependencies-Research-notebooks)
    - [Execute notebooks from command line](#Execute-notebooks-from-command-line)
1. [Tasks: Model package](#Tasks-Model-package)
    - [Install dependencies: Model package](#Install-dependencies-Model-package)
    - [Get data for modelling](#Get-data-for-modelling)
    - [Train the regression pipeline](#Train-the-regression-pipeline)
    - [Build the model package](#Build-the-model-package)
    - [Run automated tests: model package](#Run-automated-tests-model-package)
1. [Tasks: API package](#Tasks-API-package)
    - [Install dependencies: API package](#Install-dependencies-API-package)
    - [Run the API package](#Run-the-API-package)
    - [Run automated tests: API package](#Run-automated-tests-API-package)
    - [Docker container: API package](#Docker-container-API-package)
1. [Tasks: CI/CD](#Tasks-CICD)
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

It *should* be possible to run the code in JupyterLab (or another IDE) from your own machine (i.e. not on Binder), but this hasn't been tested. Follow the bullet point to install it *Locally on Windows* in [Package environment](#Package-environment) below.

All console commands are **run from the root folder of this project** unless otherwise stated.

### Start Binder instance
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/A-Breeze/deploying-machine-learning-models/Sect04_extra?urlpath=lab)

### Package environment
We create a conda-env to track the version of Python, and then use a `venv` that is specified *within* the conda-env.
- **Binder**: A conda-env is created from `binder/environment.yml` in Binder is called `notebook` by default. Commands for the Binder Console (in Linux) are as follows (although there are separate instructions to [Install dependencies: Research notebooks](#Install-dependencies-Research-notebooks)).
    ```
    conda activate notebook
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip  # Necessary to have pip>=19.0.* for tensorflow
    ```
- **Locally** (on Windows):
    ```
    conda env create -f environment.yml --force
    conda activate deploy_ml_env
    python -m venv venv
    source venv\Scripts\activate
    pip install --upgrade pip
    ```

<p align="right"><a href="#top">Back to top</a></p>

## Structure of the repo and course
*Note*: The structure of the repo changes as we work through the course, so the description here may not be entirely up to date. Section numbers refer to the Udemy course. 
- `jupyter_notebooks/.`: Research environment (before productionising code). Subfolders `built/` store the assignment submissions (including notebook output).
    - `Sect02_Research_Env/` **Section 2**: Creating an ML model, and Assignment 1.
    - `Sect04_ML_Pipeline/.` **Section 4**: Worked examples of how to productionise a machine pipeline, and Assignments 2 and 3.
    - `Sect12_DeepLearningModel/` **Section 12**: Copy of notebook that is run on Kaggle here: <https://www.kaggle.com/btw78jt/deploy-ml-course-cnn>.
- **Section 3**: Considerations for the architecture of the package.
- `packages/`:
    - `regression_model` **Section 6**: A reproducible pipeline to build the model from source data, including pre-processing.
    - `neural_network_model` **Section 13**: The dataset for this model is large (2GB), so I don't want to load it into Binder (as per: <https://github.com/binder-examples/getting-data#large-public-files>). Therefore, I have created a Kaggle Kernel and uploaded this repo as a "dataset" for the kernel. The commands to train and build the package are recorded on Kaggle (see: <https://www.kaggle.com/btw78jt/deploy-ml-commands>) and also copied to `deploy-ml-commands.py`.
    - `ml_api` **Section 7**: Serve the model as a Flask API to be consumed.
        - `tests/differential_tests/` **Section 9**
- `scripts/`
    - `fetch_kaggle_dataset.sh`: Automatically get the data (in this case, from an online Kaggle API).
    - `fetch_kaggle_large_dataset.sh`: Same but for the `neural_network_model`. \[I am not running this - build the package on Kaggle.\]
    - `fetch_kaggle_nn_package.sh`: The `neural_network_model` package built distribution is stored on Kaggle. This script fetches it. You must *manually* ensure the Kaggle dataset that stores the distribution is updated from the latest build: <https://www.kaggle.com/btw78jt/neural-network-package-repo>.
    - `publish_model.sh`: Push a model package to an online repo. \[I decided not to do this, to avoid signing up to another service.\]
- `.circleci` **Section 8**: Configure tasks to be run in Continuous Integration pipeline.
- `Procfile` **Section 10**: Configuration for the Heroku deployment.
- `Dockerfile` and `Makefile`: Docker image specifications used for:
    - **Section 11**: Deployment to Heroku
    - **Section 12**: Deployment to AWS. *Note*: I did not replicate this section, so the commands are not amended to work. just included for the record.
- `.idea/runConfigurations`: I previously set this up to automate the running of common tasks in PyCharm. I'm no longer using PyCharm, so these are not maintained (but may still work).

### Other materials
The Udemy course provided slides and notes (not saved in this repo).

<p align="right"><a href="#top">Back to top</a></p>

## Tasks: Research notebooks
Notebooks and scripts that were originally used to analyse the data and build the model, and also to investigate productionisation options, i.e. the *research environment*. Since then, the main code has been converted to the model packages (see below), so these are no longer part of the (automated) modelling pipeline. They are kept in the repo as an example of how the inspiration would be kept close to the deployment code (i.e. a *mono-repo*). 

The notebook for research of the `neural_network_model` was run in a Kaggle kernel *not* within Binder. The Kaggle kernel (that is kept in sync *manually* with the copy of the notebook in this repo) is here: <https://www.kaggle.com/btw78jt/deploy-ml-course-cnn>.

### Install dependencies: Research notebooks
To run the notebooks, you need to:
1. Create the conda-env and register it as a kernel for use in the JupyterLab session:
    ```
    conda activate notebook
    conda env create -f jupyter_notebooks/environment.yml --force
    conda activate deploy_ML_research_env
    /srv/conda/envs/deploy_ML_research_env/bin/python -m ipykernel install --name deploy_ML_research_env --prefix /srv/conda/envs/notebook
    ```
    The `--prefix` option ensures the new conda-env is registered as a kernel in the `notebook` conda-env (i.e. the conda-env that is running in JupyterLab). See below for further info on managing Jupyter kernels.

    From the JupyterLab *launcher*, you will now see there is an option to start a notebook using the new kernel (it may take a moment for this to take effect).
1. Install the dependencies for the relevant environment:
    ```
    # For both Section 2 and Section 4:
    pip install -r jupyter_notebooks/Sect02_Research_Env/requirements.txt
    # For both Section 12:
    pip install -r jupyter_notebooks/Sect12_DeepLearningModel/requirements.txt
    ```
1. Get the data for modelling, as [below](#Get-data-for-modelling)

#### Managing Jupyter kernels
```
conda activate notebook
jupyter kernelspec list  # Get a list of the available kernels
jupyter kernelspec remove [kernel name]  # Unregister a kernel
```

### Execute notebooks from command line
The notebooks have been saved in `jupytext` markdown format, so they can be executed (to produce the outputs) as follows, for example, for the Section 2 notebooks:
```
conda activate deploy_ML_research_env
jupytext --execute jupyter_notebooks/Sect02_Research_Env/02.*.md
# OR (the following is for single notebooks)
jupytext --to notebook --output jupyter_notebooks/Sect02_Research_Env/built/Predicting-Survival-Titanic-Assignment.ipynb --execute jupyter_notebooks/Sect02_Research_Env/Predicting-Survival-Titanic-Assignment.md
```

<p align="right"><a href="#top">Back to top</a></p>

## Tasks: Model package
In many cases, the tasks listed in this document are are carried out in an automated way by the CI integration (see [Run continuous integration](#Run-continuous-integration)).

You'll generally want to carry out the tasks in the order given in this document.

### Install dependencies: Model package
```
pip install -r packages/regression_model/requirements.txt
# OR
pip install -r packages/neural_network_model/requirements.txt
```
For some reason, on Binder, I could install the pip `neural_network_model` into the *conda-env* `notebook`, but *not* into the `venv` (Error message: `Could not find a version that satisfies the requirement tensorflow==2.1.0`). I was only testing anyway, so I did not pursue an explanation. 

### Get data for modelling
Data is required for fitting the model in the `regression_model` package. It is downloaded from Kaggle using the Kaggle CLI. For this we need an API key as per <https://www.kaggle.com/docs/api>.
- Get an API Key by signing in to Kaggle and go to: `My Account` - `API` section - `Create new API Token`. 
    - This downloads a `kaggle.json` which should normally be saved at `~/.kaggle/kaggle.json` (Linux) or `C:\Users<Windows-username>.kaggle\kaggle.json` (Windows).
- Create a `kaggle.json` file manually in JupyterLab in the project root directory (which is `~`). Then move it to a `.kaggle` folder by (in console since JupyterLab can't see folders that being with `.`):
    ```
    touch kaggle.json
    chmod 600 kaggle.json  # Advised to run this so it is not visible by other users
    # Open the file and paste in the JSON from your `kaggle.json`
    mkdir .kaggle
    mv kaggle.json .kaggle/kaggle.json
    ```
- Now ensure the requirements for fetching data are installed and run the relevant script by:
    ```
    pip install -r ./scripts/requirements.txt
    chmod +x scripts/fetch_kaggle_dataset.sh
    scripts/fetch_kaggle_dataset.sh
    ```
- Also get the `neural_network_model` package distribution from the Kaggle kernel output where it is built:
    ```
    pip install -r ./scripts/requirements.txt
    chmod +x scripts/fetch_kaggle_nn_package.sh
    scripts/fetch_kaggle_nn_package.sh
    ```
- **REMEMBER** to `Expire API Token` on Kaggle (or delete the `kaggle.json` from Binder) after running (because Binder cannot be guaranteed to be secure).

### Train the regression pipeline
Install the requirements, then run the script to train the pipeline.
```
PYTHONPATH=./packages/regression_model python packages/regression_model/regression_model/train_pipeline.py
# OR
export EPOCHS=1  # Default is 1 for testing the code. Use 8 for fitting the model
python -c "import os; print(os.getenv('EPOCHS'))"  # Check it worked (i.e. python can access the env var)
# Can also amend DATA_FOLDER. Default (for code testing) is: export DATA_FOLDER=packages/neural_network_model/neural_network_model/datasets/test_data
PYTHONPATH=./packages/neural_network_model python packages/neural_network_model/neural_network_model/train_pipeline.py
```
Logs are printed to console, and the model object is added in  `PACKAGE_ROOT / 'trained_models'` as per `packages/[...]_model/[...]_model/config/config.py`. For the `neural_network_model`, you can 

### Build the model package
The following will create a *source* distribution and a *wheel* distribution out of a Python package that you have written (and which includes a `setup.py`), and puts the resulting files in `build/` and `dist/` folders.
```
cd packages/regression_model    # OR:  cd packages/neural_network_model
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
# OR
pytest packages/neural_network_model/tests
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
The resulting API will be served at: `<notebook-base>/proxy/127.0.0.1:5000` (or, if running with `gunicorn`, the port will be `8000`)
- That is, remove `/lab` from the URL and replace it with `/proxy/127.0.0.1:5000`.
- Go to the following endpoints to check it is working:
    - `/health`
    - `/version`
- Also watch the server console as it logs your interactions with the API.
- In addition, the logs are saved (but ignored by the Git repo) to the following location: `packages/ml_api/logs/ml_api.log`
    - This location `LOG_FILE` is a configuration setting from `packages/ml_api/api/config.py`.
    - Also in the config file, we define the message level that will go to the console `console_handler.setLevel()` and to the file `file_handler.setLevel()`. Both of these should be greater than the `logger.setLevel()` within `get_logger()`.

As per: <https://jupyter-server-proxy.readthedocs.io/en/latest/arbitrary-ports-hosts.html>.

Alternatively, you can query the API using `curl` from another console instance, e.g.:
```
curl -X GET localhost:8000/health
curl -X GET localhost:8000/version
# Use the scripts/input_test.json data to get a response from regression_model
curl --header "Content-Type: application/json" --request POST --data "@scripts/input_test.json" localhost:8000/v1/predict/regression
# Use test_data to get a response from neural_network_model
curl --request POST -form "file=@packages/neural_network_model/neural_network_model/datasets/test_data/Black-grass/1.png;type=image/png" localhost:8000/predict/classifier
```

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

### Docker container: API package
Instead of installing Python and dependencies, we can specify the environment from OS (Operating System) upwards using a Docker container. 

Useful commands are:
```
docker build -t ml_api:latest .   # Build the image from the root Dockerfile and call it `ml_api:latest`
    # If we needed to include environment variables, we'd use the option `--build-arg MY_ENV_VAR=%MY_ENV_VAR%`
docker run --name ml_api -d -p 8000:5000 --rm ml_api:latest   # Start a container from the image
docker ps   # Check it is running, and get the container ID
docker logs CONTAINER_ID --tail   # View the container's logs (given the ID from above)
```

I have not run this locally, and Docker cannot be run from within Binder. You can get a Dockerfile produced by `repo2docker` that was used to start the Binder instance, although the docs say 
> This Dockerfile output is for debugging purposes of repo2docker only - it can not be used by docker directly.

<https://repo2docker.readthedocs.io/en/latest/usage.html#debugging-repo2docker-with-debug-and-no-build>

```
pip install jupyter-repo2docker
jupyter-repo2docker --no-build --debug . >  Dockerfile
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
- Similarly, to automate the deployment to Heroku, you need to supply `HEROKU_APP_NAME` (= `udemy-ml-api-ab`), `HEROKU_API_KEY` and (if you want to deploy by Docker container) `HEROKU_EMAIL`. (Note: This is *not* in the "Heroku Key" in my personal settings.) See [below](#Deploy-to-Heroku).

### Deploy to Heroku
#### Setup
- You need to have a [Heroku](https://www.heroku.com) (free) account and have installed the Heroku CLI (this cannot be installed to Binder).
- Create a new app. I called mine `udemy-ml-api-ab`. 
- Add a Heroku remote Git repo to your clone of this repo:
    ```
    heroku login -i   # This is an alias of: heroku auth:login. Enter your details.
    heroku whoami   # Shows you've logged in
    cd [root folder of this project]
    heroku git:remote -a udemy-ml-api-ab  # The name of the remote will be `heroku` (as opposed to `origin`)
    heroku logout   # The command to log out
    ```
- If I were using GemFury to store my built packages, it requires an API key to get downloads to `pip`. The API key could be added as an environment variable to the app in Heroku by going to **Settings** - **Config Vars**. In fact, I am using Kaggle to store the `neural_network_model` package distribution, so I need to add the Kaggle API key to Heroku.

#### Deploy
##### Manually
Deploy a particular branch to Heroku by pushing it to `master` of the `heroku` remote:
```
heroku login -i
git push heroku master_AB:master
```
Should return a message to show it has been deployed successfully. You can also look at the **Activity** tab in the Heroku dashboard.

##### Push to Heroku remote
Alternatively, instead of logging on to Heroku, we can get an API key to the Heroku Git remote and push it all in one go. This is implemented in the CircleCI task `section_10_deploy_to_heroku` (for `master_AB` branch only).
- To manage Heroku API keys, see: <https://devcenter.heroku.com/articles/heroku-cli-commands#heroku-authorizations>
    ```
    # Note that logining-in creates a new API key that lasts until you log out (upto max 1 year)
    heroku login -i
    heroku authorizations   # List the keys I have set up. Add "--json" option to see all details.
    heroku authorizations:info ID   # Details about a specific token
    # Make a new one and get the details to a file. By default, it has no expiry date.
    heroku authorizations:create --json -d "Key for CircleCI AB" > tmp.json
    heroku authorizations:revoke ID   # To stop a token
    ```
- Push it in one go without being logged on (substitute `$HEROKU_API_KEY`):
    ```
    git push https://heroku:$HEROKU_API_KEY@git.heroku.com/udemy-ml-api-ab.git master_AB:master
    ```

**Note**: This method of using `git push` to deploy to Heroku is currently failing (through the CircleCI automated CI commands) because the size of the resulting slug is above Heroku's 500 MB limit - but not by much, as it is coming in at 591 MB. If we use cv2 (i.e. opencv-python) package instead of matplotlib.image and scikit-image, the size is still 566 MB.

##### Build Docker image then push
This is implemented in the CircleCI task `section_11_build_and_push_to_heroku_docker` (for `master_AB` branch only). See the comments in `.circleci/config` and `Makefile`. Docs are here:
- Heroku Docker container registry - push and release: <https://devcenter.heroku.com/articles/container-registry-and-runtime#pushing-an-existing-image>
- Using a CI/CD platform to automate it: <https://devcenter.heroku.com/articles/container-registry-and-runtime#using-a-ci-cd-platform>

If you build using Docker, but then wish to switch back to the `git push` method, you need to first manually change the `stack` that the app uses. Specifically:
```
heroku login -i
heroku apps:stacks -a udemy-ml-api-ab  # Get a list of the available stacks for this app
# If using Docker, then the "container" stack will be selected.
heroku stack:set heroku-18 -a udemy-ml-api-ab   # To switch to the "heroku-18" option
```
`heroku-18` is currently the default stack for new apps. See: <https://devcenter.heroku.com/articles/stack>


#### See it running
From the dashboard, click **Open app**. Alternatively, it is here: <https://udemy-ml-api-ab.herokuapp.com/version>.

See the live console logs from the app as it updates:
```
heroku logs --tail
# To stop: Ctrl+C
```

#### Test it manually
The following submits the JSON input data at `scripts/input_test.json` to the deployed API using `curl` (which must be installed):
```
curl --request GET https://udemy-ml-api-ab.herokuapp.com/version
curl --header "Content-Type: application/json" --request POST --data "@scripts/input_test.json" https://udemy-ml-api-ab.herokuapp.com/v1/predict/regression
curl --request POST --form "file=@packages/neural_network_model/neural_network_model/datasets/test_data/Black-grass/1.png;type=image/png" https://udemy-ml-api-ab.herokuapp.com/predict/classifier
```

#### Other commands
- Docs here: <https://devcenter.heroku.com/articles/heroku-cli-commands>
- Clone a repo from Heroku (see <https://stackoverflow.com/a/32895401>):
    ```
    heroku git:clone -a YOUR_APP_NAME
    ```

<p align="right"><a href="#top">Back to top</a></p>

## Trouble-shooting
### Package environment
There were various problems installing and using `scikit-learn` specifically. 

- The line `pip install -r requirements.txt` failed, although `scikit-learn` appeared to be in the `pip list` for the venv, it was not accessible from Python.
- After various experiments, it seems that there is a limit (on my Windows machine) on the length of the path, and `scikit-learn` (or one of its dependencies) was exceeding this limit, whereas the other packages were not.  
    - Inspired by: <https://stackoverflow.com/a/56857828>...
    - ...which links to: <https://stackoverflow.com/a/1880453>

A common problem when updating a conda-env is described here: <https://github.com/conda/conda/issues/7279#issuecomment-389359679>.

### Binder
I spent some time trying to get VSCode to work inside JupyterLab on Binder, using the potential solution from here: <https://github.com/betatim/vscode-binder>. However, I was not successful, so concluded it was sufficient to use JupyterLab only. Also see my attempts here: <https://github.com/A-Breeze/binder_tests>.

### Heroku
#### Heroku CLI version
When I first installed Heroku CLI, for any command entered, I got a message saying an update (to `6.99.0`) is available. I ignored it (as per <https://github.com/heroku/cli/issues/1182#issue-397716857>), and it appears to have gone away after some time.

#### Dyno hours on free account
The free option for Heroku gives 550 dyno hours per month. To check how many have been used and are remaining, see here: <https://help.heroku.com/FRHZA2YG/how-do-i-monitor-my-free-dyno-hours-quota> or run the following from the Heroku API (for each app that I have):
```
heroku login -i
heroku ps -a udemy-ml-api-ab
heroku logout
```

#### Platform API
To use the Heroku Platform API from Windows, we need to:
- Set up the session:
    ```
    heroku login -i
    # The above creates a file `_netrc` in %USERPROFILE%... 
    # ...but the below needs to use `_netrc` and assumes it is in %HOME%, so...
    set HOME=%USERPROFILE%   # Sets an environment variable only for the duration of the session
    set   # You can see it listed here
    ```
- We can use `curl -n` (aka `curl --netrc`) to send requests to the API, e.g.:
    ```
    # List the apps
    curl -i -n -X GET https://api.heroku.com/apps -H "Accept: application/vnd.heroku+json; version=3"
    # Get the "formation" details of the app
    curl -n https://api.heroku.com/apps/udemy-ml-api-ab/formation -H "Accept: application/vnd.heroku+json; version=3"
    ```

See:
- API reference: <https://devcenter.heroku.com/articles/platform-api-reference>
- The reason I wanted to investigate this: <https://devcenter.heroku.com/articles/container-registry-and-runtime#api>. After some attempts (see commit `4fbad6`), I decided this didn't work and reverted to the fix suggested in the lecture notes (i.e. do not tag the docker image and always deploy the `latest` image).

<p align="right"><a href="#top">Back to top</a></p>

## Further ideas
- Make this an independent repo, not a fork of the train repo.
- Add Swagger UI view for the `ml_api` using flasgger: <https://github.com/flasgger/flasgger>
- Convert `ml_api` from a Flask API to using [Flask-RESTX](https://github.com/python-restx/flask-restx) or Flask-RESTful. Not much difference, as per <https://stackoverflow.com/a/41783739>.
- Remove comments from the PyCharm lint tests (e.g. `# noinspection PyShadowingBuiltins`) and run `pylint` tests instead.
- Look back at the course - there are some additional lessons in the 2020 update, including intro to *Tox* (Section 5.9). Complete these lessons.
- Try out different hosted development, CI and CD options, e.g.:
    - *Git Actions* instead of CircleCI
    - *Azure DevOps* instead of GitHub. Looks like you can use GitHub credentials to access Azure DevOps.
    - *Azure Test Plans* and *Pipelines* instead of CircleCI, e.g.: <https://docs.microsoft.com/en-us/azure/devops/pipelines/artifacts/pypi>
    - *Azure Artifacts* instead of GemFury for a (private) Python package registry, e.g.: <https://docs.microsoft.com/en-us/azure/devops/artifacts/quickstarts/python-packages?view=azure-devops>
    - *Azure App Service* with *Web Apps for Containers* instead of Heroku
- Try using an online environment to run the Docker commands that I cannot run locally, e.g.: 
    - The Docker website provides a playground <https://labs.play-with-docker.com/> (requires login)
    - Katacoda <https://www.katacoda.com/>.
