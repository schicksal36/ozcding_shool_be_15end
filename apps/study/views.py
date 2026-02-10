"""
스터디 관련 API 뷰

SOLID 원칙:
- Single Responsibility: HTTP 요청/응답 처리만 담당
- Dependency Inversion: 서비스 레이어에 의존
"""
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import StudyEvent, StudyContent
from .services import StudyEventService, StudyTimerService, StudyContentService
from .serializers import (
    StudySerializer,
    TimerStartSerializer,
    TimerEndSerializer,
    StudyContentSerializer,
)


@extend_schema(
    tags=['스터디'],
    summary='스터디 목록 조회/생성',
    description='사용자의 전체 스터디 일정을 조회하거나 생성합니다'
)
class StudyListCreateView(generics.ListCreateAPIView):
    """스터디 이벤트 목록 조회 및 생성 API"""
    permission_classes = [IsAuthenticated]
    serializer_class = StudySerializer
    
    def get_queryset(self):
        """서비스 레이어를 통해 스터디 이벤트 목록 조회"""
        return StudyEventService.get_user_study_events(self.request.user)
    
    def perform_create(self, serializer):
        """스터디 이벤트 생성 시 서비스 레이어 사용"""
        event = StudyEventService.create_study_event(
            user=self.request.user,
            validated_data=serializer.validated_data
        )
        serializer.instance = event


@extend_schema(
    tags=['스터디'],
    summary='스터디 상세/수정/삭제',
    description='특정 스터디 일정의 상세 정보를 조회하거나 수정/삭제합니다'
)
class StudyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """스터디 이벤트 상세/수정/삭제 API"""
    permission_classes = [IsAuthenticated]
    serializer_class = StudySerializer
    
    def get_queryset(self):
        """서비스 레이어를 통해 스터디 이벤트 조회"""
        return StudyEventService.get_user_study_events(self.request.user)
    
    def perform_update(self, serializer):
        """스터디 이벤트 수정 시 서비스 레이어 사용"""
        event = StudyEventService.update_study_event(
            user=self.request.user,
            event_id=self.kwargs['pk'],
            validated_data=serializer.validated_data
        )
        serializer.instance = event
    
    def perform_destroy(self, instance):
        """스터디 이벤트 삭제 시 서비스 레이어 사용"""
        StudyEventService.delete_study_event(
            user=self.request.user,
            event_id=self.kwargs['pk']
        )


@extend_schema(
    tags=['타이머'],
    summary='타이머 시작',
    description='스터디 일정의 공부 시간을 기록하기 위해 타이머를 시작합니다'
)
class StudyTimerStartView(APIView):
    """타이머 시작 API"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, event_id):
        """타이머 시작"""
        try:
            timer = StudyTimerService.start_timer(
                user=request.user,
                event_id=event_id
            )
            serializer = TimerStartSerializer(timer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=['타이머'],
    summary='타이머 종료',
    description='스터디 일정의 공부 시간 기록을 종료합니다'
)
class StudyTimerEndView(APIView):
    """타이머 종료 API"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, event_id):
        """타이머 종료"""
        try:
            timer = StudyTimerService.stop_timer(
                user=request.user,
                event_id=event_id
            )
            serializer = TimerEndSerializer(timer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=['공부 내용'],
    summary='공부 내용 추가/조회',
    description='스터디 일정에 공부한 내용을 추가하거나 목록을 조회합니다'
)
class StudyContentView(APIView):
    """공부 내용 추가/조회/수정/삭제 API (설계서 기준: RetrieveUpdateDestroyAPIView)"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, event_id):
        """공부 내용 추가 (POST /api/study-events/{id}/contents/)"""
        serializer = StudyContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        content = StudyContentService.create_study_content(
            user=request.user,
            event_id=event_id,
            validated_data=serializer.validated_data
        )
        
        response_serializer = StudyContentSerializer(content)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, event_id):
        """공부 내용 목록 조회 (GET /api/study-events/{id}/contents/)"""
        contents = StudyContentService.get_study_contents_by_event(
            user=request.user,
            event_id=event_id
        )
        serializer = StudyContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['공부 내용'],
    summary='공부 내용 상세/수정/삭제',
    description='등록된 공부 내용의 상세 정보를 조회하거나 수정/삭제합니다'
)
class StudyContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """공부 내용 상세/수정/삭제 API (설계서 기준: RetrieveUpdateDestroyAPIView)"""
    permission_classes = [IsAuthenticated]
    serializer_class = StudyContentSerializer
    
    def get_queryset(self):
        """서비스 레이어를 통해 공부 내용 조회"""
        return StudyContent.objects.filter(study_event__user=self.request.user)
    
    def perform_update(self, serializer):
        """공부 내용 수정 시 서비스 레이어 사용"""
        content_id = self.kwargs.get('content_id') or self.kwargs.get('pk')
        content = StudyContentService.update_study_content(
            user=self.request.user,
            content_id=content_id,
            validated_data=serializer.validated_data
        )
        serializer.instance = content
    
    def perform_destroy(self, instance):
        """공부 내용 삭제 시 서비스 레이어 사용"""
        content_id = self.kwargs.get('content_id') or self.kwargs.get('pk')
        StudyContentService.delete_study_content(
            user=self.request.user,
            content_id=content_id
        )
