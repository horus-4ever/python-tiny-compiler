from ast import *


__all__ = (
    "builtin_functions",
)

builtin_functions = {
    "print": BuiltinFunction(
        "print",
        [Parameter("object", NormalType("String"))],
        NormalType("Empty")
    )
}