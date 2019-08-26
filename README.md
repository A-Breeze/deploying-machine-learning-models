# Deployment of Machine Learning Models
Fork of repo for the online course Deployment of Machine Learning Models.

For the documentation, visit the [course on Udemy](https://www.udemy.com/deployment-of-machine-learning-models/?couponCode=TIDREPO).

## Setup
### Environment
I will use the `venv` that is specified *within* the conda-env `Udemy_deploy_ML` that I set up for the other part of the course (because it tracks the correct version of Python).

Commands are (in Anaconda prompt):
```
> cd [to home folder of this project]
> conda activate Udemy_deploy_ML
> python -m venv env   # Create new venv called "env"
> env\Scripts\activate   # Activate env
> pip install -r requirements.txt
```

### IDE
I am using PyCharm (Community Edition). The inherited `.gitignore` ignores all of the `.idea/` folder, so not IDE settings will be saved in the repo.

Set the 'Project Interpreter' to be the venv interpreter. 

When opening PyCharm, commands are (in Anaconda prompt):
```
> cd [to home folder of this project]
> conda activate Udemy_deploy_ML
> env\Scripts\activate
> [location of PyCharm.exe] 
```
To get the PyCharm location, right click on the PyCharm desktop icon, then right click again -- select ' Properties'. The path to the `.exe` is in the 'Target:' field.

This ensures that the 'Terminal' is in the conda-env *and* venv. 

### Git
`.gitignore` was already set up when I cloned the repo. It is very similar to the recommended Python gitignore from here: <https://gitignore.io/api/python>.

This is a "monorepo" (i.e. will hold all work on the product, including various packages). In a Python script, you may want to `import` a module that is saved in the root folder of the specific package that you are in. PyCharm will not be able to the find the module unless it knows that the package root folder is indeed a root (otherwise it will think the only root folder is the main project root). To enable this:

- Right click on the package root folder in the Project view.
- Select `Mark Directory as...` (near bottom of list) `Source Root`.

From <https://stackoverflow.com/a/35553721>.
