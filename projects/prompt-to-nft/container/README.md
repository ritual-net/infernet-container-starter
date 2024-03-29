# Prompt-to-NFT Container


## Overview


## Building & Running the Container in Isolation

Note that this container is meant to be started by the infernet-node. For development &
Testing purposes, you can run the container in isolation using the following commands.

### Building the Container

Simply run the following command to build the container.

```bash
make build
```

Consult the [Makefile](./Makefile) for the build command.

### Adding Arweave File
Add your arweave wallet file



### Running the Container

To run the container, you can use the following command:

```bash
make run
```

## Testing the Container

Run the following command to run an inference:

```bash
curl -X POST http://127.0.0.1:3000/service_output \
     -H "Content-Type: application/json" \
     -d '{"source":1, "data": {"prompt": "a golden retriever skiing"}}'
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

### Output

By running the above command, you should get a response similar to the following:

```json
[
  [
    [
      0.0010151526657864451,
      0.014391022734344006,
      0.9845937490463257
    ]
  ]
]
```

The response corresponds to the model's prediction for each of the classes:

```python
['setosa', 'versicolor', 'virginica']
```

In this case, the model predicts that the input corresponds to the class `virginica`with
a probability of `0.9845937490463257`(~98.5%).
