#!/usr/bin/env python3

"""Gemini CLI interface"""

import asyncio
import sys
import yaml
from dotenv import load_dotenv

from ykatt.main import get_messages, adjust_roles
from .helper import BColors
from .model import interact

load_dotenv()


def parse_yaml_content(content: str) -> list:
    """Parse YAML content into message objects"""
    try:
        messages = get_messages(content, verbose=False)
        if not messages:
            return [{"role": "user", "content": content.strip()}]
        return adjust_roles(messages, last_role=None)
    except ImportError:
        print(
            f"{BColors.WARNING}[Warning] ykatt module not available, treating YAML as plain text{BColors.END_C}",  # pylint: disable=line-too-long
            file=sys.stderr,
        )
        return [{"role": "user", "content": content.strip()}]
    except (yaml.YAMLError, yaml.MarkedYAMLError) as e:
        print(
            f"{BColors.WARNING}[Warning] YAML parsing error: {e}{BColors.END_C}",
            file=sys.stderr,
        )
        return [{"role": "user", "content": content.strip()}]


def main() -> None:
    """Main entry point"""

    asyncio.run(interact())


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
