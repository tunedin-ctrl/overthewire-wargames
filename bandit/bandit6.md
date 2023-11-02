Really similar to bandit 5 where it needs us to use find to find the byte size of the file. 
However, this time we also want to find the `-group name` and `-user name.
So, the command would look something like this:
`find / -user bandit6 -group -bandit5 -size 33c 2>/dev/null`
`2>/dev/null` is used because there were lots of permission denied errors