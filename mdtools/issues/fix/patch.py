"""Contains facilities for file patching."""


from dataclasses import dataclass
from typing import List, Dict, Callable
from pathlib import Path

from mdtools.tree.tree import MdTree, File


@dataclass
class Patch:
    """Describes a change to be made to a specific file."""

    target:         Path
    patch_function: Callable[[], None]

    def apply(self) -> None:
        """Apply the patch."""
        self.patch_function()   # type: ignore


class PatchTarget:
    """Describes a patch target (single file to be patched), and all the patches."""

    file:    File
    patches: List[Patch]

    def __init__(self, file: File) -> None:
        self.file = file
        self.patches = []

    def add_patch(self, patch: Patch) -> None:
        """Register a patch to be added to this target."""
        self.patches.append(patch)

    def apply(self) -> None:
        """Apply patches for this target. This is where the actual file is changed. """
        for patch in self.patches:
            patch.apply()
        with open(self.file.path, 'w', encoding='utf-8') as f:      # pylint: disable=invalid-name
            rendered = self.file.marko.render(self.file.m_document) # type: ignore
            f.write(rendered)


class Patches:
    """Describes all patches to be applied during this session."""

    tree:    MdTree
    targets: Dict[Path, PatchTarget] = {}   # Patch targets
    empty:   bool       = True

    def __init__(self, tree: MdTree):
        self.tree = tree

    def add(self, patch: Patch) -> None:
        """Register a patch."""
        self.empty = False
        file: File = self.tree.files[patch.target]
        self.targets.setdefault(patch.target, PatchTarget(file)).add_patch(patch)

    def apply(self) -> None:
        """Apply all registered patches."""
        for target in self.targets.values():
            target.apply()
