From using `ls -la`, the executable to work with is `leviathan6`. 

When executing leviathan6, the output looks like this:

```
leviathan6@gibson:~$ ./leviathan6 
usage: ./leviathan6 <4 digit code>
```

Since we do not know what the executable is doing, we use objdump to peek into the executable's dynamic symbol table:

```
leviathan6@gibson:~$ objdump -T leviathan6 

leviathan6:     file format elf32-i386

DYNAMIC SYMBOL TABLE:
00000000      DF *UND*  00000000 (GLIBC_2.34) __libc_start_main
00000000      DF *UND*  00000000 (GLIBC_2.0)  printf
00000000      DF *UND*  00000000 (GLIBC_2.0)  geteuid
00000000      DF *UND*  00000000 (GLIBC_2.0)  puts
00000000      DF *UND*  00000000 (GLIBC_2.0)  system
00000000  w   D  *UND*  00000000  Base        __gmon_start__
00000000      DF *UND*  00000000 (GLIBC_2.0)  exit
00000000      DF *UND*  00000000 (GLIBC_2.0)  setreuid
00000000      DF *UND*  00000000 (GLIBC_2.0)  atoi
0804a004 g    DO .rodata        00000004  Base        _IO_stdin_used
```
Observations from the output:

    - The program uses functions like `printf` and puts for displaying outputs.
    - It retrieves the user's effective UID using geteuid.
    - It seems to execute system commands (`system`) and converts strings to integers (`atoi`).

```
leviathan6@gibson:~$ ltrace ./leviathan6 777
__libc_start_main(0x80491d6, 2, 0xffffd694, 0 <unfinished ...>
atoi(0xffffd7d1, 0xf7fd6f90, 0xf7c184be, 0xf7fbe4a0)                                                                                = 777
puts("Wrong"Wrong
)                                                                                                                       = 6
+++ exited (status 0) +++
```

Now we need to probe the excepted input with an integer to find what its doing.
Using GDB:

```
leviathan6@gibson:~$ gdb --args ./leviathan6 666
Dump of assembler code for function main:
...
0x0804922a <+84>:    cmp    %eax,-0xc(%ebp)
...
```

This is the input. Now we need to find cmp and allocate a breakpoint:

```
(gdb) b *0x0804922a
Breakpoint 1 at 0x804922a
also make a breakpoint at main
b main
layout reg
r
```

As you step through the instructions using `si` and `ni`, observe the register value at `x/d $ebp-0xc` which reveals the number `7123`.

Now we input into executable and get our password:

```
leviathan6@gibson:~$ ./leviathan6 7123
$ cat /etc/leviathan_pass/leviathan7
8GpZ5f8Hze
$ 
```

Pretty much this level teaches us how to use GDB, ltrace and strace. These are useful tools for reverse engineering and doing binary exploitations for later stages.