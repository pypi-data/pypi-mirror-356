# 🧪 `sortium` Test Suite

This directory contains a complete suite of tests for the `sortium` Python library — a utility for organizing and sorting files by type and date, along with file flattening and extension discovery utilities.

The test suite ensures correctness, robustness, and graceful handling of errors across core features of the library.

## 📁 Directory Overview

```
tests/
│
├── test_sorter.py         # Tests for the core Sorter class
├── test_file_utils.py     # Tests for file utility functions
└── test_file_tree.py      # Fixtures and temporary file structures used in tests
```

---

## ✅ What’s Tested

### `test_sorter.py`

Tests the `Sorter` class, responsible for organizing files by type or date.

* **`sort_by_type()`**

  * Categorizes files into `Documents`, `Images`, `Music`, and `Others`.
  * Verifies movement of files into appropriate category folders.
  * Handles invalid/non-existent paths with a `FileNotFoundError`.

* **`sort_by_date()`**

  * Sorts files inside specified folders into subfolders by the current date.
  * Verifies creation of date-based folders and correct placement of files.
  * Skips gracefully when specified folders don't exist.
  * Raises `FileNotFoundError` for an invalid root directory.

---

### `test_file_utils.py`

Tests the `FileUtils` class for operations like flattening directory trees and discovering file extensions.

* **`flatten_dir()`**

  * Moves all files from nested subdirectories into a single destination directory.
  * Supports ignoring certain directories during flattening.
  * Validates removal of subdirectories when `rm_subdir=True`.
  * Raises `FileNotFoundError` on invalid source paths.

* **`find_unique_extensions()`**

  * Detects and returns all unique file extensions from a directory tree.
  * Validates against expected extensions.
  * Handles invalid root paths correctly by raising `FileNotFoundError`.

---

## 🧪 Fixtures Breakdown

### `setup_test_dirs`

Creates a deeply nested file structure to test `flatten_dir()` and `find_unique_extensions()`.

```
base/
├── sub1/
│   ├── sub_sub1/
│   │   ├── file1.txt
│   │   └── image1.jpg
│   ├── file_outer.txt
│   └── video1.mp4
├── sub2/
│   ├── sub_sub2/
│   │   ├── file2.txt
│   │   └── page1.html
│   └── audio1.mp3
└── ignoreme/
    └── ignored.txt

dest/
└── dest_test/              # Destination for flattened files
```

Files:

* Various formats: `.txt`, `.jpg`, `.html`, `.mp4`, `.mp3`
* Used to validate flattening, ignoring paths, and detecting extensions

---

### `setup_type_sort`

Creates a flat directory with mixed file types to test file sorting by type.

```
base/
├── doc.txt        # → Documents
├── image.jpg      # → Images
├── music.mp3      # → Music
└── random.xyz     # → Others
```

---

### `setup_date_sort`

Creates category folders (`Images`, `Documents`) containing files to be sorted into date folders.

```
base/
├── Images/
│   └── photo.png       # → Images/<current_date>/
└── Documents/
    └── report.pdf      # → Documents/<current_date>/
```

---
Here’s a cleaner, shorter version of the “Adding Tests” section for your `README.md`:

---

## ➕ Adding Tests

To extend the test suite follow these quick steps:

### 1. **Pick the Right File**

| Target           | Test File            |
| ---------------- | -------------------- |
| `Sorter` methods | `test_sorter.py`     |
| `FileUtils`      | `test_file_utils.py` |
| Fixtures/setup   | `test_file_tree.py`  |

---

### 2. **Add Your Test**

Create a new `def test_...` function using pytest style.

Example:

```python
def test_sort_by_size_creates_folders(size_tree):
    sorter.sort_by_size(size_tree["base"])
    assert "Small" in os.listdir(size_tree["base"])
    assert "Large" in os.listdir(size_tree["base"])
```

---

### 3. **Write a Fixture (if needed)**

Put fixtures in `test_file_tree.py`:

```python
@pytest.fixture
def size_tree():
    base = tempfile.mkdtemp()
    create_temp_file(base, "tiny.txt", "123")
    create_temp_file(base, "movie.mkv", "0" * 10_000_000)
    yield {"base": base}
    shutil.rmtree(base)
```

---

### ✅ Test Expectations

* Files/folders are in expected locations
* Invalid inputs raise proper errors (`FileNotFoundError`, etc.)
* Temporary files are cleaned up
* Tests are small, clear, and isolated

---

## 🧪 Running the Tests

Make sure `pytest` is installed:

```bash
pip install pytest
```

Then run in root folder:

```bash
pytest src/tests --cov=src/sortium
```

---

## 📦 Note

This test suite is designed for the `sortium` library hosted on [PyPI](https://pypi.org/), and ensures comprehensive validation for deployed versions of the package.

All file system changes are safely performed in temporary directories, and cleaned up automatically after test execution.

---
