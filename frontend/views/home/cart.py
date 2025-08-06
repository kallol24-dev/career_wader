from django.views.decorators.csrf import csrf_exempt #type:ignore
from django.shortcuts import render #type:ignore
from django.http import JsonResponse, HttpResponse #type:ignore
from django.conf import settings #type:ignore
from views.dashboard.services import services_list
import requests
import json


@csrf_exempt
def addToCart(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)
    
    try:
        data = json.loads(request.body)
        service = data.get("service")
       
        
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return HttpResponse("Access token not found", status=401)

        url = f"{settings.API_BASE_URL}api/cart/add-service/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
            }
        
        payload = json.dumps({
            "service":service,
            "quantity":1,
            })
        refresh_url = settings.API_BASE_URL + "api/token/refresh/"
        response = requests.post(url, headers=headers,data=payload)
        
        if response.status_code == 401:
            refresh_response = requests.post(refresh_url, json={"refresh": refresh_token})
            if refresh_response.status_code == 200:
                access_token = refresh_response.json().get("access")
                headers["Authorization"] = f"Bearer {access_token}"
                # Re-send the original request (POST, not PATCH)
                response = requests.post(url, headers=headers, data=payload)
            else:
                return HttpResponse("Unauthorized - Failed to refresh token", status=401)

        response.raise_for_status()
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
    
def cart(request):
    try:
        cookie_value = request.COOKIES.get('setToCheckout', '')
        access_token = request.COOKIES.get('access_token', '')
        refresh_token = request.COOKIES.get('refresh_token', '')
        
        checkout = safe_int(cookie_value)
        
        service = {}
        data = services_list(request, None, None)
        
        for servi in data['results']:
            if servi['id'] == checkout:
                service['id'] = servi['id']
                service['type_name'] = servi['type_name']
                service['name'] = servi['name']
                service['sale_price'] = servi['sale_price']
                service['base_price'] = servi['base_price']
                service['description'] = [item.strip() for item in servi['description'].split('|')]
                break

        context = {
            'set_to_checkout': cookie_value,
            'access_token': access_token,
            'api_base_url': settings.API_BASE_URL,
            'service': service,
            'checkout': checkout
        }

        return render(request, 'home/pages/cart.html', context)
    
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    
# def cart(request):
#     try:
#         cookie_value = request.COOKIES.get('setToCheckout', '')
#         access_token = request.COOKIES.get('access_token', '')
#         refresh_token = request.COOKIES.get('refresh_token', '')
        
#         checkout = safe_int(cookie_value)
        
#         service = {}
#         data = services_list(request,None,None)
#         for servi in data['results']:
#             if servi.id == checkout:
#                 service.id = servi.id
#                 service.type_name = servi.type_name
#                 service.name = servi.name
#                 service.sale_price = servi.sale_price
#                 service.base_price = servi.base_price
#                 service.description = servi.description.split('|')
                


#         services = data['results']
#         context = {
#             'set_to_checkout': cookie_value,
#             'access_token': access_token,
#             'api_base_url': settings.API_BASE_URL,
#             'services':service,
#             'checkout':checkout
#         }

#         return render(request, 'home/pages/cart.html', context)
    
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {e}", status=500)
    
    
@csrf_exempt
def checkout(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)

    try:
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")
        city = data.get("city")
        state = data.get("state")
        service = data.get("service")

        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "service_id": service,
        }

        url = f"{settings.API_BASE_URL}api/checkout/"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        response.raise_for_status()

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def assesment(request):
    try:
        return render(request, 'home/pages/assesment.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
