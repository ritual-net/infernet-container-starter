# infernet-container-starter

Starter examples for deploying to infernet.

# Getting Started

To interact with infernet, one could either create a job by accessing an infernet
node directly through it's API (we'll refer to this as an off-chain job), or by
creating a subscription on-chain (we'll refer to this as an on-chain job).

## Requesting an off-chain job: Hello World!

The easiest way to get started is to run our hello-world container.
This is a simple [flask-app](projects/hello-world/container/src/app.py) that
is compatible with `infernet`, and simply
[echoes what you send to it](./projects/hello-world/container/src/app.py#L16).

We already have it [hosted on docker hub](https://hub.docker.com/r/ritualnetwork/hello-world-infernet) .
If you're curious how it's made, you can
follow the instructions [here](projects/hello-world/container/README.md) to build your own infernet-compatible
container.

### Install Docker

To run this, you'll need to have docker installed. You can find instructions
for installing docker [here](https://docs.docker.com/install/).

### Running Locally

First, ensure that the docker daemon is running.

Then, from the top-level project directory, Run the following make command:

```
project=hello-world make deploy-container
```

This will deploy an infernet node along with the `hello-world` image.

### Creating an off-chain job through the API

You can create an off-chain job by posting to the `node` directly.

```bash
curl -X POST http://127.0.0.1:4000/api/jobs \
     -H "Content-Type: application/json" \
     -d '{"containers":["hello-world"], "data": {"some": "input"}}'
# returns
{"id":"d5281dd5-c4f4-4523-a9c2-266398e06007"}
``` 

This will return the id of that job.

### Getting the status/result/errors of a job

You can check the status of a job like so:

```bash
curl -X GET http://127.0.0.1:4000/api/jobs?id=d5281dd5-c4f4-4523-a9c2-266398e06007
# returns
[{"id":"d5281dd5-c4f4-4523-a9c2-266398e06007", "result":{"container":"hello-world","output": {"output":"hello, world!, your input was: {'source': 1, 'data': {'some': 'input'}}"}} ,"status":"success"}]
```

### Configuration

This project already comes with a pre-filled config file. The config
file for the hello-world project is located [here](projects/hello-world/container/config.json):

```bash
projects/hello-world/config.json
```

## Requesting an on-chain job

In this section we'll go over how to request an on-chain job in a local testnet.

### Infernet's Anvil Testnet

To request an on-chain job, you'll need to deploy contracts using the infernet sdk.
We already have a public [anvil node](https://hub.docker.com/r/ritualnetwork/infernet-anvil) docker image which has the
corresponding infernet sdk contracts deployed, along with a node that has 
registered itself to listen to on-chain subscription events.

* Coordinator Address: `0x5FbDB2315678afecb367f032d93F642f64180aa3`
* Node Address: `0x70997970C51812dc3A010C7d01b50e0d17dc79C8` (This is the second account in the anvil's accounts.)

### Deploying Infernet Node & Infernet's Anvil Testnet

This step is similar to the section above:

```bash
project=hello-world make deploy-container
```

In another terminal, run `docker container ls`, you should see something like this

```bash
CONTAINER ID   IMAGE                                      COMMAND                  CREATED          STATUS          PORTS                                NAMES
c2ca0ffe7817   ritualnetwork/infernet-anvil:0.0.0         "anvil --host 0.0.0.…"   9 seconds ago    Up 8 seconds    0.0.0.0:8545->3000/tcp               anvil-node
0b686a6a0e5f   ritualnetwork/hello-world-infernet:0.0.2   "gunicorn app:create…"   9 seconds ago    Up 8 seconds    0.0.0.0:3000->3000/tcp               hello-world
28b2e5608655   ritualnetwork/infernet-node:0.1.1          "/app/entrypoint.sh"     10 seconds ago   Up 10 seconds   0.0.0.0:4000->4000/tcp               deploy-node-1
03ba51ff48b8   fluent/fluent-bit:latest                   "/fluent-bit/bin/flu…"   10 seconds ago   Up 10 seconds   2020/tcp, 0.0.0.0:24224->24224/tcp   deploy-fluentbit-1
a0d96f29a238   redis:latest                               "docker-entrypoint.s…"   10 seconds ago   Up 10 seconds   0.0.0.0:6379->6379/tcp               deploy-redis-1
```

You can see that the anvil node is running on port `8545`, and the infernet
node is running on port `4000`. Same as before.

### Deploying Consumer Contracts

We have a [sample forge project](./projects/hello-world/contracts) which contains
a simple consumer contract, [`SaysGM`](./projects/hello-world/contracts/src/SaysGM.sol).
All this contract does is to request a job from the infernet node, and upon receiving
the result, it will use the `forge` console to print the result.

**Anvil Logs**: First, it's useful to look at the logs of the anvil node to see what's going on. In
a new terminal, run `docker logs -f anvil-node`.

**Deploying the contracts**: In another terminal, run the following command:

```bash
project=hello-world make deploy-contracts
```

You should be able to see the following logs in the anvil logs:

```bash
eth_sendRawTransaction
eth_getTransactionReceipt

    Transaction: 0x23ca6b1d1823ad5af175c207c2505112f60038fc000e1e22509816fa29a3afd6
    Contract created: 0x663f3ad617193148711d28f5334ee4ed07016602
    Gas used: 476669

    Block Number: 1
    Block Hash: 0x6b026b70fbe97b4a733d4812ccd6e8e25899a1f6c622430c3fb07a2e5c5c96b7
    Block Time: "Wed, 17 Jan 2024 22:17:31 +0000"

eth_getTransactionByHash
eth_getTransactionReceipt
eth_blockNumber
```

We can see that a new contract has been created at `0x663f3ad617193148711d28f5334ee4ed07016602`.
That's the address of the `SaysGM` contract.

### Calling the contract

Now, let's call the contract. In the same terminal, run the following command:

```bash
project=hello-world make call-contract
```

You should first see that a transaction was sent to the `SaysGm` contract:

```bash
eth_getTransactionReceipt

    Transaction: 0xe56b5b6ac713a978a1631a44d6a0c9eb6941dce929e1b66b4a2f7a61b0349d65
    Gas used: 123323

    Block Number: 2
    Block Hash: 0x3d6678424adcdecfa0a8edd51e014290e5f54ee4707d4779e710a2a4d9867c08
    Block Time: "Wed, 17 Jan 2024 22:18:39 +0000"
eth_getTransactionByHash

```

Then, right after that you should see another transaction submitted by the `node`,
which is the result of the job request:

```bash
eth_chainId
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
input:
0x
output:
0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000607b276f7574707574273a202268656c6c6f2c20776f726c64212c20796f757220696e707574207761733a207b27736f75726365273a20302c202764617461273a20273437366636663634323036643666373236653639366536373231277d227d
proof:
0x

    Transaction: 0x949351d02e2c7f50ced2be06d14ca4311bd470ec80b135a2ce78a43f43e60d3d
    Gas used: 94275

    Block Number: 3
    Block Hash: 0x57ed0cf39e3fb3a91a0d8baa5f9cb5d2bdc1875f2ad5d6baf4a9466f522df354
    Block Time: "Wed, 17 Jan 2024 22:18:40 +0000"


eth_blockNumber
eth_newFilter

```

We can see that the address of the `node` matches the address of the node in
our ritual anvil node.

### Next Steps

To learn more about on-chain requests, check out the following resources:

1. [Tutorial](./projects/hello-world/contracts/Tutorial.md) on this project's consumer smart contracts.
2. [Infernet Callback Consumer Tutorial](https://docs.ritual.net/infernet/sdk/consumers/Callback)
3. [Infernet Nodes Docoumentation](https://docs.ritual.net/infernet/nodes)


