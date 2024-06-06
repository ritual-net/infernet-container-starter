import logging
from typing import Any, cast, List

from infernet_ml.utils.common_types import TensorInput
import numpy as np
from eth_abi import decode, encode  # type: ignore
from infernet_ml.utils.model_loader import (
    HFLoadArgs,
    ModelSource,
)
from infernet_ml.utils.service_models import InfernetInput, JobLocation
from infernet_ml.workflows.inference.onnx_inference_workflow import (
    ONNXInferenceWorkflow,
    ONNXInferenceInput,
    ONNXInferenceResult,
)
from quart import Quart, request
from quart.json.provider import DefaultJSONProvider

log = logging.getLogger(__name__)


class NumpyJsonEncodingProvider(DefaultJSONProvider):
    @staticmethod
    def default(obj: Any) -> Any:
        if isinstance(obj, np.ndarray):
            # Convert NumPy arrays to list
            return obj.tolist()
        # fallback to default JSON encoding
        return DefaultJSONProvider.default(obj)


def create_app() -> Quart:
    Quart.json_provider_class = NumpyJsonEncodingProvider
    app = Quart(__name__)
    # we are downloading the model from the hub.
    # model repo is located at: https://huggingface.co/Ritual-Net/iris-dataset

    workflow = ONNXInferenceWorkflow(
        model_source=ModelSource.HUGGINGFACE_HUB,
        load_args=HFLoadArgs(repo_id="Ritual-Net/iris-dataset", filename="iris.onnx"),
    )
    workflow.setup()

    @app.route("/")
    def index() -> str:
        """
        Utility endpoint to check if the service is running.
        """
        return "ONNX Iris Classifier Example Program"

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
                web2_input = cast(dict[str, Any], infernet_input.data)
                values = cast(List[List[float]], web2_input["input"])
            case InfernetInput(source=JobLocation.ONCHAIN):
                web3_input: List[int] = decode(
                    ["uint256[]"], bytes.fromhex(cast(str, infernet_input.data))
                )[0]
                values = [[float(v) / 1e6 for v in web3_input]]

        """
        The input to the onnx inference workflow needs to conform to ONNX runtime's
        input_feed format. For more information refer to:
        https://docs.ritual.net/ml-workflows/inference-workflows/onnx_inference_workflow
        """
        _input = ONNXInferenceInput(
            inputs={"input": TensorInput(shape=(1, 4), dtype="float", values=values)},
        )
        result: ONNXInferenceResult = workflow.inference(_input)

        match infernet_input:
            case InfernetInput(destination=JobLocation.OFFCHAIN):
                """
                In case of an off-chain request, the result is returned as is.
                """
                return result
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
                predictions = result[0]
                predictions_normalized = [int(p * 1e6) for p in predictions.values]
                return {
                    "raw_input": "",
                    "processed_input": "",
                    "raw_output": encode(["uint256[]"], [predictions_normalized]).hex(),
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
