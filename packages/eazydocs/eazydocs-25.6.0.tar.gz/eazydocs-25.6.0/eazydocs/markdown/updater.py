from inspect import isclass
from pathlib import Path
from typing import Optional
from eazydocs.core._types import (
    ClassMethodType,
    FunctionMethodType,
    StrPathType,
)
from eazydocs.core.functions import create_md_file
from eazydocs.core.method import Method
from eazydocs.markdown.reader import Reader
from eazydocs.markdown.writer import Writer


class Updater:
    def __init__(
        self,
        class_or_method: ClassMethodType,
        filename: StrPathType,
        path: Optional[StrPathType] = None,
    ) -> None:
        """EazyDocs Updater class to update documentation for a class or method.

        Note:
            Providing a class will result in the file being overwritten since
            markdown files are expected to contain documentation for a
            single class and it's methods.

        Args:
            class_or_method (ClassMethodType): Class or method to update
                documentation for. If a class is provided, it will overwrite the
                provided file.
            filename (StrPathType): String or Path object representing the
                filename where the documentation is stored.
            path (StrPathType, optional): String or Path object for the path
                where the file will be saved. If not provided, the file will be
                saved in the current working directory. If provided, the
                `filename` will be joined to `path` argument. Defaults to None.
        """
        # Class provided, overwrite the file
        if isclass(class_or_method):
            return create_md_file(
                class_or_method=class_or_method,
                filename=filename,
                path=path,
                overwrite=True,
                update=True,
            )

        # Method provided, update the file
        filepath = self._valid_file(filename, path)
        self._update_md_file(filepath, class_or_method)

    def _update_md_file(
        self, filepath: Path, method: FunctionMethodType
    ) -> None:
        """Updates a method within the markdown file.

        Args:
            filepath (Path): Path object pointing to the markdown file to be
                updated.
            method (FunctionMethodType): Function or method to update
                documentation for.
        """
        method_docs = Method(method).parse(to_clipboard=False)

        contents, methods = self._read_md_file(filepath)

        old_method = methods.get(method.__name__)
        if old_method is None:
            # Append new method to the file
            contents = f"{contents}\n{method_docs}"
        else:
            self._update_method(
                contents, method.__name__, method_docs, filepath
            )

    def _valid_file(
        self,
        filename: StrPathType,
        path: Optional[StrPathType] = None,
    ) -> Path:
        """Check if the file is valid for updating.

        Args:
            filename (StrPathType): String or Path object representing the
                filename. Expected to be a markdown file (ends with .md).
            path (StrPathType, optional): The path where the file is located. If
                provided, it will be joined with the filename. Defaults to None.

        Returns:
            Path: A Path object pointing to the valid markdown file.

        Raises:
            ValueError: If the provided filename is invalid or does not exist at
                the specified path.
        """
        # Handle filename
        if isinstance(filename, str):
            filename = Path(filename)
        if not filename.suffix == ".md":
            filename = filename.with_suffix(".md")
        # Handle path
        if path is not None:
            filepath = Path(path) / filename
        else:
            filepath = Path(filename)

        if not filepath.exists():
            raise ValueError(
                f"Invalid file: '{filepath}'. Ensure the filename is spelled correctly and the path is correct."
            )
        return filepath

    def _read_md_file(self, filepath: Path) -> tuple[str, dict]:
        """Read the markdown file"""
        with Reader(filepath) as reader:
            contents = reader.contents
            methods = reader.methods
        return contents, methods

    def _update_method(
        self,
        current_docs: str,
        method_name: str,
        new_docs: str,
        filepath: Path,
    ) -> None:
        """Trim the old method documentation from the markdown file and
        replace it with the new documentation.

        Args:
            current_docs (str):  Current contents of the markdown file.
            method_name (str): Name of the method to be updated.
            new_docs (str): New documentation for the method.
            filepath (Path): Path object pointing to the markdown file to be
                updated.
        """
        # Format the method name to match the markdown format
        method_name = method_name.replace("_", "-")
        method_name = f"<strong id='{method_name}'"
        # Find the start and end of the old method
        start = current_docs.find(method_name)
        end = current_docs[start:].find("<hr>")
        # Get before and after old method docs
        before = current_docs[:start].strip()
        after = current_docs[(start + (end + 4)) :].strip()
        # Join parts
        updated_docs = f"{before}\n\n{new_docs}\n{after}"

        writer = Writer(updated_docs, filepath, overwrite=True, update=True)
        return writer.write()
