# Deployment of Machine Learning Models
Fork of repo for the online course Deployment of Machine Learning Models.

For the documentation, visit the [course on Udemy](https://www.udemy.com/deployment-of-machine-learning-models/?couponCode=TIDREPO).

<!--This table of contents is maintained *manually*-->
## Contents
1. [Setup](#Setup)
    - [Start Binder instance](#Start-Binder-instance)
    - [Package environment](#Package-environment)
1. [Structure of the repo](#Structure-of-the-repo)
1. [Tasks](#Tasks)
    - [Build the packages](#Build-the-packages)
    - [Run automated tests](#Run-automated-tests)
    - [Run continuous integration](#Run-continuous-integration)
1. [Trouble-shooting](#Trouble-shooting)

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
$ conda activate notebook  # Or `py369` if not on Binder
$ python -m venv env   # Create new venv called "env"
$ source env/bin/activate   # Activate env (or `env\Scripts\activate` on Windows)
$ pip install -r requirements.txt   # Requirements for the project
# Requirements for the self-contained regression_model package
$ pip install -r packages/regression_model/requirements.txt 
# Requirements for the API package
$ pip install -r packages/ml_api/requirements.txt
```

### Get data
**TODO**: Write this section

## Structure of the repo
**TODO**: Write this section

## Tasks
### Build the packages
The following will create a *source* distribution and a *wheel* distribution out of a Python package that you have written (and which includes a `setup.py`).
```
> python packages/regression_model/setup.py sdist bdist_wheel
```

To install a package (that has been built) locally, use the `-e` switch for `pip`, e.g.:
```
$ pip install -e packages/regression_model
```

### Run automated tests
**TODO**: Write this section

### Run continuous integration
**TODO**: Write this section

## Trouble-shooting
There were various problems installing and using `scikit-learn` specifically. 

- The line `pip install -r requirements.txt` failed, although `scikit-learn` appeared to be in the `pip list` for the venv, it was not accessible from Python.
- After various experiments, it seems that there is a limit (on my Windows machine) on the length of the path, and `scikit-learn` (or one of its dependencies) was exceeding this limit, whereas the other packages were not.  
    - Inspired by: <https://stackoverflow.com/a/56857828>...
    - ...which links to: <https://stackoverflow.com/a/1880453>

