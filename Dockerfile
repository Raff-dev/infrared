FROM python:3.10-alpine

# TODO change user for safety purposes
ENV PYTHONUNBUFFERED 1

ARG ENVIRONMENT=development

RUN apk update && \
    apk upgrade && \
    apk add libpq-dev python3-dev gcc musl-dev jpeg-dev zlib-dev

RUN python3 -m pip install --upgrade pip && pip install poetry

RUN mkdir /code
WORKDIR /code/

# add package dependencies separately from the code to utilize caching
ADD pyproject.toml poetry.lock /code/

# install dev dependencies based on environment varaible
RUN poetry config virtualenvs.create false --local \
    && if [ ${ENVIRONMENT} == production ]; then \
    poetry install --no-dev; \
    else \
    poetry install; \
    fi

ADD ./api /code/api/

EXPOSE 80
WORKDIR /code/api/
CMD ["gunicorn", "--bind", "0.0.0.0:80", "api.wsgi"]
