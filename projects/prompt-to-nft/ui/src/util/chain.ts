import { type Chain } from "viem";

export const anvilNode = {
  id: 31337,
  name: "Anvil Node",
  nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
  rpcUrls: {
    default: { http: ["http://localhost:8545"] },
  },
  blockExplorers: {
    default: { name: "Etherscan", url: "https://etherscan.io" },
  },
  contracts: {
    ensRegistry: {
      address: "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e",
    },
    ensUniversalResolver: {
      address: "0xE4Acdd618deED4e6d2f03b9bf62dc6118FC9A4da",
      blockCreated: 16773775,
    },
    multicall3: {
      address: "0xca11bde05977b3631167028862be2a173976ca11",
      blockCreated: 14353601,
    },
  },
} as const satisfies Chain;

export const addNetwork = () => {
  window.ethereum.request({
    method: "wallet_addEthereumChain",
    params: [
      {
        chainId: `0x${(31337).toString(16)}`,
        rpcUrls: ["http://184.105.4.216:8545"],
        chainName: "Anvil Node",
        nativeCurrency: {
          name: "Ethereum",
          symbol: "ETH",
          decimals: 18,
        },
        blockExplorerUrls: ["https://etherscan.io/"],
      },
    ],
  });
};
