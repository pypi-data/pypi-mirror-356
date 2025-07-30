import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Set


class FileUtils:
    """
    FileUtils class for file utilities that provides various methods for working with files and directories and also are used in the Sorter class.
    A Custom FileUtils class can be provided to the Sorter class to satisfy the specific requirements.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the FileUtils class.

        This constructor currently does not perform any specific actions
        upon instantiation.
        """
        pass
    
    def _get_files_and_sub_dir(
        self,
        folder_path: str,
        ignore_dir: list[str] | None = None,
    ) -> tuple[List[str], List[str]]:
        source_root: Path = Path(folder_path)
        # Get name of the sub directories ignoring the one in ignore_dir list.
        sub_dir_list = self.get_subdirectories_names(str(source_root), ignore_dir)

        # Get the list of files to be moved.
        file_list = [
            item.name
            for item in source_root.iterdir()
            if item.is_file() and item.name not in (ignore_dir or [])
        ]

        return sub_dir_list, file_list
    
    def get_file_modified_date(self, file_path: str) -> datetime:
        """
        Returns the last modified datetime of a file.

        Args:
            file_path (str): Full path to the file.

        Returns:
            datetime: Datetime object representing the last modification time.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        path: Path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        return datetime.fromtimestamp(path.stat().st_mtime)

    def get_subdirectories_names(
        self, folder_path: str, ignore_dir: list[str] = None
    ) -> list[str]:
        """
        Returns a list of subdirectory names in a given folder, excluding any specified to be ignored.

        Args:
            folder_path (str): Full path to the folder.
            ignore_dir (list[str], optional): List of subdirectory names to ignore. Defaults to [] if not provided.

        Returns:
            list[str]: List of subdirectory names.
        """
        folder: Path = Path(folder_path)
        if ignore_dir is None:
            ignore_dir = []
        sub_dir_list = [
            item.name
            for item in folder.iterdir()
            if item.is_dir() and item.name not in ignore_dir
        ]
        return sub_dir_list

    def flatten_dir(
        self,
        folder_path: str,
        dest_folder_path: str,
        ignore_dir: list[str] | None = None,
        rm_subdir: bool = False,
    ) -> None:
        """
        Moves all files from subdirectories of a given folder into a destination folder.

        This is useful for flattening a directory structure by collecting all files
        from nested folders and moving them into one target folder.

        Args:
            folder_path (str): Path to the root folder containing subdirectories with files.
            dest_folder_path (str): Path to the folder where all files should be moved.
            ignore_dir (list[str]): Names of subdirectories within `folder_path` that should be ignored during processing.
            rm_subdir (bool): If True, subdirectories will be removed after moving their contents. Default is False.
        Raises:
            FileNotFoundError: If the root folder (`folder_path`) does not exist.

        Notes:

            - Any errors encountered while moving files or removing subdirectories are caught and printed, but not raised.
            - Fails silently (with printed messages) on permission issuesmissing files, or non-empty directories during deletion.
        """
        source_root: Path = Path(folder_path)
        dest_root: Path = Path(dest_folder_path)
        if not source_root.exists():
            raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

        dest_root.mkdir(parents=True, exist_ok=True)

        try:
            # Get the list of files and sub directories.
            sub_dir_list, file_list = self._get_files_and_sub_dir(
                folder_path, ignore_dir
            )

            # If file_list empty then then return the function for sub_dir.
            if sub_dir_list and not file_list:
                for sub_dir_name in sub_dir_list:
                    self.flatten_dir(
                        str(source_root / sub_dir_name),
                        str(dest_root),
                        ignore_dir,
                    )

            # Move the files in the file_list to the dest_folder and check for folder in sub_dir_list.
            elif file_list:
                for name in file_list:
                    source_item = source_root / name
                    dest_item = dest_root / name
                    try:
                        shutil.move(str(source_item), str(dest_item))
                    except Exception as e:
                        print(f"Failed to move '{source_item}' to '{dest_item}': {e}")
                if sub_dir_list:
                    for sub_dir_name in sub_dir_list:
                        self.flatten_dir(
                            str(source_root / sub_dir_name),
                            str(dest_root),
                            ignore_dir,
                        )

                    # Remove the sub directories if rm_subdir is True.
            if rm_subdir:
                for sub_dir_name in sub_dir_list:
                    sub_dir_path = source_root / sub_dir_name
                    try:
                        if sub_dir_path != dest_root:
                            shutil.rmtree(sub_dir_path)
                    except Exception as e:
                        print(
                            f"Failed to remove directory '{sub_dir_path}': {e}"
                        )   

        except Exception as e:
            print(f"Error occurred while cleaning up folders: {e}")

    def find_unique_extensions(
        self, source_path: str, ignore_dir: list[str] | None = None
    ) -> Set[str]:
        """
        Recursively finds all unique file extensions in a given directory and its subdirectories.

        Args:
            source_path (str): Path to the root directory.
            ignore_dir (list[str], optional): List of directory names to ignore. Defaults to None.

        Returns:
            Set[str]: A set of unique file extensions found in the directory tree.

        Raises:
            FileNotFoundError: If the source_path does not exist.
        """
        source_root: Path = Path(source_path)
        if not source_root.exists():
            raise FileNotFoundError(
                f"The folder path '{str(source_root)}' does not exist."
            )

        extension_list: Set[str] = set()

        try:
            sub_dir_list, file_list = self._get_files_and_sub_dir(
                str(source_root), ignore_dir
            )

            for name in file_list:
                source_item = source_root / name
                extension_list.add(source_item.suffix.lower())

            for sub_dir_name in sub_dir_list:
                sub_dir_path = source_root / sub_dir_name
                extension_list.update(
                    self.find_unique_extensions(str(sub_dir_path), ignore_dir)
                )

        except Exception as e:
            print(f"Error occurred while finding unique extensions: {e}")

        return extension_list
