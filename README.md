# studentidrett-backend

## Description
This project is the back end for The Norwegian Association of University Sports (Norges Studentidrettsforbund, NSI) that is meant to let students find NSI's sports offers all over Norway. There is also a questionnaire that recommends sports based on the answers given. Admins can use the back end to create new objects in the database, as well as a primitive view of interests (clicks) on groups from the front end.

Back end is hosted at: https://kundestyrt-nsi-backend.azurewebsites.net/ \
Swagger for back end: https://app.swaggerhub.com/apis/kundestyrt_h20/Backend/v3

Front end is hosted at: https://kundestyrt-nsi-frontend-staging.azurewebsites.net/ \
Front end repository: https://github.com/Studentidrettsforbundet/studentidrett-frontend


## Technologies
This is a general overview of the technologies used in the project. All dependencies used are included in 'requirements.txt'.
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [Elasticsearch](https://www.elastic.co/elasticsearch/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [Azure](https://azure.microsoft.com/)

# Running locally

## Install Docker
https://docs.docker.com/get-docker/

## Create .env file
For the system to run correctly it requires a set of environment variables:

```
# Django
DJANGO_SECRET_KEY= [INSERT_KEY]
ENV_NAME= ['local' (default), 'staging', 'production']

# Postgres
POSTGRES_DB=[DATABASE_NAME]
POSTGRES_USER=[DATABASE_USERNAME]
POSTGRES_PASSWORD=[DATABASE_PASSWORD]
POSTGRES_HOST=postgres
```
## Run [Docker Machine](https://docs.docker.com/machine/)
If you have an older Mac or Windows system you will need to install and use Docker Machine, since you cannot enable Hyper-V services.

Make sure to have a Docker Daemon running to be able to run the project.
This can be done by running `docker-machine start default` and `
@FOR /f "tokens=*" %i IN ('docker-machine env') DO @%i`. Find the ip-address that Docker-machine
runs on by running `docker-machine ip`. This will be the access point to test
the project, and is by default `192.168.99.100`.

## Run the project
To run the project locally, simply run `docker-compose -f docker-compose.local.yml up --build -d`
at the root of the project. This will install dependencies and run migrations and create a docker image
with the app running.

### Dependencies

Dependencies are stored in `requirements.txt`, and is installed by running `pip install -r requirements.txt`.

After adding a new dependency, add it to `requirements.txt` in the proper subsection.
Running `pip freeze > requirements.txt` to update the dependency list will add many unnecessary packages and should not be used.

# Git-conventions

Automatic linting, code formatting and security testing is implemented using
[pre-commit](https://pre-commit.com/), with isort, Black, Flake8 and Bandit.
To enable run `pre-commit install` once, and then `pre-commit autoupdate`.

The pre-commit hooks will then run before every commit, and check the files changed.
To run on all files, run `pre-commit run --all-files`

When the pre-commit hooks automatically run and any of them fail, the attempted committed files need to be re-added and committed again.

Branches:

- main: update only for deployment (merge from dev)
- dev: development branch, update continuously
- feat/feature-name: a branch that creates/improves a new feature into dev
- task/task-name: a branch that creates/improves a new task into feat. Is used when multiple developers work on a feature
- design/area-name: a branch that creates/improves GUI/UX into dev
- fix/bug-name: a branch that fix a bug or security issue for dev

Pull requests:

- At least one collaborator have to review and approve a pull request before it is merged into dev-branch
- Always use "Squash and merge" as merge-options