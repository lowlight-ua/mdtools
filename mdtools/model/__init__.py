"""This package provides a simple model of a markdown tree."""

import os
import re
from pathlib import Path
from typing import Union, Tuple

import marko # type: ignore
from marko.md_renderer import MarkdownRenderer # type: ignore

from mdtools.model.tree import Tree, Anchor, Link
from mdtools import util

###############################################################################


ignore_paths = ['.git']

RE_ANCHOR = r"""<a\s*(name|id).*?>"""
rc_anchor = re.compile(RE_ANCHOR)


###############################################################################


def __on_link(path: Path, tree: Tree,
              marko_node: Union[marko.inline.Link, marko.inline.Image]) -> None:
    """Called when a link node is encountered in the AST."""
    tree.on_link(path, Link(marko_node))

def __on_image(path: Path, tree: Tree, marko_node: marko.inline.Image) -> None:
    """Called when an image node is encountered in the AST."""
    tree.on_link(path, Link(marko_node))

def __on_inline_html(path: Path, tree: Tree, html: str) -> None:
    """Called when inline HTML is encountered in the AST."""
    match = rc_anchor.match(html)
    if match:
        tree.on_anchor(path, Anchor(html=html))

def __on_heading(path: Path, tree: Tree, text: str) -> None:
    """Called when a heading node is encountered in the AST."""
    tree.on_heading_anchor(path, Anchor(heading=text))

def __traverse_ast(path: Path, tree: Tree, node) -> None:
    """Recursively traverse the AST produced by Marko, and update the markdown tree model."""

    if isinstance(node, marko.inline.InlineHTML):
        __on_inline_html(path, tree, node.children)
    elif isinstance(node, marko.inline.Link):
        __on_link(path, tree, node)
    elif isinstance(node, marko.inline.Image):
        __on_image(path, tree, node)
    elif isinstance(node, marko.block.Heading):
        text = node.children[0].children
        if isinstance(text, str):
            __on_heading(path, tree, text)

    if hasattr(node, 'children') and isinstance(node.children, list):
        for child in node.children:
            __traverse_ast(path, tree, child)


def read_md_tree(tree: Tree) -> None:
    """Scan a markdown tree and populate the model."""

    def parse_markdown(path: Path): #  -> Tuple[marko, Document]:
        """Parse a markdown file and update the markdown tree model."""
        with open(path, encoding='utf-8') as file:
            markdown = file.read()
        match = marko.Markdown(renderer = MarkdownRenderer)
        doc = match.parse(markdown)
        __traverse_ast(path, tree, doc)
        return match, doc

    # Walk the file tree
    for dir_, dirs, files in os.walk(tree.base, topdown=True):
        dirs[:] = [d for d in dirs if d not in ignore_paths]

        for dir_name in dirs:
            # Treat directories as files (for some links that can point to directories)
            path = Path(dir_).joinpath(Path(dir_name)).resolve()
            tree.on_file(path)

        for file_name in files:
            path = Path(dir_).joinpath(Path(file_name)).resolve()
            the_file = tree.on_file(path)

            ext = Path(file_name).suffix
            if ext == '.md':
                try:
                    match, doc = parse_markdown(path)
                    the_file.marko = match
                    the_file.m_document = doc
                except:
                    print(util.clr("RED") + "Parser error in: " +  str(path) + util.clr(""))

    tree.all_anchors = {**tree.anchors, **tree.h_anchors}
