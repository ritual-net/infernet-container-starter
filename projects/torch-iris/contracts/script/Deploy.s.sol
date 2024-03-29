// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.13;

import {Script, console2} from "forge-std/Script.sol";
import {IrisClassifier} from "../src/IrisClassifier.sol";

contract Deploy is Script {
    function run() public {
        // Setup wallet
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        // Log address
        address deployerAddress = vm.addr(deployerPrivateKey);
        console2.log("Loaded deployer: ", deployerAddress);

        address coordinator = 0x5FbDB2315678afecb367f032d93F642f64180aa3;
        // Create consumer
        IrisClassifier classifier = new IrisClassifier(coordinator);
        console2.log("Deployed IrisClassifier: ", address(classifier));

        // Execute
        vm.stopBroadcast();
        vm.broadcast();
    }
}
