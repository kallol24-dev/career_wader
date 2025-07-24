
from django.urls import path
from educationLoan import views
urlpatterns = [
    path('', views.EducationLoanListView.as_view(), name='education-loan-list'),
    path('create/', views.EducationLoanCreateView.as_view(), name='education-loan-create'),
    path('<int:pk>/', views.EducationLoanDetailView.as_view(), name='education-loan-detail'),
    path('<int:pk>/update/', views.EducationLoanUpdateView.as_view(), name='education-loan-update'),
    path('<int:pk>/delete/', views.EducationLoanDeleteView.as_view(), name='education-loan-delete')
    
] 
