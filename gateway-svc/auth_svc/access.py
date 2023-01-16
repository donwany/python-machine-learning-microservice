import os
import requests


def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/api/v1.0/login", auth=basicAuth
    )
    # http://auth:5000/api/v1.0/login

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)