"""
일정 및 시험 관련 커스텀 예외 클래스

SOLID 원칙:
- Single Responsibility: 예외 처리만 담당
- Open/Closed: 새로운 예외 타입 추가 가능
"""
from rest_framework import status
from rest_framework.exceptions import APIException


class CalendarException(APIException):
    """일정 관련 기본 예외 클래스"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "일정 처리 중 오류가 발생했습니다."
    default_code = "calendar_error"


class EventNotFoundException(CalendarException):
    """일정을 찾을 수 없을 때 발생하는 예외"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "일정을 찾을 수 없습니다."
    default_code = "event_not_found"


class RepeatEventNotFoundException(CalendarException):
    """반복 일정을 찾을 수 없을 때 발생하는 예외"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "반복 일정을 찾을 수 없습니다."
    default_code = "repeat_event_not_found"


class ExamNotFoundException(CalendarException):
    """시험을 찾을 수 없을 때 발생하는 예외"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "시험을 찾을 수 없습니다."
    default_code = "exam_not_found"
