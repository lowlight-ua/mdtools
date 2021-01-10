"""Represents an anchor in a markdown file."""


import re
from typing import List, Dict
from pathlib import Path


RE_ANCHOR_NAME = r"""=(?:\s*['"]([^'"]*?)['"]|\s*([^'">]*?)(?:\s|>))"""
rc_anchor_name = re.compile(RE_ANCHOR_NAME)


RE_H2A_1 = r"""[^\w\- ]+"""
rc_h2a_1 = re.compile(RE_H2A_1)

RE_H2A_1 = r"""\s"""
rc_h2a_2 = re.compile(RE_H2A_1)


class Anchor:
    """Represents an anchor in a markdown file."""

    name: str

    def __init__(self, html: str = None, heading: str = None) -> None:
        # The name part of the anchor (e.g. "anchor_name")

        if html:
            match = rc_anchor_name.search(html)
            if match:
                self.name = match.group(1) or match.group(2)

        elif heading:
            self.name = Anchor.heading_to_anchor(heading)

    @staticmethod
    def heading_to_anchor(heading: str) -> str:
        """github-compatible translation of a heading to a corresponding autogenerated
        anchor name.
        """

        ret = heading.strip().lower()
        ret = rc_h2a_1.sub("", ret)
        ret = rc_h2a_2.sub("-", ret)
        return ret
