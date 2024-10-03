# GPT 4
In this example, we run a minimalist container that makes use of the OpenAI [completions API](https://platform.openai.com/docs/api-reference/chat) to serve text generation requests.

## Requirements
To use the model you'll need to have an OpenAI API key. Get one on [OpenAI](https://openai.com/)'s website.

## Run the Container

Build and run this container as follows:

```bash
make build
make run
```

## Test the Container

You can test this container by making inference requests directly through your terminal:

```bash
curl -X POST localhost:3000/service_output -H "Content-Type: application/json" \
  -d '{"source": 1, "data": {"prompt": "can shrimps actually fry rice?"}}'
```

## Next steps

This container is for demonstration purposes only, and is purposefully simplified for readability and ease of comprehension. For a production-ready version of this code, check out:

- The [CSS Inference Workflow](https://infernet-ml.docs.ritual.net/reference/infernet_ml/workflows/inference/css_inference_workflow/): A Python class that supports multiple API providers, including OpenAI, that can be used to build production-ready containers.
- The [CSS Inference Service](https://infernet-services.docs.ritual.net/reference/css_inference_service/): A production-ready, [Infernet](https://docs.ritual.net/infernet/node/introduction)-compatible container that works out-of-the-box with minimal configuration, and serves inference using the `CSS Inference Workflow`.
