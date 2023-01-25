FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /code/api/

RUN apt-get update -y && \
    apt-get install -y \
    libpq-dev python3-dev gcc musl-dev libjpeg-dev zlib1g netcat

RUN pip install --upgrade pip && pip install poetry

RUN pip install poetry && \
    poetry config virtualenvs.create false --local

COPY ./pyproject.toml ./poetry.lock* /code/api/

RUN poetry install

ADD ./api /code/api/

EXPOSE 8000

CMD ./entrypoint.sh

