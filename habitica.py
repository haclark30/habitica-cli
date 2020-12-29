import requests

CLIENT_KEY = "93c29c04-03b3-416f-bc6f-0edbfd806238-HabiticaCLI"
AUTH_CFG = 'auth.cfg'
USER_ID = ""
API_KEY = ""

BASE_URL = "https://habitica.com/api/v3"

with open(AUTH_CFG, 'r') as auth_file:
    USER_ID = auth_file.readline()
    USER_ID = USER_ID.split('=')[1].strip()

    API_KEY = auth_file.readline()
    API_KEY = API_KEY.split('=')[1].strip()

AUTH_HEADERS = {'x-api-user': USER_ID, 'x-api-key': API_KEY, 'x-client': CLIENT_KEY}
r = requests.get("{url}/tasks/user".format(url=BASE_URL), headers=AUTH_HEADERS)
print(r.text)

