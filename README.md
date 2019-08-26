# Deployment of Machine Learning Models
Fork of repo for the online course Deployment of Machine Learning Models.

For the documentation, visit the [course on Udemy](https://www.udemy.com/deployment-of-machine-learning-models/?couponCode=TIDREPO).

## Setup
### Environment
I will use the `venv` that is specified *within* a conda-env `py369`. This conda-env onctains only `python=3.6.9`.

Commands are (in Anaconda prompt):
```
> cd [to home folder of this project]
> conda activate py369
> python -m venv env   # Create new venv called "env"
> env\Scripts\activate   # Activate env
> pip install -r requirements.txt
```

#### Trouble-shooting
There were various problems installing and using `scikit-learn` specifically. 

- The line `pip install -r requirements.txt` failed, although `scikit-learn` appeared to be in the `pip list` for the venv, it was not accessible from Python.
- After various experiments, it seems that there is a limit (on my Windows machine) on the length of the path, and `scikit-learn` (or one of its dependencies) was exceeding this limit, wheras the other packages were not.  
    - Inspired by: <https://stackoverflow.com/a/56857828>...
    - ...which links to: <https://stackoverflow.com/a/1880453>


### IDE
I am using PyCharm (Community Edition). The inherited `.gitignore` ignores all of the `.idea/` folder, so not IDE settings will be saved in the repo.

Set the 'Project Interpreter' to be the venv interpreter. This should mean that, when you open the project, the correct interpreter is referenced.

If you want the conda-env to be open in the background, when opening PyCharm, commands are (in Anaconda prompt):
```
> cd [to home folder of this project]
> conda activate py369
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
