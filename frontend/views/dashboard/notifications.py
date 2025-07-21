from django.shortcuts import render #type: ignore
from django.http import HttpResponse #type: ignore
import requests
from django.shortcuts import render #type: ignore
from django.conf import settings #type: ignore
from urllib.parse import urlencode
from .newAccessToken import refreshNewtoken, fetch_api_data_with_new_token, getStates
import math
def notifications(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('perPage', 10))
    state = request.GET.get('state')
    search_query = request.GET.get('search', '').strip().lower()
    query_params = {'page': page, 'page_size': per_page}
    if state != None:
        query_params['state'] = state
        
    url = f"{settings.API_BASE_URL}api/notifications/?{urlencode(query_params)}"
    context = {}
    django_response = render(request, 'dashboard/pages/notifications.html', context)
    response, _ = fetch_api_data_with_new_token(request, url, response_override=django_response)
    
    if not response:
        return HttpResponse("Unauthorized - Token refresh failed", status=401)
    if not response.ok:
        return HttpResponse(f"API Error: {response.status_code}", status=response.status_code)
    data = response.json()

    notifications = data['results']
    total_count = data['count']
    # if search_query:
    #     all_students = [
    #         f for f in all_students if any([
    #             search_query in (f.get('name') or '').lower(),
    #             search_query in (f.get('email') or '').lower(),
    #             search_query in (f.get('phone') or '').lower(),
    #             search_query in (f.get('city') or '').lower(),
    #             search_query in (f.get('state') or '').lower(),
    #         ])
    #     ]
    total_pages = (total_count + per_page - 1) // per_page
    preserved_params = request.GET.copy()
    if 'page' in preserved_params:
        del preserved_params['page']
    base_url = '?' + urlencode(preserved_params)
    page_range = range(1, total_pages + 1)
    start_index = (page - 1) * per_page + 1
    end_index = min(page * per_page, total_count)
    return render(
        request,
        'dashboard/pages/notifications.html',
        {
            'notifications': notifications,
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
    # try:
        
    #     role = request.COOKIES.get('role', 'Guest')
        
    #     access_token = request.COOKIES.get('access_token')
    #     refresh_token = request.COOKIES.get('refresh_token')

    #     if not access_token:
    #         return HttpResponse("Access token not found", status=401)
        
        
    #     page = int(request.GET.get("page", 1))
    #     page_size = 10  # You can adjust this as needed

    # # You need to define refresh_token and access_token properly in your context
    #     onNotifications = fetchData(
    #         f"{settings.API_BASE_URL}api/notifications/?{urlencode({'page': page, 'page_size': page_size})}",
    #         refresh_token,
    #         access_token
    #     )

    #     notifications = onNotifications.get('results', [])
    #     total_count = onNotifications.get('count', 0)
    #     total_pages = math.ceil(total_count / page_size)

    #     return render(request, 'dashboard/pages/notifications.html', {
    #         'api_base_url': settings.API_BASE_URL,
    #         'notifications': notifications,
    #         'current_page': page,
    #         'total_pages': total_pages,
    #     })
#     except Exception as e:
#         return HttpResponse(f"An error occurred {e}", status=500)
    
    
# def fetchData(url = "", refresh_token = "", access_token = ""):
    
#         if not url or not access_token or not refresh_token:
#             return
#         headers = {'Authorization': f'Bearer {access_token}'}
#         try:
#             response = requests.get(url, headers=headers)
#             if response.status_code == 401:
#                 response = refreshNewtoken(refresh_token,url)
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {e}", status=500)