# TGI Service

Check out the full tutorial [here](https://learn.ritual.net/examples/tgi_inference_with_mistral_7b).

### Run the Container

The [Makefile](./Makefile) for this service simply invokes Huggingface's `huggingface/text-generation-inference:1.4` Docker image. Ensure that you are running this on a machine with a GPU.

For example, to run the TGI container with model `mistralai/Mistral-7B-v0.1`, you can use the following command:

```bash
make run model=mistralai/Mistral-7B-v0.1 volume=/path/to/your/data
```

* `model`: is defaulted to `mistralai/Mistral-7B-v0.1`
* `volume`: is defaulted to `./data`
