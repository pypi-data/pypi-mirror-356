#!/usr/bin/env python

"""Convert HTML to Markdown"""

import readline  # pylint: disable=unused-import
import sys
from markdownify import markdownify as md


def main():
    """Main conversion function"""
    html_content = sys.stdin.read()
    print(md(html_content).strip())


if __name__ == "__main__":
    main()
