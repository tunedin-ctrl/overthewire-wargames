This level is quite tricky. First, the hint given is quite abstract where it says: 

<img title="inspect html" alt="Alt text" src="image_resources/natas4_hint.png">

From the hint, we need to find a way to access the website from natas5 where we have no authorisation access. So, how do we do that?

Well, there is a concept of a referer (without the r).
Referers serve as headers, pinpointing the original URL or webpage from which a request emerged.

For clarity, here's a Chrome definition: The referer-policy header specifies the data available in the Referer header, relevant for navigation and iframes within the destination's document.

By default, "strict-origin-when-cross-origin" ensures only the origin transmits in the referer header during cross-origin requests.

Now we know about referers and can solve the problem. For me, I solved it using a referer control chrome extension to refer me from natas5 website to natas4 website which worked.

<img title="inspect html" alt="Alt text" src="image_resources/natas4_refer.png">

<img title="inspect html" alt="Alt text" src="image_resources/natas4_pass.png">