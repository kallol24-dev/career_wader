
# from django.contrib import admin
# from django.urls import path
# from rest_framework_simplejwt.views import TokenVerifyView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
# ]

from django.urls import path, include # type: ignore
from django.conf import settings
from django.conf.urls.static import static
# from account.views import UserListView, StudentRegisterView, CounselorRegisterView, StudentListView, CounselorListView
from account import views
from django.contrib import admin # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore

from rest_framework import permissions # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore
from rest_framework.permissions import IsAdminUser # type: ignore

schema_view = get_schema_view(
   openapi.Info(
      title="Career Wader API",
      default_version='v1',
      description="API documentation for Career Wader platform",
      terms_of_service="https://www.careerwader.in/terms/",
      contact=openapi.Contact(email="support@careerwader.in"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[],
)


router = DefaultRouter()

# router.register(r"counselor", views.CounselorViewSet, basename="counselor")






urlpatterns = [
    

    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('api/franchise/', include('franchaise.urls')),
    path('api/students/', include('student.urls')),
    path("api/", include(router.urls)),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/careertest/', include('career_test.urls')),
    path('api/counselors/', include('counselor.urls')),
    path('api/services/', include('service.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/checkout/', include('checkout.urls')),
    path('api/pre-assesment/', include('preassesment.urls')),
    path('api/placement-enquiry/', include('placementEnquiry.urls')),
    path('captcha/', include('captcha.urls')),
    path('api/captcha/', include('djangoCaptcha.urls')),

    # Swagger API Documentation
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)