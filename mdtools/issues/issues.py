"""Classes that represent issues that the script can detect."""

from pathlib import Path
from mdtools.util import clr
from mdtools.tree.tree import Link, Anchor


class Issue:
    """Base class for all issues that the script can detect."""

    # The Path to the file where this issue was found
    path: Path

    def __init__(self, path: Path) -> None:
        self.path = path

    def describe(self):
        """Provide a textual description of the issue."""


class DuplicateAnchor(Issue):
    """Class for the 'duplicate anchor' issue."""

    anchor: Anchor

    def __init__(self, path: Path, anchor: Anchor) -> None:
        super().__init__(path)
        self.anchor = anchor

    def describe(self):
        return clr("YELLOW") + "   Duplicate anchor: " + clr("") + self.anchor.name


class LinkIssue(Issue):
    """Base class for all link-related issues."""

    link: Link

    def __init__(self, path: Path, link: Link) -> None:
        super().__init__(path)
        self.link = link


class TargetNotFound(LinkIssue):
    """Class for the 'target not found' issue
    (the link points to a target that does not exist).
    """

    def describe(self):
        return clr("YELLOW") + "   Target not found: " + clr("") + self.link.get_dest()


class AnchorNotFound(LinkIssue):
    """Class for the 'anchor not found' issue
    (the link contains an anchor that doesn't exist in the file).
    """

    def describe(self):
        return clr("YELLOW") + "   Anchor not found: " + clr("") + self.link.get_dest()
