from django.shortcuts import render #type: ignore
from django.http import HttpResponse #type: ignore
import requests
from django.shortcuts import render #type: ignore
from django.conf import settings #type: ignore
from urllib.parse import urlencode
# from .newAccessToken import refreshNewtoken
from .newAccessToken import refreshNewtoken, fetch_api_data_with_new_token, getStates

def dashboard(request):
    try:
        role = request.COOKIES.get('role', 'Guest')
        
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token:
            return HttpResponse("Access token not found", status=401)    
        
        allFranchise, _ = getStats(
            request,f"{settings.API_BASE_URL}api/franchise/?{urlencode({'page': 1, 'page_size': 1})}"
        )
        approvedFranchisee, _ = getStats(
            request,f"{settings.API_BASE_URL}api/franchise/?{urlencode({'page': 1, 'page_size': 1, 'is_approved': True})}"
        )
        onHoldFranchise, _ = getStats(
            request,f"{settings.API_BASE_URL}api/franchise/?{urlencode({'page': 1, 'page_size': 1, 'is_approved': False})}"
        )
        
        allStudents, _ = getStats(
            request,f"{settings.API_BASE_URL}api/checkout/?{urlencode({'page': 1, 'page_size': 1})}"
        )
        onboardedStudents, _ = getStats(
            request,f"{settings.API_BASE_URL}api/checkout/?{urlencode({'page': 1, 'page_size': 1})}"
        )
        onHoldStudents, _ = getStats(
            request,f"{settings.API_BASE_URL}api/checkout/?{urlencode({'page': 1, 'page_size': 1})}"
        )
        onNotifications, _ = getStats(
            request,f"{settings.API_BASE_URL}api/notifications/?{urlencode({'page': 1, 'page_size': 1})}"
        )
        context = {
            'role': role, 
            'api_base_url': settings.API_BASE_URL,
            'allFranchise':allFranchise,
            'approvedFranchise':approvedFranchisee,
            'onHoldFranchise':onHoldFranchise,
            'allStudents':allStudents,
            'notifications': onNotifications,
            }
        if _:
            context['access_token']=_
        return render(request, 'dashboard/pages/dashboard.html', context )
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"An error occurred while fetching data: {e}", status=500)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    
    
def getStats(request,url = ""):
    response, _ = fetch_api_data_with_new_token(request, url, None)

    if not response:
        raise Exception("Token refresh failed or unauthorized")

    if not response.ok:
        raise Exception(f"API Error: {response.status_code}")

    return response.json(), _
    
    # if not url or not access_token or not refresh_token:
    #     return
    # headers = {'Authorization': f'Bearer {access_token}'}
    # try:
    #     response = requests.get(url, headers=headers)
    #     if response.status_code == 401:
    #         response = refreshNewtoken(refresh_token,url)
    #     response.raise_for_status()
    #     return response.json()
    # except Exception as e:
    #     return HttpResponse(f"An error occurred: {e}", status=500)