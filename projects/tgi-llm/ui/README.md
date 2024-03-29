# Gradio UI

This is a utility UI project to chat with your TGI LLM.

## Configuration

Copy the [`gradio_ui.env.sample`](./gradio_ui.env.sample) file into a new file
called `gradio_ui.env` and fill in the necessary environment variables.

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

Simply run:

```bash
make run
```

The UI will run on port `3001` on your localhost. You can change that configuration
[here](./Makefile#L11).

Congratulations! You have successfully set up the Gradio UI for your TGI LLM.

Now you can go to `http://localhost:3001` and chat with your LLM instance.
