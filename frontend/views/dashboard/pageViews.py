from django.shortcuts import render #type: ignore
from django.http import HttpResponse #type: ignore
import requests
import traceback
from django.shortcuts import render #type: ignore
from django.conf import settings #type: ignore


def loginPageDisplay(request):
    try:
        return render(request, 'dashboard/pages/auth/auth-login.html',{'api_base_url': settings.API_BASE_URL})        
    except Exception as e:
        return HttpResponse(f"An error occured {e}",status = 500)
    
def registerDisplay(request,role):
    try:
        return render(request, 'dashboard/pages/auth/auth-register.html', {'role':role,'api_base_url': settings.API_BASE_URL})
    except Exception as e:
        return HttpResponse(f"An error occured {e}",status = 500)
    
def forgetPassword(request):
    try:
        return render(request, 'dashboard/pages/auth/forget-password.html', {'api_base_url': settings.API_BASE_URL})
    except Exception as e:
        return HttpResponse(f"An error occured {e}",status = 500)
    
def confirmResetPassword(request):
    try:
        return render(request, 'dashboard/pages/auth/confirm-reset-password.html', {'api_base_url': settings.API_BASE_URL})
    except Exception as e:
        return HttpResponse(f"An error occured {e}",status = 500)
    
def verifyOtp(request):
    try:
        return render(request, 'dashboard/pages/auth/verification-page.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}",status = 500)
    
