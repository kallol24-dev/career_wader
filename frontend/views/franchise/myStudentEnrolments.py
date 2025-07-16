import requests
import json
from urllib.parse import urlencode
from django.views.decorators.csrf import csrf_exempt #type: ignore
from django.shortcuts import render #type: ignore
from django.http import HttpResponse, JsonResponse #type: ignore
from views.dashboard.services import services_list
from django.conf import settings #type: ignore


def studentDisplay(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')

    if not access_token:
        return HttpResponse("Access token not found", status=401)

    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('perPage', 10))
    state = request.GET.get('state')
    search_query = request.GET.get('search', '').strip().lower()
    
    query_params = {'page': page, 'page_size': per_page}
    if state != None:
        query_params['state'] = state

    url = f"{settings.API_BASE_URL}api/checkout/?{urlencode(query_params)}"
    headers = {'Authorization': f'Bearer {access_token}'}
    refresh_url = settings.API_BASE_URL + 'api/token/refresh/'
    serviceData = services_list("",access_token,refresh_token)
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            refresh_response = requests.post(refresh_url, json={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                access_token = refresh_response.json().get('access')
                headers['Authorization'] = f'Bearer {access_token}'
                response = requests.get(url, headers=headers)
            else:
                return HttpResponse("Unauthorized - Failed to refresh token", status=401)

        response.raise_for_status()
        data = response.json()
        all_students = data['results']
        total_count = data['count']
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

    # Optional frontend-side search on paginated results (useful for filtering page contents)
    if search_query:
        all_students = [
            f for f in all_students if any([
                search_query in (f.get('name') or '').lower(),
                search_query in (f.get('email') or '').lower(),
                search_query in (f.get('phone') or '').lower(),
                search_query in (f.get('city') or '').lower(),
                search_query in (f.get('state') or '').lower(),
            ])
        ]

    # Prepare pagination values
    total_pages = (total_count + per_page - 1) // per_page
    states = [
            "Andhra Pradesh",
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
            "Madhya",
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
            "West Bengal"
        ]

    # Preserve query except page
    preserved_params = request.GET.copy()
    if 'page' in preserved_params:
        del preserved_params['page']
    base_url = '?' + urlencode(preserved_params)
    page_range = range(1, total_pages + 1)
    start_index = (page - 1) * per_page + 1
    end_index = min(page * per_page, total_count)
    print(all_students)
    return render(
        request,
        'dashboard/pages/franchise/students/students.html',
        {
            'students': all_students,
            'services':serviceData['results'],
            'states': states,
            'per_page': per_page,
            'page': page,
            "start_index":start_index,
            "end_index":end_index,
            'total_count':total_count,
            'total_pages': total_pages,
            'page_range':page_range,
            'search_query': search_query,
            'base_url': base_url
        }
    )

@csrf_exempt 
def enrollStudent(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)

    
    try:
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")
            
        if not access_token:
                return HttpResponse("Access token not found", status=401)
        
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
        
        
        refresh_url = settings.API_BASE_URL + "api/token/refresh/"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=payload)
        # If token expired, try refresh
        if response.status_code == 401:
            refresh_response = requests.post(refresh_url, json={"refresh": refresh_token})
            if refresh_response.status_code == 200:
                access_token = refresh_response.json().get("access")
                headers["Authorization"] = f"Bearer {access_token}"
                response = requests.post(url, headers=headers, json=payload)
            else:
                return HttpResponse("Unauthorized - Failed to refresh token", status=401)
        response.raise_for_status()
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# import requests
# import json
# from django.conf import settings
# from urllib.parse import urlencode


# def studentDisplay(request):
#     access_token = request.COOKIES.get('access_token')
#     refresh_token = request.COOKIES.get('refresh_token')

#     if not access_token:
#         return HttpResponse("Access token not found", status=401)

#     page = int(request.GET.get('page', 1))
#     per_page = int(request.GET.get('perPage', 10))
#     state = request.GET.get('state')
#     search_query = request.GET.get('search', '').strip().lower()
    
#     query_params = {'page': page, 'page_size': per_page}
#     if state != None:
#         query_params['state'] = state

#     url = f"{settings.API_BASE_URL}api/students/?{urlencode(query_params)}"
#     headers = {'Authorization': f'Bearer {access_token}'}
#     refresh_url = settings.API_BASE_URL + 'api/token/refresh/'

#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code == 401:
#             refresh_response = requests.post(refresh_url, json={'refresh': refresh_token})
#             if refresh_response.status_code == 200:
#                 access_token = refresh_response.json().get('access')
#                 headers['Authorization'] = f'Bearer {access_token}'
#                 response = requests.get(url, headers=headers)
#             else:
#                 return HttpResponse("Unauthorized - Failed to refresh token", status=401)

#         response.raise_for_status()
#         data = response.json()
#         all_students = data['results']
#         total_count = data['count']
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {e}", status=500)

#     # Optional frontend-side search on paginated results (useful for filtering page contents)
#     if search_query:
#         all_students = [
#             f for f in all_students if any([
#                 search_query in (f['user'].get('first_name') or '').lower(),
#                 search_query in (f['user'].get('last_name') or '').lower(),
#                 search_query in (f['user'].get('email') or '').lower(),
#                 search_query in (f['user'].get('phone') or '').lower(),
#                 search_query in (f['user'].get('city') or '').lower(),
#                 search_query in (f['user'].get('state') or '').lower(),
#             ])
#         ]

#     # Prepare pagination values
#     total_pages = (total_count + per_page - 1) // per_page
#     states = [
#             "Andhra Pradesh",
#             "Arunachal Pradesh",
#             "Assam",
#             "Bihar",
#             "Chhattisgarh",
#             "Goa",
#             "Gujarat",
#             "Haryana",
#             "Himachal ",
#             "Dharamshala",
#             "Jharkhand",
#             "Karnataka",
#             "Belgaum ",
#             "Kerala",
#             "Madhya",
#             "Maharashtra",
#             "Nagpur",
#             "Manipur",
#             "Meghalaya",
#             "Mizoram",
#             "Nagaland",
#             "Odisha",
#             "Punjab",
#             "Rajasthan",
#             "Sikkim",
#             "Tamil Nadu",
#             "Telangana",
#             "Tripura",
#             "Uttar Pradesh",
#             "Uttarakhand",
#             "Dehradun",
#             "West Bengal"
#         ]

#     # Preserve query except page
#     preserved_params = request.GET.copy()
#     if 'page' in preserved_params:
#         del preserved_params['page']
#     base_url = '?' + urlencode(preserved_params)
#     page_range = range(1, total_pages + 1)
#     start_index = (page - 1) * per_page + 1
#     end_index = min(page * per_page, total_count)
#     return render(
#         request,
#         'dashboard/pages/franchise/students/students.html',
#         {
#             'students': all_students,
#             'states': states,
#             'per_page': per_page,
#             'page': page,
#             "start_index":start_index,
#             "end_index":end_index,
#             'total_count':total_count,
#             'total_pages': total_pages,
#             'page_range':page_range,
#             'search_query': search_query,
#             'base_url': base_url
#         }
#     )

# @csrf_exempt 
# def enrollStudent(request):
#     if request.method != "POST":
#         return HttpResponse("Invalid request method", status=405)
#     try:
#         data = json.loads(request.body)
#         first_name = data.get("first_name") 
#         last_name = data.get("last_name") 
#         email = data.get("email") 
#         phone = data.get("phone") 
#         country = data.get("country") 
#         state = data.get("state") 
#         city = data.get("city") 

#         access_token = request.COOKIES.get("access_token")
#         refresh_token = request.COOKIES.get("refresh_token")

#         if not access_token:
#             return HttpResponse("Access token not found", status=401)

#         # API URLs
#         url = f"{settings.API_BASE_URL}api/franchise/students/onboard-by-franchise/"
#         refresh_url = settings.API_BASE_URL + "api/token/refresh/"
#         headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
#         payload = json.dumps({
#             "user":{
#             "first_name": first_name,
#             "last_name": last_name,
#             "email": email,
#             "phone": phone,
#             "country": country,
#             "state": state,
#             "city": city,
#             "password": "123456",
#             }})
        
#         # First attempt
#         response = requests.post(url, headers=headers, data=payload)
#         print(response._content)
#         # If token expired, try refresh
#         if response.status_code == 401:
#             refresh_response = requests.post(refresh_url, json={"refresh": refresh_token})
#             if refresh_response.status_code == 200:
#                 access_token = refresh_response.json().get("access")
#                 headers["Authorization"] = f"Bearer {access_token}"
#                 response = requests.patch(url, headers=headers, data=payload)
#             else:
#                 return HttpResponse("Unauthorized - Failed to refresh token", status=401)

#         response.raise_for_status()
#         return JsonResponse({"success": True})

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)