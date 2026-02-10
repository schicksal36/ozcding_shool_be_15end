"""
스터디 관련 커스텀 예외 클래스

SOLID 원칙:
- Single Responsibility: 예외 처리만 담당
- Open/Closed: 새로운 예외 타입 추가 가능
"""
from rest_framework import status
from rest_framework.exceptions import APIException


class StudyException(APIException):
    """스터디 관련 기본 예외 클래스"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "스터디 처리 중 오류가 발생했습니다."
    default_code = "study_error"


class StudyEventNotFoundException(StudyException):
    """스터디 이벤트를 찾을 수 없을 때 발생하는 예외"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "스터디 이벤트를 찾을 수 없습니다."
    default_code = "study_event_not_found"


class TimerNotFoundException(StudyException):
    """타이머를 찾을 수 없을 때 발생하는 예외"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "실행 중인 타이머가 없습니다."
    default_code = "timer_not_found"


class StudyContentNotFoundException(StudyException):
    """공부 내용을 찾을 수 없을 때 발생하는 예외"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "공부 내용을 찾을 수 없습니다."
    default_code = "study_content_not_found"
