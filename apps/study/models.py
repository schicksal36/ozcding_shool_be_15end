"""
스터디 이벤트, 타이머, 공부 내용 관련 모델
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class StudyEvent(models.Model):
    """
    스터디 이벤트 모델
    
    사용자의 스터디 세션을 저장
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_events',
        help_text="스터디 소유자"
    )
    title = models.CharField(max_length=200, help_text="스터디 제목")
    goal = models.TextField(help_text="학습 목표")
    start_at = models.DateTimeField(help_text="시작 시간")
    end_at = models.DateTimeField(help_text="종료 시간")
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 시간")
    
    class Meta:
        verbose_name = '스터디 이벤트'
        verbose_name_plural = '스터디 이벤트들'
        ordering = ['-start_at']
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"


class StudyTimer(models.Model):
    """
    스터디 타이머 모델
    
    스터디 세션의 타이머 정보를 저장
    """
    study_event = models.ForeignKey(
        StudyEvent,
        on_delete=models.CASCADE,
        related_name='timers',
        help_text="연관된 스터디 이벤트"
    )
    started_at = models.DateTimeField(null=True, blank=True, help_text="타이머 시작 시간")
    ended_at = models.DateTimeField(null=True, blank=True, help_text="타이머 종료 시간")
    total_minutes = models.IntegerField(default=0, help_text="총 공부 시간 (분)")
    is_running = models.BooleanField(default=False, help_text="타이머 실행 중 여부")
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 시간")
    
    class Meta:
        verbose_name = '스터디 타이머'
        verbose_name_plural = '스터디 타이머들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"타이머 - {self.study_event.title} ({self.total_minutes}분)"


class StudyContent(models.Model):
    """
    공부 내용 모델
    
    스터디 세션에서 학습한 내용을 저장
    """
    study_event = models.ForeignKey(
        StudyEvent,
        on_delete=models.CASCADE,
        related_name='contents',
        help_text="연관된 스터디 이벤트"
    )
    content = models.TextField(help_text="공부한 내용")
    duration_minutes = models.IntegerField(help_text="공부 시간 (분)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 시간")
    
    class Meta:
        verbose_name = '공부 내용'
        verbose_name_plural = '공부 내용들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.study_event.title} - {self.content[:50]}..."
