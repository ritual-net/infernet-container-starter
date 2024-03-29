import { useAccount, useWriteContract } from "wagmi";
import { nftAbi } from "@/util/nftAbi";
import { NFT_ADDRESS } from "@/util/constants";
import {Button} from "@/components/Button";

export const MintButton = ({ prompt }: { prompt: string }) => {
  const { address } = useAccount();
  const { writeContract } = useWriteContract();

  return (
    <Button
      onClick={() => {
        if (!address) {
          return;
        }
        writeContract({
          chainId: 31337,
          abi: nftAbi,
          address: NFT_ADDRESS,
          functionName: "mint",
          args: [prompt, address],
        });
      }}
    >
      <span className={"text-xl"}>Generate NFT</span>
    </Button>
  );
};
