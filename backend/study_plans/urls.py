from django.urls import path
from . import views

app_name = 'study_plans'

urlpatterns = [
    # Study Plan URLs
    path('plans/', views.StudyPlanListCreateView.as_view(), name='plan_list_create'),
    path('plans/<int:pk>/', views.StudyPlanDetailView.as_view(), name='plan_detail'),
    path('plans/<int:pk>/progress/', views.StudyPlanProgressView.as_view(), name='plan_progress'),
    
    # Study Session URLs
    path('plans/<int:plan_pk>/sessions/', views.StudySessionListCreateView.as_view(), name='session_list_create'),
    path('sessions/<int:pk>/', views.StudySessionDetailView.as_view(), name='session_detail'),
    
    # Goal URLs
    path('plans/<int:plan_pk>/goals/', views.GoalListCreateView.as_view(), name='goal_list_create'),
    path('goals/<int:pk>/', views.GoalDetailView.as_view(), name='goal_detail'),
] 