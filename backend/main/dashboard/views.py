from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework import generics
from account.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
# Create your views here.

class DashboardView(APIView):
      permission_classes = []

      def get(self, request, *args, **kwargs):
        # data = {}

        # groups = Group.objects.all().prefetch_related('user_set')
        # # student_group = Group.objects.all().prefetch_related('user_set').get(name="Students")
        # # data["Students"] = student_group.user_set.count()

        # for group in groups:
        #     # data[group.name] 
        #     if group.name == "franchise":
        #       users = group.user_set.get(group_name=group.name)
              
        #   #  approved_count = users.filter(is_approved=True).count()
        #   #  not_approved_count = users.filter(is_approved=False).count()
        #   #  total_count = users.count()
            
        #   #  data[group.name] = {
        #   #       "approved": approved_count,
        #   #       "not_approved": not_approved_count,
        #   #       "total": total_count
        #   #   }
        # print(data)
        
        with connection.cursor() as cursor:
          cursor.execute("""
              WITH
                  total_franchises AS (
                    SELECT COUNT(*) AS count FROM public.franchaise_franchise
                  ),
                  total_students AS (
                    SELECT COUNT(*) AS count FROM public.student_student
                  ),
                  approved_franchises AS (
                    SELECT COUNT(*) AS count FROM public.franchaise_franchise WHERE is_approved = TRUE
                  ),
                  pending_franchises AS (
                    SELECT COUNT(*) AS count FROM public.franchaise_franchise WHERE is_approved = FALSE
                  ),
                  onboarded_students_by_franchise AS (
                  select COUNT(*) from public.student_student where franchise_id is not null
                  ),
                  students_by_approval AS (
                    SELECT
                      
                      COUNT(s.id) FILTER (WHERE f.is_approved = FALSE) AS pending_students
                    FROM public.student_student s
                    LEFT JOIN public.franchaise_franchise f ON s.franchise_id = f.id
                  )

                SELECT
                  tf.count AS total_franchises,
                  
                  af.count AS approved_franchise_count,
                  pf.count AS pending_franchise_count,
                  ts.count AS total_students,
                  fs.count AS total_onboarded_by_franchise
                FROM total_franchises tf,
                    total_students ts,
                    approved_franchises af,
                    pending_franchises pf,
                    students_by_approval sba,
                  onboarded_students_by_franchise fs;
          """)
          result = cursor.fetchall()  # ✅ Fetch inside the block
          
          data ={
            "franchise" :{
              "total" : result[0][0],
              "approved": result[0][1],
              "pending": result[0][2],
            },
            "students" : {
              "total" : result[0][3],
              "onboard_by_franchise": result[0][4]
              
            }
            
          }

        print("Approved Franchise Count:", data)  # ✅ Safe to use outside
        return Response(data)
        # return Response(data)
    