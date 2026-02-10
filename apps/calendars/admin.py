"""
일정 및 시험 관리자 설정
"""
from django.contrib import admin
from .models import Event, RepeatEvent, Exam


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'start_at', 'end_at', 'created_at')
    list_filter = ('created_at', 'start_at')
    search_fields = ('title', 'user__username')
    date_hierarchy = 'start_at'


@admin.register(RepeatEvent)
class RepeatEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'start_at', 'end_at', 'until', 'created_at')
    list_filter = ('created_at', 'start_at')
    search_fields = ('title', 'user__username')
    date_hierarchy = 'start_at'


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'exam_date', 'score', 'max_score', 'created_at')
    list_filter = ('exam_date', 'created_at')
    search_fields = ('subject', 'user__username')
    date_hierarchy = 'exam_date'
