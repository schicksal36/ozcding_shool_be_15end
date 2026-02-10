# 로컬 개발 환경 설정 가이드

이 가이드는 Docker 없이 로컬 환경에서 프로젝트를 실행하는 방법을 설명합니다.

## 사전 요구사항

- Python 3.13 이상
- uv (Python 패키지 관리자) 또는 pip
- (선택사항) Redis (Celery 사용 시)

## 설치 및 설정

### 1. 가상환경 생성 및 활성화

```bash
# uv 사용 시
uv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 또는 pip 사용 시
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 2. 의존성 설치

```bash
# uv 사용 시
uv pip install -e .

# 또는 pip 사용 시
pip install -e .
```

### 3. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하세요:

```bash
cp .env.example .env
```

`.env` 파일을 열어서 `SECRET_KEY`를 설정하세요:

```bash
# SECRET_KEY 생성 (Python 실행)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

생성된 키를 `.env` 파일의 `SECRET_KEY`에 붙여넣으세요.

### 4. 데이터베이스 마이그레이션

```bash
# 마이그레이션 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate
```

### 5. 슈퍼유저 생성 (선택사항)

Django Admin에 접근하려면 슈퍼유저를 생성하세요:

```bash
python manage.py createsuperuser
```

## 실행

### 개발 서버 실행

```bash
python manage.py runserver
```

서버가 실행되면 `http://127.0.0.1:8000/`에서 접근할 수 있습니다.

### API 문서 확인

- Swagger UI: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- ReDoc: `http://127.0.0.1:8000/api/schema/redoc/`

## 데이터베이스

로컬 개발 환경에서는 **SQLite**를 사용합니다.

- 데이터베이스 파일: `db.sqlite3` (프로젝트 루트)
- 별도의 데이터베이스 서버 설치 불필요
- PostgreSQL을 사용하려면 `config/settings/local.py`에서 설정 변경

## Celery (선택사항)

로컬에서 Celery를 사용하려면 Redis를 설치해야 합니다:

### Windows
1. [Redis for Windows](https://github.com/microsoftarchive/redis/releases) 다운로드
2. 또는 WSL2 사용

### Linux/Mac
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# Mac
brew install redis
```

Redis 실행:
```bash
redis-server
```

Celery 워커 실행 (별도 터미널):
```bash
celery -A config worker -l info
```

Celery Beat 실행 (스케줄러, 별도 터미널):
```bash
celery -A config beat -l info
```

## 문제 해결

### 앱을 찾을 수 없다는 오류

`config/settings/base.py`의 `OWN_APPS`에서 앱 경로를 확인하세요:
- 올바른 형식: `'apps.users'`
- 잘못된 형식: `'users.apps.UsersConfig'`

### 데이터베이스 연결 오류

SQLite를 사용하는 경우 별도의 설정이 필요 없습니다.
PostgreSQL을 사용하는 경우 `.env` 파일의 데이터베이스 설정을 확인하세요.

### CORS 오류

프론트엔드가 다른 포트에서 실행되는 경우, `config/settings/local.py`의 `CORS_ALLOWED_ORIGINS`에 프론트엔드 주소를 추가하세요.

## 추가 정보

- Django Admin: `http://127.0.0.1:8000/admin/`
- 정적 파일: `http://127.0.0.1:8000/static/`
- 미디어 파일: `http://127.0.0.1:8000/media/`
