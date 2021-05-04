import ir
import ast
import hashlib


BASIC_PROGRAM_SHAPE = """
section .rodata
{rodata}

section .text
extern malloc
extern free
global main


memcpy:
    ; eax=source, ecx=number of bytes, edx=destination
    ; eax ecx edx
    push esi
    push edi
.L1:
    cmp ecx, 0
    je .end
    lea esi, [eax+ecx-1]
    lea edi, [edx+ecx-1]
    mov bl, byte[esi]
    mov byte[edi], bl
    dec ecx
    jmp .L1
.end:
    pop edi
    pop esi
    ret


print:
    mov	edx, [esi+4]; message length
    mov	ecx, [esi]	; message to write
    mov	ebx,1		; file descriptor (stdout)
    mov	eax,4		; system call number (sys_write)
    int	0x80		; call kernel

    mov ebx, [esi]
    call _String__drop
    ret

int_eq:
    mov eax, dword[esi]
    mov edx, dword[esi+4]
    cmp eax, edx
    je .eq
    mov dword[edi], 0
    ret
.eq:
    mov dword[edi], 1
    ret

add:
    mov eax, [esi]
    mov ebx, [esi+4]
    add eax, ebx
    mov dword[edi], eax
    ret

sub:
    mov eax, [esi+4]
    mov ebx, [esi]
    sub eax, ebx
    mov dword[edi], eax
    ret

mul:
    mov eax, [esi]
    mov ecx, [esi+4]
    mov edx, 0
    mul ecx
    mov dword[edi], eax
    ret

_Int__to_string:
    push ebp
    mov ebp, esp

    push esi
    push edi
    push esp

    mov eax, [esi]
    mov ebx, 0
.L1:
    mov edx, 0
    mov ecx, 10
    div ecx
    add edx, 48
    sub esp, 1
    mov byte[esp], dl
    inc ebx
    cmp eax, 0
    jne .L1
.end:
    mov eax, esp
    sub esp, 8
    mov dword[esp], eax
    mov dword[esp+4], ebx
    mov esi, esp
    call _String__from

    pop esp
    pop edi
    pop esi

    leave
    ret

_String__from:
    push ebp
    mov ebp, esp

    push edi
    push esi
    
    mov edx, dword[esi+4]

    push edx
    call malloc
    pop edx

    push eax
    mov edx, eax
    mov eax, dword[esi]
    mov ecx, dword[esi+4]
    call memcpy
    pop eax

    mov edx, dword[esi+4]
    mov dword [edi], eax
    mov dword [edi+4], edx

    pop esi
    pop edi
    leave
    ret

_String__copy:
    push ebp
    mov ebp, esp

    mov eax, dword[esi+4]
    sub esp, 4
    
    pusha
    push eax
    call malloc
    mov dword[ebp-4], eax
    add esp, 4
    popa

    mov eax, dword[esi]
    mov ecx, dword[esi+4]
    mov edx, dword[ebp-4]
    call memcpy

    mov edx, dword[ebp-4]
    mov ecx, dword[esi+4]
    mov dword[edi], edx
    mov dword[edi+4], ecx

    leave
    ret

_String__drop:
    push edi
    push esi
    push ecx
    push edx

    push ebx
    call free
    add esp, 4

    pop edx
    pop ecx
    pop esi
    pop edi

    ret

{main}
{text}
"""

MAIN_FUNCTION = """
main:
    sub esp, {return_size}
    mov edi, esp
    sub esp, {scope_size}
    mov esi, esp
    call {main_hash}
    add esp, {scope_size}
    add esp, {return_size}
    ret
"""

FUNCTION_BODY = """
{function_name}:
    push ebp
    mov ebp, esp
{function_code}
"""


class ToASM:
    def __init__(self, code):
        self.code = code

    def to_asm(self):
        rodata = self.generate_rodata(self.code.rodata)
        text = self.generate_text(self.code.text)
        main_name = f"function_{hashlib.md5('main'.encode()).hexdigest()}"
        main = self.generate_main(self.code.text.functions[main_name])
        return BASIC_PROGRAM_SHAPE.format(rodata=rodata, text=text, main=main)

    def generate_rodata(self, rodata):
        result = ""
        for id, string in rodata.string_litterals.items():
            result += f"_{id}: db '{string}'\n"
        return result

    def generate_main(self, function):
        main_hash = function.name #"function_" + hashlib.md5(function.name.encode()).hexdigest()
        return_size = function.return_size
        scope_size = function.scope_size
        return MAIN_FUNCTION.format(main_hash=main_hash, return_size=return_size, scope_size=scope_size)

    def generate_function(self, function):
        function_name = function.name#"function_" + hashlib.md5(function.name.encode()).hexdigest()
        function_code = ""
        for instruction in function.instructions:
            if isinstance(instruction, ir.PREPARE_RETURN):
                function_code += f"\tsub esp, {instruction.size}\n"
            elif isinstance(instruction, ir.PREPARE_SCOPE):
                function_code += "\tpush esi\n"
                function_code += "\tpush edi\n"
                function_code += f"\tlea esi, [esp+8]\n"
                function_code += f"\tlea edi, [esp+8+{instruction.scope_size}]\n"
            elif isinstance(instruction, ir.CALL_FUNCTION):
                func_name = instruction.function
                """
                function_code += "\tpush esi\n"
                function_code += "\tpush edi\n"
                function_code += f"\tlea esi, [esp+8]\n"
                function_code += f"\tlea edi, [esp+8+{instruction.function.scope_size}]\n"
                """
                function_code += f"\tcall {func_name}\n"
            elif isinstance(instruction, ir.POP_SCOPE):
                function_code += "\tpop edi\n"
                function_code += "\tpop esi\n"
                function_code += f"\tadd esp, {instruction.scope_size}\n"
            elif isinstance(instruction, ir.LOAD_VALUE):
                function_code += f"\tsub esp, 4\n"
                function_code += f"\tmov dword[esp], {int(instruction.value.value)}\n"
            elif isinstance(instruction, ir.LOAD_STRING_LITTERAL):
                function_code += f"\tsub esp, 8\n"
                function_code += f"\tmov dword[esp], _{instruction.id}\n"
                function_code += f"\tmov dword[esp+4], {len(self.code.rodata.string_litterals[instruction.id])}\n"
            elif isinstance(instruction, ir.STORE_VARIABLE):
                if len(instruction.variable) == 4:
                    function_code += f"\tmov eax, dword[esp]\n"
                    function_code += f"\tmov dword[esi+{instruction.variable.offset}], eax\n"
                    function_code += f"\tadd esp, {len(instruction.variable)}\n"
                else: # instruction.variable.typename == "String":
                    function_code += f"\tlea edx, [esi+{instruction.variable.offset}]\n"
                    function_code += f"\tmov eax, esp\n"
                    function_code += f"\tmov ecx, {len(instruction.variable)}\n"
                    function_code += f"\tcall memcpy\n"
            elif isinstance(instruction, ir.LOAD_VARIABLE):
                if len(instruction.variable) == 4:
                    function_code += f"\tsub esp, {len(instruction.variable)}\n"
                    function_code += f"\tmov eax, dword[esi+{instruction.variable.offset}]\n"
                    function_code += f"\tmov dword[esp], eax\n"
                elif instruction.variable.typename == "String":
                    function_code += f"\tsub esp, 8\n"
                    function_code += f"\tpush esi\n"
                    function_code += f"\tpush edi\n"
                    function_code += f"\tlea esi, [esi+{instruction.variable.offset}]\n"
                    function_code += f"\tlea edi, [esp+8]\n"
                    function_code += f"\tcall _String__copy\n"
                    function_code += f"\tpop edi\n"
                    function_code += f"\tpop esi\n"
            elif isinstance(instruction, ir.RETURN):
                if len(instruction.expr_kind) == 4:
                    function_code += f"\tmov eax, dword[esp]\n"
                    function_code += f"\tmov dword[edi], eax\n"
                elif instruction.expr_kind.name == "String":
                    function_code += f"\tmov eax, esp\n"
                    function_code += f"\tmov edx, edi\n"
                    function_code += f"\tmov ecx, 8\n"
                    function_code += f"\tcall memcpy\n"
                function_code += "\tleave\n"
                function_code += "\tret\n"
            elif isinstance(instruction, ir.LABEL):
                function_code += f".L{instruction.label}:\n"
            elif isinstance(instruction, ir.POP_JMP_IF_FALSE):
                function_code += f"\tmov eax, dword[esp]\n"
                function_code += f"\tadd esp, 4\n"
                function_code += f"\tcmp eax, 0\n"
                function_code += f"\tje .L{instruction.label}\n"

        return FUNCTION_BODY.format(function_name=function_name, function_code=function_code)

    def generate_text(self, text):
        result = ""
        for name, function in text.functions.items():
            result += self.generate_function(function)
        return result