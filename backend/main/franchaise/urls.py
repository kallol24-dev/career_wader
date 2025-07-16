from django.urls import path
from franchaise import views

urlpatterns = [
     path("register/", views.FranchiseRegisterView.as_view(), name="franchise-register"),
     path("", views.FranchiseListView.as_view(), name="franchise-list"),
     path('shortlist-by-city/', views.ShortlistFranchisesByCityView.as_view(), name='shortlist-by-city'),
     path("action/", views.AdminFranchiseActionView.as_view(), name="admin-franchise-action"),
     path('students/onboard-by-franchise/', views.FranchiseStudentRegisterView.as_view(), name='franchise-onboard-student'),
     

]

