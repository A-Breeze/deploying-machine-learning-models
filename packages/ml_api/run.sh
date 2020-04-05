#!/usr/bin/env bash

# Set the following environment variable
export IS_DEBUG=${DEBUG:-false}
# The syntax "${parameter:-word}" means: 
# - If "parameter" exists (and not null), then return its value
# - If "parameter" is not set (or null), then return "word" (or the expansion of it, if it is an expression)
# See: <https://unix.stackexchange.com/a/122848>

# Explanation of options:
# -b  (i.e. --bind) => Socket to bind to (i.e. )
# --access-logfile -  => log to stdout
# --error-logfile -  => similarly for error logs
# See: <https://docs.gunicorn.org/en/stable/settings.html>
exec gunicorn -b :${PORT:-5000} --pythonpath packages/ml_api --access-logfile - --error-logfile - run:application

# Note: To deploy on AWS (which I am not doing), the following command was suggested.
# exec gunicorn --bind 0.0.0.0:5000 --access-logfile - --error-logfile - run:application
