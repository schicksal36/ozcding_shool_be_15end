from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.db.base import TORTOISE_ORM


def init_tortoise(app: FastAPI) -> None:
    """
    ===============================================================
    🔥 FastAPI 애플리케이션에 Tortoise ORM을 연결하는 초기화 함수
    ---------------------------------------------------------------
    FastAPI의 startup / shutdown 이벤트에 자동으로 아래 작업을 등록함:

    ▶ startup 시:
        1) DB 연결 생성
        2) 모델 파일(app.models.*) import
        3) ORM registry 구성
        4) generate_schemas=True일 경우 DB 테이블 생성(create table)
        5) Aerich을 사용할 경우 마이그레이션 기반으로 테이블 관리

    ▶ shutdown 시:
        - 모든 DB 연결을 정리하며 clean shutdown 진행

    이 함수는 main.py 또는 app/main.py에서 한 번만 호출하면 됨.
    ===============================================================
    """

    register_tortoise(
        app,
        config=TORTOISE_ORM,          # 💡 database 설정(dict) 주입
                                      #    connections / apps / models 구조 포함

        generate_schemas=False,       # 💡 매우 중요한 설정
                                      # True → startup마다 CREATE TABLE 실행 (비추천)
                                      # False → Aerich 마이그레이션으로 스키마 관리
                                      #
                                      # 운영환경, 협업 프로젝트에서는 반드시 False여야 함.
                                      # 왜?
                                      #    - 테이블 자동 생성은 위험 (데이터 날릴 가능성)
                                      #    - 스키마 버전 관리(Aerich)가 불가능해짐

        add_exception_handlers=True,  # 💡 ORM 관련 기본 예외를 FastAPI에 자동 등록
                                      # 예: 모델을 찾지 못할 때 발생하는 DoesNotExist → 404로 변환
                                      #     ValidationError → 422로 자동 처리
    )
