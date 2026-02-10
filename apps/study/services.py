"""
스터디 관련 비즈니스 로직 서비스 레이어

SOLID 원칙:
- Single Responsibility: 각 서비스 클래스는 하나의 책임만 가짐
- Open/Closed: 확장에는 열려있고 수정에는 닫혀있음
- Dependency Inversion: 뷰는 서비스 추상화에 의존
"""
from django.utils import timezone
from datetime import timedelta

from .models import StudyEvent, StudyTimer, StudyContent
from .exceptions import StudyException


class StudyEventService:
    """스터디 이벤트 관련 비즈니스 로직 서비스"""
    
    @staticmethod
    def create_study_event(user, validated_data):
        """
        스터디 이벤트 생성
        
        :param user: 현재 사용자
        :param validated_data: 검증된 데이터
        :return: 생성된 StudyEvent 인스턴스
        """
        validated_data['user'] = user
        return StudyEvent.objects.create(**validated_data)
    
    @staticmethod
    def get_user_study_events(user):
        """
        사용자의 스터디 이벤트 목록 조회
        
        :param user: 현재 사용자
        :return: QuerySet
        """
        return StudyEvent.objects.filter(user=user)
    
    @staticmethod
    def get_study_event_by_id(user, event_id):
        """
        특정 스터디 이벤트 조회
        
        :param user: 현재 사용자
        :param event_id: 스터디 이벤트 ID
        :return: StudyEvent 인스턴스
        :raises: StudyException
        """
        try:
            return StudyEvent.objects.get(id=event_id, user=user)
        except StudyEvent.DoesNotExist:
            from .exceptions import StudyEventNotFoundException
            raise StudyEventNotFoundException()
    
    @staticmethod
    def update_study_event(user, event_id, validated_data):
        """
        스터디 이벤트 수정
        
        :param user: 현재 사용자
        :param event_id: 스터디 이벤트 ID
        :param validated_data: 검증된 데이터
        :return: 수정된 StudyEvent 인스턴스
        """
        event = StudyEventService.get_study_event_by_id(user, event_id)
        for key, value in validated_data.items():
            setattr(event, key, value)
        event.save()
        return event
    
    @staticmethod
    def delete_study_event(user, event_id):
        """
        스터디 이벤트 삭제
        
        :param user: 현재 사용자
        :param event_id: 스터디 이벤트 ID
        :return: None
        """
        event = StudyEventService.get_study_event_by_id(user, event_id)
        event.delete()


class StudyTimerService:
    """스터디 타이머 관련 비즈니스 로직 서비스"""
    
    @staticmethod
    def start_timer(user, event_id):
        """
        타이머 시작
        
        :param user: 현재 사용자
        :param event_id: 스터디 이벤트 ID
        :return: StudyTimer 인스턴스
        :raises: StudyException
        """
        study_event = StudyEventService.get_study_event_by_id(user, event_id)
        
        # 기존 실행 중인 타이머가 있으면 종료
        StudyTimer.objects.filter(
            study_event=study_event,
            is_running=True
        ).update(
            is_running=False,
            ended_at=timezone.now()
        )
        
        # 새 타이머 생성
        timer = StudyTimer.objects.create(
            study_event=study_event,
            started_at=timezone.now(),
            is_running=True
        )
        
        return timer
    
    @staticmethod
    def stop_timer(user, event_id):
        """
        타이머 종료
        
        :param user: 현재 사용자
        :param event_id: 스터디 이벤트 ID
        :return: StudyTimer 인스턴스
        :raises: StudyException
        """
        study_event = StudyEventService.get_study_event_by_id(user, event_id)
        
        timer = StudyTimer.objects.filter(
            study_event=study_event,
            is_running=True
        ).first()
        
        if not timer:
            from .exceptions import TimerNotFoundException
            raise TimerNotFoundException()
        
        # 타이머 종료 처리
        timer.ended_at = timezone.now()
        if timer.started_at:
            duration = timer.ended_at - timer.started_at
            timer.total_minutes = int(duration.total_seconds() / 60)
        timer.is_running = False
        timer.save()
        
        return timer


class StudyContentService:
    """공부 내용 관련 비즈니스 로직 서비스"""
    
    @staticmethod
    def create_study_content(user, event_id, validated_data):
        """
        공부 내용 생성
        
        :param user: 현재 사용자
        :param event_id: 스터디 이벤트 ID
        :param validated_data: 검증된 데이터
        :return: 생성된 StudyContent 인스턴스
        :raises: StudyException
        """
        study_event = StudyEventService.get_study_event_by_id(user, event_id)
        validated_data['study_event'] = study_event
        return StudyContent.objects.create(**validated_data)
    
    @staticmethod
    def get_study_contents_by_event(user, event_id):
        """
        특정 스터디 이벤트의 공부 내용 목록 조회
        
        :param user: 현재 사용자
        :param event_id: 스터디 이벤트 ID
        :return: QuerySet
        """
        return StudyContent.objects.filter(
            study_event_id=event_id,
            study_event__user=user
        )
    
    @staticmethod
    def get_study_content_by_id(user, content_id):
        """
        특정 공부 내용 조회
        
        :param user: 현재 사용자
        :param content_id: 공부 내용 ID
        :return: StudyContent 인스턴스
        :raises: StudyException
        """
        try:
            return StudyContent.objects.get(id=content_id, study_event__user=user)
        except StudyContent.DoesNotExist:
            from .exceptions import StudyContentNotFoundException
            raise StudyContentNotFoundException()
    
    @staticmethod
    def update_study_content(user, content_id, validated_data):
        """
        공부 내용 수정
        
        :param user: 현재 사용자
        :param content_id: 공부 내용 ID
        :param validated_data: 검증된 데이터
        :return: 수정된 StudyContent 인스턴스
        """
        content = StudyContentService.get_study_content_by_id(user, content_id)
        for key, value in validated_data.items():
            setattr(content, key, value)
        content.save()
        return content
    
    @staticmethod
    def delete_study_content(user, content_id):
        """
        공부 내용 삭제
        
        :param user: 현재 사용자
        :param content_id: 공부 내용 ID
        :return: None
        """
        content = StudyContentService.get_study_content_by_id(user, content_id)
        content.delete()
