"""Linkcheck script tests."""


import os
import shutil
import tempfile

from .compare_dirs import are_dir_trees_equal

from mdtools import linkcheck


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def test_automatic(monkeypatch):
    """ Test the automatic mode of the linkcheck script by running it against a
    pre-built test tree, and comparing the output to the desired output.
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        tree_dir = os.path.join(tmpdir, 'tree')
        monkeypatch.setattr("sys.argv", ["pytest", "-a", tree_dir])
        shutil.copytree('./tree', tree_dir)

        # Invole the script
        linkcheck.main()

        # Verify the result
        assert are_dir_trees_equal(tree_dir, './tree_out')
