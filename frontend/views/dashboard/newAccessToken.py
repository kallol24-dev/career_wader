from django.conf import settings # type: ignore
import requests 

def refreshNewtoken(refresh_token):
    if not refresh_token:
        return None

    refresh_url = settings.API_BASE_URL + 'api/token/refresh/'
    refresh_response = requests.post(refresh_url, json={'refresh': refresh_token})

    if refresh_response.status_code == 200:
        return refresh_response.json().get('access')
    return None

def refresh_access_token(refresh_token):
    response = requests.post(f'{settings.API_BASE_URL}api/token/refresh/', data={'refresh': refresh_token})
    if response.ok:
        return response.json().get('access')
    return None

def fetch_api_data_with_new_token(request, api_url, response_override=None):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 401 and refresh_token:
        new_access_token = refresh_access_token(refresh_token)
        if new_access_token:
            headers = {'Authorization': f'Bearer {new_access_token}'}
            response = requests.get(api_url, headers=headers)

            # Set the new access token in the Django response
            if response.ok and response_override:
                response_override.set_cookie(
                    'access_token',
                    new_access_token,
                    max_age=3600,
                    httponly=True,
                    secure=True,
                    samesite='Lax'
                )
            return response, new_access_token

        return None, None

    return response, None

def fetch_api_data_with_refresh(request, api_url):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 401 and refresh_token:
        new_access_token = refreshNewtoken(refresh_token)
        if new_access_token:
            headers = {'Authorization': f'Bearer {new_access_token}'}
            response = requests.get(api_url, headers=headers)

            if response.ok:
                response.set_cookie(
                    'access_token',
                    new_access_token,
                    max_age=3600,
                    httponly=True,
                    secure=True,
                    samesite='Lax'
                )
                return response, new_access_token

        return None, None  # Refresh failed

    return response, None  # Either success or other failure

def getStates():
    return ["Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal ",
    "Dharamshala",
    "Jharkhand",
    "Karnataka",
    "Belgaum ",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Nagpur",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "Dehradun",
    "West Bengal"]
