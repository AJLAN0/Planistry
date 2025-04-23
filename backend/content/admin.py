from django.contrib import admin
from .models import CourseFile, StudyMaterial, Note, Quiz, QuizQuestion, QuizAnswer, Flashcard

@admin.register(CourseFile)
class CourseFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'category', 'file_type', 'created_at', 'size')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('course', 'category', 'file_type', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'material_type', 'created_at')
    list_filter = ('material_type', 'created_at')
    search_fields = ('title', 'content', 'course__name', 'course__code')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'content')
        }),
        ('Details', {
            'fields': ('material_type',)
        }),
    )

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'course__name', 'course__code')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'content')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
    )

class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 4
    fields = ('answer_text', 'is_correct', 'explanation')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text', 'question_type')
    list_filter = ('question_type', 'quiz')
    search_fields = ('question_text', 'explanation', 'quiz__title')
    ordering = ('quiz', 'id')
    inlines = [QuizAnswerInline]
    
    fieldsets = (
        (None, {
            'fields': ('quiz', 'question_text', 'question_type')
        }),
        ('Additional Info', {
            'fields': ('explanation',)
        }),
    )

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'time_limit', 'passing_score', 'created_at')
    list_filter = ('created_at', 'course')
    search_fields = ('title', 'description', 'course__name', 'course__code')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'description', 'source_file')
        }),
        ('Settings', {
            'fields': ('time_limit', 'passing_score')
        }),
    )

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('course', 'difficulty', 'review_count', 'last_reviewed', 'next_review')
    list_filter = ('difficulty', 'last_reviewed', 'next_review', 'course')
    search_fields = ('front_content', 'back_content', 'course__name', 'course__code')
    ordering = ('next_review', 'created_at')
    date_hierarchy = 'next_review'
    
    fieldsets = (
        (None, {
            'fields': ('course', 'source_file', 'front_content', 'back_content')
        }),
        ('Study Info', {
            'fields': ('difficulty', 'tags')
        }),
        ('Review Data', {
            'fields': ('last_reviewed', 'next_review', 'review_count')
        }),
    )
