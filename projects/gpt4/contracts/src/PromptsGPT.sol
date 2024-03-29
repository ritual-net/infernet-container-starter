// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.13;

import {console2} from "forge-std/console2.sol";
import {CallbackConsumer} from "infernet-sdk/consumer/Callback.sol";

contract PromptsGPT is CallbackConsumer {
    string private EXTREMELY_COOL_BANNER = "\n\n"
    "_____  _____ _______ _    _         _                 \n"
    "|  __ \\|_   _|__   __| |  | |  /\\   | |             \n"
    "| |__) | | |    | |  | |  | | /  \\  | |              \n"
    "|  _  /  | |    | |  | |  | |/ /\\ \\ | |             \n"
    "| | \\ \\ _| |_   | |  | |__| / ____ \\| |____        \n"
    "|_|  \\_\\_____|  |_|   \\____/_/    \\_\\______|   \n\n";
    constructor(address coordinator) CallbackConsumer(coordinator) {}

    function promptGPT(string calldata prompt) public {
        _requestCompute(
            "gpt4",
            abi.encode(prompt),
            20 gwei,
            1_000_000,
            1
        );
    }

    function _receiveCompute(
        uint32 subscriptionId,
        uint32 interval,
        uint16 redundancy,
        address node,
        bytes calldata input,
        bytes calldata output,
        bytes calldata proof
    ) internal override {
        console2.log(EXTREMELY_COOL_BANNER);
        (bytes memory raw_output, bytes memory processed_output) = abi.decode(output, (bytes, bytes));
        (string memory outputStr) = abi.decode(raw_output, (string));

        console2.log("subscription Id", subscriptionId);
        console2.log("interval", interval);
        console2.log("redundancy", redundancy);
        console2.log("node", node);
        console2.log("output:", outputStr);
    }
}
