"""Helper file functions for Gemini CLI"""

import os
import readline  # pylint: disable=unused-import
import sys

from dataclasses import dataclass


def get_width() -> int:
    """Get terminal width"""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def prompt_preview(prompt: str):
    """Preview prompt with visual markers"""
    width = get_width()
    start = "[ PROMPT ] "
    end = "[ / PROMPT ] "
    asterisks_start = "*" * (width - len(start))
    asterisks_end = "*" * (width - len(end))
    sys.stderr.write(
        "\n".join(
            [start + asterisks_start, prompt.rstrip(), end + asterisks_end + "\n\n"]
        )
    )


def get_question() -> str:
    """Read question from stdin"""
    question: str = ""
    if not sys.stdin.isatty():
        question = sys.stdin.read()
    else:
        sys.stderr.write("Press Ctrl+D to submit\n\n")
        while True:
            try:
                ask = input()
                question += ask + "\n"
            except EOFError:
                break
        question = question.strip()
        sys.stderr.write("\n")
    return question


def read_file_content(filename: str) -> str | None:
    """Read file content with error handling"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f'{BColors.WARNING}[Warning]{BColors.END_C} File "{filename}" not found')
    return None


@dataclass
class BColors:
    """Terminal color codes"""

    WARNING = "\033[93m"
    END_C = "\033[0m"
