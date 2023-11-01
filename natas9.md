For this level, the provided source code is using a grep command to search through dictionary.txt which likely does not contain the password.

<img title="inspect html" alt="Alt text" src="image_resources/natas9_code.png">

So,  we can instead try to inject shell commands into the form. To do this, we can first use: `test; find / -name *natas*;` to find where the password is located.

<img title="inspect html" alt="Alt text" src="image_resources/natas9_form1.png">

After this we can use `; ls ../../../../etc/natas_webpass.` to get the password.

<img title="inspect html" alt="Alt text" src="image_resources/natas9_form2.png">

";" is used to end the egrep query for you to do command injection on the form.

<img title="inspect html" alt="Alt text" src="image_resources/natas9_pass.png">