import { useAccount } from "wagmi";
import { ConnectButton } from "@rainbow-me/rainbowkit";
import { FaucetButton } from "@/components/FaucetButton";
import { useState } from "react";
import { ClientRendered } from "@/components/ClientRendered";
import { MintButton } from "@/components/MintButton";
import { NftCollection } from "@/components/NftCollection";
import { addNetwork } from "@/util/chain";
import {Button} from "@/components/Button";

export default function Home() {
  const account = useAccount();
  const [prompt, setPrompt] = useState<string>(
    "A picture of a golden retriever fighting sparta in the 300 movie",
  );

  return (
    <ClientRendered>
      <nav
        className="
          backdrop-blur-[17px] bg-white bg-opacity-10 fixed bg-fixed
          dark:border-b-white dark:border-opacity-[15%] py-4
          w-[calc(100%-36px)] rounded-[8px] px-[22px] mx-[18px]
          mt-[30px] gap-3 flex flex-row justify-end"
      >
        <Button onClick={addNetwork}>Add Network</Button>
        <FaucetButton />
        <ConnectButton />
      </nav>
      <main
        className={`flex min-h-screen flex-col items-center pt-[140px] gap-3`}
      >
        <div
          className={"flex flex-row items-center gap-3 w-[80%] md:max-w-[80%]"}
        >
          <label htmlFor="prompt" className={"text-xl"}>
            Your Prompt
          </label>
          <input
            name={"prompt"}
            className={
              "p-2 border-2 rounded-md min-w-96 bg-opacity-20 bg-white border-0 flex-1"
            }
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
        </div>
        <MintButton prompt={prompt} />
        <NftCollection />
      </main>
    </ClientRendered>
  );
}
