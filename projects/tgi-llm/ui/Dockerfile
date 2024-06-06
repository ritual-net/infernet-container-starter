FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH src
ARG index_url
ENV UV_EXTRA_INDEX_URL ${index_url}

WORKDIR /app

RUN apt-get update

COPY src/requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src src

COPY prompt.txt .

ENTRYPOINT ["python", "src/app.py"]
CMD ["-b", "0.0.0.0:3000"]
