from inspect import getmembers, isfunction, ismethod
from re import sub
from typing import Optional, Self
from eazydocs.core._parser import _Parser
from eazydocs.core.method import Method
from subprocess import run


class ClassType(metaclass=_Parser):
    """Eazydocs ClassType used to represent a class and its methods.

    This class is used to parse the docstring of a class and extract its
    methods, arguments, parameters, and examples. It is
    used in the Eazydocs documentation generation process.

    Args:
        cls (object): The class object to be parsed.
        include_methods (bool): Whether to include methods in the documentation.
            Defaults to True.
        include_private_methods (bool): Whether to include private methods in
            the documentation. Defaults to False.
        include_examples (bool): Whether to include examples in the
            documentation. Defaults to True.
        include_table_of_contents (bool): Whether to include a table of contents
            in the documentation. Defaults to True.

    Attributes:
        cls (object): The class object that this ClassType represents.
        docstring (str | None): The docstring of the class.
        id (str): The ID of the class, used for HTML element IDs.
        name (str): The name of the class.


    """

    def __init__(
        self,
        cls: object,
        include_methods: bool = True,
        include_private_methods: bool = False,
        include_examples: bool = True,
        include_table_of_contents: bool = True,
    ):
        self.include_methods = include_methods
        self.include_private_methods = include_private_methods
        self.include_examples = include_examples
        self.include_table_of_contents = include_table_of_contents

        self.init = None
        self.methods: list[Method] = []

    def parse(self, to_clipboard: bool = True) -> str:
        """This method parses the class and generates the documentation.
        Args:
            to_clipboard (bool): If True, the output will be copied to the
                clipboard. Defaults to True.

        Returns:
            str: The formatted documentation string for the class and its
                methods. If `to_clipboard` is True, the output will also be
                copied to the clipboard.
        """
        if self.output is None:
            self.__parse__()

        if to_clipboard:
            run(["clip.exe"], input=self.output.encode("utf-8"))
            print("Successfully copied to clipboard!")

        return self.output

    def __parse__(self) -> Self:
        for name, member in getmembers(self.cls):
            if ismethod(member) or isfunction(member):
                if self.include_methods:
                    if self.include_private_methods:
                        self.methods.append(
                            Method(member, self.include_examples)
                        )
                    elif not name.startswith("_"):
                        self.methods.append(
                            Method(member, self.include_examples)
                        )
                if name == "__init__":
                    self.init = member

        if self.init is not None:
            self.output = self._get_cls_documentation()

    def _get_cls_documentation(self) -> str:
        """Generates the documentation for the class.

        Returns:
            str: The formatted documentation string for the class and its
                methods.
        """
        method = self.init
        if method.__doc__ is None:
            return ""

        output = f"# {self.name}\n\n"

        if self.include_table_of_contents:
            output += self._get_table_of_contents()

        # Parse the docstring of the __init__ method
        docstring = Method(method)
        docstring.name = self.name

        # function_fmtd = docstring.function.replace(
        #     "--init--", self.name
        # ).replace("__init__", self.name)

        # Append the formatted function signature and summary
        output += f"{docstring.function}\n\n{docstring.summary}\n\n"
        # Append the examples if they exist
        if docstring.args:
            output += f"> Parameters:\n\n{docstring.args_fmtd}\n\n"

        output = sub(r"--init--|__init__", self.name, output)

        if docstring.examples:
            output += f"> Examples:\n\n{docstring.examples}\n\n"

        if self.methods != []:
            output += self._get_method_documentation()

        return output

    def _get_table_of_contents(self) -> str:
        """Generates the table of contents providing links to methods."""
        table_of_contents = f"- [Class Documentation](#{self.id})\n"

        for method in self.methods:
            table_of_contents += f"- [{method.name}](#{method.id})\n"
        table_of_contents += "\n"
        return table_of_contents

    def _get_method_documentation(self) -> str:
        """Generates the documentation for the class methods."""
        output = "## Class Methods\n\n"
        for method in self.methods:
            output += method._get_documentation()
        return output

    @property
    def cls(self) -> object:
        """The class object that this ClassType represents."""
        return self._cls

    @cls.setter
    def cls(self, val: object) -> None:
        self._cls = val

    @property
    def docstring(self) -> str | None:
        """The docstring of the class."""
        return self.cls.__init__.__doc__ or self.cls.__doc__ or None

    @property
    def id(self) -> str:
        """The ID of the class, used for HTML element IDs."""
        return self.name.replace("_", "-").lower()

    @property
    def init(self) -> Method | None:
        """The __init__ method of the class, if it exists."""
        return self._init

    @init.setter
    def init(self, val: Optional[Method] = None) -> None:
        self._init = val

    @property
    def methods(self) -> list[Method]:
        """The list of methods in the class."""
        return self._methods

    @methods.setter
    def methods(self, val: list[Method]) -> None:
        self._methods = val

    @property
    def name(self) -> str:
        """The name of the class."""
        return self.cls.__name__

    @property
    def output(self) -> str:
        """The formatted output of the class documentation."""
        return self._output

    @output.setter
    def output(self, val: str) -> None:
        self._output = val
