#!/usr/bin/env python3

"""Concatenate files with Markdown code blocks"""

import os
import sys

from gemini.helper import get_question


def get_file_content(filename: str) -> str:
    """Read file content with error handling"""
    if filename == "-":
        content = get_question()
        if not content:
            print("Error: No content provided", file=sys.stderr)
            return ""
        return content.rstrip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f"```{filename}\n{f.read()}\n```"
    except FileNotFoundError:
        print(f"Error: {filename} not found", file=sys.stderr)
        return ""


def main() -> None:
    """Main processing function"""
    filenames = (
        ["-"]
        if not sys.argv[1:]
        else [arg for arg in sys.argv[1:] if not os.path.isdir(arg)]
    )
    print("\n\n".join(filter(None, map(get_file_content, filenames))), end="")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
