"""Represents an anchor in a markdown file."""


import re
from typing import List, Dict
from pathlib import Path


RE_ANCHOR_NAME = r"""=(?:\s*['"]([^'"]*?)['"]|\s*([^'">]*?)(?:\s|>))"""
rc_anchor_name = re.compile(RE_ANCHOR_NAME)


class Anchor:
    """Represents an anchor in a markdown file."""

    name: str

    def __init__(self, html: str) -> None:
        # The name part of the anchor (e.g. "anchor_name")

        match = rc_anchor_name.search(html)
        if match:
            self.name = match.group(1) or match.group(2)
            
