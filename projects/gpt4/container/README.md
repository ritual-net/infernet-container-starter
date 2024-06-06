# GPT 4
In this example, we run a minimalist container that makes use of our closed-source model
workflow: `CSSInferenceWorkflow`. Refer to [src/app.py](src/app.py) for the
implementation of the quart application.

## Requirements
To use the model you'll need to have an OpenAI api key. Get one at
[OpenAI](https://openai.com/)'s website.

## Run the Container

```bash
make run
```

## Test the Container
```bash
curl -X POST localhost:3000/service_output -H "Content-Type: application/json" \
  -d '{"source": 1, "data": {"prompt": "can shrimps actually fry rice?"}}'
```
