"""Scans a markdown file tree for issues and fixes them.

Terms:

- Target: a physical resource (file, directory) existing on the disk,
  which a markdown link can point to.

- Path: a fully qualified OS path to the Target.

- Href: a hyper reference from the markdown file to a Target (in a Link).
  In [hello.md#world] the href is 'hello.md'.
  - Absolute href: a href that is absolute w.r.t. the base directory of the markdown tree
    e.g. /docs/hello/hello.md
  - Relative href: a href that is relative to the file containing the Link
    e.g. ../hello/hello.md

- Anchor: a named point inside a markdown file.
  In [hello.md#world] the href is 'world'.

- Link: contains a href and an anchor;
  hrefs and anchors are each optional (but one of them must be present).
"""

import sys
import getopt
from pathlib import Path

from mdtools import util
from mdtools.model.tree import Tree
from mdtools.model import read_md_tree
from mdtools.issues import analyze
from mdtools.issues.fix.options import Options
from mdtools.issues.fix import fix_all

# pylint: disable=multiple-statements

# -----------------------------------------------------------------------------
# Usage info

def print_usage():
    """Print info about the command-line arguments of the script."""
    print("""
Usage: link_checker.py <modes and options> <markdown_dir_root>
Modes:
    <nothing>: Just check the links and print results.
    -i: Fix interactively with automatic suggestions.
    -a: Fix non-ambiguous cases automatically. Skip otherwise.
Options:
    -f: If interactive mode, use fuzzy matching for suggestions. Slower.
    -c: Colorize output for better readability.
""")

# -----------------------------------------------------------------------------
# Argument parsing

def main():
    """Script entry point"""

    try:
        optlist, args = getopt.getopt(sys.argv[1:], "ifac")
    except getopt.GetoptError as exc:
        print(exc.msg + "\n")
        print_usage()
        exit()

    if len(args) != 1:
        print_usage()
        exit()

    opt = Options()
    for o in optlist:
        if   o[0] == '-i': opt.mode = '-i'
        elif o[0] == '-a': opt.mode = '-a'
        elif o[0] == '-f': opt.fuzzy = True
        elif o[0] == '-c': opt.colorize = True

    root_dir = args[0]
    if not Path(root_dir).resolve().exists():
        print("Input path " + root_dir + " does not exist\n")
        print_usage()
        exit()

    util.colorize_setting = opt.colorize
    if opt.colorize:
        from colorama import init as colorama_init  # type: ignore
        colorama_init()

    # -----------------------------------------------------------------------------
    # Doing the thing

    tree = Tree(root_dir)
    read_md_tree(tree)
    issues = analyze(tree)
    fix_all(issues, tree, opt)


if __name__ == "__main__":
    main()
