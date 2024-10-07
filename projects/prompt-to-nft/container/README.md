# Prompt-to-NFT Container

This container uses a remote StableDiffusion service to generate an image NFT, and stores it on [Arweave](https://docs.arweave.org). There are several components to running this example end-to-end, so we highly recommend you follow the full [Prompt to NFT](https://learn.ritual.net/examples/prompt_to_nft) instead.

Check out the full tutorial [here](https://learn.ritual.net/examples/prompt_to_nft).

### Requirements

- An [Arweave](https://docs.arweave.org) key. Create a key file following the instructions [here](https://docs.arweave.org/developers/mining/mining-quickstart#creating-your-first-arweave-wallet). You should then place your `keyfile-arweave.json` under `projects/prompt-to-nft/container/wallet/`.
- A Stable Diffusion service. You can use an API, or [deploy your own](https://learn.ritual.net/examples/prompt_to_nft#setting-up-a-stable-diffusion-service).

### Build the Container

Simply run the following command to build the container:

```bash
make build
```

Consult the [Makefile](./Makefile) for the build command.

### Add the Arweave File

Create an Arweave key file following the instructions [here](https://docs.arweave.org/developers/mining/mining-quickstart#creating-your-first-arweave-wallet). You should then place your `keyfile-arweave.json` file under `projects/prompt-to-nft/container/wallet/`.

### Run the Container

To run the container, you can use the following command:

```bash
make run
```

### Test the Container

You can test the container by making inference requests directly via your terminal:

```bash
curl -X POST http://127.0.0.1:3000/service_output \
     -H "Content-Type: application/json" \
     -d '{"source": 1, "data": {"prompt": "a golden retriever skiing"}}'
```

## Next steps

This container is for demonstration purposes only, and is purposefully simplified for readability and ease of comprehension. For a production-ready version of this code, check out:

- The [Stable Diffusion Workflow](https://infernet-ml.docs.ritual.net/reference/infernet_ml/workflows/inference/stable_diffusion_workflow/): A Python class that runs a Stable Diffusion pipeline to generate images given an input prompt.
