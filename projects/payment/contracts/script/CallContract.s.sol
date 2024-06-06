// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.0;

import {Script, console2} from "forge-std/Script.sol";
import {SaysGM} from "../src/SaysGM.sol";

contract CallContract is Script {
    function run() public {
        // Setup wallet
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        uint256 amount = vm.envUint("amount");
        address wallet = vm.envAddress("wallet");

        vm.startBroadcast(deployerPrivateKey);

        address registry = 0x13D69Cf7d6CE4218F646B759Dcf334D82c023d8e;
        SaysGM saysGm = SaysGM(registry);

        saysGm.sayGM(amount, wallet);

        vm.stopBroadcast();
    }
}
