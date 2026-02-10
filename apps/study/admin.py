"""
스터디 관리자 설정
"""
from django.contrib import admin
from .models import StudyEvent, StudyTimer, StudyContent


@admin.register(StudyEvent)
class StudyEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'start_at', 'end_at', 'created_at')
    list_filter = ('created_at', 'start_at')
    search_fields = ('title', 'user__username', 'goal')
    date_hierarchy = 'start_at'


@admin.register(StudyTimer)
class StudyTimerAdmin(admin.ModelAdmin):
    list_display = ('study_event', 'started_at', 'ended_at', 'total_minutes', 'is_running', 'created_at')
    list_filter = ('is_running', 'created_at')
    search_fields = ('study_event__title', 'study_event__user__username')


@admin.register(StudyContent)
class StudyContentAdmin(admin.ModelAdmin):
    list_display = ('study_event', 'content', 'duration_minutes', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'study_event__title', 'study_event__user__username')
