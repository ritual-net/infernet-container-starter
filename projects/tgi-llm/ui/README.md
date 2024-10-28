# Gradio UI

This is a utility UI project to chat with your TGI LLM. Check out the full tutorial [here](https://learn.ritual.net/examples/tgi_inference_with_mistral_7b).

## Configuration

Copy the [`gradio_ui.env.sample`](./gradio_ui.env.sample) file into a new file called `gradio_ui.env` and fill in the necessary environment variables.

```bash
cp gradio_ui.env.sample gradio_ui.env
```

Environment variables are as follows:

```bash
TGI_SERVICE_URL= # URL to your running TGI service
HF_API_TOKEN=
PROMPT_FILE_PATH= # path to a prompt file
```

## Running

You can run the container as follows:

```bash
make run
```

The UI will run on port `3001` on your `localhost`. You can change that configuration [here](./Makefile#L11).

Congratulations! You have successfully set up the Gradio UI for your TGI LLM. Navigate to `http://localhost:3001` in your browser to chat with your LLM instance!

## Next steps

This container is for demonstration purposes only, and is purposefully simplified for readability and ease of comprehension. For a production-ready version of this code, check out:

- The [HF Inference Client Workflow](https://infernet-ml.docs.ritual.net/reference/infernet_ml/workflows/inference/hf_inference_client_workflow): A Python class that runs inference on any models compatible with the HuggingFace API.
- The [HF Inference Client Service](https://infernet-services.docs.ritual.net/reference/hf_inference_client_service): A production-ready, [Infernet](https://docs.ritual.net/infernet/node/introduction)-compatible container that works out-of-the-box with minimal configuration, and serves inference using the `HF Inference Client Workflow`.
