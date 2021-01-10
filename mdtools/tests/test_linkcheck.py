"""Linkcheck script tests."""


import os
import shutil
import tempfile
import pytest

from .compare_dirs import are_dir_trees_equal

from mdtools import linkcheck


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


@pytest.fixture
def copy_input_tree_to_tmp_dir():
    tmp_dir = tempfile.TemporaryDirectory()
    tree_path = os.path.join(tmp_dir.name, 'tree')
    shutil.copytree('./tree', tree_path)
    return [tmp_dir, tree_path]


def test_automatic_fix(copy_input_tree_to_tmp_dir, monkeypatch, capfd):
    """ Test the automatic mode of the linkcheck script by running it against a
    pre-built test tree, and comparing the output to the desired output.
    """

    tmp_dir = copy_input_tree_to_tmp_dir[0]
    tree_path = copy_input_tree_to_tmp_dir[1]
    monkeypatch.setattr("sys.argv", ["pytest", "-a", tree_path])

    # Invole the script
    linkcheck.main()
    out, err = capfd.readouterr()

    #with open('out.txt', 'w') as f:
    #    f.write(out)

    # Verify the result
    assert are_dir_trees_equal(tree_path, './tree_out')
    tmp_dir.cleanup()