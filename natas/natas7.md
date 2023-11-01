This level introduces us to a new concept of "Local File Inclusion (LFI)" which is a type of URL manipulation vulnerabilities.

Using chrome's developer mode, the HTML provides us a hint pointing to a folder called: `/etc/natas_webpass/natas8`. 

<img title="inspect html" alt="Alt text" src="image_resources/natas7_hint.png">

However, a straightforward attempt to navigate using this route ends in a familiar 'page not found' (404) error. This error arises because we're bypassing the expected query parameter. 
To crack this, we need to do traverse the route which leads us to the password like so:
`http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8`

<img title="inspect html" alt="Alt text" src="image_resources/natas7_pass.png">


