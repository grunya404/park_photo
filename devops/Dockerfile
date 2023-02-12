FROM python:3.10

COPY pyproject.toml poetry.lock /app/
RUN apt-get update && apt-get install ffmpeg  -y

WORKDIR /app
RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install
COPY src/ .
