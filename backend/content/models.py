from django.db import models
from django.utils.translation import gettext_lazy as _
from academic.models import Course

class CourseFile(models.Model):
    """
    Represents a file uploaded for a course (syllabus, notes, etc.).
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='course_files/')
    file_type = models.CharField(max_length=50)  # e.g., 'pdf', 'docx', 'ppt'
    size = models.PositiveIntegerField(null=True, blank=True)  # Make size optional
    upload_date = models.DateTimeField(auto_now_add=True)
    
    # File categories
    FILE_CATEGORIES = [
        ('syllabus', 'Syllabus'),
        ('lecture_notes', 'Lecture Notes'),
        ('assignment', 'Assignment'),
        ('reading', 'Reading Material'),
        ('other', 'Other'),
    ]

    category = models.CharField(max_length=20, choices=FILE_CATEGORIES)
    
    is_processed = models.BooleanField(default=False)
    processed_content = models.TextField(blank=True)  # Extracted text content
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('course file')
        verbose_name_plural = _('course files')
        
    def __str__(self):
        return f"{self.title} - {self.course}"

    # Add a method to calculate file size
    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
        super().save(*args, **kwargs)

class Quiz(models.Model):
    """
    Represents a quiz generated from course materials.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    source_file = models.ForeignKey(CourseFile, on_delete=models.SET_NULL, null=True, related_name='generated_quizzes')
    
    # Quiz settings
    time_limit = models.IntegerField(null=True, blank=True, help_text='Time limit in minutes')
    passing_score = models.IntegerField(default=70, help_text='Passing score percentage')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('quiz')
        verbose_name_plural = _('quizzes')
        
    def __str__(self):
        return f"{self.course.code} - {self.title}"

class QuizQuestion(models.Model):
    """
    Represents a question in a quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    explanation = models.TextField(blank=True)
    
    # Question types
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = _('quiz question')
        verbose_name_plural = _('quiz questions')
        
    def __str__(self):
        return f"{self.quiz.title} - Question {self.id}"

class QuizAnswer(models.Model):
    """
    Represents an answer option for a quiz question.
    """
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = _('quiz answer')
        verbose_name_plural = _('quiz answers')
        
    def __str__(self):
        return f"{self.question.quiz.title} - Question {self.question.id} - Answer {self.id}"

class Flashcard(models.Model):
    """
    Represents a flashcard generated from course materials.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='flashcards')
    source_file = models.ForeignKey(CourseFile, on_delete=models.SET_NULL, null=True, related_name='generated_flashcards')
    front_content = models.TextField()
    back_content = models.TextField()
    
    # Metadata
    tags = models.JSONField(default=list)
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium'
    )
    
    # Spaced repetition data
    last_reviewed = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['next_review', 'created_at']
        verbose_name = _('flashcard')
        verbose_name_plural = _('flashcards')
        
    def __str__(self):
        return f"{self.course.code} - Flashcard {self.id}"

class StudyMaterial(models.Model):
    MATERIAL_TYPES = (
        ('lecture', 'Lecture Notes'),
        ('summary', 'Summary'),
        ('practice', 'Practice Material'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_materials')
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.course}"

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.course}"
