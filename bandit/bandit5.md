Worked using `du -b (bytes) -a (all) | egrep 1033 to find byte size 1033`

Initally tried to write a shell script which traversed through the ls in inhere and an inner loop to traverse through the files inside the `maybehere` files to see if there are non executable and a file with ascii
From retrospective, maybe another method to find it out, we could use:

`find / -size 1033c to find the file`