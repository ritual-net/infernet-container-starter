// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.13;

import {console2} from "forge-std/console2.sol";
import {CallbackConsumer} from "infernet-sdk/consumer/Callback.sol";
import {ERC721} from "solmate/tokens/ERC721.sol";

contract DiffusionNFT is CallbackConsumer, ERC721 {
    string private EXTREMELY_COOL_BANNER = "\n\n" "_____  _____ _______ _    _         _\n"
        "|  __ \\|_   _|__   __| |  | |  /\\   | |\n" "| |__) | | |    | |  | |  | | /  \\  | |\n"
        "|  _  /  | |    | |  | |  | |/ /\\ \\ | |\n" "| | \\ \\ _| |_   | |  | |__| / ____ \\| |____\n"
        "|_|  \\_\\_____|  |_|   \\____/_/    \\_\\______|\n\n";

    constructor(address registry) CallbackConsumer(registry) ERC721("DiffusionNFT", "DN") {}

    function mint(string memory prompt, address to) public {
        _requestCompute(
            "prompt-to-nft",
            abi.encode(prompt, to),
            1, // redundancy
            address(0), // paymentToken
            0, // paymentAmount
            address(0), // wallet
            address(0) // prover
        );
    }

    uint256 public counter = 0;

    mapping(uint256 => string) public arweaveHashes;

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        return string.concat("https://arweave.net/", arweaveHashes[tokenId]);
    }

    function nftCollection() public view returns (uint256[] memory) {
        uint256 balance = balanceOf(msg.sender);
        uint256[] memory collection = new uint256[](balance);
        uint256 j = 0;
        for (uint256 i = 0; i < counter; i++) {
            if (ownerOf(i) == msg.sender) {
                collection[j] = i;
                j++;
            }
        }
        return collection;
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
        (string memory arweaveHash) = abi.decode(raw_output, (string));
        (bytes memory raw_input, bytes memory processed_input) = abi.decode(input, (bytes, bytes));
        (string memory prompt, address to) = abi.decode(raw_input, (string, address));
        counter += 1;
        arweaveHashes[counter] = arweaveHash;
        console2.log("nft minted!", string.concat("https://arweave.net/", arweaveHashes[counter]));
        console2.log("nft id", counter);
        console2.log("nft owner", to);
        _mint(to, counter);
    }
}
