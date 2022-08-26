FROM python:3.10-alpine as requirements-stage

ENV PYTHONUNBUFFERED 1

WORKDIR /tmp

RUN python3 -m pip install --upgrade pip && pip install poetry

# add package dependencies separately from the code to utilize caching
ADD pyproject.toml poetry.lock /tmp/

# We don't need to have Poetry and its dependencies installed in the final image.
# To keep the image small - we will use pip to install dependencies,
# and poetry just for requirements generation.
RUN poetry export -f requirements.txt \
    --output requirements.txt \
    --without-hashes \
    $(test "$ENVIRONMENT" == production && echo "--no-dev")

FROM python:3.10-alpine

WORKDIR /code/api/

RUN apk update && \
    apk upgrade && \
    apk -y add --no-cache \
    libpq-dev python3-dev gcc musl-dev jpeg-dev zlib-dev

COPY --from=requirements-stage /tmp/requirements.txt /code/api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/api/requirements.txt

ADD ./api /code/api/

EXPOSE 80

CMD ./entrypoint.sh

