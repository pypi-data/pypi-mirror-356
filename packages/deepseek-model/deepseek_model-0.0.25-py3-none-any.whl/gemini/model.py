"""Gemini model interaction"""

import sys

from google import genai
from google.genai import types
from .helper import get_question, prompt_preview


async def interact():
    """Interact with Gemini model using message objects"""

    client = genai.Client()
    model = "gemini-2.5-pro-preview-06-05"

    question = get_question()

    if not question:
        raise ValueError("No messages to send")

    prompt_preview(question)

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)],
        )
    ]

    last_chunk = None

    async for chunk in await client.aio.models.generate_content_stream(
        model=model,
        contents=contents,
    ):
        last_chunk = chunk
        print(last_chunk.text, end="", file=sys.stderr)
        if not sys.stdout.isatty() and sys.stderr.isatty():
            print(last_chunk.text, end="")

    print(
        "\n\nTotal token count: " + str(last_chunk.usage_metadata.total_token_count),
        file=sys.stderr,
    )
