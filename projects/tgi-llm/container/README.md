# TGI LLM

In this example, we're running an Infernet Node along with a TGI service.

## Deploying TGI Service

If your TGI service is already running, feel free to skip this part. Otherwise,
you can deploy a TGI service using the following command.

For more information, check out our [Setting up a TGI LLM Service](https://learn.ritual.net/examples/tgi_inference_with_mistral_7b#setting-up-a-tgi-llm-service) tutorial!

## Deploying Infernet Node Locally

Running an Infernet Node involves a simple configuration step & running step.

### Configuration

Copy our [sample config file](./config.sample.json) into a new file called `config.json`.

```bash
cp config.sample.json config.json
```

Then provide the `"env"` field of the `"containers"` section of the file to point to the
TGI Service you just deployed.

```json
{
  // ...
  "containers": [
    {
      "id": "tgi-llm",
      "image": "ritualnetwork/llm_inference_service:latest",
      "external": true,
      "port": "3000",
      "allowed_delegate_addresses": [],
      "allowed_addresses": [],
      "allowed_ips": [],
      "command": "--bind=0.0.0.0:3000 --workers=2",
      "env": {
        // TODO: replace with your service ip & port
        "TGI_SERVICE_URL": "http://{your-service-ip}:{your-service-port}"
      }
    }
  ]
}
```

### Running the Infernet Node Locally

With that out of the way, you can now run the Infernet Node using the following command
at the top-level directory of this repo:

```
make deploy-container project=tgi-llm
```

## Testing the Infernet Node

You can test the Infernet Node by posting a job in the node's REST api.

```bash copy
curl -X POST "http://127.0.0.1:4000/api/jobs" \
   -H "Content-Type: application/json" \
   -d '{"containers": ["tgi-llm"], "data": {"prompt": "can shrimp actually fry rice?"}}'
```

which should return something like this:

```json
{
  "id": "f026c7c2-7027-4c2d-b662-2b48c9433a12"
}
```

You can then check the status of the job using the following command:

```bash copy
curl -X GET http://127.0.0.1:4000/api/jobs\?id\=f026c7c2-7027-4c2d-b662-2b48c9433a12
```

You can expect a response similar to the following:

```
# [
#   {
#     "id":"f026c7c2-7027-4c2d-b662-2b48c9433a12",
#     "result": {
#       "container": "tgi-llm",
#       "output":
#         {
#           "output": "\n\nI\u2019m not sure if this is a real question or not, but I\u2019m"
#         }
#       },
#     "status": "success"
#   }
# ]
```

Congratulations! You've successfully ran an Infernet Node with a TGI service.

## Next steps

This container is for demonstration purposes only, and is purposefully simplified for readability and ease of comprehension. For a production-ready version of this code, check out:

- The [TGI Client Inference Workflow](https://infernet-ml.docs.ritual.net/reference/infernet_ml/workflows/inference/tgi_client_inference_workflow): A Python class that implements a TGI service client similar to this example, and can be used to build production-ready containers.
- The [TGI Client Inference Service](https://infernet-services.docs.ritual.net/reference/tgi_client_inference_service): A production-ready, [Infernet](https://docs.ritual.net/infernet/node/introduction)-compatible container that works out-of-the-box with minimal configuration, and serves inference using the `TGI Client Inference Workflow`.
