import { Address } from "viem";
import { useAccount, useReadContract } from "wagmi";
import { nftAbi } from "@/util/nftAbi";
import { LoadImg } from "@/components/LoadImg";

export const NftImage = ({
  tokenId,
  contractAddress,
}: {
  tokenId: number;
  contractAddress: Address;
}) => {
  const { address } = useAccount();
  console.log(
    "tokenid",
    tokenId,
    "contractAddress",
    contractAddress,
    "address",
    address,
  );

  const { data } = useReadContract({
    address: contractAddress,
    abi: nftAbi,
    account: address,
    functionName: "tokenURI",
    query: {
      enabled: Boolean(address),
      refetchInterval: 1000,
    },
    args: [BigInt(tokenId)],
  });

  console.log("nft image data", data);

  if (!data) {
    return <>loading...</>;
  }

  return (
    <div className={"p-2 w-[100%] md:w-1/2 lg:w-1/3 flex"}>
      <LoadImg url={data} tokenId={tokenId} />
    </div>
  );
};
