# Command to build the Docker image
# The image name is specified by the `-t` option, including: 
# - hub location (Heroku registry)
# - image name (the app's name). Note that no tag is specified, so it will be "latest"
build-ml-api-heroku:
	docker build -t registry.heroku.com/$(HEROKU_APP_NAME)/web .

# This command is of the form: docker push registry.heroku.com/<app>/<process-type>
push-ml-api-heroku:
	docker push registry.heroku.com/$(HEROKU_APP_NAME)/web:latest
	