from app.core.config import settings
from typing import List

# ================================================================
# 🔥 프로젝트에서 사용할 모든 모델 목록
# ---------------------------------------------------------------
# Tortoise ORM은 Django처럼 "앱" 개념을 갖고 있지만,
# 모델을 찾기 위해 Python import 경로 문자열을 반드시 지정해야 함.
#
# 즉, Tortoise는 자동 스캔이 없어서,
# 사용 모델을 전부 정확히 명시해야 DB 테이블이 생성됨.
# ================================================================
TORTOISE_MODELS: List[str] = [
    "app.models.user",       # 사용자(User) 모델
    "app.models.diary",      # 다이어리(Diary) 모델
    "app.models.quote",      # 명언(Quote) 모델
    "app.models.question",   # 질문(Question) 모델
    "aerich.models",         # Aerich 마이그레이션용 내부 모델 (필수)
]


# ================================================================
# 🔥 Tortoise ORM 설정 딕셔너리 (FastAPI + Aerich 구조)
# ---------------------------------------------------------------
# FastAPI에서 Tortoise를 초기화할 때 즉시 이 dict를 전달하게 됨.
#
# from tortoise.contrib.fastapi import register_tortoise
# register_tortoise(app, config=TORTOISE_ORM, ...)
#
# 이렇게 하면 다음이 자동 처리됨:
#   1) DB 연결 생성
#   2) 각 모델 import
#   3) 스키마 생성(optional)
#   4) Aerich 마이그레이션 호환
# ================================================================
TORTOISE_ORM = {
    # -----------------------------------------------------------
    # 1) DB connections 설정
    # -----------------------------------------------------------
    "connections": {
        # "default"는 ORM에서 기본으로 사용할 연결 이름
        #
        # settings.db_url은 다음과 같은 규칙:
        #   (1) .env에 DATABASE_URL 있으면 → 그 값을 그대로 사용
        #   (2) 없으면 DB_USER, DB_PASSWORD 등 조합해서 생성된 URL 사용
        #
        # 예: postgres://postgres:1234@localhost:5432/my_diary_db
        "default": settings.db_url,
    },

    # -----------------------------------------------------------
    # 2) apps 정의 — Django와 유사한 논리적 모듈 그룹
    # -----------------------------------------------------------
    "apps": {
        "models": {
            # 사용할 모든 모델 파일 경로
            "models": TORTOISE_MODELS,

            # 위의 connections 중 어떤 연결을 사용할지 지정
            # 대부분의 경우 default 하나만 쓰므로 이렇게 설정
            "default_connection": "default",
        }
    }
}
