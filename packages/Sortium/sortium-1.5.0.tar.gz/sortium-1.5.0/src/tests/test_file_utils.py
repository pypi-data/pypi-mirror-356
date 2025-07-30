import os
from .test_file_tree import setup_test_dirs
from sortium.file_utils import FileUtils
import pytest

file_utiles = FileUtils()
test_tree = setup_test_dirs



# Tests for flatten_dir
def test_flatten_dir_moves_files(test_tree):
    file_utiles.flatten_dir(test_tree["base"], test_tree["dest"])

    dest_files = os.listdir(test_tree["dest"])
    setup_dest_files = test_tree["files"]
    for file in setup_dest_files:
        assert file in dest_files
    assert test_tree["ignored_file"] in dest_files


def test_flatten_dir_moves_files_ignored(test_tree):
    file_utiles.flatten_dir(
        test_tree["base"], test_tree["dest_test"], ignore_dir=test_tree["ignored_file"]
    )

    dest_files = os.listdir(test_tree["dest_test"])
    setup_dest_files = test_tree["files"]
    for file in setup_dest_files:
        assert file in dest_files
    assert os.path.exists(test_tree["dest_test"])
    assert test_tree["ignored_file"] not in dest_files

def test_flatten_dir_moves_files_source_error(test_tree):
    with pytest.raises(FileNotFoundError):
        file_utiles.flatten_dir("wrong_path", test_tree["dest"], ignore_dir=test_tree["ignored_file"])

def test_flatten_dir_remove_subdir(test_tree):
    file_utiles.flatten_dir(test_tree["base"], test_tree["dest"], rm_subdir=True)
    assert not os.path.exists(test_tree["sub1"])


# Test for find_unique_extensions
def test_find_unique_extensions(test_tree):
    unique_extensions = file_utiles.find_unique_extensions(test_tree["base"])
    for ext in unique_extensions:
        assert ext in test_tree["unique_extensions"]

def test_find_unique_extensions_error(test_tree):
    with pytest.raises(FileNotFoundError):
        file_utiles.find_unique_extensions("wrong_path")
