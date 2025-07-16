from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CounselorListCreateView.as_view(), name='counselor-list-create'),
    path('', views.CounselorListView.as_view(), name='counselor-list'),
    
    path('<int:pk>/', views.CounselorListView.as_view(), name='counselor-List'),
    path('counseling-sessions/', views.CounselingSessionCreateView.as_view(), name='counseling-session-create'),
    path('counseling-sessions/<int:pk>/', views.CounselingSessionRetrieveUpdateDestroyView.as_view(), name='counseling-session-detail'),
    path('counseling-sessions/<int:session_id>/feedback/', views.CounselorFeedbackCreateView.as_view(), name='counselor-feedback-create'),
    path('counseling-sessions/<int:session_id>/feedback/<int:pk>/', views.CounselorFeedbackRetrieveUpdateDestroyView.as_view(), name='counselor-feedback-detail'),
]