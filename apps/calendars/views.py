"""
일정 및 시험 관련 API 뷰

SOLID 원칙:
- Single Responsibility: HTTP 요청/응답 처리만 담당
- Dependency Inversion: 서비스 레이어에 의존
"""
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Event, RepeatEvent, Exam
from .services import EventService, RepeatEventService, ExamService
from .serializers import (
    CalendarSerializer,
    RepeatCalendarSerializer,
    ExamSerializer,
)


@extend_schema(
    tags=['일정'],
    summary='일정 생성',
    description='학습 또는 개인 일정을 생성합니다'
)
class CalendarCreateView(generics.CreateAPIView):
    """일정 생성 API (설계서 기준: CalendarSerializer 사용)"""
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarSerializer
    
    def perform_create(self, serializer):
        """일정 생성 시 서비스 레이어 사용"""
        event = EventService.create_event(
            user=self.request.user,
            validated_data=serializer.validated_data
        )
        serializer.instance = event


@extend_schema(
    tags=['일정'],
    summary='일정 목록 조회',
    description='전체 일정을 조회합니다'
)
class CalendarListView(generics.ListAPIView):
    """일정 목록 조회 API"""
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarSerializer
    
    def get_queryset(self):
        """서비스 레이어를 통해 일정 목록 조회"""
        return EventService.get_user_events(self.request.user)


@extend_schema(
    tags=['일정'],
    summary='일정 상세/수정/삭제',
    description='일정의 상세 정보를 조회하거나 수정/삭제합니다'
)
class CalendarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """일정 상세/수정/삭제 API"""
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarSerializer
    
    def get_queryset(self):
        """서비스 레이어를 통해 일정 조회"""
        return EventService.get_user_events(self.request.user)
    
    def perform_update(self, serializer):
        """일정 수정 시 서비스 레이어 사용"""
        event = EventService.update_event(
            user=self.request.user,
            event_id=self.kwargs['pk'],
            validated_data=serializer.validated_data
        )
        serializer.instance = event
    
    def perform_destroy(self, instance):
        """일정 삭제 시 서비스 레이어 사용"""
        EventService.delete_event(
            user=self.request.user,
            event_id=self.kwargs['pk']
        )


@extend_schema(
    tags=['반복 일정'],
    summary='반복 일정 생성',
    description='반복 규칙이 있는 일정을 생성합니다'
)
class RepeatCalendarCreateView(generics.CreateAPIView):
    """반복 일정 생성 API (설계서 기준: CreateAPIView)"""
    permission_classes = [IsAuthenticated]
    serializer_class = RepeatCalendarSerializer
    
    def perform_create(self, serializer):
        """반복 일정 생성 시 서비스 레이어 사용"""
        event = RepeatEventService.create_repeat_event(
            user=self.request.user,
            validated_data=serializer.validated_data
        )
        serializer.instance = event


@extend_schema(
    tags=['반복 일정'],
    summary='반복 일정 상세/수정/삭제',
    description='반복 일정의 상세 정보를 조회하거나 수정/삭제합니다'
)
class RepeatCalendarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """반복 일정 상세/수정/삭제 API (설계서 기준: RetrieveUpdateDestroyAPIView)"""
    permission_classes = [IsAuthenticated]
    serializer_class = RepeatCalendarSerializer
    
    def get_queryset(self):
        """서비스 레이어를 통해 반복 일정 조회"""
        return RepeatEvent.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        """반복 일정 수정 시 서비스 레이어 사용"""
        event = RepeatEventService.update_repeat_event(
            user=self.request.user,
            event_id=self.kwargs['pk'],
            validated_data=serializer.validated_data
        )
        serializer.instance = event
    
    def perform_destroy(self, instance):
        """반복 일정 삭제 시 서비스 레이어 사용"""
        RepeatEventService.delete_repeat_event(
            user=self.request.user,
            event_id=self.kwargs['pk']
        )


@extend_schema(
    tags=['시험'],
    summary='시험 관리',
    description='시험 또는 모의고사 일정을 생성, 조회, 수정, 삭제합니다'
)
class ExamView(viewsets.ModelViewSet):
    """시험 ViewSet (설계서 기준: ExamView, ModelViewSet)"""
    permission_classes = [IsAuthenticated]
    serializer_class = ExamSerializer
    
    def get_queryset(self):
        """서비스 레이어를 통해 시험 목록 조회"""
        return ExamService.get_user_exams(self.request.user)
    
    def perform_create(self, serializer):
        """시험 생성 시 서비스 레이어 사용"""
        exam = ExamService.create_exam(
            user=self.request.user,
            validated_data=serializer.validated_data
        )
        serializer.instance = exam
    
    def perform_update(self, serializer):
        """시험 수정 시 서비스 레이어 사용"""
        exam = ExamService.update_exam(
            user=self.request.user,
            exam_id=self.kwargs['pk'],
            validated_data=serializer.validated_data
        )
        serializer.instance = exam
    
    def perform_destroy(self, instance):
        """시험 삭제 시 서비스 레이어 사용"""
        ExamService.delete_exam(
            user=self.request.user,
            exam_id=self.kwargs['pk']
        )


@extend_schema(
    tags=['시험'],
    summary='다가오는 시험 조회',
    description='시험일이 가까운 시험 목록을 조회합니다'
)
class UpcomingExamView(generics.ListAPIView):
    """다가오는 시험 목록 조회 API (설계서 기준)"""
    permission_classes = [IsAuthenticated]
    serializer_class = ExamSerializer
    
    def get_queryset(self):
        """오늘 이후의 시험 중 점수가 없는 시험만 조회"""
        from django.utils import timezone
        today = timezone.now().date()
        return Exam.objects.filter(
            user=self.request.user,
            exam_date__gte=today,
            score__isnull=True
        ).order_by('exam_date')
