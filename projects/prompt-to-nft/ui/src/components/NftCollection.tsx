import { useAccount, useReadContract } from "wagmi";
import { NFT_ADDRESS } from "@/util/constants";
import { nftAbi } from "@/util/nftAbi";
import { NftImage } from "@/components/NftImage";

export const NftCollection = () => {
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

  if (readContract.data === 0n) {
    return <>No NFTs</>;
  }
  console.log("read contract data", readContract.data);

  if (!readContract.data) {
    return <>Please connect your wallet.</>;
  }

  const counter = parseInt(readContract.data.toString());
  const nftIds = new Array(counter).fill(0n).map((_, index) => index + 1);

  console.log(`counter: ${counter}`);

  return (
    <div
      className={
        "bg-emerald-700 bg-opacity-10 p-3 flex-1 flex flex-col w-[100%]"
      }
    >
      <h2 className={"text-2xl ml-2 my-3"}>The Collection</h2>
      {nftIds.length === 0 ? (
        <div className={"justify-center flex mt-20 text-opacity-80"}>
          No NFTs minted.
        </div>
      ) : (
        <div className={"flex flex-wrap"}>
          {nftIds.map((id) => {
            return (
              <NftImage key={id} tokenId={id} contractAddress={NFT_ADDRESS} />
            );
          })}
        </div>
      )}
    </div>
  );
};
