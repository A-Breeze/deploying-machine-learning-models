TAG_OR_COMMIT_ID=$(shell git describe --tags --always HEAD)
# Alternatively, to get the (short) SHA: git rev-parse --short HEAD

# Command to build the Docker image
# The image name is specified by the `-t` option, including: 
# - hub location (Heroku registry)
# - image name (the app's name)
# - tag: set to be the current tag (or short hash is there is no tag), which we got from above
build-ml-api-heroku:
	docker build -t registry.heroku.com/$(HEROKU_APP_NAME)/web:$(TAG_OR_COMMIT_ID) .

# This command is of the form: docker push registry.heroku.com/<app>/<process-type>
# As per: <https://devcenter.heroku.com/articles/container-registry-and-runtime#pushing-an-existing-image>
# Get the docker image ID as per: <https://devcenter.heroku.com/articles/container-registry-and-runtime#getting-a-docker-image-id>
# Also used this: <https://gist.github.com/jincod/04bc7c402720d3d8472fbb094c4741bc>
push-ml-api-heroku:
	docker push registry.heroku.com/$(HEROKU_APP_NAME)/web:$(TAG_OR_COMMIT_ID)
	WEB_DOCKER_IMAGE_ID=$( docker images -q registry.heroku.com/$(HEROKU_APP_NAME)/web:$(TAG_OR_COMMIT_ID) )
	curl -n -X PATCH https://api.heroku.com/apps/$(HEROKU_APP_NAME)/formation \
		-d '{"updates": [{"type": "web", "docker_image": "$(WEB_DOCKER_IMAGE_ID)"}]}' \
		-H "Content-Type: application/json" \
		-H "Accept: application/vnd.heroku+json; version=3.docker-releases"
	