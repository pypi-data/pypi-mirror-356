import shutil
from pathlib import Path
from .file_utils import FileUtils
from .config import DEFAULT_FILE_TYPES

"""
This module defines the Sorter class for organizing files within directories.

The Sorter class helps sort files based on their type (e.g., Images, Documents)
and their last modification date. It can move files into categorized folders,
further organize them by modification date, and flatten nested directories by
moving files out.
"""

# Main sorter class.


class Sorter:
    """
    Sorter class to organize files in a directory by file type and modification date.

    Attributes:
        file_types_dict (dict[str, list[str]]): A mapping of file category names (e.g., "Images", "Documents") to lists of associated file extensions (e.g., [".jpg", ".png"]). This dictionary is used to determine how files should be grouped during sorting. If not provided, the default mapping from `DEFAULT_FILE_TYPES` is used.

    Example:
        >>> file_types = {
        ...     "Images": [".jpg", ".jpeg", ".png", ".gif"],
        ...     "Documents": [".pdf", ".docx", ".txt"],
        ...     "Videos": [".mp4", ".avi"],
        ...     "Music": [".mp3", ".wav"],
        ...     "Others": []
        ... }
        >>> sorter = Sorter(file_types)
        >>> sorter.sort_by_type('/path/to/downloads')
        >>> sorter.sort_by_date('/path/to/downloads', ['Images', 'Documents'])
    """

    def __init__(
        self,
        file_types_dict: dict[str, list[str]] = DEFAULT_FILE_TYPES,
        file_utils: FileUtils = None,
    ):
        """
        Initializes an instance of the Sorter class.

        Args:
            file_types_dict (dict[str, list[str]], optional): A dictionary mapping file category names to lists of associated file extensions. Defaults to DEFAULT_FILE_TYPES if not provided.
            file_utils (FileUtils, optional): An instance of FileUtils to use for file utilities. Defaults to FileUtils() if not provided.
        """
        self.file_types_dict = file_types_dict
        self.file_utils = file_utils or FileUtils()

    def __get_category(self, extension: str) -> str:
        """
        Determines the category of a file based on its extension.

        Args:
            extension (str) : The extension of the file that will be sorted.

        Returns:
            str: Category of the file based on the file_types_dict.
        """
        for category, extensions in self.file_types_dict.items():
            if extension.lower() in extensions:
                return category
        return "Others"

    def sort_by_type(self, folder_path: str, ignore_dir: list[str] = None) -> None:
        """
        Sorts files in a directory into subdirectories by file type.

        Args:
            folder_path (str): Path to the directory containing unsorted files.
            ignore_dir (list[str]): Names of subdirectories within `folder_path` that should be ignored during processing.

        Raises:
            FileNotFoundError: If the specified folder does not exist.
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"The path '{folder}' does not exist.")

        try:
            sub_dir_list = self.file_utils.get_subdirectories_names(
                str(folder), ignore_dir
            )
            for sub_dir_name in sub_dir_list:
                file_path = folder / sub_dir_name

                if file_path.is_file():
                    category = self.__get_category(file_path.suffix)
                    dest_folder = folder / category
                    dest_folder.mkdir(parents=True, exist_ok=True)

                    try:
                        shutil.move(str(file_path), str(dest_folder / file_path.name))
                    except Exception as e:
                        print(f"Error moving file '{file_path.name}': {e}")
        except Exception as e:
            print(f"An error occurred while sorting by type: {e}")

    def sort_by_date(self, folder_path: str, folder_types: list[str]) -> None:
        """
        Sorts files inside specified category folders into subfolders based on their last modified date.

        Each file is moved into a subfolder named by the modification date in the format "DD-MMM-YYYY".

        Args:
            folder_path (str): Root directory path containing the category folders.
            folder_types (list[str]): List of category folder names to process (e.g., ['Images', 'Documents']).

        Raises:
            FileNotFoundError: If the root folder (`folder_path`) does not exist.

        Notes:
            - If a category folder in `folder_types` does not exist, it will be skipped with a printed message.
            - Errors during moving individual files are caught and printed but do not stop the process.
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"The folder path '{folder}' does not exist.")
        for folder_type in folder_types:
            sub_folder = folder / folder_type
            if sub_folder.exists():
                try:
                    for file_path in sub_folder.iterdir():
                        if file_path.is_file():
                            try:
                                # Get modified date and format it
                                modified = self.file_utils.get_file_modified_date(
                                    str(file_path)
                                )
                                date_folder = sub_folder / modified.strftime("%d-%b-%Y")

                                # Create a subfolder for the date and move the file
                                date_folder.mkdir(parents=True, exist_ok=True)
                                shutil.move(
                                    str(file_path), str(date_folder / file_path.name)
                                )
                            except Exception as e:
                                print(
                                    f"Error sorting file '{file_path.name}' by date: {e}"
                                )
                except Exception as e:
                    print(
                        f"An error occurred while processing folder '{sub_folder}': {e}"
                    )
            else:
                print(f"Sub-folder '{sub_folder}' not found, skipping.")
