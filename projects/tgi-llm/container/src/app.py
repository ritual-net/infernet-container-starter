import logging
import os
from typing import Any, cast

from eth_abi.abi import decode, encode
from quart import Quart, request
from text_generation import Client  # type: ignore

log = logging.getLogger(__name__)


def create_app() -> Quart:
    app = Quart(__name__)

    @app.route("/")
    def index() -> str:
        """
        Utility endpoint to check if the service is running.
        """
        return "LLM Inference Service is running."

    @app.route("/service_output", methods=["POST"])
    async def inference() -> dict[str, Any]:
        """
        Input data has the format:
            source: (0 on-chain, 1 off-chain)
            destination: (0 on-chain, 1 off-chain)
            data: dict[str, Any]
        """
        req_data: dict[str, Any] = await request.get_json()
        onchain_source = True if req_data.get("source") == 0 else False
        onchain_destination = True if req_data.get("destination") == 0 else False
        data = req_data.get("data")

        if onchain_source:
            """
            For on-chain requests, the prompt is sent as a generalized hex-string
            which we will decode to the appropriate format.
            """
            (prompt,) = decode(["string"], bytes.fromhex(cast(str, data)))
        else:
            """For off-chain requests, the prompt is sent as is."""
            prompt = cast(dict[str, Any], data).get("prompt")

        service_url = os.environ["TGI_SERVICE_URL"]
        client = Client(service_url, timeout=30)
        reponse = client.generate(cast(str, prompt))
        content = reponse.generated_text

        # Depending on the destination, the result is returned in a different format.
        if onchain_destination:
            """
            For on-chain requests, the result is returned in the format:
                {
                    "raw_input": str,
                    "processed_input": str,
                    "raw_output": str,
                    "processed_output": str,
                    "proof": str,
                }
            refer to: https://docs.ritual.net/infernet/node/advanced/containers for more
            info.
            """
            return {
                "raw_input": "",
                "processed_input": "",
                "raw_output": encode(["string"], [content]).hex(),
                "processed_output": "",
                "proof": "",
            }
        else:
            """
            For off-chain request, the result is returned as is.
            """
            return {"data": content}

    return app


if __name__ == "__main__":
    """
    Utility to run the app locally. For development purposes only.
    """
    create_app().run(port=3000)
