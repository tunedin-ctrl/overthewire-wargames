After logging in, it just looks like a standard linux os without anything special. 
In the root folder, there is nothing shown on the surface when using `ls`, however, after executing `ls -a` to show all files and folders, there is a few hidden config files and a `.backup` folder which looks suspicious. 
Inide the `.backup` folder, there is a `bookmarks.html` file which contains a lot of lines with some passwords. 
To filter out the passwords, we can use `grep leviathan1` on `bookmarks.html`, and successfully locate the password for leviathan1.
