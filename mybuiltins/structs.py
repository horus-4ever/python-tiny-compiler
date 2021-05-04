from ast import *


__all__ = (
    "builtin_structs",
)

builtin_structs = {
    "Int": BuiltinStructure(
        "Int",
        stack_size=4,
        fields={},
        builtin_methods={
            "to_string": BuiltinFunction(
                "to_string",
                [Parameter("number", TypeReference("Int", None))],
                TypeReference("String", None)
            )
        }
    ),
    "Empty": BuiltinStructure(
        "Empty",
        stack_size=0,
        fields={},
        builtin_methods={}
    ),
    "Str": BuiltinStructure(
        "Str",
        stack_size=8,
        fields={},
        builtin_methods={}
    ),
    "String": BuiltinStructure(
        "String",
        stack_size=8, # ptr + length
        fields={},
        builtin_methods={
            "from": BuiltinFunction(
                "from",
                [Parameter("string", TypeReference("Str", None))],
                TypeReference("String", None)
            )
        }
    ),
    "Bool": BuiltinStructure(
        "Bool",
        stack_size=4,
        fields={},
        builtin_methods={}
    )
}