from pathlib import Path
from typing import Literal, Optional
from eazydocs.core._types import StrPathType


class Writer:
    def __init__(
        self,
        contents: str,
        filename: StrPathType,
        path: Optional[StrPathType] = None,
        overwrite: bool = False,
        **kwargs,
    ) -> None:
        """Eazydocs Writer class to write markdown files.

        Args:
            contents (str): String object to write to the markdown file.
            filename (StrPathType): String or Path object for the filename.
            path (StrPathType, optional): String or Path object for the path
                where the file will be saved. If not provided, the file will be
                saved in the current working directory. If provided, the
                `filename` will be joined to `path` argument. Defaults to None.
            overwrite (bool, optional): Whether to overwrite the file if it
                already exists. Defaults to False.
        """
        self.contents = contents
        self.overwrite = overwrite

        self.filepath = self._get_filepath(filename, path)

        if kwargs:
            if kwargs.get("update") is not None:
                self.msg = (
                    f"Successfully updated markdown file: '{self.filepath}"
                )
        else:
            self.msg = f"Successfully created markdown file: '{self.filepath}'"

    def write(self) -> None:
        """Writes the `contents` to the markdown file at `filepath`, generated
        from the `filename` and `path`."""

        if not self._valid_path(self.filepath):
            return

        with open(self.filepath, "w+") as f:
            f.write(self.contents)

        print(self.msg)

    def _get_filepath(
        self,
        filename: StrPathType,
        path: Optional[StrPathType] = None,
    ) -> Path:
        """Get the filepath for the markdown file.

        Args:
            filename (StrPathType): String or Path object for the filename.
            path (StrPathType, optional): Directory path where the file will be
                saved. If not provided, the file will be saved in the current
                working directory. If provided, the `filename` will be joined to
                `path` argument. Defaults to None.

        Returns:
            Path: The Path object representing the filepath for the markdown file.
        """
        if isinstance(filename, str) and not filename.endswith(".md"):
            filename = f"{filename}.md"

        if path is not None:
            if isinstance(path, str):
                path = Path(path)
            filepath = Path(path) / filename
        else:
            if isinstance(filename, str):
                filepath = Path(filename)
            else:
                # Filename is already a Path object - Sanitize it
                if not filename.suffix:
                    filename = f"{filename}.md"
                filepath = filename

        return filepath

    def _valid_path(self, path: Path) -> bool:
        """Validate the filepath for the markdown file.

        If the filepath does not exist, prompt the user to create it. If the
        filepath exists and overwrite is False, prompt the user to confirm
        overwriting the file.

        Args:
            path: Path object representing the filepath to validate.

        Returns:
            bool: True if the filepath is valid, False otherwise.
        """
        if not path.exists():
            while True:
                confirm = input(
                    f"Filepath '{path}' does not exist. Do you want to create it? (y/n): "
                )
                match confirm.lower():
                    case "y":
                        print(f"Creating directory: '{path.parent}'")
                        break
                    case "n":
                        print("Exiting without creating the directory.")
                        return False
                    case _:
                        print(
                            "Invalid input. Please enter 'y' or 'n', or press Esc to exit."
                        )
        elif not self.overwrite:
            while True:
                confirm = input(
                    f"Filepath '{path}' already exists. Do you want to overwrite it? (y/n): "
                )
                match confirm.lower():
                    case "y":
                        print(f"Overwriting existing file: '{path}'")
                        break
                    case "n":
                        print("Exiting without overwriting the file.")
                        return False
                    case _:
                        print(
                            "Invalid input. Please enter 'y' or 'n', or press Esc to exit."
                        )

        path.parent.mkdir(parents=True, exist_ok=True)
        return True
