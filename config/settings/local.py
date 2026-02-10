#studycalender\config\settings\local.py
"""
로컬 개발 환경 설정
- PostgreSQL 데이터베이스 사용 (로컬 PostgreSQL 설치 필요)
- Celery 비활성화 (로컬 개발 시 선택사항)
- 디버그 모드 활성화
"""

from .base import *

# 디버그 모드 설정
# 환경변수에서 DEBUG 값을 가져오고, 없으면 기본값으로 True 사용
# 로컬 개발 환경에서는 디버그 모드를 활성화하여 상세한 에러 정보를 확인할 수 있음
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# CORS (Cross-Origin Resource Sharing) 설정
# 프론트엔드와 백엔드가 다른 도메인/포트에서 실행될 때 필요한 설정

# 허용된 호스트 설정
# 로컬 개발용으로 모든 호스트 허용 (보안상 프로덕션에서는 사용하지 않음)
ALLOWED_HOSTS = ['*']  # 로컬 개발용

# CORS를 허용할 오리진(Origin) 목록
# 프론트엔드 애플리케이션이 실행되는 주소들을 명시
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",        # 로컬 프론트 개발 (Next.js 기본 포트)
    "http://127.0.0.1:3000",        # 로컬 프론트 개발 (IP 주소)
    "http://localhost:8000",        # Django 개발 서버
    "http://127.0.0.1:8000",        # Django 개발 서버 (IP 주소)
]

# CORS 요청 시 인증 정보(쿠키, 인증 헤더 등)를 포함할 수 있도록 설정
CORS_ALLOW_CREDENTIALS = True

# 허용할 HTTP 메서드
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# 허용할 HTTP 헤더
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ========== 데이터베이스 설정 (PostgreSQL 사용) ==========
# PostgreSQL 데이터베이스 연결 정보를 환경변수에서 가져옴
# 환경변수가 없으면 기본값 사용
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'studycalender'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# SQLite를 사용하고 싶다면 아래 설정 사용 (로컬 개발용)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # SQLite 데이터베이스 엔진 사용
#         'NAME': BASE_DIR / 'db.sqlite3',         # 데이터베이스 파일 경로 (프로젝트 루트)
#     }
# }

# ========== Celery 설정 (로컬 개발용) ==========
# 로컬 개발 시 Celery를 사용하지 않으려면 아래 설정 주석 처리
# 또는 로컬 Redis 설치 후 localhost로 변경

# Celery 비활성화 (로컬 개발 시 선택사항)
# CELERY_BROKER_URL = None
# CELERY_RESULT_BACKEND = None

# 로컬 Redis 사용 (Redis 설치 필요: https://redis.io/download)
# Windows: https://github.com/microsoftarchive/redis/releases
# 또는 WSL2 사용
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'django-db')
