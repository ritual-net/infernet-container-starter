from quart import Quart, request, Response

from stable_diffusion_workflow import StableDiffusionWorkflow


def create_app() -> Quart:
    app = Quart(__name__)
    workflow = StableDiffusionWorkflow()
    workflow.setup()

    @app.get("/")
    async def hello():
        return "Hello, World! I'm running stable diffusion"

    @app.post("/service_output")
    async def service_output():
        req_data = await request.get_json()
        image_bytes = workflow.inference(req_data)
        return Response(image_bytes, mimetype="image/png")

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=3002)
