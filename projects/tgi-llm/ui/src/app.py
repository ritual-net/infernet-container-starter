import os
from builtins import str
from pathlib import Path
from typing import Union, cast, Any, Callable

import gradio as gr  # type: ignore
from dotenv import load_dotenv
from huggingface_hub import InferenceClient  # type: ignore

load_dotenv()

TGI_SERVICE_URL = os.getenv("TGI_SERVICE_URL")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

client = InferenceClient(model=TGI_SERVICE_URL)


def start_interface(
    lambdafn: Callable[[str, list[str]], Any],
    examples: list[str],
    title: str,
    description: str,
    share: bool = True,
    height: int = 300,
    placeholder: str = "Chat with me!",
    scale: int = 7,
    container: bool = False,
) -> None:
    """
    Starts the Gradio interface for the Jazz model.

    Args:
        lambdafn (callable): text_generation lambda fn with message, history
        examples (list[str]): A list of example inputs for the interface.
        title (str): The gradio title.
        description (str): The gradio description.
        share (bool): Whether to generate a global gradio link for 72 hours.
        height (int): Height of chat window in pixels.
        placeholder (str): Placeholder when chat window is empty.
        scale (int): The scale of the chat window.
        container (bool): Show the chat window in a container.
    """
    gr.ChatInterface(
        lambdafn,
        chatbot=gr.Chatbot(height=height),
        textbox=gr.Textbox(placeholder=placeholder, container=container, scale=scale),
        description=description,
        title=title,
        examples=examples,
        retry_btn="Retry",
        undo_btn="Undo",
        clear_btn="Clear",
    ).queue().launch(share=share, server_name="0.0.0.0")


def read_text_file(file_path: Union[Path, str]) -> str:
    """Reads content from file as a string."""
    with open(file_path, "r") as file:
        return file.read()


def main() -> None:
    cwd = os.getcwd()

    PROMPT_FILE_PATH: str = cast(str, os.getenv("PROMPT_FILE_PATH"))

    if not PROMPT_FILE_PATH:
        raise ValueError("PROMPT_FILE_PATH is not set in the environment.")

    input_text = read_text_file(os.path.join(cwd, PROMPT_FILE_PATH))

    def prompt_formatter(user_prompt: str, input_text: str) -> str:
        return user_prompt

    # You should write your own lambdafn to set the parameters
    # Gradio doesn't currently support functions with more than
    # [message,history] as parameters into the interface
    # if you don't want the user to see them.
    def stream_inference(message: str, history: list[str]) -> Any:
        response = client.text_generation(
            prompt_formatter(message, input_text),
            max_new_tokens=40,
            temperature=0.3,
            details=True,
        ).generated_text
        # this is just for the gradio front end, you can ignore for
        # backend in the ML model for strikethroughs.
        if response.startswith("<s>"):
            response = response[3:]
        yield response

    title = "Your Ritual Model🎷"
    description = "This is the demo for your model."

    # if you want a global url others can visit.
    share = True
    examples = ["Can shrimp actually fry rice?"]

    start_interface(
        lambdafn=stream_inference,
        title=title,
        description=description,
        share=share,
        examples=examples,
    )


if __name__ == "__main__":
    main()
