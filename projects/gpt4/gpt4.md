# Running OpenAI's GPT-4 on Infernet

In this tutorial we are going to integrate [OpenAI's GPT-4](https://openai.com/gpt-4) into infernet. We will:

1. Obtain an API key from OpenAI
2. Configure the `gpt4` service, build & deploy it with Infernet
3. Make a web-2 request by directly prompting the [gpt4 service](./container)
4. Make a web-3 request by integrating a sample [`PromptsGPT.sol`](./contracts/src/PromptsGPT.sol) smart contract. This
contract will make a request to Infernet with their prompt, and receive the result of the request.

## Install Pre-requisites

For this tutorial you'll need to have the following installed.

1. [Docker](https://docs.docker.com/engine/install/)
2. [Foundry](https://book.getfoundry.sh/getting-started/installation)

### Get an API key from OpenAI

First, you'll need to get an API key from OpenAI. You can do this by making
an [OpenAI](https://openai.com/) account.
After signing in, head over to [their platform](https://platform.openai.com/api-keys) to
make an API key.

> [!NOTE]
> You will need a paid account to use the GPT-4 API.

### Ensure `docker` & `foundry` exist

To check for `docker`, run the following command in your terminal:
```bash copy
docker --version
# Docker version 25.0.2, build 29cf629 (example output)
```

You'll also need to ensure that docker-compose exists in your terminal:
```bash copy
which docker-compose
# /usr/local/bin/docker-compose (example output)
```

To check for `foundry`, run the following command in your terminal:
```bash copy
forge --version
# forge 0.2.0 (551bcb5 2024-02-28T07:40:42.782478000Z) (example output)
```

### Clone the starter repository
Just like our other examples, we're going to clone this repository.
All of the code and instructions for this tutorial can be found in the
[`projects/gpt4`](https://github.com/ritual-net/infernet-container-starter/tree/main/projects/gpt4)
directory of the repository.

```bash copy
# Clone locally
git clone --recurse-submodules https://github.com/ritual-net/infernet-container-starter
# Navigate to the repository
cd infernet-container-starter
```

### Configure the `gpt4` container

#### Configure API key in `config.json`
This is where we'll use the API key we obtained from OpenAI.

```bash
cd projects/gpt4/container
cp config.sample.json config.json
```

In the `containers` field, you will see the following. Replace `your-openai-key` with your OpenAI API key.

```json
"containers": [
    {
        // etc. etc.
        "env": {
            "OPENAI_API_KEY": "your-openai-key" // replace with your OpenAI API key
        }
    }
],
```

### Build the `gpt4` container

First, navigate back to the root of the repository. Then simply run the following command to build the `gpt4`
container:

```bash copy
cd ../../..
make build-container project=gpt4
```

### Deploy infernet node locally

Much like our [hello world](../hello-world/hello-world.md) project, deploying the infernet node is as
simple as running:

```bash copy
make deploy-container project=gpt4
```

## Making a Web2 Request

From here, you can directly make a request to the infernet node:

```bash
curl -X POST http://127.0.0.1:4000/api/jobs \
     -H "Content-Type: application/json" \
     -d '{"containers":["gpt4"], "data": {"prompt": "Hello, can shrimp actually fry rice?"}}'
# {"id":"cab6eea8-8b1e-4144-9a70-f905c5ef375b"}
```

If you have `jq` installed, you can pipe the output of the last command to a file:

```bash copy
curl -X POST http://127.0.0.1:4000/api/jobs \
     -H "Content-Type: application/json" \
     -d '{"containers":["gpt4"], "data": {"prompt": "Hello, can shrimp actually fry rice?"}}' | jq -r ".id" > last-job.uuid
```

You can then check the status of the job by running:

```bash copy
curl -X GET http://127.0.0.1:4000/api/jobs\?id\=cab6eea8-8b1e-4144-9a70-f905c5ef375b
# response [{"id":"07026571-edc8-42ab-b38c-6b3cf19971b6","result":{"container":"gpt4","output":{"message":"No, shrimps cannot fry rice by themselves. However, in culinary terms, shrimp fried rice is a popular dish in which cooked shrimp are added to fried rice along with other ingredients. Cooks or chefs prepare it by frying the rice and shrimps together usually in a wok or frying pan."}},"status":"success"}]
```

And if you have `jq` installed and piped the last output to a file, you can instead run:

```bash
curl -X GET "http://127.0.0.1:4000/api/jobs?id=$(cat last-job.uuid)" | jq .
# returns something like:
[
  {
    "id": "1b50e85b-2295-44eb-9c85-40ae5331bd14",
    "result": {
      "container": "gpt4",
      "output": {
        "output": "Yes, shrimp can be used to make fried rice. In many Asian cuisines, shrimp is a popular ingredient in fried rice dishes. The shrimp adds flavor and protein to the dish, and can be cooked along with the rice and other ingredients such as vegetables, eggs, and seasonings."
      }
    },
    "status": "success"
  }
]
```

## Making a Web3 Request

Now let's bring this service onchain! First we'll have to deploy the contracts.
The [contracts](contracts)
directory contains a simple foundry project with a simple contract called `PromptsGpt`.
This contract exposes a single
function `function promptGPT(string calldata prompt)`. Using this function you'll be
able to make an infernet request.

**Anvil Logs**: First, it's useful to look at the logs of the anvil node to see what's
going on. In a new terminal, run
`docker logs -f anvil-node`.

**Deploying the contracts**: In another terminal, run the following command:

```bash
make deploy-contracts project=gpt4
```

### Calling the contract

Now, let's call the contract. So far everything's been identical to
the [hello world](projects/hello-world/README.mdllo-world/README.md) project. The only
difference here is that calling the contract requires an input. We'll pass that input in
using an env var named
`prompt`:

```bash copy
make call-contract project=gpt4 prompt="Can shrimps actually fry rice"
```

On your anvil logs, you should see something like this:

```bash
eth_sendRawTransaction

_____  _____ _______ _    _         _
|  __ \|_   _|__   __| |  | |  /\   | |
| |__) | | |    | |  | |  | | /  \  | |
|  _  /  | |    | |  | |  | |/ /\ \ | |
| | \ \ _| |_   | |  | |__| / ____ \| |____
|_|  \_\_____|  |_|   \____/_/    \_\______|


subscription Id 1
interval 1
redundancy 1
node 0x70997970C51812dc3A010C7d01b50e0d17dc79C8
output: {'output': 'Yes, shrimps can be used to make fried rice. Fried rice is a versatile dish that can be made with various ingredients, including shrimp. Shrimp fried rice is a popular dish in many cuisines, especially in Asian cuisine.'}

    Transaction: 0x9bcab42cf7348953eaf107ca0ca539cb27f3843c1bb08cf359484c71fcf44d2b
    Gas used: 93726

    Block Number: 3
    Block Hash: 0x1cc39d03bb1d69ea7f32db85d2ee684071e28b6d6de9eab6f57e011e11a7ed08
    Block Time: "Fri, 26 Jan 2024 02:30:37 +0000"
```

beautiful, isn't it? 🥰
