from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Course File URLs
    path('files/', views.CourseFileListCreateView.as_view(), name='file_list_create'),
    path('files/<int:pk>/', views.CourseFileDetailView.as_view(), name='file_detail'),
    path('files/<int:pk>/download/', views.CourseFileDownloadView.as_view(), name='file_download'),
    
    # Study Material URLs
    path('materials/', views.StudyMaterialListCreateView.as_view(), name='material_list_create'),
    path('materials/<int:pk>/', views.StudyMaterialDetailView.as_view(), name='material_detail'),
    
    # Note URLs
    path('notes/', views.NoteListCreateView.as_view(), name='note_list_create'),
    path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    
    # Course Content URLs
    path('courses/<int:course_pk>/content/', views.CourseContentListView.as_view(), name='course-content-list'),

] 