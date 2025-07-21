import requests
import json
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.shortcuts import render # type: ignore
from django.http import HttpResponse, JsonResponse # type: ignore
from django.conf import settings # type: ignore
from urllib.parse import urlencode
from .newAccessToken import refreshNewtoken, fetch_api_data_with_new_token, getStates
from django.template.loader import render_to_string  # type: ignore
from django.http import HttpResponse # type: ignore

def studentDisplay(request):
    
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('perPage', 10))
    state = request.GET.get('state')
    search_query = request.GET.get('search', '').strip().lower()
    query_params = {'page': page, 'page_size': per_page}
    if state != None:
        query_params['state'] = state
        
    url = f"{settings.API_BASE_URL}api/checkout/?{urlencode(query_params)}"
    context = {} 
    django_response = render(request, 'dashboard/pages/users/studentDisplay.html', context)
    response, _ = fetch_api_data_with_new_token(request, url, response_override=django_response)
    
    if not response:
        return HttpResponse("Unauthorized - Token refresh failed", status=401)
    if not response.ok:
        return HttpResponse(f"API Error: {response.status_code}", status=response.status_code)
    data = response.json()
    
    all_students = data['results']
    total_count = data['count']
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
        'dashboard/pages/users/studentDisplay.html',
        {
            'students': all_students,
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
    
def franchiseDisplay(request):
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('perPage', 10))
    state = request.GET.get('state')
    search_query = request.GET.get('search', '').strip().lower()

    query_params = {'page': page, 'page_size': per_page, "is_approved": False}
    if state:
        query_params['state'] = state

    url = f"{settings.API_BASE_URL}api/franchise/?{urlencode(query_params)}"
    context = {} 
    django_response = render(request, 'dashboard/pages/users/franchisee/franchiseDisplay.html', context)
    response, _ = fetch_api_data_with_new_token(request, url, response_override=django_response)

    if not response:
        return HttpResponse("Unauthorized - Token refresh failed", status=401)
    if not response.ok:
        return HttpResponse(f"API Error: {response.status_code}", status=response.status_code)

    data = response.json()
    all_franchises = data['results']
    total_count = data['count']

    # Search filter
    if search_query:
        all_franchises = [
            f for f in all_franchises if any([
                search_query in (f['user'].get('first_name') or '').lower(),
                search_query in (f['user'].get('last_name') or '').lower(),
                search_query in (f['user'].get('email') or '').lower(),
                search_query in (f['user'].get('phone') or '').lower(),
                search_query in (f['user'].get('city') or '').lower(),
                search_query in (f['user'].get('state') or '').lower(),
                search_query in (f['user'].get('country') or '').lower(),
            ])
        ]

    total_pages = (total_count + per_page - 1) // per_page
    preserved_params = request.GET.copy()
    preserved_params.pop('page', None)
    base_url = '?' + urlencode(preserved_params)
    page_range = range(1, total_pages + 1)
    start_index = (page - 1) * per_page + 1
    end_index = min(page * per_page, total_count)

    return render(
        request,
        'dashboard/pages/users/franchisee/franchiseDisplay.html',
        {
            'franchises': all_franchises,
            'states': getStates(),
            'per_page': per_page,
            'page': page,
            "start_index": start_index,
            "end_index": end_index,
            'total_count': total_count,
            'total_pages': total_pages,
            'page_range': page_range,
            'search_query': search_query,
            'base_url': base_url
        }
    )
    
def franchiseOnboarded(request):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return HttpResponse("Access token not found", status=401)
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('perPage', 10))
    state = request.GET.get('state')
    search_query = request.GET.get('search', '').strip().lower()
    
    query_params = {'page': page, 'page_size': per_page, 'is_approved': True}
    if state != None:
        query_params['state'] = state
    
    url = f"{settings.API_BASE_URL}api/franchise/?{urlencode(query_params)}"
    
    context = {} 
    django_response = render(request, 'dashboard/pages/users/franchisee/franchiseOnboarded.html', context)
    response, _ = fetch_api_data_with_new_token(request, url, response_override=django_response)
    
    if not response:
        return HttpResponse("Unauthorized - Token refresh failed", status=401)
    if not response.ok:
        return HttpResponse(f"API Error: {response.status_code}", status=response.status_code)
    data = response.json()
    all_franchises = data['results']
    total_count = data['count']
    
    if search_query:
        all_franchises = [
            f for f in all_franchises if any([
                search_query in (f['user'].get('first_name') or '').lower(),
                search_query in (f['user'].get('last_name') or '').lower(),
                search_query in (f['user'].get('email') or '').lower(),
                search_query in (f['user'].get('phone') or '').lower(),
                search_query in (f['user'].get('city') or '').lower(),
                search_query in (f['user'].get('state') or '').lower(),
                search_query in (f['user'].get('country') or '').lower(),
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
        'dashboard/pages/users/franchisee/franchiseOnboarded.html',
        {
            'franchises': all_franchises,
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

def state_franchise_display(request):
    states = getStates()
    state_data = []
    total_count = 0

    # Create empty dummy response to pass for cookie setting
    response = HttpResponse()

    try:
        for state in states:
            query_url = f"{settings.API_BASE_URL}api/franchise/?state={state}"
            api_response, _ = fetch_api_data_with_new_token(request, query_url, response_override=response)

            if not api_response:
                state_data.append({'state': state, 'count': 0})
                continue

            if api_response.status_code == 200:
                data = api_response.json()
                count = data.get('count', 0)
                total_count += count
                state_data.append({'state': state, 'count': count})
            else:
                state_data.append({'state': state, 'count': 0})
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

    # Render template manually and assign content to the response
    rendered_html = render_to_string(
        'dashboard/pages/users/franchisee/stateWiseFranchise.html',
        {
            'state_data': state_data,
            'total_count': total_count,
        },
        request=request
    )
    response.content = rendered_html
    return response

    
@csrf_exempt
def franchise_approval(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)

    try:
        data = json.loads(request.body)
        franchise_id = int(data.get("id"))
        is_approved = bool(data.get("is_approved"))  # Expecting true/false from frontend

        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return HttpResponse("Access token not found", status=401)

        # API URLs
        url = f"{settings.API_BASE_URL}api/franchise/approval/{franchise_id}/"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        payload = json.dumps({"is_approved": is_approved})

        # First attempt
        response = requests.patch(url, headers=headers, data=payload)

        # If token expired, try refresh
        if response.status_code == 401:
            response = refreshNewtoken(refresh_token,url)

        response.raise_for_status()
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

