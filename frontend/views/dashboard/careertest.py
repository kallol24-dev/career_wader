from django.shortcuts import render #type:ignore
from django.http import HttpResponse #type:ignore
from django.conf import settings #type:ignore
from urllib.parse import urlencode
from .newAccessToken import fetch_api_data_with_new_token

# def categories(request):
#     try:
        
#         return render(request, 'dashboard/pages/careertest/categories.html')
#     except Exception as e:
#         return HttpResponse(f"An error occured {e}", status = 500)
    
def categories(request):
    try:
        
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('perPage', 10))
        query_params = {'page': page, 'page_size': per_page}
        
        context = {}
        django_response = render(request, 'dashboard/pages/careertest/categories.html', context)
        data, _ = categories_list(request, query_params, response_override=django_response)
        
        categories = data['results']
        total_count = data['count']
        total_pages = (total_count + per_page - 1) // per_page
        preserved_params = request.GET.copy()
        if 'page' in preserved_params:
            del preserved_params['page']
        base_url = '?' + urlencode(preserved_params)
        page_range = range(1, total_pages + 1)
        start_index = (page - 1) * per_page + 1
        end_index = min(page * per_page, total_count)
        context = {
                'categories': categories,
                'page': page,
                "start_index":start_index,
                "end_index":end_index,
                'per_page': per_page,
                'total_count': total_count,
                'page_range': page_range,
                'base_url': base_url
            }
        
        if _:
            context['access_token'] = _
        return render(
            request,
            'dashboard/pages/careertest/categories.html',
            
        )

    except Exception as e:
        return HttpResponse(f"Error loading categories: {e}", status=500)
    
def categories_list(request, query_params=None, response_override=None):
    query_string = urlencode(query_params or {})
    url = f"{settings.API_BASE_URL}api/careertest/categories/?{query_string}"
    response, _ = fetch_api_data_with_new_token(request, url, response_override)
    print(response)
    if not response:
        raise Exception("Token refresh failed or unauthorized")

    if not response.ok:
        raise Exception(f"API Error: {response.status_code}")

    return response.json(), _