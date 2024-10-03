# Running a Torch Model on Infernet

Welcome to this comprehensive guide where we'll explore how to run a `pytorch` model on Infernet. If you've followed
our ONNX example, you'll find this guide to be quite similar.

**Model:** This example uses a pre-trained model to classify iris flowers. The code for the model
is located at the [simple-ml-models](https://github.com/ritual-net/simple-ml-models/tree/main/iris_classification)
repository.

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
under the `projects/torch-iris` directory.

```bash copy
# Clone locally
git clone --recurse-submodules https://github.com/ritual-net/infernet-container-starter
# Navigate to the repository
cd infernet-container-starter
```

### Build the `torch-iris` container

From the top-level directory of this repository, simply run the following command to build the `torch-iris` container:

```bash copy
make build-container project=torch-iris
```

After the container is built, you can deploy an infernet-node that utilizes that
container by running the following command:

```bash
make deploy-container project=torch-iris
```

## Making Inference Requests via Node API (a la Web2 request)

Now, you can make inference requests to the infernet-node. In a new tab, run:

```bash
curl -X POST "http://127.0.0.1:4000/api/jobs" \
     -H "Content-Type: application/json" \
     -d '{"containers":["torch-iris"], "data": {"input": [[1.0380048, 0.5586108, 1.1037828, 1.712096]]}}'
```

You should get an output similar to the following:

```json
{
  "id": "6d5e47f0-5907-4ab2-9523-862dccb80d67"
}
```

Now, you can check the status of the job by running (make sure job id matches the one
you got from the previous request):

```bash
curl "http://127.0.0.1:4000/api/jobs?id=6d5e47f0-5907-4ab2-9523-862dccb80d67"
```

Should return:

```json
[
  {
    "id": "6d5e47f0-5907-4ab2-9523-862dccb80d67",
    "result": {
      "container": "torch-iris",
      "output": {
        "input_data": [
          [
            1.038004755973816,
            0.5586107969284058,
            1.1037827730178833,
            1.7120959758758545
          ]
        ],
        "input_shapes": [
          [
            4
          ]
        ],
        "output_data": [
          [
            0.0016699483385309577,
            0.021144982427358627,
            0.977185070514679
          ]
        ]
      }
    },
    "status": "success"
  }
]
```

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

```solidity
        uint256[] memory iris_data = new uint256[](4);
iris_data[0] = 1_038_004;
iris_data[1] = 558_610;
iris_data[2] = 1_103_782;
iris_data[3] = 1_712_096;
```

We have multiplied the input by 1e6 to have enough decimals accuracy. This can be seen
[here](contracts/src/IrisClassifier.sol#19) in the contract's
code.

### Infernet's Anvil Testnet

To request an on-chain job, you'll need to deploy contracts using the infernet sdk.
We already have a public [anvil node](https://hub.docker.com/r/ritualnetwork/infernet-anvil) docker image which has the
corresponding infernet sdk contracts deployed, along with a node that has
registered itself to listen to on-chain subscription events.

* Registry Address: `0x663F3ad617193148711d28f5334eE4Ed07016602`
* Node Address: `0x70997970C51812dc3A010C7d01b50e0d17dc79C8` (This is the second account in the anvil's accounts.)

### Monitoring the EVM Logs

The infernet node configuration for this project includes our anvil node. You can monitor the logs of the anvil node to
see what's going on. In a new terminal, run:

```bash
docker logs -f anvil-node
```

As you deploy the contract and make requests, you should see logs indicating the
requests and responses.

### Deploying the Contract

Simply run the following command to deploy the contract:

```bash
project=torch-iris make deploy-contracts
```

In your anvil logs you should see the following:

```bash
eth_feeHistory
eth_sendRawTransaction
eth_getTransactionReceipt

    Transaction: 0x8e7e96d0a062285ee6fea864c43c29af65b962d260955e6284ab79dae145b32c
    Contract created: 0x13D69Cf7d6CE4218F646B759Dcf334D82c023d8e
    Gas used: 725947

    Block Number: 1
    Block Hash: 0x88c1a1af024cca6f921284bd61663b1d500aa6d22d06571f0a085c2d8e1ffe92
    Block Time: "Mon, 19 Feb 2024 16:44:00 +0000"

eth_blockNumber
eth_newFilter
eth_getFilterLogs
eth_blockNumber
```

beautiful, we can see that a new contract has been created
at `0x13D69Cf7d6CE4218F646B759Dcf334D82c023d8e`. That's the address of
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
project=torch-iris make call-contract
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


about to decode babyyy
predictions: (adjusted by 6 decimals, 1_000_000 = 100%, 1_000 = 0.1%)
Setosa:  1669
Versicolor:  21144
Virginica:  977185

    Transaction: 0x252158ab9dd2178b6a11e417090988782861d208d8e9bb01c4e0635316fd95c9
    Gas used: 111762

    Block Number: 3
    Block Hash: 0xfba07bd65da8dde644ba07ff67f0d79ed36f388760f27dcf02d96f7912d34c4c
    Block Time: "Mon, 19 Feb 2024 16:54:07 +0000"

eth_blockNumbereth_blockNumber
eth_blockNumber
```

Beautiful! We can see that the same result has been posted to the contract.

For more information about the container, consult
the [container's readme.](container/README.md)

### Next Steps

From here, you can bring your own trained pytorch model, and with minimal changes, you can make it both work with an
infernet-node as well as a smart contract.

### More Information

1. Check out our [ONNX example](../onnx-iris/onnx-iris.md) if you haven't already.
2. [Infernet Callback Consumer Tutorial](https://docs.ritual.net/infernet/sdk/consumers/Callback)
3. [Infernet Nodes Docoumentation](https://docs.ritual.net/infernet/node/introduction)
4. [Infernet-Compatible Containers](https://docs.ritual.net/infernet/node/advanced/containers)
