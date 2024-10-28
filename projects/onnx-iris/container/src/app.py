import logging
from typing import Any, cast, List

from eth_abi import decode, encode  # type: ignore
from huggingface_hub import hf_hub_download  # type: ignore
import numpy as np
import onnx
from onnxruntime import InferenceSession  # type: ignore
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

    # Model repo is located at: https://huggingface.co/Ritual-Net/iris-dataset
    REPO_ID = "Ritual-Net/iris-dataset"
    FILENAME = "iris.onnx"

    @app.route("/")
    def index() -> str:
        """
        Utility endpoint to check if the service is running.
        """
        return "ONNX Iris Classifier Example Program"

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
            web3_input: List[int] = decode(
                ["uint256[]"], bytes.fromhex(cast(str, data))
            )[0]
            values = [[float(v) / 1e6 for v in web3_input]]
        else:
            """For off-chain requests, the input is sent as is."""
            web2_input = cast(dict[str, Any], data)
            values = cast(list[list[float]], web2_input["input"])

        # Prepare the input data for the model
        dtype = cast(np.dtype[np.float32], "float32")
        shape = (len(values), len(values[0]))

        # Download the model from the hub
        path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME, force_download=False)
        model = onnx.load(path)
        onnx.checker.check_model(model)
        session = InferenceSession(path)
        output_names = [output.name for output in model.graph.output]

        # Run the model
        outputs = session.run(
            output_names,
            {
                "input": np.array(
                    values,
                    dtype=dtype,
                ).reshape(shape)
            },
        )

        # Get the predictions
        output = outputs[0]
        predictions = {
            "values": output.flatten(),
            "dtype": "float32",
            "shape": output.shape,
        }

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
            predictions_normalized = [int(p * 1e6) for p in predictions["values"]]
            return {
                "raw_input": "",
                "processed_input": "",
                "raw_output": encode(["uint256[]"], [predictions_normalized]).hex(),
                "processed_output": "",
                "proof": "",
            }
        else:
            """
            For off-chain request, the result is returned as is.
            """
            return {"output": predictions["values"]}

    return app


if __name__ == "__main__":
    """
    Utility to run the app locally. For development purposes only.
    """
    create_app().run(port=3000)
