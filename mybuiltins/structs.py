from ast import *


__all__ = (
    "builtin_structs",
)

builtin_structs = {
    "Int": BuiltinStructure(
        "Int",
        stack_size=4,
        fields={},
        builtin_methods={}
    ),
    "Empty": BuiltinStructure(
        "Empty",
        stack_size=0,
        fields={},
        builtin_methods={}
    ),
    "String": BuiltinStructure(
        "String",
        stack_size=8, # ptr + length
        fields={},
        builtin_methods={}
    )
}