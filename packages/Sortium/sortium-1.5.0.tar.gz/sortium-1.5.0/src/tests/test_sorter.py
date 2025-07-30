import os
import shutil
import tempfile
import pytest
from datetime import datetime
from sortium.sorter import Sorter
from .test_file_tree import setup_type_sort, setup_date_sort

type_sort_tree = setup_type_sort
date_sort_tree = setup_date_sort

sorter = Sorter()

def test_sort_by_type_moves_files_to_categories(type_sort_tree):
    
    sorter.sort_by_type(type_sort_tree["base"])

    for category in ["Documents", "Images", "Music", "Others"]:
        category_path = os.path.join(type_sort_tree["base"], category)
        if os.path.exists(category_path):
            for file in os.listdir(category_path):
                assert file in ["doc.txt", "image.jpg", "music.mp3", "random.xyz"]


def test_sort_by_type_handles_invalid_path():
    with pytest.raises(FileNotFoundError):
        sorter.sort_by_type("non_existent_path")


def test_sort_by_date_sorts_into_date_folders(date_sort_tree):
    sorter.sort_by_date(date_sort_tree["base"], ["Images", "Documents"])

    today = datetime.now().strftime("%d-%b-%Y")
    expected_img_dir = os.path.join(date_sort_tree["Images"], today)
    expected_doc_dir = os.path.join(date_sort_tree["Documents"], today)

    assert os.path.isdir(expected_img_dir)
    assert os.path.isdir(expected_doc_dir)

    assert "photo.png" in os.listdir(expected_img_dir)
    assert "report.pdf" in os.listdir(expected_doc_dir)


def test_sort_by_date_missing_category_skips_gracefully(date_sort_tree):
    # 'Videos' does not exist, should be skipped
    sorter.sort_by_date(date_sort_tree["base"], ["Videos"])


def test_sort_by_date_invalid_root_raises():
    with pytest.raises(FileNotFoundError):
        sorter.sort_by_date("invalid_path", ["Images"])
