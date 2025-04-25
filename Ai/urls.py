from django.urls import path
from . import views
from .views import (
    TranslatePDFView,
    GenerateMCQsFromPDFView,
    GenerateFlashcardsFromPDFView,
    GenerateFromCourseFileView,
)

urlpatterns = [
    path('translate/', TranslatePDFView.as_view(), name='ai-translate'),
    path('mcqs/', GenerateMCQsFromPDFView.as_view(), name='ai-mcqs'),
    path('flashcards/', GenerateFlashcardsFromPDFView.as_view(), name='ai-flashcards'),
    path('generate/', GenerateFromCourseFileView.as_view(), name='generate'),
]