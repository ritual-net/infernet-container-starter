import logging
import os
from typing import Any, cast

from eth_abi import decode, encode  # type: ignore
from quart import Quart, request
import requests

log = logging.getLogger(__name__)


def create_app() -> Quart:
    app = Quart(__name__)

    @app.route("/")
    def index() -> str:
        """
        Utility endpoint to check if the service is running.
        """
        return "GPT4 Example Program"

    @app.route("/service_output", methods=["POST"])
    async def inference() -> Any:
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
            # On-chain requests are sent as a generalized hex-string which we will
            # decode to the appropriate format.
            (prompt,) = decode(
                ["string"], bytes.fromhex(cast(str, data))
            )
        else:
            """ For off-chain requests, the prompt is sent as is. """
            prompt = cast(dict[str, Any], data).get("prompt")

        # Make request to the OpenAI API to get a completion of the prompt.
        # See https://platform.openai.com/docs/api-reference/chat for more info.
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            },
            json={
                "model": "gpt-4-0613",
                "messages": [
                    {"role": "system", "content": "you are a helpful assistant."},
                    {"role": "user", "content": cast(str, prompt)}
                ],
            }
        )

        # Ensure the request was successful, and get the result.
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]

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
            return {"message": content}

    return app


if __name__ == "__main__":
    """
    Utility to run the app locally. For development purposes only.
    """
    create_app().run(port=3000)
