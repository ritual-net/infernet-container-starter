// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.0;

import {Script, console2} from "forge-std/Script.sol";
import {Prompter} from "../src/Prompter.sol";

contract CallContract is Script {
    function run() public {
        // Setup wallet
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        Prompter prompter = Prompter(0x13D69Cf7d6CE4218F646B759Dcf334D82c023d8e);

        prompter.promptLLM(vm.envString("prompt"));

        vm.stopBroadcast();
    }
}
