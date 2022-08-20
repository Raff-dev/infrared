FROM python:3.10-alpine

RUN python3 -m pip install --upgrade pip && pip install poetry

RUN mkdir /app/
WORKDIR /app/

# add package dependencies separately from the code to utilize caching
ADD pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false --local && poetry install --no-dev

ADD . /app/

# TODO remove --reload on production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
