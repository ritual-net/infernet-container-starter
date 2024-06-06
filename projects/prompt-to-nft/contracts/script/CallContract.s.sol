// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.0;

import {Script, console2} from "forge-std/Script.sol";
import {DiffusionNFT} from "../src/DiffusionNFT.sol";

contract CallContract is Script {
    string defaultPrompt = "A picture of a shrimp dunking a basketball";

    function run() public {
        // Setup wallet
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address mintTo = vm.envOr("mint_to", msg.sender);
        string memory prompt = vm.envOr("prompt", defaultPrompt);
        vm.startBroadcast(deployerPrivateKey);

        DiffusionNFT nft = DiffusionNFT(0x13D69Cf7d6CE4218F646B759Dcf334D82c023d8e);

        nft.mint(prompt, mintTo);

        vm.stopBroadcast();
    }
}
