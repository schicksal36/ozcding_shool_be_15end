"""
일정 및 시험 관련 비즈니스 로직 서비스 레이어

SOLID 원칙:
- Single Responsibility: 각 서비스 클래스는 하나의 책임만 가짐
- Open/Closed: 확장에는 열려있고 수정에는 닫혀있음
- Dependency Inversion: 뷰는 서비스 추상화에 의존
"""
from django.utils import timezone
from django.db import transaction

from .models import Event, RepeatEvent, Exam


class EventService:
    """일정 관련 비즈니스 로직 서비스"""
    
    @staticmethod
    def create_event(user, validated_data):
        """
        일정 생성
        
        :param user: 현재 사용자
        :param validated_data: 검증된 데이터
        :return: 생성된 Event 인스턴스
        """
        validated_data['user'] = user
        return Event.objects.create(**validated_data)
    
    @staticmethod
    def get_user_events(user):
        """
        사용자의 일정 목록 조회
        
        :param user: 현재 사용자
        :return: QuerySet
        """
        return Event.objects.filter(user=user)
    
    @staticmethod
    def get_event_by_id(user, event_id):
        """
        특정 일정 조회
        
        :param user: 현재 사용자
        :param event_id: 일정 ID
        :return: Event 인스턴스
        :raises: CalendarException
        """
        try:
            return Event.objects.get(id=event_id, user=user)
        except Event.DoesNotExist:
            from .exceptions import EventNotFoundException
            raise EventNotFoundException()
    
    @staticmethod
    def update_event(user, event_id, validated_data):
        """
        일정 수정
        
        :param user: 현재 사용자
        :param event_id: 일정 ID
        :param validated_data: 검증된 데이터
        :return: 수정된 Event 인스턴스
        """
        event = EventService.get_event_by_id(user, event_id)
        for key, value in validated_data.items():
            setattr(event, key, value)
        event.save()
        return event
    
    @staticmethod
    def delete_event(user, event_id):
        """
        일정 삭제
        
        :param user: 현재 사용자
        :param event_id: 일정 ID
        :return: None
        """
        event = EventService.get_event_by_id(user, event_id)
        event.delete()


class RepeatEventService:
    """반복 일정 관련 비즈니스 로직 서비스"""
    
    @staticmethod
    def create_repeat_event(user, validated_data):
        """
        반복 일정 생성
        
        :param user: 현재 사용자
        :param validated_data: 검증된 데이터
        :return: 생성된 RepeatEvent 인스턴스
        """
        validated_data['user'] = user
        return RepeatEvent.objects.create(**validated_data)
    
    @staticmethod
    def get_repeat_event_by_id(user, event_id):
        """
        특정 반복 일정 조회
        
        :param user: 현재 사용자
        :param event_id: 반복 일정 ID
        :return: RepeatEvent 인스턴스
        :raises: CalendarException
        """
        try:
            return RepeatEvent.objects.get(id=event_id, user=user)
        except RepeatEvent.DoesNotExist:
            from .exceptions import RepeatEventNotFoundException
            raise RepeatEventNotFoundException()
    
    @staticmethod
    def update_repeat_event(user, event_id, validated_data):
        """
        반복 일정 수정
        
        :param user: 현재 사용자
        :param event_id: 반복 일정 ID
        :param validated_data: 검증된 데이터
        :return: 수정된 RepeatEvent 인스턴스
        """
        event = RepeatEventService.get_repeat_event_by_id(user, event_id)
        for key, value in validated_data.items():
            setattr(event, key, value)
        event.save()
        return event
    
    @staticmethod
    def delete_repeat_event(user, event_id):
        """
        반복 일정 삭제
        
        :param user: 현재 사용자
        :param event_id: 반복 일정 ID
        :return: None
        """
        event = RepeatEventService.get_repeat_event_by_id(user, event_id)
        event.delete()


class ExamService:
    """시험 관련 비즈니스 로직 서비스"""
    
    @staticmethod
    def create_exam(user, validated_data):
        """
        시험 생성
        
        :param user: 현재 사용자
        :param validated_data: 검증된 데이터
        :return: 생성된 Exam 인스턴스
        """
        validated_data['user'] = user
        return Exam.objects.create(**validated_data)
    
    @staticmethod
    def get_user_exams(user):
        """
        사용자의 시험 목록 조회
        
        :param user: 현재 사용자
        :return: QuerySet
        """
        return Exam.objects.filter(user=user)
    
    @staticmethod
    def get_exam_by_id(user, exam_id):
        """
        특정 시험 조회
        
        :param user: 현재 사용자
        :param exam_id: 시험 ID
        :return: Exam 인스턴스
        :raises: CalendarException
        """
        try:
            return Exam.objects.get(id=exam_id, user=user)
        except Exam.DoesNotExist:
            from .exceptions import ExamNotFoundException
            raise ExamNotFoundException()
    
    @staticmethod
    def update_exam(user, exam_id, validated_data):
        """
        시험 수정
        
        :param user: 현재 사용자
        :param exam_id: 시험 ID
        :param validated_data: 검증된 데이터
        :return: 수정된 Exam 인스턴스
        """
        exam = ExamService.get_exam_by_id(user, exam_id)
        for key, value in validated_data.items():
            setattr(exam, key, value)
        exam.save()
        return exam
    
    @staticmethod
    def delete_exam(user, exam_id):
        """
        시험 삭제
        
        :param user: 현재 사용자
        :param exam_id: 시험 ID
        :return: None
        """
        exam = ExamService.get_exam_by_id(user, exam_id)
        exam.delete()
