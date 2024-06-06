import logging
import os
from pathlib import Path
from typing import Any, cast

import aiohttp
from eth_abi import decode, encode  # type: ignore
from infernet_ml.utils.service_models import InfernetInput, JobLocation
from quart import Quart, request
from ritual_arweave.file_manager import FileManager

log = logging.getLogger(__name__)


async def run_inference(prompt: str, output_path: str) -> None:
    async with aiohttp.ClientSession() as session:
        app_url = os.getenv("IMAGE_GEN_SERVICE_URL")
        async with session.post(
            f"{app_url}/service_output",
            json={
                "prompt": prompt,
            },
        ) as response:
            image_bytes = await response.read()
            with open(output_path, "wb") as f:
                f.write(image_bytes)


def ensure_env_vars() -> None:
    if not os.getenv("IMAGE_GEN_SERVICE_URL"):
        raise ValueError("IMAGE_GEN_SERVICE_URL environment variable not set")


def create_app() -> Quart:
    app = Quart(__name__)
    ensure_env_vars()

    @app.route("/")
    def index() -> str:
        """
        Utility endpoint to check if the service is running.
        """
        return "Stable Diffusion Example Program"

    @app.route("/service_output", methods=["POST"])
    async def inference() -> dict[str, Any]:
        req_data = await request.get_json()
        """
        InfernetInput has the format:
            source: (0 on-chain, 1 off-chain)
            data: dict[str, Any]
        """
        infernet_input: InfernetInput = InfernetInput(**req_data)
        temp_file = "image.png"

        match infernet_input:
            case InfernetInput(source=JobLocation.OFFCHAIN):
                prompt: str = cast(dict[str, str], infernet_input.data)["prompt"]
            case InfernetInput(source=JobLocation.ONCHAIN):
                # On-chain requests are sent as a generalized hex-string which we will
                # decode to the appropriate format.
                (prompt, mintTo) = decode(
                    ["string", "address"], bytes.fromhex(cast(str, infernet_input.data))
                )
                log.info("mintTo: %s", mintTo)
                log.info("prompt: %s", prompt)
            case _:
                raise ValueError("Invalid source")

        # run the inference and download the image to a temp file
        await run_inference(prompt, temp_file)

        tx = FileManager(wallet_path=os.environ["ARWEAVE_WALLET_FILE_PATH"]).upload(
            Path(temp_file), {"Content-Type": "image/png"}
        )

        match infernet_input:
            case InfernetInput(destination=JobLocation.OFFCHAIN):
                """
                In case of an off-chain request, the result is returned as is.
                """
                return {
                    "prompt": prompt,
                    "hash": tx.id,
                    "image_url": f"https://arweave.net/{tx.id}",
                }
            case InfernetInput(destination=JobLocation.ONCHAIN):
                """
                In case of an on-chain request, the result is returned in the format:
                {
                    "raw_input": str,
                    "processed_input": str,
                    "raw_output": str,
                    "processed_output": str,
                    "proof": str,
                }
                refer to: https://docs.ritual.net/infernet/node/containers for more
                info.
                """
                return {
                    "raw_input": infernet_input.data,
                    "processed_input": "",
                    "raw_output": encode(["string"], [tx.id]).hex(),
                    "processed_output": "",
                    "proof": "",
                }
            case _:
                raise ValueError("Invalid destination")

    return app


if __name__ == "__main__":
    """
    Utility to run the app locally. For development purposes only.
    """
    create_app().run(host="0.0.0.0", port=3000)
