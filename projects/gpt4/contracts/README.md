# GPT4 Example Contracts

This is a minimalist foundry project that implements a [callback consumer](https://docs.ritual.net/infernet/sdk/consumers/Callback)
that makes a prompt to the [container](../container/README.md), which then makes a call to OpenAI's GPT4. For an
end-to-end flow of how this works, follow the [guide here](../gpt4.md).

## Deploying

The [`Deploy.s.sol`](./script/Deploy.s.sol) deploys the contracts.
The [Makefile](./Makefile) in this project containes
a utility deploy target.

```bash
make deploy
```

## Prompting

The [`CallContract.s.sol`](./script/CallContract.s.sol) calls
the [`promptGPT`](./src/PromptsGPT.sol#L10) function.
The [Makefile](./Makefile) in this project contains a utility call target. You'll need
to pass in the prompt as an
env var.

```bash
make call-contract prompt="What is 2 * 3?"
```
