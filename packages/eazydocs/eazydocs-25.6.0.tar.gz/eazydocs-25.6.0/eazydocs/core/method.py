from collections import defaultdict
import re
from subprocess import run
from types import FunctionType
from typing import Any, Optional
from eazydocs.core._parser import _Parser
from eazydocs.core._templates import (
    ARG_TEMPLATE,
    ARG_TEMPLATE_NODEFAULT,
    EXAMPLE_TEMPLATE,
)
from eazydocs.core._types import ArgsTuple, ParamsDict


class Method(metaclass=_Parser):
    """EazyDocs Method class.

    This class is used to parse the docstring of a method and extract
    information such as arguments, examples, and parameters. It is designed
    to be used with methods of a class, or functions, to generate documentation
    in a structured format.

    Upon initialization, it takes a method as an argument and parses its
    docstring to extract relevant information. The parsed information includes
    arguments, examples, and parameters, which can be accessed through the
    respective properties of the class.

    Attributes:
        method (object): The method to be parsed with docstring formatting
            defined by Google's style guide.

    Examples:
        >>> example_method.__doc__
        Example method for <class Example>.

        Args:
            param (list): Example required argument. If `param=None` then...
                else if `param=[]` then...
            param2 (str, optional): Example default None argument. Defaults to
                None.
            param3 (str, optional): Example default str argument. Defaults to
                "Test".

        Examples:

        General

            >>> d
            col1     col2
            0       First
            1      Second

        With DataFrame

            >>> data = Data("data.csv")
            >>> data.df
            Date_Time_1          vo2_1 vo2_2
            2025-01-01 00:00:00    0.0   0.0
            2025-01-01 01:00:00    0.0   0.0
            2025-01-01 02:00:00    0.0   0.0
            ...

        >>> Method(example_method).parse()
        <strong id='example'>Example</strong>(<b>param</b>=<i>None</i>, <b>param2</b>=<i>None</i>, <b>param3</b>=<i>"Test"</i>)

        Example method for <class Example>.

        > Parameters:

        <ul>
            <li>
                <b>param : <i>list, None</i></b>
                <ul style='list-style: none'>
                    <li>Example required argument. If <code>param=None</code> then... else if <code>param=[]</code> then...</li>
                </ul>
            </li>
            <li>
                <b>param2 : <i>str, optional, None</i></b>
                <ul style='list-style: none'>
                    <li>Example default None argument. Defaults to None.</li>
                </ul>
            </li>
            <li>
                <b>param3 : <i>str, optional, "Test"</i></b>
                <ul style='list-style: none'>
                    <li>Example default str argument. Defaults to "Test".</li>
                </ul>
            </li>
        </ul>

        > Examples:
        General

        ```python
        >>> d
        col1     col2
        0       First
        1      Second
        ```

        With DataFrame

        ```python
        >>> data = Data("data.csv")
        >>> data.df
        Date_Time_1          vo2_1 vo2_2
        2025-01-01 00:00:00    0.0   0.0
        2025-01-01 01:00:00    0.0   0.0
        2025-01-01 02:00:00    0.0   0.0
        ...
        ```
        <hr>
    """

    def __init__(self, method: object, include_examples: bool = True) -> None:
        """Initializes the Method instance.

        Args:
            method (object): The method to be parsed. It should have a docstring
                formatted according to Google's style guide.
            include_examples (bool, optional): Whether to include examples in
                the documentation. Defaults to True.
        """

        self.method = method
        self.docstring_split = self.docstring.split("\n")
        self.include_examples = include_examples

    def parse(self, to_clipboard: bool = True) -> str:
        """Parse the docstring of the method to extract arguments, examples,
        and parameters.

        Args:
            to_clipboard (bool, optional): If True, the output will be copied
                to the clipboard. Defaults to True.

        Returns:
            str: A formatted string containing the method's signature,
                summary, parameters, and examples (if `include_examples=True`).
        """
        if self.docstring is None:
            raise ValueError(
                f"{self.method} does not have a docstring, or is using an unsupported format. Ensure the method has a docstring formatted according to Google's style guide."
            )

        output = self._get_documentation()

        if to_clipboard:
            run(["clip.exe"], input=output.encode("utf-8"))
            print("Successfully copied to clipboard!")

        return output

    def _get_documentation(self) -> str:
        """Generates the documentation for the method."""
        output = f"{self.function}\n\n"
        output += f"{self.summary}\n\n"
        if self.args is not None:
            output += f"> Parameters:\n\n{self.args_fmtd}\n"
        if self.include_examples and self.examples is not None:
            output += f"> Examples:\n\n{self.examples}"

        output += "\n<hr>\n"

        return output

    def _get_args(self) -> list[ArgsTuple] | None:
        """Parse the arguments from the docstring.

        Returns:
            Optional[list[ArgsTuple]]: A list of tuples containing the
            arguments of the method, their types, and descriptions, or None if
            the docstring does not contain an 'Args' or 'Attributes' section.

        Notes:
            The returned args is a list of tuples, where each tuple contains:
                - param (str) - Name of the argument.
                - arg_type (str) - Type of the argument (e.g., int, str, list)
                - description (str) - Description of the argument.
        """
        if self.docstring is None:
            return None

        args_section = re.search(
            r"(Args|Attributes):\n(.*?)(\n\n|\Z)", self.docstring, re.DOTALL
        )
        if args_section is None:
            return None

        args_section = args_section.group(2)
        args_pattern = re.compile(
            r"\s*(\w+)\s*\(([\w\s,[\]\|]+)\):\s*(.*?)(?=\n\s*\w+\s*\(|\n\n|\Z)",
            re.DOTALL,
        )
        args = args_pattern.findall(args_section)
        return args

    def _get_examples(self) -> str | None:
        """Extracts examples from the docstring.

        Notes:
        - The Examples section is expected to be formatted as follows:
        ```
        Examples:
            Example 1

                >>> example_method(param1, param2)
                <optional output>

            Example 2

                >>> example_method(param1, param2)
                <optional output>
        ```
            - The formatted output will be wrapped in a template defined by the
                parameter's default value. See eazydocs.core._templates.py for
                templates.

        Returns:
            str | None: A string containing the formatted examples, or None if
                no examples are found in the docstring.
        """
        if self.docstring is None:
            return None

        pattern = re.compile(r"Example[s]?:.*?(?=\Z|Example:)", re.DOTALL)
        examples_section = pattern.search(self.docstring)
        if examples_section is None:
            return None

        examples_section = examples_section.group(0)

        pattern = re.compile(r"^\s{8}(\S.*)\n((\s{8}.*\n)*)", re.MULTILINE)
        matches = pattern.findall(examples_section)

        if matches is None:
            return None

        output = ""
        for match in matches:
            title = match[0].strip()
            example = "\n".join(
                line.strip() for line in match[1].strip().splitlines()
            )
            template = EXAMPLE_TEMPLATE.replace("{example}", example)
            output += f"{title}\n{template}\n\n"

        output = output.strip()

        return output

    def _get_function_signature(self) -> str | None:
        """Generates the function signature from the method's name and
        arguments."""
        if self.docstring is None:
            return None

        output = f"<strong id='{self.id}'>{self.name}</strong>("

        # Method has no params, close the signature and return
        if self.params is None:
            output += ")"
            return output

        # Otherwise, iterate through the params and add them to the signature
        for param in self.params:
            default_value = self.params[param].get("default_value")

            if default_value is None:
                output += f"<b>{param}</b>, "
            elif default_value == "None":
                output += f"<b>{param}</b>=<i>None</i>, "
            else:
                output += f"<b>{param}</b>=<i>{self.params[param].get("default_value")}</i>, "

        # Strip the trailing comma and space then add a closing parenthesis
        if output.endswith(", "):
            output = output[:-2] + ")"

        return output

    def _get_id(self) -> str:
        """Formats method name to create a unique ID."""
        id = self.name.replace("_", "-").lower()
        return id

    def _get_params(self) -> defaultdict[ParamsDict] | None:
        if self.args is None:
            return None

        params = defaultdict(ParamsDict)

        for arg in self.args:
            param, arg_type, description = arg
            description = self._format_description(description)
            default_value = self._get_default_value(description)

            params[param] = {
                "arg_type": arg_type,
                "description": description,
                "default_value": default_value,
            }

        return params

    def _get_summary(self) -> str | None:
        """Extracts the summary from the docstring.

        Returns:
            str|None: A string containing the summary of the method, or None
                if no summary is found in the docstring.
        """
        if self.docstring_split is None:
            return None

        summary = ""
        for line in self.docstring_split:
            if line.strip() in ["Args:", "Example:", "Equation:"]:
                break
            else:
                line = line.strip() + " "
                summary += line
        summary = summary.strip()

        return summary

    def _format_description(self, description: str) -> str:
        """Format the description of the argument by replace backticks and
            apostrophes with <code> tags.

        Args:
            description (str): String expression to format.
        """
        arg = re.sub(r"\s+", " ", description).strip()
        pattern = r"`"
        count = 0

        def replace(arg):
            nonlocal count
            count += 1
            return "<code>" if count % 2 != 0 else "</code>"

        return re.sub(pattern, replace, arg)

    def _get_default_value(self, arg: str) -> str:
        """Extracts the default value from the arg.

        Args:
            arg (str): Line from docstring to extract default value from.

        Returns:
            str: Default value of the argument or 'None' if
                no default value is found.
        """
        pattern = r"Defaults to (.+)\."
        match_obj = re.search(pattern, arg.strip())

        if match_obj:
            default_value = match_obj.group(1).strip()
            return f"{default_value}"
        else:
            default_value = "None"

        return default_value

    def _format_args(self) -> str:
        output = ""

        if self.params is None:
            return None

        for name, arg in self.params.items():
            default_arg = arg.get("default_value")

            if default_arg is None:
                template = ARG_TEMPLATE_NODEFAULT
                output += template.format(
                    method=self.name,
                    name=name,
                    arg_type=arg.get("arg_type"),
                    description=arg.get("description"),
                )
            else:
                template = ARG_TEMPLATE
                output += template.format(
                    method=self.name,
                    name=name,
                    arg_type=arg.get("arg_type"),
                    default_arg=default_arg,
                    description=arg.get("description"),
                )

        return f"<ul>\n{output}</ul>\n"

    # == Properties ==
    @property
    def args(self) -> list[Any]:
        return self._args

    @args.setter
    def args(self, val: list[Any]) -> None:
        self._args = val

    @property
    def args_fmtd(self) -> str:
        return self._args_fmtd

    @args_fmtd.setter
    def args_fmtd(self, val: str) -> None:
        self._args_fmtd = val

    @property
    def docstring(self) -> str:
        """The docstring of the method."""
        return self.method.__doc__ or ""

    @property
    def docstring_split(self) -> list[str] | None:
        """Split the docstring into a list of lines."""
        return self._docstring_split

    @docstring_split.setter
    def docstring_split(self, val: Optional[list[str]]) -> None:
        self._docstring_split = val

    @property
    def examples(self) -> str | None:
        """String containing examples from the docstring."""
        return self._examples

    @examples.setter
    def examples(self, val: str | None) -> None:
        self._examples = val

    @property
    def function(self) -> str:
        """Function signature for the method."""
        return self._function

    @function.setter
    def function(self, val: str) -> None:
        self._function = val

    @property
    def id(self) -> str:
        """The ID of the method, used for HTML element IDs."""
        return self.name.replace("_", "-").lower()

    @property
    def method(self) -> object:
        """The method object that this Method represents."""
        return self._method

    @method.setter
    def method(self, val: object) -> None:
        self._method = val

    @property
    def name(self) -> str:
        """The name of the method."""
        return self.method.__name__

    @name.setter
    def name(self, val: str) -> None:
        self._name = val

    @property
    def params(self) -> defaultdict[Any, ParamsDict]:
        return self._params

    @params.setter
    def params(self, val: list) -> None:
        self._params = val

    @property
    def summary(self) -> str | None:
        """Summary of the method extracted from the docstring."""
        return self._summary

    @summary.setter
    def summary(self, val: str | None) -> None:
        self._summary = val
