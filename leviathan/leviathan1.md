For this question, I used ls -la to look at the non-hidden file `check` and found out that the check file is an executable with the owner as leviathan2 like so:

```
-r-sr-x---  1 leviathan2 leviathan1 ... check
```

So I execute the check file and find that it asks for a password which I have no clue. So, I used `objdump -T check` to go through the table and find it uses `strcmp` for comparing the password string against our `getchar(input)`. Also, `system` might mean it executes shell commands like so:

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

Since we have a rough idea of the structure, I used `ltrace` to walk through the executable like so:

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

In the above code, the strcmp is comparing against the string `sex` which is likely the password. So, I execute `./check` again with the string `sex` and it got me into a shell terminal which then I just use `cat /etc/leviathan_pass/leviathan2` which works since the owner of the executable is leviathan2. Pretty much these steps got me the password.