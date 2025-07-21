from django.http import HttpResponse #type: ignore
import requests
from django.shortcuts import render #type: ignore
from django.conf import settings #type: ignore


def submitOtp(request):
    if request.method == 'POST':
        try:
            # Get each digit from POST and concatenate
            email = request.POST.get('email', '').strip()
            otp = ''.join([
                request.POST.get('digit-1', ''),
                request.POST.get('digit-2', ''),
                request.POST.get('digit-3', ''),
                request.POST.get('digit-4', ''),
                request.POST.get('digit-5', ''),
                request.POST.get('digit-6', '')
            ])
            
            payload = {
                'email': email,
                'otp': otp
            }

            # Send POST request to external API
            response = requests.post(settings.API_BASE_URL + 'api/verifyemail/', json=payload)

            if response.status_code == 200:
                return render(request, 'dashboard/pages/dashboard.html')
            else:
                return render(
                    request,
                    'dashboard/pages/auth/verification-page.html',
                    {
                        'email': email,
                        'otp_error': True,  # This flag will be used to trigger SweetAlert
                        'otp_error_message': 'Invalid OTP. Please try again.'  # Optional custom message
                    }
                )
           
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
    else:
        return HttpResponse('Invalid request method', status=405)
    
    
def resendOtp(request):
    if request.method == 'POST':
        try:
            # Get each digit from POST and concatenate
            email = request.POST.get('email', '').strip()            
            payload = {
                'email': email,
            }

            # Send POST request to external API
            response = requests.post(settings.API_BASE_URL +'api/resendotp', json=payload)

            if response.status_code == 200:
               return render(request, 'dashboard/pages/auth/auth-login.html')
            else:
                return render(request, 'dashboard/pages/auth/verification-page.html',{'email':email,'message':'Invalid OTP'})
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
    else:
        return HttpResponse('Invalid request method', status=405)
