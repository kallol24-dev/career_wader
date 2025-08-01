from django.views.decorators.csrf import csrf_exempt #type: ignore
from django.shortcuts import render #type: ignore
from django.http import HttpResponse, JsonResponse #type: ignore
import requests
import json
from django.conf import settings #type: ignore
from urllib.parse import urlencode
from .newAccessToken import refreshNewtoken, fetch_api_data_with_new_token, getStates

def shortEnquiryDisplay(request):
    # access_token = request.COOKIES.get('access_token')
    # refresh_token = request.COOKIES.get('refresh_token')

    # if not access_token:
    #     return HttpResponse("Access token not found", status=401)

    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('perPage', 10))
    search_query = request.GET.get('search', '').strip().lower()
    state = request.GET.get('state')
    
    
    query_params = {'page': page, 'page_size': per_page, 'search': search_query }
    
    if state != None:
        query_params['state'] = state
    url = f"{settings.API_BASE_URL}api/enquiry/?{urlencode(query_params)}"
    context = {} 
    django_response = render(request, 'dashboard/pages/enquiry/shortEnquiryDisplay.html', context)
    response, _ = fetch_api_data_with_new_token(request, url, response_override=django_response)
    
    # headers = {'Authorization': f'Bearer {access_token}'}
    # refresh_url = settings.API_BACKEND_URL + 'api/token/refresh/'

    # try:
    #     response = requests.get(url, headers=headers)
    #     if response.status_code == 401:
    #         response = refreshNewtoken(refresh_token,url)
    #     response.raise_for_status()
    #     data = response.json()

    #     enquiries = data['results']
    #     total_count = data['count']
    # except Exception as e:
    #     return HttpResponse(f"An error occurred: {e}", status=500)
    
    if not response:
        return HttpResponse("Unauthorized - Token refresh failed", status=401)
    if not response.ok:
        return HttpResponse(f"API Error: {response.status_code}", status=response.status_code)
    
    data = response.json()
    enquiries = data['results']
    total_count = data['count']
    total_pages = (total_count + per_page - 1) // per_page
    
    preserved_params = request.GET.copy()
    if 'page' in preserved_params:
        del preserved_params['page']
    base_url = '?' + urlencode(preserved_params)
    page_range = range(1, total_pages + 1)
    start_index = (page - 1) * per_page + 1
    end_index = min(page * per_page, total_count)
    context ={
            'enquiries': enquiries,
            'per_page': per_page,
            'page': page,
            "states":getStates(),
            "start_index":start_index,
            "end_index":end_index,
            'total_count':total_count,
            'total_pages': total_pages,
            'page_range':page_range,
            'search_query': search_query,
            'base_url': base_url
        }
    if _:
        context['access_token'] = _
    return render(
        request,
        'dashboard/pages/enquiry/shortEnquiryDisplay.html',
        context
    )
    
@csrf_exempt
def mark_as_read(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)

    try:
        data = json.loads(request.body)

        enquiry_id = int(data.get("id"))
        
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return HttpResponse("Access token not found", status=401)

        url = f"{settings.API_BASE_URL}api/enquiries/{enquiry_id}/mark-read/"
        headers = {"Authorization": f"Bearer {access_token}"}
        refresh_url = settings.API_BASE_URL + "api/token/refresh/"
        response = requests.patch(url, headers=headers)
        if response.status_code == 401:
            response = refreshNewtoken(refresh_token,url)
        response.raise_for_status()
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
