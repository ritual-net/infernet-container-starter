# GPT 4

In this example, we will run a minimalist container that makes use of the OpenAI [completions API](https://platform.openai.com/docs/api-reference/chat) to serve text generation requests.

Check out the full tutorial [here](https://learn.ritual.net/examples/running_gpt_4).

## Requirements

To use the model you'll need to have an OpenAI API key. Get one on [OpenAI](https://openai.com/)'s website.

## Build the Container

Simply run the following command to build the container:

```bash
make build
```

## Run the Container

To run the container, you can use the following command:

```bash
make run
```

## Test the Container

You can test the container by making inference requests directly via your terminal:

```bash
curl -X POST localhost:3000/service_output -H "Content-Type: application/json" \
  -d '{"source": 1, "data": {"prompt": "can shrimps actually fry rice?"}}'
```

## Next steps

This container is for demonstration purposes only, and is purposefully simplified for
readability and ease of comprehension. For a production-ready version of this code, check out:

- The [CSS Inference Workflow](https://infernet-ml.docs.ritual.net/reference/infernet_ml/workflows/inference/css_inference_workflow/): A Python class that supports multiple API providers, including OpenAI, and can be used to build production-ready containers.
- The [CSS Inference Service](https://infernet-services.docs.ritual.net/reference/css_inference_service/): A production-ready, [Infernet](https://docs.ritual.net/infernet/node/introduction)-compatible container that works out-of-the-box with minimal configuration, and serves inference using the `CSS Inference Workflow`.
