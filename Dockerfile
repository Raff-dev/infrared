FROM python:3.10-alpine

ARG ENVIRONMENT=development

RUN echo "this is my bariable ${ENVIRONMENT}"
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

ADD ./app /code/app/

EXPOSE 80

# TODO remove --reload on production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
