from django.shortcuts import render #type: ignore
from django.http import HttpResponse #type: ignore
import requests
from django.shortcuts import render #type: ignore
from django.conf import settings #type: ignore
from urllib.parse import urlencode
from .newAccessToken import refreshNewtoken, fetch_api_data_with_new_token, getStates
import json

def counselorDisplay(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('perPage', 10))
    state = request.GET.get('state')
    search_query = request.GET.get('search', '').strip().lower()
    query_params = {'page': page, 'page_size': per_page}
    if state != None:
        query_params['state'] = state

    url = f"{settings.API_BASE_URL}api/counselors/?{urlencode(query_params)}"
    context = {} 
    django_response = render(request, 'dashboard/pages/users/studentDisplay.html', context)
    response, _ = fetch_api_data_with_new_token(request, url, response_override=django_response)

    if not response:
        return HttpResponse("Unauthorized - Token refresh failed", status=401)
    if not response.ok:
        return HttpResponse(f"API Error: {response.status_code}", status=response.status_code)
    data = response.json()
    
    all_counselors = data['results']
    print(all_counselors)
    total_count = data['count']
    if search_query:
        all_counselors = [
            f for f in all_counselors if any([
                search_query in (f.get('name') or '').lower(),
                search_query in (f.get('email') or '').lower(),
                search_query in (f.get('phone') or '').lower(),
                search_query in (f.get('city') or '').lower(),
                search_query in (f.get('state') or '').lower(),
            ])
        ]
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
        'dashboard/pages/counselor/listCounsellor.html',
        {
            'counselors': all_counselors,
            'states': getStates(),
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
    
    
    
def addCounselor(request):
    try:
        return render(request, 'dashboard/pages/counselor/addCounselor.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}",status = 500)