from django.shortcuts import render #type:ignore
from django.http import HttpResponse #type:ignore

def blogs(request):
    try:
        return render(request, 'home/pages/blogs/blogs.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)

def blog1(request):
    try:
        return render(request, 'home/pages/blogs/the-science-behind-choosing-the-right-career.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def blog2(request):
    try:
        return render(request, 'home/pages/blogs/the-yawning-hr-gap-in-indias-development-needs-and-critical-growth-sectors.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def blog3(request):
    try:
        return render(request, 'home/pages/blogs/strategic-approach-to-job-hunting.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def blog4(request):
    try:
        return render(request, 'home/pages/blogs/finding-the-best-fit.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)

def blog5(request):
    try:
        return render(request, 'home/pages/blogs/finding-the-fittest-job.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def blog6(request):
    try:
        return render(request, 'home/pages/blogs/implementing-new-career.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def blog7(request):
    try:
        return render(request, 'home/pages/blogs/perfect-resume.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)
    
def blog8(request):
    try:
        return render(request, 'home/pages/blogs/rethinking-career.html')
    except Exception as e:
        return HttpResponse(f"An error occured {e}", status = 500)