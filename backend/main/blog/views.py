from django.shortcuts import render
from .models import Blog
from rest_framework import generics
from .serializers import BlogSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class BlogCreateListView(generics.ListCreateAPIView):
    """
    View to list or create blog posts.
    """
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class BlogRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]