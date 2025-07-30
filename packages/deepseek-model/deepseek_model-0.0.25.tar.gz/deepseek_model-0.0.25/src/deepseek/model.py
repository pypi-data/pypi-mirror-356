"""DeepSeek model interaction"""

import sys
from together import Together
from together.types import ChatCompletionChunk
from .helper import prompt_preview, strip_thinking


def interact(messages: list):
    """Interact with DeepSeek model using message objects"""
    model = "deepseek-ai/DeepSeek-R1"
    client = Together()

    # Preview the entire conversation
    preview = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    prompt_preview(preview)

    if not messages:
        raise ValueError("No messages to send")

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
        max_tokens=16384,
    )

    full_response = ""
    for chunk in stream:
        if not isinstance(chunk, ChatCompletionChunk):
            raise ValueError("Unexpected chunk type")
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            sys.stderr.write(content)

    if not sys.stdout.isatty() and sys.stderr.isatty():
        sys.stdout.write(strip_thinking(full_response))

    if hasattr(chunk, "usage") and chunk.usage:
        sys.stderr.write("\n\nUsage: " + chunk.usage.model_dump_json() + "\n")
