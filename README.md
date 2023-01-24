# FM-Images
Recruitment task

## About
Project was created as a recruitment task and follows requirements given.

## Technologies used
Project was built using Django & Django Rest Framework.
Application is Dockerized together with PostgreSQL database.

## How to run locally
* First clone the repository
* Make sure you have docker and docker-compose installed
* Prepare the .env file `cp .env.template .env` and fill in any missing credentials
* Run `docker-compose build` to build the image
* Run `docker-compose up` (see all the logs in console) or `docker-compose up -d` (detached mode, app works in the background) to start the app
* To stop application use `ctr + c` or `docker-compose stop`

## How to run commands inside a container
* First start the application
* Run `docker-compose exec backend python manage.py command_name`, for example `docker-compose exec backend python manage.py migrate`

## Testing
* First start the application
* Run `docker-compose exec backend pytest`

## Autoformatting
There is pre-commit config prepared for this repo
* Make sure you have pre-commit installed
* Run `pre-commit install` to install all hooks

## Documentation
* There is a swagger documentation available at http://localhost:8000/swagger/
