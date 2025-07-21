from django.shortcuts import render
import traceback
from account.permissions import IsAdmin, IsCounselor
from rest_framework.response import Response 
from .models import CounselingSession, Counselor, CounselorFeedback
from .serializers import CounselingSessionCreateSerializer, CounselingSessionSerializer, CounselorFeedbackSerializer, CounselorSerializer
# Create your views here.
from rest_framework import generics, permissions, filters
from .models import Counselor
from .serializers import CounselorSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

class CounselorListCreateView(generics.CreateAPIView):
    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [IsAdmin]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request  # 👈 This is important
        return context
    def create(self, request, *args, **kwargs):
        print("⚠️ Hit view.create()")
        data = request.data.copy()
        files = request.FILES

        user_data = {
        "email": data.get("user[email]"),
        "first_name": data.get("user[first_name]"),
        "last_name": data.get("user[last_name]"),
        "phone": data.get("user[phone]"),
        "country": data.get("user[country]"),
        "password": data.get("user[password]"),
        "state": data.get("user[state]"),
        "city": data.get("user[city]"),
        "motivation_reason": data.get("user[motivation_reason]"),
        "hope_reason": data.get("user[hope_reason]"),
        
    }
        data["user"] = user_data
        
        # ✅ Parse background[]
        background = []
        i = 0
        while f"background[{i}][certification_qualification]" in files:
            background.append({
                "certification_qualification": files.get(f"background[{i}][certification_qualification]"),
                "counselling_specialization": data.get(f"background[{i}][counselling_specialization]"),
                "relevant_exp": data.get(f"background[{i}][relevant_exp]"),
            })
            i += 1

        # ✅ Final payload passed to serializer
        payload = {
            "user": user_data,
            "current_occupation": data.get("current_occupation"),
            "experience_in_years": data.get("experience_in_years"),
            "is_terms_agreed": data.get("is_terms_agreed", False),
            "background": background
        }


        serializer = self.get_serializer(data=payload, context={"request": request})
        if not serializer.is_valid():
            print("❌ Errors:", serializer.errors)
            raise ValidationError(serializer.errors)

        self.perform_create(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Now request is available in serializer.context['request']
        serializer.save()
class CounselorListView(generics.ListAPIView):
    queryset = Counselor.objects.all().order_by('-id')
    serializer_class = CounselorSerializer
    permission_classes = [permissions.IsAdminUser] # Allow public access to the list of students
    filterset_fields = ['user__state', 'user__city', 'user__created_at', 'user__country', "is_approved"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['user__city', 'user__state', 'user__created_at', 'user__phone', 'user__email', 'user__first_name', 'user__last_name', 'user__country', "is_approved"]


class CounselingSessionCreateView(generics.CreateAPIView):
    serializer_class = CounselingSessionSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'counselor'):  # If it's a counselor
            serializer.save(counselor=user.counselor)
        elif user.is_superuser or user.is_staff: 
            print(serializer.validated_data)  # If it's admin
            if not serializer.validated_data.get('counselor'):
                raise ValidationError("Admin must provide a counselor.")
            serializer.save()
        else:
            raise ValidationError("User must be a counselor or admin.")
        
        
class CounselingSessionListView(generics.ListAPIView):
    serializer_class = CounselingSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        counselor = self.request.user.counselor if hasattr(self.request.user, 'counselor') else None
        print(f"Counselor: {counselor}")
        if counselor:
            return counselor.sessions.all()
        return CounselingSession.objects.none()  # Return an empty queryset if the user is not a counselor
class CounselingSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CounselingSession.objects.all()
    serializer_class = CounselingSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]  # Allow public access to retrieve sessions
    
class CounselorFeedbackCreateView(generics.CreateAPIView):
    serializer_class = CounselorFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        session_id = self.kwargs.get('session_id')
        try:
            session = CounselingSession.objects.get(id=session_id)
        except CounselingSession.DoesNotExist:
            raise ValidationError("Counseling session does not exist.")
        
        counselor = self.request.user.counselor if hasattr(self.request.user, 'counselor') else None
        if not counselor:
            raise ValidationError("This user is not registered as a counselor.")
        
        serializer.save(session=session, counselor=counselor)
class CounselorFeedbackRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CounselorFeedback.objects.all()
    serializer_class = CounselorFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]  # Allow public access to retrieve feedback