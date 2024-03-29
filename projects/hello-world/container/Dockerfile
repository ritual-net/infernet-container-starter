FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH src

WORKDIR /app

RUN apt-get update

COPY src/requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src src

ENTRYPOINT ["gunicorn", "app:create_app()"]
CMD ["-b", "0.0.0.0:3000"]
