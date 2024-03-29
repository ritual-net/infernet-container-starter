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
