"""eazydocs.core._templates.py

This module contains templates for generating documentation pages.
"""

ARG_TEMPLATE = """    <li>
        <b id='{method}-{name}'>{name} : <i>{arg_type}, {default_arg}</i></b>
        <ul style='list-style: none'>
            <li id='{method}-{name}-description'>{description}</li>
        </ul>
    </li>
"""

ARG_TEMPLATE_NODEFAULT = """    <li>
        <b id='{method}-{name}'>{name} : <i>{arg_type}</i></b>
        <ul style='list-style: none'>
            <li id='{method}-{name}-description'>{description}</li>
        </ul>
    </li>
"""


EXAMPLE_TEMPLATE = """
```python
{example}
```"""
