from rest_framework import viewsets
from .models import Category, Question, TestType
from .serializers import CategorySerializer, QuestionSerializer, TestTypeSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [] 
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = []
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    
class TestTypeViewSet(viewsets.ModelViewSet):
    queryset = TestType.objects.all()  # Assuming TestType is a model similar to Question
    serializer_class = TestTypeSerializer  # Replace with the appropriate serializer for TestType
    permission_classes = [] 
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]# Adjust permissions as needed