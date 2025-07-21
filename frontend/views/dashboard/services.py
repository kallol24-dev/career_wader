from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.shortcuts import render # type: ignore
from django.http import JsonResponse, HttpResponse # type: ignore
import json
from django.conf import settings # type: ignore
from urllib.parse import urlencode
from .serviceType import getServiceTypes
from .newAccessToken import fetch_api_data_with_new_token
from .api_services import create_service_api, update_service_api, delete_service_api

def serviceList(request):
    try:
        
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('perPage', 10))
        query_params = {'page': page, 'page_size': per_page}
        
        context = {}
        django_response = render(request, 'dashboard/pages/service/services.html', context)
        data = services_list(request, query_params, response_override=django_response)
        
        services = data['results']
        total_count = data['count']
        total_pages = (total_count + per_page - 1) // per_page
        preserved_params = request.GET.copy()
        if 'page' in preserved_params:
            del preserved_params['page']
        base_url = '?' + urlencode(preserved_params)
        page_range = range(1, total_pages + 1)
        start_index = (page - 1) * per_page + 1
        end_index = min(page * per_page, total_count)
        serviceTypes = getServiceTypes(request)
        return render(
            request,
            'dashboard/pages/service/services.html',
            {
                'services': services,
                'page': page,
                "start_index":start_index,
                "end_index":end_index,
                'serviceTypes':serviceTypes,
                'per_page': per_page,
                'total_count': total_count,
                'page_range': page_range,
                'base_url': base_url
            }
        )

    except Exception as e:
        return HttpResponse(f"Error loading services: {e}", status=500)
    
def services_list(request, query_params=None, response_override=None):
    query_string = urlencode(query_params or {})
    url = f"{settings.API_BASE_URL}api/services/?{query_string}"
    response, _ = fetch_api_data_with_new_token(request, url, response_override)

    if not response:
        raise Exception("Token refresh failed or unauthorized")

    if not response.ok:
        raise Exception(f"API Error: {response.status_code}")

    return response.json()
    
@csrf_exempt
def create_service(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)

    try:
        data = json.loads(request.body)
        response = create_service_api(data, request)
        if response.status_code in [200, 201]:
            return JsonResponse({"success": True})
        return JsonResponse({"error": response.text}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def delete_service(request):
    if request.method != "DELETE":
        return HttpResponse("Invalid request method", status=405)

    try:
        service_id = request.GET.get("id")
        if not service_id:
            return HttpResponse("Missing service ID", status=400)

        response = delete_service_api(service_id, request)
        if response.ok:
            return JsonResponse({"success": True})
        return JsonResponse({"error": response.text}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
  
@csrf_exempt
def update_service(request):
    if request.method != "PUT":
        return HttpResponse("Invalid request method", status=405)

    try:
        service_id = request.GET.get("id")
        if not service_id:
            return HttpResponse("Missing service ID", status=400)

        data = json.loads(request.body)
        response = update_service_api(service_id, data, request)
        if response.ok:
            return JsonResponse({"success": True})
        return JsonResponse({"error": response.text}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  
