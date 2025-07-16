from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework import generics
from account.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class DashboardView(APIView):
      permission_classes = []
      def get(self, request, *args, **kwargs):
        data = {}

        groups = Group.objects.all().prefetch_related('user_set')

        for group in groups:
            data[group.name] = group.user_set.count()
        print(data)

        return Response(data)

