import requests
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that require authentication
        self.protected_paths = ['/dashboard/']  # Add yours here

    def __call__(self, request):
        # Only check for protected paths
        if any(request.path.startswith(p) for p in self.protected_paths):
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')

            if not access_token:
                # messages.warning(request, "Session expired. Please login again.")
                return redirect('login') 
                return self.get_response(request)

            # Check if token is valid by hitting a protected endpoint
            check_url = settings.API_BASE_URL + 'api/enquiry/'
            refresh_url = settings.API_BASE_URL + 'api/token/refresh/'
            headers = {'Authorization': f'Bearer {access_token}'}

            response = requests.get(check_url, headers=headers)

            if response.status_code == 401:
                # Attempt to refresh
                refresh_response = requests.post(refresh_url, json={'refresh': refresh_token})
                if refresh_response.status_code == 200:
                    new_token = refresh_response.json().get('access')
                    # Replace token in request object (useful for view decorators or other logic)
                    request._new_access_token = new_token
                    # Note: Django middleware can't modify response cookies directly at this point
                else:
                    return HttpResponse("Unauthorized - Token expired and refresh failed", status=401)

        # Proceed to view
        response = self.get_response(request)

        # Optional: set new token in response cookie if refreshed
        if hasattr(request, '_new_access_token'):
            response.set_cookie(
                'access_token',
                request._new_access_token,
                max_age=3600,
                path='/'
            )

        return response
