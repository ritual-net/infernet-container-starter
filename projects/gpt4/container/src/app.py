import logging
import os
from typing import Any, cast

from eth_abi import decode, encode  # type: ignore
from infernet_ml.utils.css_mux import (
    ConvoMessage,
    CSSCompletionParams,
    CSSRequest,
    Provider,
)
from infernet_ml.utils.service_models import InfernetInput
from infernet_ml.utils.service_models import JobLocation
from infernet_ml.workflows.inference.css_inference_workflow import CSSInferenceWorkflow
from quart import Quart, request

log = logging.getLogger(__name__)


def create_app() -> Quart:
    app = Quart(__name__)

    workflow = CSSInferenceWorkflow(
        api_keys={Provider.OPENAI: os.environ["OPENAI_API_KEY"]}
    )

    workflow.setup()

    @app.route("/")
    def index() -> str:
        """
        Utility endpoint to check if the service is running.
        """
        return "GPT4 Example Program"

    @app.route("/service_output", methods=["POST"])
    async def inference() -> Any:
        req_data = await request.get_json()
        """
        InfernetInput has the format:
            source: (0 on-chain, 1 off-chain)
            data: dict[str, Any]
        """
        infernet_input: InfernetInput = InfernetInput(**req_data)

        match infernet_input:
            case InfernetInput(source=JobLocation.OFFCHAIN):
                prompt = cast(dict[str, Any], infernet_input.data).get("prompt")
            case InfernetInput(source=JobLocation.ONCHAIN):
                # On-chain requests are sent as a generalized hex-string which we will
                # decode to the appropriate format.
                (prompt,) = decode(
                    ["string"], bytes.fromhex(cast(str, infernet_input.data))
                )
            case _:
                raise ValueError("Invalid source")

        result = workflow.inference(
            CSSRequest(
                provider=Provider.OPENAI,
                endpoint="completions",
                model="gpt-4-0613",
                params=CSSCompletionParams(
                    messages=[
                        ConvoMessage(
                            role="system", content="you are a helpful " "assistant."
                        ),
                        ConvoMessage(role="user", content=cast(str, prompt)),
                    ]
                ),
            )
        )

        match infernet_input:
            case InfernetInput(destination=JobLocation.OFFCHAIN):
                """
                In case of an off-chain request, the result is returned as is.
                """
                return {"message": result}
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
                    "raw_input": "",
                    "processed_input": "",
                    "raw_output": encode(["string"], [result]).hex(),
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
    create_app().run(port=3000)
