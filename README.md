# Infrared
Infrared is a dockerized django web app infrastructure project.   
Covers whole software development cycle from development to production.   
Deployed on **AWS ECS** with **Github Actions** running as **CI/CD**.   

The website is accesible under [**this link**](http://ec2-3-72-36-186.eu-central-1.compute.amazonaws.com:8000/). 

---

## Contents

<!-- vscode-markdown-toc -->
  - [Tech stack](#tech-stack)
  - [Development setup](#development-setup)
  - [Amazon S3 Storage](#amazon-s3-storage)
  - [Poetry](#poetry)
  - [Testing](#testing)
  - [Pre-commit](#pre-commit)
  - [Django commands](#django-commands)
  - [Deployment & Checks](#deployment--checks)
  - [Documentation](#documentation)
<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=false
	/vscode-markdown-toc-config -->

---

## Tech stack

-   Backend - [Django](https://www.djangoproject.com/) + [DRF](https://www.django-rest-framework.org/)
-   Database - [PostgreSQL](https://www.postgresql.org/) + [Amazon RDS](https://aws.amazon.com/rds/)
-   Dependency management - [Poetry](https://python-poetry.org/)
-   API Documentation - [Swagger](https://swagger.io/)
-   Containerization - [Docker](https://www.docker.com/)
-   CI/CD - [Github Actions](https://github.com/features/actions)
-   Hosting - [Amazon ECS](https://aws.amazon.com/ecs/) + [EC2](https://aws.amazon.com/ec2/)

---

## Development setup

Build the Docker images:

    docker-compose build

For any actions concerning database usage like migrations, testing, creating superuser you're going to need the database.    
Here's how you can start it as a detached (running in background) container:

    docker-compose up -d database

Do not forget to run migrations:

    docker-compose run backend python manage.py migrate

Run the development application:

    docker-compose up backend
    # or alternatively run all the services at once
    docker-compose up

Access the server locally with port 8000:

    http://localhost:8000


Install pre-commit hooks:

    pre-commit install

### You're also going to need an .env file, so have a look at this [example](./.env.example).

### Now you're ready to roll 😎

---
## Amazon S3 Storage
In order to work on S3 bucket, you're going to need to set this env variable:

    DJANGO_SETTINGS_MODULE=api.settings.storage
    # of course you'll also going to need all the AWS credentials

Otherwise use this settings module to work on a local store:

    DJANGO_SETTINGS_MODULE=api.settings.local

## Poetry
Here are some helpful poetry commands in case you need to alter the dependencies.

    poetry install # installing dependencies
    poetry shell   # run virtual environment shell
    poetry add     # add a dependency
    poetry remove  # remove a dependency
    poetry update  # update dependency list
    poetry show    # list isntalled dependencies
## Testing    
! Make sure you have `DJANGO_SETTINGS_MODULE=api.settings.local` specified in your .env or container environment !

    docker-compose run backend pytest -s
---

## Pre-commit

    pre-commit                  # runs pre-commit for staged files only
    pre-commit run {hook_id}    # run specified hoot
    pre-commit run --all-files  # run for all files

## Django commands

    docker-compose run backend python manage.py {your_command} {your_args}
---

## Deployment & Checks

Deployment as well as static code checks and running tests is fully automated using Github actions.   
Push to `feature/*` and `main` branches triggers code checks and tests.   
Push to `main` branch automatically triggers deploy to `AWS ECS`.

---

## Documentation

You can find interactive Swagger documentation on the main page of the app.

---
