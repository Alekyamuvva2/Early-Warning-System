from rest_framework import viewsets, views, response, filters
from rest_framework.permissions import IsAuthenticated

from .models import Student
from .serializers import StudentSerializer
from django.db.models import Count, Avg, Q
from django.db import models
import joblib
import os
import pandas as pd

# Load model and encoders
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ml/student_ews_model.pkl'))
ENCODER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ml/label_encoders.pkl'))

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['=id_student', 'code_module']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Student.objects.all().order_by('-risk_probability')
        
        # Student role: can only see their own student record
        # Assuming username is the id_student
        try:
            student_id = int(user.username)
            return Student.objects.filter(id_student=student_id)
        except ValueError:
            return Student.objects.none()

class DashboardStatsView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        stats = Student.objects.aggregate(
            total_students=Count('id_student'),
            at_risk_count=Count('id_student', filter=models.Q(is_at_risk=True)),
            avg_score=Avg('avg_first_two_score'),
            avg_clicks=Avg('total_clicks')
        )
        
        if stats['total_students'] == 0:
            return response.Response({"error": "No data available"}, status=404)
        
        # Risk distribution for charts
        total = stats['total_students']
        at_risk = stats['at_risk_count']
        risk_dist = [
            {"label": "At Risk", "value": at_risk},
            {"label": "Safe", "value": total - at_risk}
        ]
        
        # Module-wise risk
        module_risk = Student.objects.values('code_module').annotate(
            total=Count('id_student'),
            at_risk=Count('id_student', filter=models.Q(is_at_risk=True))
        )

        return response.Response({
            "total_students": total,
            "at_risk_count": at_risk,
            "at_risk_percent": round((at_risk / total) * 100, 2) if total > 0 else 0,
            "avg_score": round(stats['avg_score'] or 0, 2),
            "avg_clicks": round(stats['avg_clicks'] or 0, 2),
            "risk_distribution": risk_dist,
            "module_risk": module_risk
        })


class PredictionView(views.APIView):
    def post(self, request):
        # This would be used to predict risk for new/updated data
        # For simplicity, we'll return the importance from the model
        if not os.path.exists(MODEL_PATH):
            return response.Response({"error": "Model not found"}, status=500)
            
        model = joblib.load(MODEL_PATH)
        importances = model.feature_importances_
        # ... logic to format importances
        return response.Response({"status": "Model loaded", "importance": list(importances)})

from .models import Message, Intervention
from .serializers import MessageSerializer, InterventionSerializer

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer


    def get_queryset(self):
        user = self.request.user
        qs = Message.objects.all().select_related('student')
        
        if user.is_staff:
            student_id = self.request.query_params.get('student')
            if student_id:
                qs = qs.filter(student__id_student=student_id)
            return qs
        
        # Student role: can only see their own messages
        try:
            student_id = int(user.username)
            return qs.filter(student__id_student=student_id)
        except ValueError:
            return Message.objects.none()

class InterventionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer


class CourseAnalyticsView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):

        # Aggregate by Region
        region_stats = Student.objects.values('region').annotate(
            total=Count('id_student'),
            at_risk=Count('id_student', filter=models.Q(is_at_risk=True)),
            avg_score=Avg('avg_first_two_score')
        ).order_by('-at_risk')

        # Aggregate by Module
        module_stats = Student.objects.values('code_module').annotate(
            total=Count('id_student'),
            at_risk=Count('id_student', filter=models.Q(is_at_risk=True)),
            avg_score=Avg('avg_first_two_score')
        ).order_by('-at_risk')

        # Matrix for Heat Map: Module vs Region (Avg Score)
        heatmap_data = Student.objects.values('code_module', 'region').annotate(
            avg_score=Avg('avg_first_two_score')
        ).order_by('code_module', 'region')

        return response.Response({
            'by_region': region_stats,
            'by_module': module_stats,
            'heatmap': heatmap_data
        })



