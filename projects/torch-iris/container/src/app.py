import logging
from typing import Any, cast, List

from eth_abi import decode, encode  # type: ignore
from infernet_ml.utils.model_loader import ModelSource
from infernet_ml.utils.service_models import InfernetInput, InfernetInputSource
from infernet_ml.workflows.inference.torch_inference_workflow import (
    TorchInferenceWorkflow,
)
from quart import Quart, request

# Note: the IrisClassificationModel needs to be imported in this file for it to exist
# in the classpath. This is because pytorch requires the model to be in the classpath.
# Simply downloading the weights and model from the hub is not enough.
from iris_classification_model import IrisClassificationModel

log = logging.getLogger(__name__)


def create_app() -> Quart:
    app = Quart(__name__)
    # we are downloading the model from the hub.
    # model repo is located at: https://huggingface.co/Ritual-Net/iris-dataset
    model_source = ModelSource.HUGGINGFACE_HUB
    model_args = {"repo_id": "Ritual-Net/iris-dataset", "filename": "iris.torch"}

    workflow = TorchInferenceWorkflow(model_source=model_source, model_args=model_args)
    workflow.setup()

    @app.route("/")
    def index() -> str:
        """
        Utility endpoint to check if the service is running.
        """
        return (
            f"Torch Iris Classifier Example Program: {IrisClassificationModel.__name__}"
        )

    @app.route("/service_output", methods=["POST"])
    async def inference() -> dict[str, Any]:
        req_data = await request.get_json()
        """
        InfernetInput has the format:
            source: (0 on-chain, 1 off-chain)
            data: dict[str, Any]
        """
        infernet_input: InfernetInput = InfernetInput(**req_data)

        if infernet_input.source == InfernetInputSource.OFFCHAIN:
            web2_input = cast(dict[str, Any], infernet_input.data)
            values = cast(List[List[float]], web2_input["input"])
        else:
            # On-chain requests are sent as a generalized hex-string which we will
            # decode to the appropriate format.
            web3_input: List[int] = decode(
                ["uint256[]"], bytes.fromhex(cast(str, infernet_input.data))
            )[0]
            values = [[float(v) / 1e6 for v in web3_input]]

        """
        The input to the torch inference workflow needs to conform to this format:

        {
            "dtype": str,
            "values": list[Any]
        }

        For more information refer to:
        https://docs.ritual.net/ml-workflows/inference-workflows/torch_inference_workflow

        """
        inference_result = workflow.inference({"dtype": "float", "values": values})

        result = [o.detach().numpy().reshape([-1]).tolist() for o in inference_result]

        if infernet_input.source == InfernetInputSource.OFFCHAIN:
            """
            In case of an off-chain request, the result is returned as is.
            """
            return {"result": result}
        else:
            """
            In case of an on-chain request, the result is returned in the format:
            {
                "raw_input": str,
                "processed_input": str,
                "raw_output": str,
                "processed_output": str,
                "proof": str,
            }
            refer to: https://docs.ritual.net/infernet/node/containers for more info.
            """
            predictions = cast(List[List[float]], result)
            predictions_normalized = [int(p * 1e6) for p in predictions[0]]
            return {
                "raw_input": "",
                "processed_input": "",
                "raw_output": encode(["uint256[]"], [predictions_normalized]).hex(),
                "processed_output": "",
                "proof": "",
            }

    return app


if __name__ == "__main__":
    """
    Utility to run the app locally. For development purposes only.
    """
    create_app().run(port=3000)
