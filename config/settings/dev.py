#studycalender\config\settings\dev.py
# 운영 체제 관련 기능을 사용하기 위한 모듈
import os

# 기본 설정 파일에서 모든 설정을 가져옴
# noqa: F403는 linter가 wildcard import에 대한 경고를 무시하도록 하는 주석
from .base import *  # noqa: F403

# 허용된 호스트 설정
# Django가 서비스할 수 있는 호스트 이름 목록
# 개발 환경에서 사용할 수 있는 호스트들을 명시
ALLOWED_HOSTS = [
    "localhost",      # 로컬호스트 도메인명
    "127.0.0.1",      # 로컬호스트 IP 주소
    "0.0.0.0",        # 개발 서버 바인딩 때문에 들어오는 경우 대비 (모든 네트워크 인터페이스)
]

# CSRF 보호를 위한 신뢰할 수 있는 오리진 설정
# Cross-Site Request Forgery 공격을 방지하기 위해 특정 오리진에서의 요청만 허용
# 개발 서버에서 사용하는 주소들을 신뢰할 수 있는 오리진으로 등록
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",    # 로컬호스트 도메인명으로 접근하는 경우
    "http://127.0.0.1:8000",    # 로컬호스트 IP 주소로 접근하는 경우
]

# 데이터베이스 엔진 설정 (ImproperlyConfigured 에러 해결책)
# PostgreSQL 데이터베이스 연결 정보를 환경변수에서 가져옴
# Docker 환경에서 실행될 때를 고려한 설정
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",                    # PostgreSQL 데이터베이스 엔진 사용
        "NAME": os.environ.get("POSTGRES_DB"),                       # 데이터베이스 이름 (환경변수에서 가져옴)
        "USER": os.environ.get("POSTGRES_USER"),                     # 데이터베이스 사용자명 (환경변수에서 가져옴)
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),             # 데이터베이스 비밀번호 (환경변수에서 가져옴)
        "HOST": os.environ.get("DJANGO_DB_HOST", "db"),              # 데이터베이스 호스트 주소 (기본값: 'db' - 도커 서비스 이름)
        "PORT": os.environ.get("DJANGO_DB_PORT", "5432"),           # 데이터베이스 포트 번호 (기본값: PostgreSQL 기본 포트)
    }
}

# 디버그 모드 활성화
# 개발 환경에서는 True로 설정하여 상세한 에러 정보와 디버깅 도구를 사용할 수 있음
DEBUG = True
