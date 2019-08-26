# Deployment of Machine Learning Models
Fork of repo for the online course Deployment of Machine Learning Models.

For the documentation, visit the [course on Udemy](https://www.udemy.com/deployment-of-machine-learning-models/?couponCode=TIDREPO).

## Setup
### Environment
I will use the `venv` that is specified *within* the conda-env `Udemy_deploy_ML` that I set up for the other part of the course (because it tracks the correct version of Python).

Commands are (in Anaconda prompt):
```
cd [to home folder of this project]
conda activate Udemy_deploy_ML
python -m venv env   # Create new venv called "env"
env\Scripts\activate   # Activate env
pip install -r requirements.txt
```
### Git
`.gitignore` was already set up when I cloned the repo. It is very similar to the recommended Python gitignore from here: <https://gitignore.io/api/python>.

### IDE
I am using PyCharm (Community Edition). The inherited `.gitignore` ignores all of the `.idea/` folder, so not IDE settings will be saved in the repo.
