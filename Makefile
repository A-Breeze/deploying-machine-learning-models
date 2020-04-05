

# Command to build the Docker image
# The image name is specified by the `-t` option, including: 
# - hub location (Heroku registry)
# - image name (the app's name). Note that no tag is specified, so it will be "latest"
build-ml-api-heroku:
	docker build -t registry.heroku.com/$(HEROKU_APP_NAME)/web .

# This command is of the form: docker push registry.heroku.com/<app>/<process-type>
push-ml-api-heroku:
	docker push registry.heroku.com/$(HEROKU_APP_NAME)/web:latest

# ----------------------
# Deploying to AWS
# (I have not done this, so these commands are not run, just for documentation)

AWS_ACCOUNT_ID=None
TAG_OR_COMMIT_ID=$(shell git describe --tags --always HEAD)
# Alternatively, to get the (short) SHA: git rev-parse --short HEAD

build-ml-api-aws:
	docker build --build-arg PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL} -t $(NAME):$(TAG_OR_COMMIT_ID) .

push-ml-api-aws:
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$(NAME):$(TAG_OR_COMMIT_ID)

tag-ml-api:
	docker tag $(NAME):$(TAG_OR_COMMIT_ID) ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$(NAME):$(TAG_OR_COMMIT_ID)
