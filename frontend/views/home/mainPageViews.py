from django.shortcuts import render #type:ignore
from django.http import HttpResponse #type:ignore
from django.conf import settings #type:ignore

# Create your views here.
def index(request):
    try:
        return render(request, 'home/pages/index.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def about(request):
    try:
        return render(request, 'home/pages/about.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def contact(request):
    try:
      return render(request, 'home/pages/contact.html', {'api_base_url': settings.API_BASE_URL})  
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def franchise(request):
    try:
        return render(request, 'home/pages/franchise.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def counsellor(request):
    try:
        return render(request, 'home/pages/counsellor.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def franchiseLanding(request):
    try:
        return render(request, 'home/pages/franchiseLanding.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def faqFranchise(request):
    try:
        return render(request, 'home/pages/faqFranchise.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def interviewAssistance(request):
    try:
        return render(request, 'home/pages/interviewAssistance.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def careerCounsellings(request):
    try:
        return render(request, 'home/pages/career-counselling.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def resumeBuilding(request):
    try:
        return render(request, 'home/pages/resumeBuilding.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
def eduLoan(request):
    try:
        return render(request, 'home/pages/edu-loan.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def freelanceCareerCounselor(request):
    try:
        return render(request, 'home/pages/freelance-career-counselor.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
    
def testimonial(request):
    try:
        return render(request, 'home/pages/testimonial.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def studyAbroad(request):
    try:
        return render(request, 'home/pages/studyAbroad.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
    
def careerCounsellor(request):
    try:
        return render(request, 'home/pages/call-counselor.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)


def termsAndConditions(request):
    try:
        return render(request, 'home/pages/terms-and-conditions.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)


def privacyPolicy(request):
    try:
        return render(request, 'home/pages/privacy-policy.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
