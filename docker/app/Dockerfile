FROM python:3.10

COPY pyproject.toml poetry.lock /opt/app/

WORKDIR /opt/app

RUN pip install poetry
RUN poetry install

VOLUME ["/opt/app"]
EXPOSE 8000


