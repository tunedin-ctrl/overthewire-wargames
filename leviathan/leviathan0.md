After logging in, it just looks like a standard linux os without anything special. 
In the root folder, there is nothing, however after executing `ls -a`, there is a few hidden config files and a `.backup` folder which looks suspicious. 
Inide the `.backup` folder, there is a `bookmarks.html` file which contains a lot of lines with some passwords. 
To filter out the passwords, we can use `grep leviathan1` on `bookmarks.html`, and successfully locate the password for leviathan1.
