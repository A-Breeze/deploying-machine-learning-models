APP_NAME=udemy-ml-api-ab
TAG_OR_COMMIT_ID=$(shell git describe --tags --always HEAD)
# Alternatively, to get the (short) SHA: git rev-parse --short HEAD

# Command to build the Docker image
# The image name is specified by the `-t` option, including: 
# - hub location (Heroku registry)
# - image name (the app's name)
# - tag: set to be the current tag (or short hash is there is no tag), which we got from above
build-ml-api-heroku:
	docker build -t registry.heroku.com/$(APP_NAME)/web:$(TAG_OR_COMMIT_ID) .

# This command is of the form: docker push registry.heroku.com/<app>/<process-type>
# As per: <https://devcenter.heroku.com/articles/container-registry-and-runtime#pushing-an-existing-image>
push-ml-api-heroku:
	docker push registry.heroku.com/${HEROKU_APP_NAME}/web:$(TAG_OR_COMMIT_ID)
