"""Contains logic for interactive or automatic fixing of LinkIssues."""

# pylint: disable=invalid-name

from typing import Optional, List, Dict
from pathlib import Path

from mdtools.util import clr
from mdtools.issues import issues
from mdtools.model.tree import Tree
from mdtools.issues.fix import href, options, util, fuzzy
from mdtools.issues.fix.patch import Patch, Patches


def __fuzzy_match(object_name: str,
                  object_index: Dict[str, List[Path]],
                  max_dist: int) -> Optional[str]:
    """Perform fuzzy match of `object_name` in `object_index`, if possible."""

    fuzzy_match, dist = fuzzy.best_match(object_name, object_index)
    if dist <= max_dist:
        print(clr("RED") + '      Did you mean: ' + fuzzy_match + '?' + clr(""))
        return fuzzy_match
    return None


def __fix_a(issue: issues.LinkIssue,
            tree: Tree,
            object_name: str,
            object_index: Dict[str, List[Path]],
            patches: Patches) -> None:
    """Generate a fix of a link issue automatically, if possible."""

    # Exactly one target candidate must be available for the automatic mode to work.
    if not object_name in object_index or len(object_index[object_name]) != 1:
        return

    is_abs = issue.link.is_absolute()
    if is_abs:
        # Generate an absolute fix for an absolute link
        h = href.path_to_href_abs(object_index[object_name][0], tree.base)
    else:
        # Generate a relative fix to a relative link
        h = href.path_to_href_rel(object_index[object_name][0], issue.path)

    def patch_func():
        """ Patch lambda. """
        issue.link.set_href(h)

    if h is not None:
        # pylint: disable=W0108
        anchor = issue.link.get_anchor()
        print(clr("GREEN") + "      -> " + h + (('#' + anchor) if anchor else '') + clr(""))
        patches.add(Patch(issue.path, lambda: patch_func()))


# Note: `__fix_target_not_found_i` and `__fix_anchor_not_found_i` are similar in principle
# but have enough differences to make a unified parametrized implementation infeasible.


def __fix_target_not_found_i(issue: issues.TargetNotFound,
                            tree: Tree,
                            patches: Patches,
                            opt: options.Options) -> None:
    """Fix a `TargetNotFound` issue in interactive mode, if spossible."""

    files = tree.names
    file_name = Path(issue.link.get_href()).name
    # `files[file_name]`: Files in the tree with this file name
    choices: List[Patch] = []

    if not file_name in files and opt.fuzzy:
        # No exact match; try to find a fuzzy match.
        fm = __fuzzy_match(file_name, files, 3)
        if fm:
            file_name = fm

    if not file_name in files:
        return       # No candidate targets!

    def add_choice(new_href):
        # pylint: disable=W0108

        def patch_func():
            """Patch lambda."""
            issue.link.set_href(new_href)

        if new_href is not None:
            # Formulate and print a hint
            a = issue.link.get_anchor()
            a = ('#' + a) if a else ''
            print(clr("GREEN") + "         " + str(len(choices)) + "\t" + new_href + a  + clr(""))
            # Add a patch candidate
            choices.append(Patch(issue.path, lambda: patch_func()))

    # For each candidate target...
    for f in files[file_name]:
        # Generate choice with absolute link
        h_abs = href.path_to_href_abs(f, tree.base)
        print(clr("GREY") + "      Candidate target: " + h_abs + clr(""))
        add_choice(h_abs)

        # Generate choice with relative link
        h_rel = href.path_to_href_rel(f, issue.path)
        add_choice(h_rel)

    # Ask user and apply
    choice = util.choose(len(choices))
    if choice is not None:
        patches.add(choices[choice])


def __fix_anchor_not_found_i(issue: issues.AnchorNotFound,
                            tree: Tree,
                            patches: Patches,
                            opt: options.Options) -> None:
    """Fix an `AnchorNotFound` issue in interactive mode, if possible."""

    files = tree.all_anchors
    anchor = issue.link.get_anchor()
    # `files[anchor]`: Files in the tree that contain this anchor
    choices: List[Patch] = []

    if not anchor in files and opt.fuzzy:
        # No exact match; try to find a fuzzy match.
        fm = __fuzzy_match(anchor, files, 4)
        if fm:
            anchor = fm

    if not anchor in files:
        return          # No candidate targets!

    def add_choice(new_href):
        # pylint: disable=W0108

        def patch_func():
            """Patch lambda."""
            issue.link.set_href(new_href)
            issue.link.set_anchor(anchor)

        if new_href is not None:
            # Formulate and print a hint
            a = anchor
            a = ('#' + a) if a else ''
            print(clr("GREEN") + "         " + str(len(choices)) + "\t" + new_href + a + clr(""))
             # Add a patch candidate
            choices.append(Patch(issue.path, lambda: patch_func()))

    # For each candidate target...
    for f in files[anchor]:
         # Generate choice with absolute link
        h_abs = href.path_to_href_abs(f, tree.base)
        print(clr("GREY") + "      Candidate target: " + h_abs + clr(""))
        add_choice(h_abs)

        # Generate choice with relative link
        h_rel = href.path_to_href_rel(f, issue.path)
        add_choice(h_rel)

     # Ask user and apply
    choice = util.choose(len(choices))
    if choice is not None:
        patches.add(choices[choice])


# -----------------------------------------------------------------------------


@util.fixes(issues.TargetNotFound)
def fix_target_not_found(issue: issues.TargetNotFound, tree: Tree, patches: Patches,
                         opt: options.Options) -> None:
    """Fix a `TargetNotFound` issue. The result of this function's successful run is a patch
    added to `patches`.
    """

    if   opt.mode == '-i':
        __fix_target_not_found_i(issue, tree, patches, opt)

    elif opt.mode == '-a':
        object_index = tree.names
        object_name = Path(issue.link.get_href()).name
        __fix_a(issue, tree, object_name, object_index, patches)


@util.fixes(issues.AnchorNotFound)
def fix_anchor_not_found(issue: issues.AnchorNotFound, tree: Tree, patches: Patches,
                         opt: options.Options) -> None:
    """Fix an `AnchorNotFound` issue. The result of this function's successful run is a patch
    added to `patches`.
    """

    if   opt.mode == '-i':
        __fix_anchor_not_found_i(issue, tree, patches, opt)

    elif opt.mode == '-a':
        object_index = tree.all_anchors
        object_name = issue.link.get_anchor()
        __fix_a(issue, tree, object_name, object_index, patches)
