# TGI Inference with Mistral-7b

In this tutorial we are going to use [Huggingface's TGI (Text Generation Interface)](https://huggingface.co/docs/text-generation-inference/en/index) to run an arbitrary LLM model
and enable users to requests jobs form it, both on-chain and off-chain.

## Install Pre-requisites

For this tutorial you'll need to have the following installed.

1. [Docker](https://docs.docker.com/engine/install/)
2. [Foundry](https://book.getfoundry.sh/getting-started/installation)

## Setting up a TGI LLM Service

Included with this tutorial, is a [containerized llm service](./tgi). We're going to deploy this service on a powerful
machine with access to GPU.

### Rent a GPU machine
To run this service, you will need to have access to a machine with a powerful GPU. In the video above, we use an
A100 instance on [Paperspace](https://www.paperspace.com/).

### Install docker
You will have to install docker.

For Ubuntu, you can run the following commands:

```bash copy
# install docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
As docker installation may vary depending on your operating system, consult the
[official documentation](https://docs.docker.com/engine/install/ubuntu/) for more information.

After installation, you can verify that docker is installed by running:

```bash
# sudo docker run hello-world
Hello from Docker!
```

### Ensure CUDA is installed
Depending on where you rent your GPU machine, CUDA is typically pre-installed. For Ubuntu, you can follow the
instructions [here](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#prepare-ubuntu).

You can verify that CUDA is installed by running:

```bash copy
# verify Installation
python -c '
import torch
print("torch.cuda.is_available()", torch.cuda.is_available())
print("torch.cuda.device_count()", torch.cuda.device_count())
print("torch.cuda.current_device()", torch.cuda.current_device())
print("torch.cuda.get_device_name(0)", torch.cuda.get_device_name(0))
'
```

If CUDA is installed and available, your output will look similar to the following:

```bash
torch.cuda.is_available() True
torch.cuda.device_count() 1
torch.cuda.current_device() 0
torch.cuda.get_device_name(0) Tesla V100-SXM2-16GB
```

### Ensure `nvidia-container-runtime` is installed
For your container to be able to access the GPU, you will need to install the `nvidia-container-runtime`.
On Ubuntu, you can run the following commands:

```bash copy
# Docker GPU support
# nvidia container-runtime repos
# https://nvidia.github.io/nvidia-container-runtime/
curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
sudo apt-key add - distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update

# install nvidia-container-runtime
# https://docs.docker.com/config/containers/resource_constraints/#gpu
sudo apt-get install -y nvidia-container-runtime
```
As always, consult the [official documentation](https://nvidia.github.io/nvidia-container-runtime/) for more
information.

You can verify that `nvidia-container-runtime` is installed by running:

```bash copy
which nvidia-container-runtime-hook
# this should return a path to the nvidia-container-runtime-hook
```

Now, with the pre-requisites installed, we can move on to setting up the TGI service.

### Clone this repository

```bash copy
# Clone locally
git clone --recurse-submodules https://github.com/ritual-net/infernet-container-starter
# Navigate to the repository
cd infernet-container-starter
```

### Run the Stable Diffusion service
```bash copy
make run-service project=tgi-llm service=tgi
```

This will start the `tgi` service. Note that this service will have to download a large model file,
so it may take a few minutes to be fully ready. Downloaded model will get cached, so subsequent runs will be faster.

## Testing the `tgi-llm` service via the gradio UI
Included with this project is a simple gradio chat UI that allows you to interact with the `tgi-llm` service. This is
not needed for running the Infernet node, but a nice way to debug and test the TGI service.

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
Just like our other examples, we're going to clone this repository. All of the code and instructions for this tutorial
can be found in the [`projects/tgi-llm`](../tgi-llm) directory of the repository.

```bash copy
# Clone locally
git clone --recurse-submodules https://github.com/ritual-net/infernet-container-starter
# Navigate to the repository
cd infernet-container-starter
```

### Configure the UI Service
You'll need to configure the UI service to point to the `tgi` service. To do this, you'll have to
pass that info as environment variables. There exists a [`gradio_ui.env.sample`](./ui/gradio_ui.env.sample)
file in the [`projects/tgi-llm/ui`](./ui)
directory. Simply copy this file to `gradio_ui.env` and set the `TGI_SERVICE_URL` to the address of the `tgi` service.

```bash copy
cd projects/tgi-llm/ui
cp gradio_ui.env.sample gradio_ui.env
```

Then modify the content of `gradio_ui.env` to look like this:

```env
TGI_SERVICE_URL={your_service_ip}:{your_service_port} # <- replace with your service ip & port
HF_API_TOKEN={huggingface_api_token} # <- replace with your huggingface api token
PROMPT_FILE_PATH=./prompt.txt # <- path to the prompt file
```

The env vars are as follows:
- `TGI_SERVICE_URL` is the address of the `tgi` service
- `HF_API_TOKEN` is the Huggingface API token. You can get one by signing up at [Huggingface](https://huggingface.co/)
- `PROMPT_FILE_PATH` is the path to the system prompt file. By default it is set to `./prompt.txt`. A simple
`prompt.txt` file is included in the `ui` directory.

### Build the UI service
From the top-level directory of the repository, simply run the following command to build the UI service:

```bash copy
# cd back to the top-level directory
cd ../../..
# build the UI service
make build-service project=tgi-llm service=ui
```

### Run the UI service
In the same directory, you can also run the following command to run the UI service:
```bash copy
make run-service project=tgi-llm service=ui
```

By default the service will run on `http://localhost:3001`. You can navigate to this address in your browser to see
the UI.

### Chat with the TGI service!
Congratulations! You can now chat with the TGI service using the gradio UI. You can enter a prompt and see the
response from the TGI service.

Now that we've tested the TGI service, we can move on to setting up the Infernet Node and the `tgi-llm` container.

## Setting up the Infernet Node along with the `tgi-llm` container

You can follow the following steps on your local machine to setup the Infernet Node and the `tgi-llm` container.

The first couple of steps are identical to that of [the previous section](#ensure-docker--foundry-exist). So if you've already completed those
steps, you can skip to [building the tgi-llm container](#build-the-tgi-llm-container).

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
[`projects/tgi-llm`](../tgi-llm)
directory of the repository.

```bash copy
# Clone locally
git clone --recurse-submodules https://github.com/ritual-net/infernet-container-starter
# Navigate to the repository
cd infernet-container-starter
```

### Configure the `tgi-llm` container

#### Configure the URL for the TGI Service
The `tgi-llm` container needs to know where to find the TGI service that we started in the steps above. To do this,
we need to modify the configuration file for the `tgi-llm` container. We have a sample [config.json](./config.sample.json) file.
Simply navigate to the `projects/tgi-llm` directory and set up the config file:

```bash
cd projects/tgi-llm/container
cp config.sample.json config.json
```

In the `containers` field, you will see the following:

```json
"containers": [
    {
        // etc. etc.
        "env": {
            "TGI_SERVICE_URL": "http://{your_service_ip}:{your_service_port}" // <- replace with your service ip & port
        }
    }
},
```

### Build the `tgi-llm` container

Simply run the following command to build the `tgi-llm` container:

```bash copy
make build-container project=tgi-llm
```

### Deploy the `tgi-llm` container with Infernet

You can run a simple command to deploy the `tgi-llm` container along with bootstrapping the rest of the
Infernet node stack in one go:

```bash copy
make deploy-container project=tgi-llm
```

### Check the running containers

At this point it makes sense to check the running containers to ensure everything is running as expected.

```bash
# > docker container ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
0dbc30f67e1e ritualnetwork/example-tgi-llm-infernet:latest "hypercorn app:creat…" 8 seconds ago Up 7 seconds
0.0.0.0:3000->3000/tcp tgi-llm
0c5140e0f41b ritualnetwork/infernet-anvil:0.0.0 "anvil --host 0.0.0.…" 23 hours ago Up 23 hours
0.0.0.0:8545->3000/tcp anvil-node
f5682ec2ad31 ritualnetwork/infernet-node:latest "/app/entrypoint.sh" 23 hours ago Up 9 seconds
0.0.0.0:4000->4000/tcp deploy-node-1
c1ece27ba112 fluent/fluent-bit:latest "/fluent-bit/bin/flu…" 23 hours ago Up 10 seconds 2020/tcp,
0.0.0.0:24224->24224/tcp, :::24224->24224/tcp deploy-fluentbit-1
3cccea24a303 redis:latest "docker-entrypoint.s…" 23 hours ago Up 10 seconds 0.0.0.0:6379->6379/tcp,
:::6379->6379/tcp deploy-redis-1
```

You should see five different images running, including the Infernet node and the `tgi-llm` container.

### Send a job request to the `tgi-llm` container
From here, we can make a Web-2 job request to the container by posting a request to the [`api/jobs`](https://docs.ritual.net/infernet/node/api#2a-post-apijobs) endpoint.

```bash copy
curl -X POST http://127.0.0.1:4000/api/jobs \
-H "Content-Type: application/json" \
-d '{"containers": ["tgi-llm"], "data": {"prompt": "Can shrimp actually fry rice fr?"}}'
# {"id":"7a375a56-0da0-40d8-91e0-6440b3282ed8"}
```
You will get a job id in response. You can use this id to check the status of the job.

### Check the status of the job
You can make a `GET` request to the [`api/jobs`](https://docs.ritual.net/infernet/node/api#3-get-apijobs) endpoint to check the status of the job.

```bash copy
curl -X GET "http://127.0.0.1:4000/api/jobs?id=7a375a56-0da0-40d8-91e0-6440b3282ed8"
# [{"id":"7a375a56-0da0-40d8-91e0-6440b3282ed8","result":{"container":"tgi-llm","output":{"data":"\n\n## Can you fry rice in a wok?\n\nThe wok is the"}},"status":"success"}]
```

Congratulations! You have successfully setup the Infernet Node and the `tgi-llm` container. Now let's move on to
calling our service from a smart contract (a la web3 request).


## Calling our service from a smart contract

In the following steps, we will deploy our [consumer contract](https://github.com/ritual-net/infernet-container-starter/blob/main/projects/tgi-llm/contracts/src/Prompter.sol) and make a subscription request by calling the
contract.

### Setup
Ensure that you have followed the steps in the previous section up until [here](#check-the-running-containers) to setup
the Infernet Node and the `tgi-llm` container.

Notice that in [the step above](#check-the-running-containers) we have an Anvil node running on port `8545`.

By default, the [`anvil-node`](https://hub.docker.com/r/ritualnetwork/infernet-anvil) image used deploys the
[Infernet SDK](https://docs.ritual.net/infernet/sdk/introduction) and other relevant contracts for you:
- Coordinator: `0x663F3ad617193148711d28f5334eE4Ed07016602`
- Primary node: `0x70997970C51812dc3A010C7d01b50e0d17dc79C8`

### Deploy our `Prompter` smart contract

In this step, we will deploy our  [`Prompter.sol`](./contracts/src/Prompter.sol)
to the Anvil node. This contract simply allows us to submit a prompt to the LLM, and receives the result of the
prompt and prints it to the anvil console.

#### Anvil logs

During this process, it is useful to look at the logs of the Anvil node to see what's going on. To follow the logs,
in a new terminal, run:

```bash copy
docker logs -f anvil-node
```

#### Deploying the contract

Once ready, to deploy the `Prompter` consumer contract, in another terminal, run:

```bash copy
make deploy-contracts project=tgi-llm
```

You should expect to see similar Anvil logs:

```bash
# > make deploy-contracts project=tgi-llm
eth_getTransactionReceipt

Transaction: 0x17a9d17cc515d39eef26b6a9427e04ed6f7ce6572d9756c07305c2df78d93ffe
Contract created: 0x13D69Cf7d6CE4218F646B759Dcf334D82c023d8e
Gas used: 731312

Block Number: 1
Block Hash: 0xd17b344af15fc32cd3359e6f2c2724a8d0a0283fc3b44febba78fc99f2f00189
Block Time: "Wed, 6 Mar 2024 18:21:01 +0000"

eth_getTransactionByHash
```

From our logs, we can see that the `Prompter` contract has been deployed to address
`0x13D69Cf7d6CE4218F646B759Dcf334D82c023d8e`.

### Call the contract

Now, let's call the contract to with a prompt! In the same terminal, run:

```bash copy
make call-contract project=tgi-llm prompt="What is 2 * 3?"
```

You should first expect to see an initiation transaction sent to the `Prompter` contract:

```bash

eth_getTransactionReceipt

Transaction: 0x988b1b251f3b6ad887929a58429291891d026f11392fb9743e9a90f78c7a0801
Gas used: 190922

Block Number: 2
Block Hash: 0x51f3abf62e763f1bd1b0d245a4eab4ced4b18f58bd13645dbbf3a878f1964044
Block Time: "Wed, 6 Mar 2024 18:21:34 +0000"

eth_getTransactionByHash
eth_getTransactionReceipt

```
Shortly after that you should see another transaction submitted from the Infernet Node which is the
result of your on-chain subscription and its associated job request:

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
output:

2 * 3 = 6

Transaction: 0xdaaf559c2baba212ab218fb268906613ce3be93ba79b37f902ff28c8fe9a1e1a
Gas used: 116153

Block Number: 3
Block Hash: 0x2f26b2b487a4195ff81865b2966eab1508d10642bf525a258200eea432522e24
Block Time: "Wed, 6 Mar 2024 18:21:35 +0000"

eth_blockNumber
```

We can now confirm that the address of the Infernet Node (see the logged `node` parameter in the Anvil logs above)
matches the address of the node we setup by default for our Infernet Node.

Congratulations! 🎉 You have successfully enabled a contract to have access to a TGI LLM service.
