"""Represents a file or directory in a file tree."""


from pathlib import Path
from typing import List, Dict
import marko # type: ignore
from mdtools.model.anchor import Anchor
from mdtools.model.link import Link


class File:
    """Represents a file or directory in a file tree."""

    # Path to the file.
    path:               Path

    # If this is markdown file, - all anchors in this file
    anchors:            Dict[str, Anchor]

    # If this is markdown file, - all headings in this file
    h_anchors:          Dict[str, Anchor]

    # If this is markdown file, - all links in this file
    links:              List[Link]

    # Markdown parser and renderer for this file. Used to parse the markdown, as well as
    # to generate an updated markdown after fixing issues (which is why it's being stored).
    marko:              marko.Markdown

    # The root node of the markdown AST, produced by `marko`.
    m_document:         marko.block.Document

    def __init__(self, path: Path):
        self.path = path        # pathlib Path
        self.anchors = {}
        self.h_anchors = {}
        self.links = []
        self.marko = None
        self.m_document = None

    def on_anchor(self, anchor: Anchor) -> None:
        """Called during file parsing if an anchor is found."""
        self.anchors[anchor.name] = anchor

    def on_heading_anchor(self, anchor: Anchor) -> None:
        """Called during file parsing if a heading anchor is found."""
        self.h_anchors[anchor.name] = anchor

    def on_link(self, link: Link) -> None:
        """Called during file parsing if a link is found."""
        self.links.append(link)
