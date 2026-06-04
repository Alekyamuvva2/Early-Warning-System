from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, DashboardStatsView, PredictionView, MessageViewSet, CourseAnalyticsView, InterventionViewSet
from .auth_views import RegisterView, LoginView, ProfileView

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'interventions', InterventionViewSet, basename='intervention')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('course-analytics/', CourseAnalyticsView.as_view(), name='course-analytics'),
    path('predict/', PredictionView.as_view(), name='predict'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
