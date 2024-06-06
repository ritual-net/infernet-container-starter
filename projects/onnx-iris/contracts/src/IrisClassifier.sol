// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.13;

import {console2} from "forge-std/console2.sol";
import {CallbackConsumer} from "infernet-sdk/consumer/Callback.sol";


contract IrisClassifier is CallbackConsumer {
    string private EXTREMELY_COOL_BANNER = "\n\n"
    "_____  _____ _______ _    _         _\n"
    "|  __ \\|_   _|__   __| |  | |  /\\   | |\n"
    "| |__) | | |    | |  | |  | | /  \\  | |\n"
    "|  _  /  | |    | |  | |  | |/ /\\ \\ | |\n"
    "| | \\ \\ _| |_   | |  | |__| / ____ \\| |____\n"
    "|_|  \\_\\_____|  |_|   \\____/_/    \\_\\______|\n\n";

    constructor(address registry) CallbackConsumer(registry) {}

    function classifyIris() public {
        /// @dev Iris data is in the following format:
        /// @dev [sepal_length, sepal_width, petal_length, petal_width]
        /// @dev the following vector corresponds to the following properties:
        ///     "sepal_length": 5.5cm
        ///     "sepal_width": 2.4cm
        ///     "petal_length": 3.8cm
        ///     "petal_width": 1.1cm
        /// @dev The data is normalized & scaled.
        /// refer to [this function in the model's repository](https://github.com/ritual-net/simple-ml-models/blob/03ebc6fb15d33efe20b7782505b1a65ce3975222/iris_classification/iris_inference_pytorch.py#L13)
        /// for more info on normalization.
        /// @dev The data is adjusted by 6 decimals

        uint256[] memory iris_data = new uint256[](4);
        iris_data[0] = 1_038_004;
        iris_data[1] = 558_610;
        iris_data[2] = 1_103_782;
        iris_data[3] = 1_712_096;

        _requestCompute(
            "onnx-iris",
            abi.encode(iris_data),
            1, // redundancy
            address(0), // paymentToken
            0, // paymentAmount
            address(0), // wallet
            address(0) // prover
        );
    }

    function _receiveCompute(
        uint32 subscriptionId,
        uint32 interval,
        uint16 redundancy,
        address node,
        bytes calldata input,
        bytes calldata output,
        bytes calldata proof,
        bytes32 containerId,
        uint256 index
    ) internal override {
        console2.log(EXTREMELY_COOL_BANNER);
        (bytes memory raw_output, bytes memory processed_output) = abi.decode(output, (bytes, bytes));
        (uint256[] memory classes) = abi.decode(raw_output, (uint256[]));
        uint256 setosa = classes[0];
        uint256 versicolor = classes[1];
        uint256 virginica = classes[2];
        console2.log("predictions: (adjusted by 6 decimals, 1_000_000 = 100%, 1_000 = 0.1%)");
        console2.log("Setosa: ", setosa);
        console2.log("Versicolor: ", versicolor);
        console2.log("Virginica: ", virginica);
    }
}
