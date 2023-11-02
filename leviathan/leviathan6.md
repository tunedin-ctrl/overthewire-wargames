From using `ls -la`, the executable to work with this time is `leviathan6`. 

When executing leviathan6, the output looks like this:

```
leviathan6@gibson:~$ ./leviathan6 
usage: ./leviathan6 <4 digit code>
```

Since we do not know what the executable is doing exactly other than needing a 4 digit code, we use objdump to peek into the executable's dynamic symbol table:

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
    
To understand more, we use `ltrace`:
```
leviathan6@gibson:~$ ltrace ./leviathan6 777
__libc_start_main(0x80491d6, 2, 0xffffd694, 0 <unfinished ...>
atoi(0xffffd7d1, 0xf7fd6f90, 0xf7c184be, 0xf7fbe4a0)                                                                                = 777
puts("Wrong"Wrong
)                                                                                                                       = 6
+++ exited (status 0) +++
```

However, we do not gain much more knowledge from `ltrace`, so we use GDB for debugging and walking through the stack.

```
leviathan6@gibson:~$ gdb --args ./leviathan6 666
Dump of assembler code for function main:
...
0x0804922a <+84>:    cmp    %eax,-0xc(%ebp)
...
```

Here is the input. Now we need to find out where the `cmp` register is and allocate a breakpoint:

```
(gdb) disassemble main
Dump of assembler code for function main:
   0x080491d6 <+0>:     lea    0x4(%esp),%ecx
   0x080491da <+4>:     and    $0xfffffff0,%esp
   0x080491dd <+7>:     push   -0x4(%ecx)
   0x080491e0 <+10>:    push   %ebp
   0x080491e1 <+11>:    mov    %esp,%ebp
   0x080491f3 <+13>:    push   %ebx
   0x080491f4 <+14>:    push   %ecx
   0x080491f5 <+15>:    sub    $0x10,%esp
   0x080491f8 <+18>:    mov    %ecx,%eax
   0x080491fb <+20>:    movl   $0x1bd3,-0xc(%ebp)
   0x080491f2 <+27>:    cmpl   $0x2,(%eax)
   0x080491f4 <+30>:    je     0x8049216 <main+64>
   0x080491f6 <+32>:    mov    0x4(%eax),%eax
   0x080491f9 <+35>:    mov    (%eax),%eax
   0x0804920b <+37>:    sub    $0x8,%esp
   0x0804920e <+40>:    push   %eax
   0x0804920f <+41>:    push   $0x804a008
   0x08049204 <+46>:    call   0x8049050 <printf@plt>
   0x08049209 <+51>:    add    $0x10,%esp
   0x0804920c <+54>:    sub    $0xc,%esp
   0x0804920f <+57>:    push   $0xffffffff
   0x08049211 <+59>:    call   0x8049090 <exit@plt>
   0x08049216 <+64>:    mov    0x4(%eax),%eax
   0x08049219 <+67>:    add    $0x4,%eax
   0x0804921c <+70>:    mov    (%eax),%eax
   0x0804921f <+72>:    sub    $0xc,%esp
   0x08049222 <+75>:    push   %eax
   0x08049223 <+76>:    call   0x80490b0 <atoi@plt>
   0x08049227 <+81>:    add    $0x10,%esp
   0x0804922a <+84>:    cmp    %eax,-0xc(%ebp)
   0x0804922f <+87>:    jne    0x804925a <main+132>
   0x0804922f <+89>:    call   0x8049060 <geteuid@plt>
   0x08049232 <+94>:    mov    %eax,%ebx
   0x08049234 <+96>:    call   0x8049060 <geteuid@plt>
   0x0804923d <+101>:   sub    $0x8,%esp
   0x0804923e <+104>:   push   %ebx
   0x0804923f <+105>:   push   %eax
   0x08049240 <+106>:   call   0x80490a0 <setreuid@plt>
   0x08049245 <+111>:   add    $0x10,%esp
   0x08049246 <+114>:   sub    $0xc,%esp
   0x08049250 <+117>:   push   $0x804a022
   0x08049253 <+122>:   call   0x8049080 <system@plt>
   0x08049256 <+127>:   add    $0x10,%esp
   0x08049258 <+130>:   jmp    0x804926a <main+148>
   0x0804925a <+132>:   sub    $0xc,%esp
   0x0804925d <+135>:   push   $0x804a02a
   0x08049262 <+140>:   call   0x8049070 <puts@plt>
...
End of assembler dump.

(gdb) b *0x0804922a
Breakpoint 1 at 0x0804922a
also make a breakpoint at main
b main
layout reg
r
...
```

As we step through the register instructions using `si` and `ni`, we finally hit the register value at `x/d $ebp-0xc` which reveals the number `7123`.

Now we input into executable and get our password:

```
leviathan6@gibson:~$ ./leviathan6 7123
$ cat /etc/leviathan_pass/leviathan7
8GpZ5f8Hze
$ 
```

Pretty much this level teaches us how to use `GDB` and `ltrace`. 
These are useful tools for reverse engineering and doing binary exploitations for later stages.

### Reflection:
Overall, this was a pretty enjoyable exercise as I got to finally learn the proper way to use gdb. Another approach of solving the task the 'easy way' is through brute force like what I did in natas for finding the `PHPSESSID`. We can allocate a few threads to iterate through different chunks of the 4 digit code. An example is chunk 1 allocated to checking 0-2500 and chunk 2 check 2501-5000, etc. 
However, I wanted to challenge myself with learning `gdb`. The challenging and fustrating part about that was going over the registers repeatedly to confirm the final register value at  `x/d $ebp-0xc`. This was mainly my fault for not accounting for the subtraction of 0xc from the initial `$ebp` register.
