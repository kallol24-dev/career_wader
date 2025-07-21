import requests
from django.conf import settings # type: ignore

def refresh_access_token(refresh_token):
    refresh_url = f"{settings.API_BASE_URL}api/token/refresh/"
    response = requests.post(refresh_url, json={"refresh": refresh_token})
    if response.status_code == 200:
        return response.json().get("access")
    return None

def fetch_with_refresh(request, method, url, json_data=None):
    access_token = request.COOKIES.get("access_token")
    refresh_token = request.COOKIES.get("refresh_token")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    method_func = getattr(requests, method)
    response = method_func(url, headers=headers, json=json_data)

    if response.status_code == 401 and refresh_token:
        new_token = refresh_access_token(refresh_token)
        if new_token:
            headers["Authorization"] = f"Bearer {new_token}"
            response = method_func(url, headers=headers, json=json_data)

    return response