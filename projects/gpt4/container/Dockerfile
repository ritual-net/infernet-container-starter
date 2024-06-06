FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR 1
ENV RUNTIME docker
ENV PYTHONPATH src
ARG index_url
ENV UV_EXTRA_INDEX_URL ${index_url}

RUN apt-get update
RUN apt-get install -y git curl

# install uv
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod 755 /install.sh
RUN /install.sh && rm /install.sh

COPY src/requirements.txt .

RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

COPY src src

ENTRYPOINT ["hypercorn", "app:create_app()"]
CMD ["-b", "0.0.0.0:3000"]
