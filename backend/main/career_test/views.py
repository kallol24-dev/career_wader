from rest_framework import viewsets #type: ignore
from rest_framework.filters import SearchFilter, OrderingFilter #type: ignore
from django_filters.rest_framework import DjangoFilterBackend #type: ignore
from rest_framework.permissions import IsAuthenticated, AllowAny #type: ignore
from rest_framework.exceptions import PermissionDenied # type: ignore
from rest_framework.response import Response # type: ignore
from .models import Category, Question, Option
from .serializers import CategorySerializer, QuestionSerializer, OptionSerializer
from account.permissions import IsAdminOrReadOnly
from account.permissions import IsAdmin
from careertest_records.models import CareerTestRecord





class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes =[IsAuthenticated, IsAdminOrReadOnly]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('options').order_by("id")
    serializer_class = QuestionSerializer
    permission_classes =[IsAuthenticated, IsAdminOrReadOnly]
    
    def get_permissions(self):
        # GETs are allowed to anonymous if key is present (handled in get_queryset)
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        # Other methods restricted to staff users only
        return [IsAdmin()]

    def validate_access_key(self, access_key: str):
        if not CareerTestRecord.objects.filter(access_key=access_key).exists():
            raise PermissionDenied("Access denied. Invalid access key.")

    def get_queryset(self):
        user = self.request.user
        access_key = self.request.query_params.get('access_key')

        if user.is_authenticated:
            # ✅ Staff/admin can see all
            if user.is_staff:
                return Question.objects.all()
            else:
                raise PermissionDenied("Only staff can access this endpoint.")
        elif access_key:
            # ✅ Anonymous users must have valid key
            self.validate_access_key(access_key)
            return Question.objects.all()
        else:
            raise PermissionDenied("Authentication required or valid key must be provided.")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        paginate_flag = request.query_params.get('paginate', 'true').lower()
        paginate = paginate_flag != 'false'

        if paginate:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        access_key = request.query_params.get('key')
        if not request.user.is_authenticated and not access_key:
            raise PermissionDenied("Access key is required for anonymous access.")
        if access_key:
            self.validate_access_key(access_key)
        return super().retrieve(request, *args, **kwargs)
   
class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.select_related('question')
    serializer_class = OptionSerializer
    permission_classes =[IsAuthenticated, IsAdminOrReadOnly]