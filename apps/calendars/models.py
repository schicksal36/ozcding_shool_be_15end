"""
일정 및 시험 관련 모델
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Event(models.Model):
    """
    일정 모델
    
    사용자별 일정을 저장하는 모델
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events',
        help_text="일정 소유자"
    )
    title = models.CharField(max_length=200, help_text="일정 제목")
    description = models.TextField(blank=True, help_text="일정 설명")
    start_at = models.DateTimeField(help_text="시작 시간")
    end_at = models.DateTimeField(help_text="종료 시간")
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 시간")
    
    class Meta:
        verbose_name = '일정'
        verbose_name_plural = '일정들'
        ordering = ['start_at']
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"


class RepeatEvent(models.Model):
    """
    반복 일정 모델
    
    RRULE 규칙을 사용하여 반복되는 일정을 저장
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='repeat_events',
        help_text="반복 일정 소유자"
    )
    title = models.CharField(max_length=200, help_text="반복 일정 제목")
    description = models.TextField(blank=True, help_text="반복 일정 설명")
    start_at = models.DateTimeField(help_text="시작 시간")
    end_at = models.DateTimeField(help_text="종료 시간")
    rule = models.CharField(max_length=500, help_text="RRULE 반복 규칙 (예: FREQ=DAILY;INTERVAL=1)")
    until = models.DateField(help_text="반복 종료일")
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 시간")
    
    class Meta:
        verbose_name = '반복 일정'
        verbose_name_plural = '반복 일정들'
        ordering = ['start_at']
    
    def __str__(self):
        return f"{self.title} (반복) ({self.user.username})"


class Exam(models.Model):
    """
    시험 모델
    
    사용자의 시험 일정 및 점수를 저장
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exams',
        help_text="시험 소유자"
    )
    subject = models.CharField(max_length=100, help_text="과목명")
    exam_date = models.DateField(help_text="시험 날짜")
    score = models.IntegerField(null=True, blank=True, help_text="점수 (시험 전에는 None)")
    max_score = models.IntegerField(help_text="만점")
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 시간")
    
    class Meta:
        verbose_name = '시험'
        verbose_name_plural = '시험들'
        ordering = ['exam_date']
    
    def __str__(self):
        return f"{self.subject} - {self.exam_date} ({self.user.username})"
    
    @property
    def is_upcoming(self):
        """다가오는 시험인지 확인"""
        return self.exam_date >= timezone.now().date() and self.score is None
