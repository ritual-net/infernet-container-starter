# Running an ONNX Model on Infernet

Welcome to this comprehensive guide where we'll explore how to run an ONNX model on Infernet, using our [infernet-container-starter](https://github.com/ritual-net/infernet-container-starter/)
examples repository. This tutorial is designed to give you and end-to-end understanding of how you can run your own
custom pre-trained models, and interact with them on-chain and off-chain.

**Model:** This example uses a pre-trained model to classify iris flowers. The code for the model
is located at our [`simple-ml-models`](https://github.com/ritual-net/simple-ml-models/tree/main/iris_classification) repository.

## Pre-requisites

For this tutorial you'll need to have the following installed.

1. [Docker](https://docs.docker.com/engine/install/)
2. [Foundry](https://book.getfoundry.sh/getting-started/installation)

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

If you haven't already, clone the infernet-container-starter repository. All of the code for this tutorial is located
under the `projects/onnx-iris` directory.

```bash copy
# Clone locally
git clone --recurse-submodules https://github.com/ritual-net/infernet-container-starter
# Navigate to the repository
cd infernet-container-starter
```

## Making Inference Requests via Node API (a la Web2 request)

### Build the `onnx-iris` container

From the top-level directory of this repository, simply run the following command to build the `onnx-iris` container:

```bash copy
make build-container project=onnx-iris
```

After the container is built, you can deploy an infernet-node that utilizes that
container by running the following command:

```bash copy
make deploy-container project=onnx-iris
```

Now, you can make inference requests to the infernet-node. In a new tab, run:

```bash copy
curl -X POST "http://127.0.0.1:4000/api/jobs" \
     -H "Content-Type: application/json" \
     -d '{"containers":["onnx-iris"], "data": {"input": [[1.0380048, 0.5586108, 1.1037828, 1.712096]]}}'
```

You should get an output similar to the following:

```json
{
  "id": "074b9e98-f1f6-463c-b185-651878f3b4f6"
}
```

Now, you can check the status of the job by running (Make sure job id matches the one
you got from the previous request):

```bash
curl -X GET "http://127.0.0.1:4000/api/jobs?id=074b9e98-f1f6-463c-b185-651878f3b4f6"
```

Should return:

```json
[
  {
    "id": "074b9e98-f1f6-463c-b185-651878f3b4f6",
    "result": {
      "container": "onnx-iris",
      "output": [
        [
          [
            0.0010151526657864451,
            0.014391022734344006,
            0.9845937490463257
          ]
        ]
      ]
    },
    "status": "success"
  }
]
```

The `output` corresponds to the model's prediction for each of the classes:

```python
['setosa', 'versicolor', 'virginica']
```

In this case, the model predicts that the input corresponds to the class `virginica`with
a probability of `0.9845937490463257`(~98.5%).

#### Note Regarding the Input

The inputs provided above correspond to an iris flower with the following
characteristics. Refer to the

1. Sepal Length: `5.5cm`
2. Sepal Width: `2.4cm`
3. Petal Length: `3.8cm`
4. Petal Width: `1.1cm`

Putting this input into a vector and scaling it, we get the following scaled input:

```python
[1.0380048, 0.5586108, 1.1037828, 1.712096]
```

Refer
to [this function in the model's repository](https://github.com/ritual-net/simple-ml-models/blob/03ebc6fb15d33efe20b7782505b1a65ce3975222/iris_classification/iris_inference_pytorch.py#L13)
for more information on how the input is scaled.

For more context on the Iris dataset, refer to
the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/iris).

## Making Inference Requests via Contracts (a la Web3 request)

The [contracts](contracts) directory contains a simple forge
project that can be used to interact with the Infernet Node.

Here, we have a very simple
contract, [IrisClassifier](contracts/src/IrisClassifier.sol),
that requests a compute job from the Infernet Node and then retrieves the result.
We are going to make the same request as above, but this time using a smart contract.
Since floats are not supported in Solidity, we convert all floats to `uint256` by
multiplying the input vector entries by `1e6`:

```Solidity
        uint256[] memory iris_data = new uint256[](4);
iris_data[0] = 1_038_004;
iris_data[1] = 558_610;
iris_data[2] = 1_103_782;
iris_data[3] = 1_712_096;
```

We have multiplied the input by 1e6 to have enough accuracy. This can be seen
[here](contracts/src/IrisClassifier.sol#19) in the contract's
code.

### Monitoring the EVM Logs

The infernet node configuration for this project includes
an [infernet anvil node](projects/hello-world/README.mdllo-world/README.md#77) with pre-deployed contracts. You can view the
logs of the anvil node to see what's going on. In a new terminal, run:

```bash
docker logs -f anvil-node
```

As you deploy the contract and make requests, you should see logs indicating the
requests and responses.

### Deploying the Contract

Simply run the following command to deploy the contract:

```bash
project=onnx-iris make deploy-contracts
```

In your anvil logs you should see the following:

```bash
eth_getTransactionReceipt

    Transaction: 0xeed605eacdace39a48635f6d14215b386523766f80a113b4484f542d862889a4
    Contract created: 0x13D69Cf7d6CE4218F646B759Dcf334D82c023d8e
    Gas used: 714269

    Block Number: 1
    Block Hash: 0x4e6333f91e86a0a0be357b63fba9eb5f5ba287805ac35aaa7698fd05445730f5
    Block Time: "Mon, 19 Feb 2024 20:31:17 +0000"

eth_blockNumber
```

beautiful, we can see that a new contract has been created
at `0x663F3ad617193148711d28f5334eE4Ed07016602`. That's the address of
the `IrisClassifier` contract. We are now going to call this contract. To do so,
we are using
the [CallContract.s.sol](contracts/script/CallContract.s.sol)
script. Note that the address of the
contract [is hardcoded in the script](contracts/script/CallContract.s.sol#L13),
and should match the address we see above. Since this is a test environment and we're
using a test deployer address, this address is quite deterministic and shouldn't change.
Otherwise, change the address in the script to match the address of the contract you
just deployed.

### Calling the Contract

To call the contract, run the following command:

```bash
project=onnx-iris make call-contract
```

In the anvil logs, you should see the following:

```bash
eth_sendRawTransaction


_____  _____ _______ _    _         _
|  __ \|_   _|__   __| |  | |  /\   | |
| |__) | | |    | |  | |  | | /  \  | |
|  _  /  | |    | |  | |  | |/ /\ \ | |
| | \ \ _| |_   | |  | |__| / ____ \| |____
|_|  \_\_____|  |_|   \____/_/    \_\______|


predictions: (adjusted by 6 decimals, 1_000_000 = 100%, 1_000 = 0.1%)
Setosa:  1015
Versicolor:  14391
Virginica:  984593

    Transaction: 0x77c7ff26ed20ffb1a32baf467a3cead6ed81fe5ae7d2e419491ca92b4ac826f0
    Gas used: 111091

    Block Number: 3
    Block Hash: 0x78f98f4d54ebdca2a8aa46c3b9b7e7ae36348373dbeb83c91a4600dd6aba2c55
    Block Time: "Mon, 19 Feb 2024 20:33:00 +0000"

eth_blockNumber
eth_newFilter
eth_getFilterLogs
```

Beautiful! We can see that the same result has been posted to the contract.

### Next Steps

From here, you can bring your own pre-trained ONNX model, and with minimal changes, you can make it both work with an
infernet-node as well as a smart contract.

### More Information

1. Check out our [other examples](../../readme.md) if you haven't already
2. [Infernet Callback Consumer Tutorial](https://docs.ritual.net/infernet/sdk/consumers/Callback)
3. [Infernet Nodes Docoumentation](https://docs.ritual.net/infernet/node/introduction)
4. [Infernet-Compatible Containers](https://docs.ritual.net/infernet/node/containers)
