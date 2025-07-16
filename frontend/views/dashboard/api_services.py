
from django.conf import settings # type: ignore
from .token_service import fetch_with_refresh 


def create_service_api(request_data, request):
    url = f"{settings.API_BASE_URL}api/services/"
    return fetch_with_refresh(
        request=request,
        method='post',
        url=url,
        json_data=request_data
    )

def update_service_api(service_id, request_data, request):
    url = f"{settings.API_BASE_URL}api/services/{service_id}update/"
    return fetch_with_refresh(
        request=request,
        method='put',
        url=url,
        json_data=request_data
    )

def delete_service_api(service_id, request):
    url = f"{settings.API_BASE_URL}api/services/{service_id}delete/"
    return fetch_with_refresh(
        request=request,
        method='delete',
        url=url
    )