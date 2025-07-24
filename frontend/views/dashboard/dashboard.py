from django.shortcuts import render #type: ignore
from django.http import HttpResponse #type: ignore
import requests
from django.shortcuts import render #type: ignore
from django.conf import settings #type: ignore
from urllib.parse import urlencode
from .newAccessToken import refreshNewtoken

def dashboard(request):
    try:
        role = request.COOKIES.get('role', 'Guest')
        
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token:
            return HttpResponse("Access token not found", status=401)    
        
        allFranchise = getStats(
            f"{settings.API_BASE_URL}api/franchise/?{urlencode({'page': 1, 'page_size': 1})}", 
            refresh_token, 
            access_token
        )
        approvedFranchisee = getStats(
            f"{settings.API_BASE_URL}api/franchise/?{urlencode({'page': 1, 'page_size': 1, 'is_approved': True})}", 
            refresh_token, 
            access_token
        )
        onHoldFranchise = getStats(
            f"{settings.API_BASE_URL}api/franchise/?{urlencode({'page': 1, 'page_size': 1, 'is_approved': False})}", 
            refresh_token, 
            access_token
        )
        
        allStudents = getStats(
            f"{settings.API_BASE_URL}api/checkout/?{urlencode({'page': 1, 'page_size': 1})}", 
            refresh_token, 
            access_token
        )
        onboardedStudents = getStats(
            f"{settings.API_BASE_URL}api/checkout/?{urlencode({'page': 1, 'page_size': 1})}", 
            refresh_token, 
            access_token
        )
        onHoldStudents = getStats(
            f"{settings.API_BASE_URL}api/checkout/?{urlencode({'page': 1, 'page_size': 1})}", 
            refresh_token, 
            access_token
        )
        onNotifications = getStats(
            f"{settings.API_BASE_URL}api/notifications/?{urlencode({'page': 1, 'page_size': 1})}", 
            refresh_token, 
            access_token
        )
        print("onNotifications", onNotifications)
        return render(request, 'dashboard/pages/dashboard.html', {
            'role': role, 
            'api_base_url': settings.API_BASE_URL,
            'allFranchise':allFranchise,
            'approvedFranchise':approvedFranchisee,
            'onHoldFranchise':onHoldFranchise,
            'allStudents':allStudents,
            'notifications': onNotifications,
            })
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"An error occurred while fetching data: {e}", status=500)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    
    
def getStats(url = "", refresh_token = "", access_token = ""):
    
    if not url or not access_token or not refresh_token:
        return
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            response = refreshNewtoken(refresh_token,url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)