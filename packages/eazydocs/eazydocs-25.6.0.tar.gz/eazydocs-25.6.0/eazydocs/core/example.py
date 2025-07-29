from typing import NamedTuple, Optional
from pandas import DataFrame
from subprocess import run


from eazydocs.core._types import FunctionMethodType, StrPathType


class DfShape(NamedTuple):
    """Shape of a DataFrame.

    Attributes:
        rows (int): Number of rows.
        columns (int): Number of columns.
    """

    rows: int
    columns: int


class Example:
    def __init__(
        self,
        arg: DataFrame | FunctionMethodType,
        df_shape: Optional[tuple[int, int] | DfShape] = None,
        copy_to_clipboard: bool = True,
        append_to_method: Optional[str] = None,
        filename: Optional[StrPathType] = None,
        path: Optional[StrPathType] = None,
    ) -> None:
        """Generate an example representation of a DataFrame or method.

        Args:
            arg (DataFrame | FunctionMethodType): The DataFrame or method to
                generate an example for.
            df_shape (tuple[int,int] | DfShape, optional): A tuple or
                DfShape specifying the number of rows and columns to display
                from the DataFrame. If `type(arg)==DataFrame` and
                `df_shape=None`, the default shape of (5,5) will be used.
                Defaults to None.
            copy_to_clipboard (bool, optional): If True, the output will be
                copied to the clipboard. Defaults to True.
            append_to_method (str, optional): If provided, the example will be
                appended to the specified method in the markdown file. If
                `append_to_method!=None`, `filename` must also be provided.
                Optionally providing the `path` argument. Defaults to None.
            filename (StrPathType, optional): String or Path object for the
                filename. Defaults to None.
            path (StrPathType, optional): Directory path where the file will be
                located. Defaults to None.

        Raises:
            ValueError: If 'append_to_method' is provided but 'filename' is
                None.
        """
        if append_to_method and filename is None:
            raise ValueError(
                "'filename' must be provided if 'append_to_method' is used"
            )

        self.arg = arg
        self.copy_to_clipboard = copy_to_clipboard
        self.append_to_method = append_to_method
        self.filename = filename
        self.path = path

        if isinstance(arg, DataFrame):
            if df_shape is None:
                df_shape = (5, 5)
            output = self._format_df(df_shape)
        elif isinstance(arg, (FunctionMethodType)):
            output = self._format_method()
        else:
            raise TypeError("'arg' must be a DataFrame or method/function")

        if append_to_method is not None:
            raise NotImplementedError(
                "Appending to method not yet implemented"
            )

        if copy_to_clipboard:
            run(["clip.exe"], input=output.encode("utf-8"))
            print("Successfully copied example to clipboard!")

    def _format_df(self, shape: tuple[int, int]) -> str:
        """Provides a string representation of a DataFrame with specified shape.

        Args:
            shape (tuple[int,int]): A tuple specifying the number of rows and
                columns to display from the DataFrame.

        Raises:
            TypeError: If 'shape' is not a tuple or list of two integers.
            ValueError: If 'shape' does not contain exactly two integers.

        Returns:
            str: A formatted string representing the DataFrame.
        """
        if not isinstance(shape, tuple) and isinstance(shape, list):
            shape = tuple(shape)
        else:
            raise TypeError("'shape' must be a tuple or list of two integers")

        if len(shape) != 2:
            raise ValueError("'shape' must be a tuple of two integers")

        df = self.arg
        df = df.head(shape[0])
        df = df.iloc[:, 0 : shape[1]]

        output = df.to_string()
        output = "\n".join(f"\t{line}" for line in output.splitlines())

        return output

    def _format_method(self) -> str:
        """Provides a string representation of a method call with its arguments.

        Returns:
            str: A formatted string representing the method call.
        """
        output = f"```python\n{self.arg.__name__}()\n```"
        return output

    def _append_to_method(self, example: str) -> None:
        """Append the example to a specified method in a markdown file.

        Args:
            example (str): The example string to append.
        """
        from eazydocs.markdown.updater import Updater
