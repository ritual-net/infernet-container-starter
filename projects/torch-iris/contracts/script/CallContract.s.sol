// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.0;

import {Script, console2} from "forge-std/Script.sol";
import {IrisClassifier} from "../src/IrisClassifier.sol";

contract CallContract is Script {
    function run() public {
        // Setup wallet
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        IrisClassifier irisClassifier = IrisClassifier(0x663F3ad617193148711d28f5334eE4Ed07016602);

        irisClassifier.classifyIris();

        vm.stopBroadcast();
    }
}
