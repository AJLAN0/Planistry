from django.urls import path
from . import views

app_name = 'academic'

urlpatterns = [
    # Semester URLs
    path('semesters/', views.SemesterListCreateView.as_view(), name='semester-list'),
    path('semesters/<int:pk>/', views.SemesterDetailView.as_view(), name='semester-detail'),
    path('semesters/<int:pk>/active/', views.SemesterActiveView.as_view(), name='semester-active'),
    path('semesters/<int:pk>/not-active/', views.SemesterNotActiveView.as_view(), name='semester-not-active'),
    
    # Course URLs
    path('courses/', views.CourseListCreateView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/schedule/', views.CourseScheduleView.as_view(), name='course-schedule'),
    
    # Assignment URLs
    path('assignments/', views.AssignmentListCreateView.as_view(), name='assignment-list'),
    path('assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignments/<int:pk>/submit/', views.AssignmentSubmitView.as_view(), name='assignment-submit'),
    path('courses/<int:course_pk>/assignments/', views.CourseAssignmentListView.as_view(), name='course-assignments'),
    path('assignments/upcoming/', views.UpcomingAssignmentsView.as_view(), name='upcoming-assignments'),
] 