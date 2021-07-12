nasm -f elf32 -o out/out.o out/out.s
gcc -m32 -o out/out out/out.o