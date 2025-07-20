from django.urls import path

from .views import PreAssesmentListCreateView

urlpatterns = [
    path("", PreAssesmentListCreateView.as_view(), name="pre-assessment-list-create"),
]