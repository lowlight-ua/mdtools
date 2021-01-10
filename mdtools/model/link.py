"""Represents a link in a markdown file."""


from typing import Tuple
import marko # type: ignore


class Link:
    """Represents a link in a markdown file. Wraps a Link or Image node in the Marko AST."""

    # "Link" object in the Marko document
    m_link: marko.inline.Link

    def __init__(self, m_link: marko.inline.Link):
        self.m_link = m_link

    def get_dest(self) -> str:
        """Get the destination string from the link. Destination is
        'hello.md#world' from '[text](<hello.md#world> "label).
        """
        return self.m_link.dest

    def set_dest(self, dest: str) -> None:
        """Set the destination string of the link."""
        self.m_link.dest = dest

    def get_href(self) -> str:
        """Get the href string from the link. Href is
        'hello.md' from '[text](<hello.md#world> "label).
        """
        href, _ = Link.split_link(self.get_dest())
        return href

    def get_anchor(self) -> str:
        """Get the href string from the link. Anchor is
        'world' from '[text](<hello.md#world> "label).
        """
        _, anchor = Link.split_link(self.get_dest())
        return anchor

    def set_href(self, href: str) -> None:
        """Set the href string of the link."""
        _, anchor = Link.split_link(self.get_dest())
        dest = href + (('#' + anchor) if anchor else '')
        self.set_dest(dest)

    def set_anchor(self, anchor: str) -> None:
        """Set the anchor string of the link."""
        href, _ = Link.split_link(self.get_dest())
        dest = href + (('#' + anchor) if anchor else '')
        self.set_dest(dest)

    def is_absolute(self) -> bool:
        """Return true if the link is absolute."""
        return self.get_dest()[0:1] == '/'

    def is_local(self) -> bool:
        """Return true if the link is local (assumed local if contains no colons)."""
        return self.get_href().find(':') == -1

    @staticmethod
    def split_link(linkstr: str) -> Tuple[str, str]:
        """Split the part in the round brackets into the href and the anchor
        (e.g. "hello.md#world -> "hello.md", "world")
        """

        href_split = linkstr.split('#')
        href = href_split[0]
        anchor = href_split[1] if len(href_split)>1 else ''
        return href, anchor