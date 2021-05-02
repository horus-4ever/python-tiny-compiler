from ast import *


__all__ = (
    "builtin_functions",
)

builtin_functions = {
    "to_string": BuiltinFunction(
        "to_string",
        [Parameter("integer", TypeReference("Int", None))],
        TypeReference("String", None)
    ),
    "print": BuiltinFunction(
        "print",
        [Parameter("object", TypeReference("String", None))],
        TypeReference("Empty", None)
    )
}