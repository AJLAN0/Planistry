from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification_list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification_detail'),
    path('<int:pk>/mark-read/', views.NotificationMarkReadView.as_view(), name='notification_mark_read'),
    path('mark-all-read/', views.NotificationMarkAllReadView.as_view(), name='notification_mark_all_read'),
    path('clear/', views.NotificationClearView.as_view(), name='notification_clear'),
] 