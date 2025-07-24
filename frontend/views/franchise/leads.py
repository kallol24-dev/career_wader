
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


def leadsDisplay(request):
    return render(request, 'dashboard/pages/franchise/leads/leads.html', {
        'title': 'Leads',})
    
    
# def createLead(request):
#     if request.method == "POST":
#         data = dict(request.POST)
#         # Optional: Convert values to strings if they're lists
#         data = {k: v[0] if isinstance(v, list) else v for k, v in data.items()}
#         return JsonResponse({"received": data})# Placeholder for lead creation logic