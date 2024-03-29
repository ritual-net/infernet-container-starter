# Creating an infernet-compatible `hello-world` container

In this tutorial, we'll create a simple hello-world container that can be used
with infernet.

> [!NOTE]  
> This directory `containers/hello-world` already includes the final result 
> of this tutorial. Run the following tutorial in a new directory.

Let's get started! 🎉

## Step 1: create a simple flask-app and a requirements.txt file

First, we'll create a simple flask-app that returns a hello-world message.
We begin by creating a `src` directory:

```
mkdir src
```

Inside `src`, we create a `app.py` file with the following content:

```python
from typing import Any

from flask import Flask, request


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        return "Hello world service!"

    @app.route("/service_output", methods=["POST"])
    def inference() -> dict[str, Any]:
        input = request.json
        return {"output": f"hello, world!, your input was: {input}"}

    return app
```

As you can see, the app has two endpoints: `/` and `/service_output`. The first
one is simply used to ping the service, while the second one is used for infernet.

We can see that our app uses the `flask` package. Additionally, we'll need to
install the `gunicorn` package to run the app. We'll create a `requirements.txt`
file with the following content:

```
Flask>=3.0.0,<4.0.0
gunicorn>=21.2.0,<22.0.0
```

## Step 2: create a Dockerfile

Next, we'll create a Dockerfile that builds the flask-app and runs it.
At the top-level directory, create a `Dockerfile` with the following content:

```dockerfile
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
```

This is a simple Dockerfile that:

1. Uses the `python:3.11-slim` image as a base image
2. Installs the requirements
3. Copies the source code
4. Runs the app on port `3000`

> [!IMPORTANT]  
> App must be exposed on port `3000`. Infernet's orchestrator
> will always assume that the container apps are exposed on that port within the container.
> Users can then remap this port to any port that they want on the host machine
> using the `port` parameter in the container specs.

By now, your project directory should look like this:

```
.
├── Dockerfile
├── README.md
└── src
    ├── __init__.py
    └── app.py
    └── requirements.txt
```

## Step 3: build the container

Now, we can build the container. At the top-level directory, run:

```
docker build -t hello-world .
```

## Step 4: run the container

Finally, we can run the container. In one terminal, run:

```
docker run --rm -p 3000:3000 --name hello hello-world
```

## Step 5: ping the container

In another terminal, run:

```
curl localhost:3000
```

It should return something like:

```
Hello world service!
```

Congratulations! You've created a simple hello-world container that can be
used with infernet. 🎉

## Step 6: request a service output

Now, let's request a service output. Note that this endpoint is called by
the infernet node, not by the user. For debugging purposes however, it's useful to
be able to call it manually.

In your terminal, run:

```
curl -X POST -H "Content-Type: application/json" -d '{"input": "hello"}' localhost:3000/service_output
```

The output should be something like:

```
{"output": "hello, world!, your input was: {'input': 'hello'}"}
```

Your users will never call this endpoint directly. Instead, they will:

1. Either [create an off-chain job request](../../../README.md#L36) through the node API
2. Or they will make a subscription on their contracts
