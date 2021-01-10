"""Provides logic for fixing issues (interactive or automatic)."""

from typing import List, Dict
from pathlib import Path

from mdtools.util import clr
from mdtools.tree.tree import MdTree
from mdtools.issues import issues
from mdtools.issues.fix import link_issues   # do not remove: decorators run
from mdtools.issues.fix.patch import Patches
from mdtools.issues.fix import options


def fix_all(all_issues: List[issues.Issue], tree: MdTree, opt: options.Options) -> None:
    '''Print issues. If the mode implies fixing, and if there's a fixer available, invoke it.
    The fixer will work interactively or manually (depending on mode) and generate patches.
    The patches are applied at the end.
    '''

    patches = Patches(tree)

    # Sort issues by file, for more natural interactive handling.
    issues_by_file: Dict[Path, List[issues.Issue]] = {}
    for i in all_issues:
        issues_by_file.setdefault(i.path, []).append(i)

    for file, issues_in_file in issues_by_file.items():
        print(clr("BOLD") + str(file) + clr(""))
        for i in issues_in_file:
            print(i.describe())
            if opt.mode and hasattr(i.__class__ ,'fixed_by'):
                fixer = i.__class__.fixed_by         # type: ignore
                fixer(i, tree, patches, opt)

    if not patches.empty:
        print("Patching files...")
        patches.apply()
        print("OK")
