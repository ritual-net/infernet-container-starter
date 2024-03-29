import { useAccount, useReadContract } from "wagmi";
import { nftAbi } from "@/util/nftAbi";
import { NFT_ADDRESS } from "@/util/constants";

const NFTBalance = () => {
  const { address } = useAccount();

  const readContract = useReadContract({
    address: NFT_ADDRESS,
    account: address,
    abi: nftAbi,
    query: {
      enabled: Boolean(address),
      refetchInterval: 1000,
    },
    functionName: "counter",
  });

  if (!readContract.data) {
    return <>loading...</>;
  }

  return <>your nft balance: {readContract.data.toString()}</>;
};
