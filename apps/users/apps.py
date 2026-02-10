"""
Django 앱 설정 모듈

역할:
- users 앱의 설정 및 초기화
- 앱이 로드될 때 실행할 코드 정의

동작 원리:
1. Django가 INSTALLED_APPS에서 'users.apps.UsersConfig'를 찾음
2. UsersConfig 클래스를 로드
3. ready() 메서드가 있으면 실행 (현재는 없음)

사용 목적:
- 앱 초기화 코드 실행
- 시그널 등록
- 설정 커스터마이징
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Users 앱 설정 클래스
    
    역할:
    - users 앱의 메타데이터 정의
    - 앱 이름 지정
    
    name 속성:
    - 앱의 Python 경로 (INSTALLED_APPS에 등록할 때 사용)
    - 'users'로 설정되어 있으면 users 앱을 의미
    
    ready() 메서드 (현재 미사용):
    - 앱이 완전히 로드된 후 실행되는 메서드
    - 시그널 등록, 초기화 작업 등에 사용
    - 예: def ready(self): signal.connect(...)
    """
    name = 'apps.users'  # 앱의 Python 경로 (INSTALLED_APPS와 일치해야 함)
