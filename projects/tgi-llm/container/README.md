# TGI LLM

In this example, we're running an infernet node along with a TGI service.

## Deploying TGI Service

If you have your own TGI service running, feel free to skip this part. Otherwise,
you can deploy the TGI service using the following command.

Make sure you have a machine with proper GPU support. Clone this repository &
run the following command:

```bash
make run-service project=tgi-llm service=tgi
```

## Deploying Infernet Node Locally

Running an infernet node involves a simple configuration step & running step.

### Configuration

Copy our [sample config file](./config.sample.json) into a new file
called `config.json`.

```bash
cp config.sample.json config.json
```

Then provide the `"env"` field of the `"containers"` section of the file to point to the
TGI Service you just deployed.

```json
{
  // etc.
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
        "TGI_SERVICE_URL": "http://{your-service-ip}:{your-service-port}" // <- Change this to the TGI service you deployed
      }
    }
  ]
}
```

### Running the Infernet Node Locally

With that out of the way, you can now run the infernet node using the following command
at the top-level directory of this repo:

```
make deploy-container project=tgi-llm
```

## Testing the Infernet Node

You can test the infernet node by posting a job in the node's REST api.

```bash
curl -X POST "http://127.0.0.1:4000/api/jobs" \
   -H "Content-Type: application/json" \
   -d '{"containers":["tgi-llm"], "data": {"prompt": "can shrimp actually fry rice?"}}'
```

You can expect a response similar to the following:

```json
{
  "id": "f026c7c2-7027-4c2d-b662-2b48c9433a12"
}
```

You can then check the status of the job using the following command:

```bash
curl -X GET http://127.0.0.1:4000/api/jobs\?id\=f026c7c2-7027-4c2d-b662-2b48c9433a12
[{"id":"f026c7c2-7027-4c2d-b662-2b48c9433a12","result":{"container":"tgi-llm","output":{"output":"\n\nI\u2019m not sure if this is a real question or not, but I\u2019m"}},"status":"success"}]
```

Congratulations! You've successfully ran an infernet node with a TGI service.
