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
    ),
    "add": BuiltinFunction(
        "add",
        [Parameter("a", TypeReference("Int", None)), Parameter("b", TypeReference("Int", None))],
        TypeReference("Int", None)
    ),
    "sub": BuiltinFunction(
        "sub",
        [Parameter("a", TypeReference("Int", None)), Parameter("b", TypeReference("Int", None))],
        TypeReference("Int", None)
    ),
    "mul": BuiltinFunction(
        "mul",
        [Parameter("a", TypeReference("Int", None)), Parameter("b", TypeReference("Int", None))],
        TypeReference("Int", None)
    ),
    "int_eq": BuiltinFunction(
        "int_eq",
        [Parameter("a", TypeReference("Int", None)), Parameter("b", TypeReference("Int", None))],
        TypeReference("Bool", None)
    )
}