"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin #type:ignore
from django.urls import path #type:ignore
from views.home import mainPageViews, enquiryViews
from views.dashboard import careertest, pageViews,usersViews,otpViews, enquiryViews as shortEnquiryViews,\
    contactFormDisplay, counselorViews, serviceType, services, dashboard, notifications
from views.franchise import myStudentEnrolments, leads
from views.home import cart, blogs
from django.urls import path, re_path #type:ignore
from django.shortcuts import redirect #type:ignore



urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    # Home Page Routes
    # path('', mainPageViews.franchiseLanding, name = 'franchiseLanding'),
    path('', mainPageViews.index, name = 'index'),
    path('contact/', mainPageViews.contact, name="contact"),
    path('franchisee/', mainPageViews.franchiseLanding, name="franchise"),
    path('about-us/', mainPageViews.about, name='about-us'),
    path('counsellor/',mainPageViews.counsellor, name='counsellor'),
    # path('franchise-landing/',mainPageViews.franchiseLanding, name = "franchiseLanding"),
    path('faq-franchise/',mainPageViews.faqFranchise, name = "faqFranchise"),
    path('interview-assistance/',mainPageViews.interviewAssistance, name = "interviewAssistance"),
    path('career-counselling/',mainPageViews.careerCounsellings, name = "careerCounselling"),
    path('resume-building/',mainPageViews.resumeBuilding, name = "resumeBuilding"),
    # path('testimonial/',mainPageViews.testimonial, name = "testimonial"),
    path('study-abroad/',mainPageViews.studyAbroad, name = "studyAbroad"),
    path('career-counsellor/',mainPageViews.careerCounsellor, name = "careerCounsellor"),
    path('education-loan/',mainPageViews.eduLoan, name = "eduLoan"),
    path('freelance-career-counselors/',mainPageViews.freelanceCareerCounselor, name = "freelanceCareerCounselor"),
    path('terms-and-conditions/',mainPageViews.termsAndConditions, name = "termsAndConditions"),
    path('privacy-policy/',mainPageViews.privacyPolicy, name = "privacyPolicy"),
    
    
    
    #enquiries
    path('enquiries/all/',enquiryViews.allEnquiries, name = 'allEnquiries'),
    path('enquiries/bangalore/',enquiryViews.enquiryBanglore, name = 'enquiryBanglore'),
    path('enquiries/mysore/',enquiryViews.enquiryMysore, name = 'enquiryMysore'),
    path('enquiries/hubli/',enquiryViews.enquiryHubli, name = 'enquiryHubli'),
    path('enquiries/mangalore/',enquiryViews.enquiryMangalore, name = 'enquiryMangalore'),
    path('enquiries/shimoga/',enquiryViews.enquiryShimoga, name = 'enquiryShimoga'),
    path('enquiries/devangere/',enquiryViews.enquiryDevangere, name = 'enquiryDevangere'),
    path('enquiries/tumkur/',enquiryViews.enquiryTumkur, name = 'enquiryTumkur'),
    path('enquiries/gulbarga/',enquiryViews.enquiryGulbarga, name = 'enquiryGulbarga'),
    path('enquiries/bidar/',enquiryViews.enquiryBidar, name = 'enquiryBidar'),
    path('enquiries/belgaum/',enquiryViews.enquiryBelgaum, name = 'enquiryBelgaum'),
    path('enquiries/vijaywada/',enquiryViews.enquiryVijaywada, name = 'enquiryVijaywada'),
    path('enquiries/vishakapatnam/',enquiryViews.enquiryVishakapatnam, name = 'enquiryVishakapatnam'),
    path('enquiries/nellore/',enquiryViews.enquiryNellore, name = 'enquiryNellore'),
    path('enquiries/kurnool/',enquiryViews.enquiryKurnool, name = 'enquiryKurnool'),
    path('enquiries/anantapur/',enquiryViews.enquiryAnantapur, name = 'enquiryAnantapur'),
    path('enquiries/eluru/',enquiryViews.enquiryEluru, name = 'enquiryEluru'),
    path('enquiries/tirupati/',enquiryViews.enquiryTirupati, name = 'enquiryTirupati'),
    path('enquiries/gwalior/',enquiryViews.enquiryGwalior, name = 'enquiryGwalior'),
    path('enquiries/indore/',enquiryViews.enquiryIndore, name = 'enquiryIndore'),
    path('enquiries/bhopal/',enquiryViews.enquiryBhopal, name = 'enquiryBhopal'),
    path('enquiries/hyderabad/',enquiryViews.enquiryHyderabad, name = 'enquiryHyderabad'),
    path('enquiries/nizamabad/',enquiryViews.enquiryNizamabad, name = 'enquiryNizamabad'),
    path('enquiries/warangal/',enquiryViews.enquiryWarangal, name = 'enquiryWarangal'),
    path('enquiries/mahabubnagar/',enquiryViews.enquiryMahabubnagar, name = 'enquiryMahabubnagar'),
    path('enquiries/coimbatore/',enquiryViews.enquiryCoimbatore, name = 'enquiryCoimbatore'),
    path('enquiries/erode/',enquiryViews.enquiryErode, name = 'enquiryErode'),
    path('enquiries/hosur/',enquiryViews.enquiryHosur, name = 'enquiryHosur'),
    path('enquiries/trichy/',enquiryViews.enquiryTrichy, name = 'enquiryTrichy'),
    path('enquiries/madurai/',enquiryViews.enquiryMadurai, name = 'enquiryMadurai'),
    path('enquiries/mumbai/',enquiryViews.enquiryMumbai, name = 'enquiryMumbai'),
    path('enquiries/pune/',enquiryViews.enquiryPune, name = 'enquiryPune'),
    path('enquiries/nagpur/',enquiryViews.enquiryNagpur, name = 'enquiryNagpur'),
    path('enquiries/nashik/',enquiryViews.enquiryNashik, name = 'enquiryNashik'),   
    path('enquiries/kolhapur/',enquiryViews.enquiryKolhapur, name = 'enquiryKolhapur'),
    path('enquiries/gurgaon/',enquiryViews.enquiryGurgaon, name = 'enquiryGurgaon'),
    path('enquiries/jaipur/',enquiryViews.enquiryJaipur, name = 'enquiryJaipur'),
    path('enquiries/udaipur/',enquiryViews.enquiryUdaipur, name = 'enquiryUdaipur'),
    path('enquiries/prayagraj/',enquiryViews.enquiryPrayagraj, name = 'enquiryPrayagraj'),
    path('enquiries/meerut/',enquiryViews.enquiryMeerut, name = 'enquiryMeerut'),
    path('enquiries/lucknow/',enquiryViews.enquiryLucknow, name = 'enquiryLucknow'),
    path('enquiries/bhubaneswar/',enquiryViews.enquiryBhubaneswar, name = 'enquiryBhubaneswar'),
    path('enquiries/delhi/',enquiryViews.enquiryDelhi, name = 'enquiryDelhi'),
    path('enquiries/kolkata/',enquiryViews.enquiryKolkata, name = 'enquiryKolkata'),
    path('enquiries/chennai/',enquiryViews.enquiryChennai, name = 'enquiryChennai'),
    path('enquiries/salem/',enquiryViews.enquirySalem, name = 'enquirySalem'),
    path('enquiries/rajahmundry/',enquiryViews.enquiryRajahmundry, name = 'enquiryRajahmundry'),
    
    # path('test/', mainPageViews.test),
    
    # Login Register Route
    path('login/', pageViews.loginPageDisplay, name = 'login'),
    path('register/<str:role>/',pageViews.registerDisplay, name = 'register'),
    path('verify-otp/',pageViews.verifyOtp, name = 'verifyOtp'),
    path('forget-password/',pageViews.forgetPassword, name = 'forgetPassword'),
    path('confirm-reset-password/',pageViews.confirmResetPassword, name = 'confirmResetPassword'),
    
    #OTP Views
    path('submit-otp/',otpViews.submitOtp, name="submitOtp"),
    path('resend-otp/',otpViews.resendOtp, name="resendOtp"),
        
    # Admin Page Routes
    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('notifications/', notifications.notifications, name='notifications'),

    # Admin Form Display Routes
    path('contact-form/', contactFormDisplay.contactFromFDetails, name = 'contactFromFDetails'),
    
    #careertest
    path('careerytest/categories/',careertest.categories, name = "careerCategories"),
    
    #counsellor
    path('counselor-display/',counselorViews.counselorDisplay, name = 'counselorDisplay'),
    # path('counselor-display/',counselorViews.Display, name = 'counselorDisplay'),
    
    #franchise
    path('short-enquiry-display/',shortEnquiryViews.shortEnquiryDisplay, name = 'shortEnquiryDisplay'),
    path("mark-enquiry-as-read/", shortEnquiryViews.mark_as_read, name="mark_enquiry_as_read"),
    path('franchise-display/',usersViews.franchiseDisplay, name = 'franchiseDisplay'),
    path('franchise-onboarded/',usersViews.franchiseOnboarded, name = 'franchiseOnboarded'),
    path('state-franchisee/',usersViews.state_franchise_display, name = 'state_franchise_display'),
    path("franchisee-approval/", usersViews.franchise_approval, name="shortlisted_franchisee"),
    
    #student
    path('student-display/',usersViews.studentDisplay, name = 'studentDisplay'),
    path('add-counselor/',counselorViews.addCounselor, name = 'addCounselor'),
    path("mark-contact-as-read/", contactFormDisplay.mark_as_read, name="mark_contact_as_read"),
    
    
    # # Franchise Form Display Routes
    # path("franchise-student-enrolments/", myStudentEnrolments.studentDisplay, name="franchiseStudentEnrolments"),
    # path("franchise-enroll-student/", myStudentEnrolments.enrollStudent, name="franchiseEnrollStudents"),
    
    path("service-types/", serviceType.serviceTypes, name="serviceTypes"),
    path("create-service-type/", serviceType.create_service_type, name="create_service_type"),
    path('delete-service-type/<int:id>/', serviceType.delete_service_type, name='delete_service_type'),
    path("service-list/", services.serviceList, name="serviceList"),
    path("create-service/", services.create_service, name="createService"),
    path("update-service/", services.update_service, name="updateService"),
    # path("delete-service-type/", services.update_service, name="updateService"),
    
    
    # Franchise Form Display Routes
    path("franchise-student-enrolments/", myStudentEnrolments.studentDisplay, name="franchiseStudentEnrolments"),
    path("franchise-enroll-student/", myStudentEnrolments.enrollStudent, name="franchiseEnrollStudents"),
    path("leads/", leads.leadsDisplay, name="leads"),
    # path("leads-create/", leads.createLead, name="create_lead"),

    #checkout
    path("cart/", cart.cart, name="cart"),
    path("add-to-cart/", cart.addToCart, name="addToCart"),
    path("checkout/", cart.checkout, name="checkout"),
    path("pre-assesment/", cart.assesment, name="assesment"),
    
    #blogs
    path("the-science-behind-choosing-the-right-career/", blogs.blog1, name="blog1"),
    path("the-yawning-hr-gap-in-indias-development-needs-and-critical-growth-sectors/", blogs.blog2, name="blog2"),
    path("strategic-approach-to-job-hunting/", blogs.blog3, name="blog3"),
    path("finding-the-best-fit/", blogs.blog4, name="blog4"),
    path("finding-the-fittest-job/", blogs.blog5, name="blog5"),
    path("implementing-new-career/", blogs.blog6, name="blog6"),
    path("perfect-resume/", blogs.blog7, name="blog7"),
    path("rethinking-career/", blogs.blog8, name="blog8"),
    path("coaching-business-industry/", blogs.blog9, name="blog9"),
    path("normative-questions/", blogs.blog10, name="blog10"),
    path("blogs/", blogs.blogs, name="blogs"),    
    
    re_path(r'^index(\.html?|\.php)?$', lambda request: redirect('', permanent=True)),
]

