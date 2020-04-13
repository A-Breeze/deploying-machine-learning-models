# This is a Linux image containing Python
FROM python:3.6.6

# Create the user that will run the app named "ml-api-user"
RUN adduser --disabled-password --gecos '' ml-api-user

WORKDIR /opt

# ARG PIP_EXTRA_INDEX_URL # AB: I'm not using GemFury, so don't need this command
ENV FLASK_APP run.py

# ==== Install requirements ====
# Copy everything from a repo directory to a container directory
ADD ./packages/ml_api /opt/packages/ml_api/
ADD ./scripts /opt/scripts/
# The API will need the model package distributions available to install
ADD ./packages/regression_model/dist /opt/packages/regression_model/dist/
# Fetch the neural_network_model package from Kaggle
RUN chmod +x /opt/scripts/fetch_kaggle_nn_package.sh
RUN pip install --upgrade pip
RUN pip install -r /opt/scripts/requirements.txt
RUN /opt/scripts/fetch_kaggle_nn_package.sh
RUN pip install -r /opt/packages/ml_api/requirements.txt

# Give permissions to the user to run the script and own the directory
RUN chmod +x /opt/packages/ml_api/run.sh
RUN chown -R ml-api-user:ml-api-user ./

USER ml-api-user

# Allow the container to pass messages through port 5000
EXPOSE 5000

# Command that will automatically run when we start the container instance
CMD ["bash", "./packages/ml_api/run.sh"]
