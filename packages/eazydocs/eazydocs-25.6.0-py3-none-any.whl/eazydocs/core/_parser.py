class _Parser(type):
    """Eazydocs Parser Metaclass utilized to parse methods and their docstrings.

    This metaclass is responsible for parsing the docstring of a method to
    extract arguments, parameters, examples, and formatted arguments. It is
    used in the MethodType class to create an instance with the parsed method.
    """

    def __call__(self, *args, **kwargs):
        """The metaclass for the ClassType and MethodType classes.

        This metaclass is used to create a new instance of the class and set the
        attributes based on the provided keyword arguments.

        A single argument is expected, which is the class/method to be parsed.

        Raises:
            TypeError: If no arguments are provided to the metaclass.

        Returns:
            ClassType|MethodType: An instance of the class or method type
            with parsed attributes.
        """
        if args is None:
            raise TypeError("Parser requires at least one argument.")

        # Get the first argument, which should be a class or method
        arg = args[0]

        from eazydocs.core.method import Method
        from eazydocs.core.class_type import ClassType

        instance = super().__call__(*args, **kwargs)

        if isinstance(instance, Method):
            instance.summary = instance._get_summary()
            instance.args = instance._get_args()
            instance.params = instance._get_params()
            instance.function = instance._get_function_signature()
            instance.examples = instance._get_examples()
            instance.args_fmtd = instance._format_args()
        elif isinstance(instance, ClassType):
            instance.cls = arg
            instance.__parse__()

        return instance
