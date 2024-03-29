import { http, useAccount } from "wagmi";
import { createWalletClient, parseUnits } from "viem";
import { anvilNode } from "@/util/chain";
import { privateKeyToAccount } from "viem/accounts";
import { Button } from "@/components/Button";

export const FaucetButton = () => {
  const account = useAccount();
  const requestEth = async () => {
    const { address: _address } = account;
    if (!_address) {
      console.log("No address found");
      return;
    }
    const address = _address!;

    const faucetAccount = privateKeyToAccount(
      "0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6",
    );

    const client = createWalletClient({
      account: faucetAccount,
      chain: anvilNode,
      transport: http(),
    });

    await client.sendTransaction({
      to: address,
      value: parseUnits("1", 18),
    });
  };

  return (
    <Button onClick={requestEth}>
      {account ? "Request 1 ETH" : "Connect Your Wallet"}
    </Button>
  );
};
