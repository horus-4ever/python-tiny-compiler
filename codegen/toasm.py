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
    push ebp
    mov ebp, esp

    push esi
    mov esi, dword[esi]

    mov	edx, [esi+4]; message length
    mov	ecx, [esi]	; message to write
    mov	ebx,1		; file descriptor (stdout)
    mov	eax,4		; system call number (sys_write)
    int	0x80		; call kernel

    pop esi
    leave
    ret

println:
    push ebp
    mov ebp, esp

    push esi
    mov esi, dword[esi]

    mov	edx, [esi+4]; message length
    mov	ecx, [esi]	; message to write
    mov	ebx,1		; file descriptor (stdout)
    mov	eax,4		; system call number (sys_write)
    int	0x80		; call kernel

    sub esp, 1
    mov byte[esp], 10
    mov edx, 1
    mov ecx, esp
    mov ebx, 1
    mov eax, 4
    int 0x80
    add esp, 1

    pop esi
    leave
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

_Int__add:
    mov eax, dword[esi]
    mov edx, dword[esi+4]
    add eax, edx
    mov dword[edi], eax
    ret

_Int__sub:
    mov eax, dword[esi]
    mov edx, dword[esi+4]
    sub eax, edx
    mov dword[edi], eax
    ret

_Int__mul:
    mov eax, dword[esi]
    mov ecx, dword[esi+4]
    mov edx, 0
    mul ecx
    mov dword[edi], eax
    ret

_Int__eq:
    mov ecx, dword[esi]
    mov eax, dword[ecx]
    mov ecx, dword[esi+4]
    mov edx, dword[ecx]
    cmp eax, edx
    je .end
    mov dword[edi], 0
    ret
.end:
    mov dword[edi], 1
    ret

_Int__neq:
    mov ecx, dword[esi]
    mov eax, dword[ecx]
    mov ecx, dword[esi+4]
    mov edx, dword[ecx]
    cmp eax, edx
    jne .end
    mov dword[edi], 0
    ret
.end:
    mov dword[edi], 1
    ret

_String__from:
    push ebp
    mov ebp, esp
    
    mov edx, dword[esi+4]

    push edi
    push esi

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

_String__add:
    push ebp
    mov ebp, esp

    push edi
    push esi

    mov eax, esi
    mov esi, dword[eax]
    mov edi, dword[eax+4]

    mov eax, dword[esi+4]
    mov edx, dword[edi+4]
    add edx, eax

    push edx

    push esi
    push edi
    push edx
    call malloc
    pop edx
    pop edi
    pop esi

    pusha
    mov edx, eax
    mov eax, dword[esi]
    mov ecx, dword[esi+4]
    call memcpy
    popa

    pusha
    mov edx, dword[esi+4]
    lea edx, [eax+edx]
    mov eax, dword[edi]
    mov ecx, dword[edi+4]
    call memcpy
    popa

    pop edx

    mov dword [esi], eax
    mov dword [esi+4], edx

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


class ToASM:
    def __init__(self, code):
        self.ir = code

    def to_asm(self):
        rodata = self.generate_rodata(self.ir.rodata)
        text = self.generate_text(self.ir.text)
        """
        main_name = f"function_{hashlib.md5('main'.encode()).hexdigest()}"
        main = self.generate_main(self.code.text.functions[main_name])
        return BASIC_PROGRAM_SHAPE.format(rodata=rodata, text=text, main=main)
        """
        return BASIC_PROGRAM_SHAPE.format(rodata=rodata, text=text)

    def generate_rodata(self, rodata):
        result = ""
        for id, string in rodata.string_litterals.items():
            result += f"string_{id}: db '{string}'\n"
        return result

    def generate_text(self, text):
        result = ""
        for instruction in text.instructions:
            result += self.generate_instruction(instruction)
        return result

    def generate_instruction(self, instruction):
        result = ""
        if isinstance(instruction, ir.LABEL):
            result += f"{instruction.name}:\n"
        elif isinstance(instruction, ir.FUNCTION_PRELUDE):
            result += "\tpush ebp\n"
            result += "\tmov ebp, esp\n"
        elif isinstance(instruction, ir.FUNCTION_END):
            result += "\tleave\n"
            result += "\tret\n"
        elif isinstance(instruction, ir.PREPARE_RETURN):
            result += f"\tsub esp, {instruction.size}\n"
        elif isinstance(instruction, ir.PREPARE_SCOPE):
            result += f"\tsub esp, {instruction.scope_size}\n"
            result += "\tpush esi\n"
            result += "\tpush edi\n"
            result += f"\tlea esi, [esp+8]\n"
            result += f"\tlea edi, [esp+8+{instruction.scope_size}]\n"
        elif isinstance(instruction, ir.CALL_FUNCTION):
            result += f"\tcall {instruction.func_name}\n"
        elif isinstance(instruction, ir.POP_SCOPE):
            result += "\tpop edi\n"
            result += "\tpop esi\n"
            result += f"\tadd esp, {instruction.scope_size}\n"
        elif isinstance(instruction, ir.LOAD_VALUE):
            result += "\tsub esp, 4\n"
            result += f"\tmov dword[esp], {instruction.value}\n"
        elif isinstance(instruction, ir.LOAD_STRING_LITTERAL):
            result += "\tsub esp, 8\n"
            result += f"\tmov dword[esp], {instruction.string_label}\n"
            result += f"\tmov dword[esp+4], {instruction.size}\n"
        elif isinstance(instruction, ir.LOAD_VARIABLE):
            result += f"\tsub esp, {instruction.size}\n"
            result += f"\tmov edx, esp\n"
            result += f"\tlea eax, [ebp+16+{instruction.variable_offset}]\n" # result += f"\tmov eax, [esi+{instruction.variable_offset}]\n"
            result += f"\tmov ecx, {instruction.size}\n"
            result += f"\tcall memcpy\n"
        elif isinstance(instruction, ir.LOAD_REF):
            result += f"\tsub esp, 4\n"
            result += f"\tlea eax, [ebp+16+{instruction.variable_offset}]\n"
            result += f"\tmov dword[esp], eax\n"
        elif isinstance(instruction, ir.LOAD_DEREF):
            result += f"\tmov eax, dword [esp]\n"
            result += f"\tadd esp, 4\n"
            result += f"\tsub esp, {instruction.size}\n"
            result += f"\tmov edx, esp\n"
            result += f"\tmov ecx, {instruction.size}\n"
            result += f"\tcall memcpy\n"
        elif isinstance(instruction, ir.GET_ATTR):
            result += f"\tlea edx, [esp+{instruction.expr_size}-{instruction.size}]\n"
            result += f"\tlea eax, [esp+{instruction.expr_size}-{instruction.size}-{instruction.offset}]\n"
            result += f"\tmov ecx, {instruction.size}\n"
            result += f"\tcall memcpy\n"
            result += f"\tmov eax, {instruction.expr_size}\n"
            result += f"\tsub eax, {instruction.size}\n"
            result += f"\tadd esp, eax\n"
        elif isinstance(instruction, ir.GET_ATTR_DEREF):
            result += f"\tmov ecx, dword[esp]\n"
            result += f"\tadd esp, 4\n"
            result += f"\tsub esp, {instruction.size}\n"
            result += f"\tmov edx, esp\n"
            result += f"\tlea eax, [ecx+{instruction.expr_size}-{instruction.size}-{instruction.offset}]\n"
            result += f"\tmov ecx, {instruction.size}\n"
            result += f"\tcall memcpy\n"
        elif isinstance(instruction, ir.STORE_ARGUMENT):
            result += f"\tlea edx, [esi+{instruction.offset}]\n"
            result += f"\tmov eax, esp\n"
            result += f"\tmov ecx, {instruction.size}\n"
            result += f"\tcall memcpy\n"
            result += f"\tadd esp, {instruction.size}\n"
        elif isinstance(instruction, ir.STORE_VARIABLE):
            result += f"\tlea edx, [ebp+16+{instruction.variable_offset}]\n"
            result += f"\tmov eax, esp\n"
            result += f"\tmov ecx, {instruction.size}\n"
            result += f"\tcall memcpy\n"
            result += f"\tadd esp, {instruction.size}\n"
        elif isinstance(instruction, ir.STORE_VARIABLE_DEREF):
            result += f"\tlea edx, [ebp+16+{instruction.variable_offset}]\n"
            result += f"\tmov edx, [edx]\n"
            result += f"\tmov eax, esp\n"
            result += f"\tmov ecx, {instruction.size}\n"
            result += f"\tcall memcpy\n"
            result += f"\tadd esp, {instruction.size}\n"
        elif isinstance(instruction, ir.RETURN):
            result += f"\tmov edx, edi\n"
            result += f"\tmov eax, esp\n"
            result += f"\tmov ecx, {instruction.size}\n"
            result += "\tcall memcpy\n"
            result += f"\tadd esp, {instruction.size}\n"
        elif isinstance(instruction, ir.POP_JMP_IF_FALSE):
            result += f"\tmov eax, dword[esp]\n"
            result += f"\tadd esp, 4\n"
            result += f"\tcmp eax, 0\n"
            result += f"\tje {instruction.label_name}\n"
        elif isinstance(instruction, ir.JMP):
            result += f"\tjmp {instruction.label_name}\n"
        return result
