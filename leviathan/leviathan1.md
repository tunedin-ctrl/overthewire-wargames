For this question, I used ls -la to look at the non-hidden file `check` and found out that the `check` file is executable with the owner as leviathan2.

```
-r-sr-x---  1 leviathan2 leviathan1 ... check
```

To understand more of what the `check` file does, I execute it and find that it asks for a password which I do not have. So, I used `objdump -T check` to go through the symbol table. In doing so, I find that it uses `strcmp` for comparing the password string against our `getchar(input)`. Also, `system` might mean that it can help us execute shell commands and help us get the password.

DYNAMIC SYMBOL TABLE:
00000000      DF *UND*  00000000 (GLIBC_2.0)  strcmp
00000000      DF *UND*  00000000 (GLIBC_2.34) __libc_start_main
00000000      DF *UND*  00000000 (GLIBC_2.0)  printf
00000000      DF *UND*  00000000 (GLIBC_2.0)  getchar
00000000      DF *UND*  00000000 (GLIBC_2.4)  __stack_chk_fail
00000000      DF *UND*  00000000 (GLIBC_2.0)  geteuid
00000000      DF *UND*  00000000 (GLIBC_2.0)  puts
00000000      DF *UND*  00000000 (GLIBC_2.0)  system
00000000  w   D  *UND*  00000000  Base        __gmon_start__
00000000      DF *UND*  00000000 (GLIBC_2.0)  setreuid
0804a004 g    DO .rodata        00000004  Base        _IO_stdin_used

Now equipped with some knowledge of the eexecutable, I used `ltrace` to walk through the executable like so:

```
__libc_start_main(0x80491e6, 1, 0xffffd6a4, 0 <unfinished ...>
printf("password: ")                                                                                                   = 10
getchar(0xf7fbe4a0, 0xf7fd6f90, 0x786573, 0x646f67password: hello
)                                                                    = 104
getchar(0xf7fbe4a0, 0xf7fd6f68, 0x786573, 0x646f67)                                                                    = 101
getchar(0xf7fbe4a0, 0xf7fd6568, 0x786573, 0x646f67)                                                                    = 108
strcmp("hel", "sex")                                                                                                   = -1
puts("Wrong password, Good Bye ..."Wrong password, Good Bye ...
)                                                                                   = 29
+++ exited (status 0) +++
```

In the above code, the `strcmp` is comparing against the string `sex` which is likely the password. So, I execute `./check` again with the string `sex` and it got me inside a shell terminal and got me the password after using `cat /etc/leviathan_pass/leviathan2`. 
The reason why this works is that the owner of the executable is leviathan2 as shown when executing `ls -la` intially. 

Pretty much all these steps got me to the password. In this challenge, it taught me how to use `ltrace` which helps intercept dynamic library calls and signals by the executable process.
