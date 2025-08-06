from rest_framework.routers import DefaultRouter #type: ignore
from .views import CategoryViewSet, QuestionViewSet, OptionViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)

urlpatterns = router.urls