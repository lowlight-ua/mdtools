"""Models the issues, which the script can detect. In the `fix` sub-package,
there are facilities for interactive/automatic fixing of the issues.
"""

from typing import List, Optional
from pathlib import Path

from mdtools.issues import issues
from mdtools.model.tree import Tree, File, Link
from mdtools import util


def analyze(md_tree: Tree) -> List[issues.Issue]:
    """Scan the markdown tree and look for known issues."""

    out = []

    def check_link(path: Path, link: Link) -> Optional[issues.Issue]:
        target: Path = util.href_to_path(path, md_tree.base, link.get_href())

        if not target in md_tree.files:
            return issues.TargetNotFound(path, link)

        thefile: File = md_tree.files[target]
        anchor = link.get_anchor()
        if (anchor
            and not anchor in thefile.anchors
            and not anchor in thefile.h_anchors):
            return issues.AnchorNotFound(path, link)

        return None

    # Check all links in all files
    path: Path
    file: File
    for path, file in md_tree.files.items():
        link: Link
        for link in file.links:
            if link.is_local():
                issue = check_link(path, link)
                if issue:
                    out.append(issue)

    return out
