import jwt as pyjwt
import requests
from datetime import datetime
from pprint import pprint

APPLICATION_ID = "2127b315-5688-4f72-993b-f1258f136a8d"
PRIVATE_KEY_PATH = "C:/Users/perso/private_business.key"

private_key = open(PRIVATE_KEY_PATH, "rb").read()

iat = int(datetime.now().timestamp())
jwt_body = {
    "iss": "enablebanking.com",
    "aud": "api.enablebanking.com",
    "iat": iat,
    "exp": iat + 3600,
}

jwt_token = pyjwt.encode(
    jwt_body,
    private_key,
    algorithm="RS256",
    headers={"kid": APPLICATION_ID},
)

base_headers = {"Authorization": f"Bearer {jwt_token}"}

CODE = "7c7bc534-d95c-43c4-b9a3-6a5cf18d213f"

r = requests.post(
    "https://api.enablebanking.com/sessions",
    json={"code": CODE},
    headers=base_headers,
)

if r.status_code == 200:
    session = r.json()
    print("Sesión creada correctamente:")
    pprint(session)
else:
    print(f"Error {r.status_code}:", r.text)