#!/usr/bin/env python3

"""YAML conversation manager"""

import sys
import os
import argparse
import readline  # pylint: disable=unused-import
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ValidationError
import yaml


class LiteralStr(str):
    """String that renders as YAML literal block"""


def literal_str_representer(dumper, data):
    """YAML representation for literal strings"""
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(LiteralStr, literal_str_representer)


class Role(str, Enum):
    """Conversation roles"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """Conversation message"""

    role: Role
    content: str


def get_messages(content: str, verbose: bool) -> List[dict]:
    """Parse YAML into message structures"""
    try:
        messages = []
        for item in yaml.safe_load_all(content):
            if isinstance(item, list):
                for msg in item:
                    message = Message(**msg)
                    messages.append(
                        {
                            "role": message.role.value,
                            "content": LiteralStr(message.content),
                        }
                    )
            elif isinstance(item, dict):
                message = Message(**item)
                messages.append(
                    {"role": message.role.value, "content": LiteralStr(message.content)}
                )
            elif isinstance(item, str):
                messages.append({"role": Role.USER.value, "content": LiteralStr(item)})
        return messages
    except (yaml.YAMLError, ValidationError) as e:
        if verbose:
            print(f"Error: {e}", file=sys.stderr)
        return [{"role": Role.USER.value, "content": LiteralStr(content)}]


def adjust_roles(messages: List[dict], last_role: Optional[str]) -> List[dict]:
    """Ensure proper role alternation"""
    adjusted = []
    current_role = last_role
    for msg in messages:
        if msg["role"] == Role.USER.value:
            if current_role == Role.USER.value:
                new_role = Role.ASSISTANT.value
            else:
                new_role = Role.USER.value
            adjusted.append({"role": new_role, "content": msg["content"]})
            current_role = new_role
        else:
            adjusted.append(msg)
            current_role = msg["role"]
    return adjusted


def main() -> None:
    """Main application logic"""
    parser = argparse.ArgumentParser(description="Manage YAML conversation files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-f", "--file", help="Conversation file")
    parser.add_argument("-t", "--tee", action="store_true", help="Print after writing")
    args = parser.parse_args()

    new_messages = []

    if not sys.stdin.isatty():
        new_messages = get_messages(sys.stdin.read(), args.verbose)

    if args.file:
        existing = []
        if os.path.exists(args.file):
            try:
                with open(args.file, "r", encoding="utf-8") as f:
                    existing = get_messages(f.read(), args.verbose)
            except OSError as e:
                if args.verbose:
                    print(f"Error reading {args.file}: {e}", file=sys.stderr)
                sys.exit(1)

        last_role = existing[-1]["role"] if existing else None
        adjusted = adjust_roles(new_messages, last_role)
        combined = existing + adjusted

        try:
            with open(args.file, "w", encoding="utf-8") as f:
                yaml.dump_all(combined, f, indent=2)
            if args.tee:
                yaml.dump_all(combined, sys.stdout, indent=2)
        except OSError as e:
            if args.verbose:
                print(f"Error writing {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        yaml.dump_all(new_messages, sys.stdout, indent=2)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
