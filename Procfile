# Explanation of the below command:
# web  => The *process type* to run. "web" is chosen because we're running a web server (using guincorn)
# gunicorn ...   => The *command* to run. Explanation of this particular gunicorn command is given in `packages/ml_api/run.sh`.
# See: <https://devcenter.heroku.com/articles/procfile>

web: gunicorn --pythonpath packages/ml_api --access-logfile - --error-logfile - run:application
