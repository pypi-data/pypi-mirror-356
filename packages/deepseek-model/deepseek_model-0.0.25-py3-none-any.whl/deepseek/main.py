#!/usr/bin/env python3

"""DeepSeek CLI interface"""

import sys
import os
from dotenv import load_dotenv
from .helper import get_question, read_file_content, BColors
from .model import interact

load_dotenv()


def parse_yaml_content(content: str) -> list:
    """Parse YAML content into message objects using ykatt logic"""
    try:
        # Import ykatt components only when needed
        from ykatt.main import get_messages, adjust_roles

        messages = get_messages(content, verbose=False)
        if not messages:
            return [{"role": "user", "content": content.strip()}]

        # Ensure proper role alternation
        return adjust_roles(messages, last_role=None)

    except ImportError:
        print(
            f"{BColors.WARNING}[Warning] ykatt module not available, treating YAML as plain text{BColors.END_C}",
            file=sys.stderr,
        )
        return [{"role": "user", "content": content.strip()}]
    except Exception as e:
        print(
            f"{BColors.WARNING}[Warning] YAML parsing error: {e}{BColors.END_C}",
            file=sys.stderr,
        )
        return [{"role": "user", "content": content.strip()}]


def main() -> None:
    """Main entry point"""
    all_messages = []

    # Process files first
    for arg in sys.argv[1:]:
        content = read_file_content(arg)
        if not content:
            continue

        if arg.lower().endswith((".yaml", ".yml")):
            parsed = parse_yaml_content(content)
            all_messages.extend(parsed)
        else:
            all_messages.append({"role": "user", "content": content.strip()})

    # Add user question last
    question = get_question()
    if question:
        all_messages.append({"role": "user", "content": question})

    if all_messages:
        interact(all_messages)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
