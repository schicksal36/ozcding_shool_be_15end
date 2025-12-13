from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    ===============================================================
    🔥 Settings 클래스 동작 원리 (Pydantic Settings v2)
    ---------------------------------------------------------------
    - BaseSettings를 상속하면 `.env`, 운영체제 환경 변수(OS ENV),
      혹은 코드 기본값(default)을 자동으로 읽어서 필드에 대입함.

    - 우선순위 (높음 → 낮음)
        1) 직접 전달된 값 (Settings(...))
        2) OS 환경 변수 (export KEY=VALUE)
        3) .env / .env.dev 파일
        4) 클래스 기본값 (여기 적힌 값)

    - FastAPI에서 settings = Settings() 하면
      애플리케이션 시작 시 단 한 번만 읽혀 캐싱됨.
    ===============================================================
    """

    # ============================
    # 🔹 Database 기본 환경 변수들
    # ============================
    DB_USER: str = "postgres"     # 기본값, 실제 값은 .env에서 override 가능
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "my_diary_db"

    # DATABASE_URL을 직접 지정할 수도 있음 → docker, railway, neon 등에서 사용
    DATABASE_URL: str = ""

    # ============================
    # 🔹 JWT 토큰 만료시간 관련 설정
    # ============================
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7일

    # ============================
    # 🔹 FastAPI 기본 설정
    # ============================
    APP_NAME: str = "my_app"
    APP_ENV: str = "my_env"
    DEBUG: bool = False

    # ============================
    # 🔹 JWT 보안 관련
    # ============================
    ALGORITHM: str = "HS256"  # JWT 서명 알고리즘
    SECRET_KEY: str = ""       # 반드시 .env에서 설정해야 함 (중요!)

    # ===============================================================
    # 🔥 DB URL 생성 로직
    # ---------------------------------------------------------------
    # - DATABASE_URL이 .env에서 들어왔다면 그걸 우선 사용
    # - 그렇지 않으면 개별 환경 변수로 PostgreSQL 연결 문자열 생성
    # ===============================================================
    @property
    def db_url(self) -> str:
        """
        🔥 동작 원리:
        1) .env 등에서 DATABASE_URL이 지정되어 있을 경우 → 가장 우선 사용
           예: DATABASE_URL="postgres://user:pw@host:5432/db"

        2) 지정되지 않았다면 → 개별 환경변수 조합해서 자동 생성
           postgres://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME

        ❗ 주의: SQLAlchemy는 "postgresql://" prefix 사용,
                Tortoise ORM은 "postgres://", "postgresql://", 둘 다 허용.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        return (
            f"postgres://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # ===============================================================
    # 🔥 SettingsConfigDict — Pydantic Settings v2 방식
    # ---------------------------------------------------------------
    # env_file: 읽을 파일 목록 (여러 개도 가능)
    # extra="ignore": .env에 정의되지 않은 값이 있어도 무시
    # env_prefix="": 모든 변수를 prefix 없이 그대로 사용
    # ===============================================================
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.dev"),  # 여러 .env 파일을 순차적으로 읽음
        extra="ignore",
        env_prefix="",                  # prefix 없이 그대로 읽기
    )


# ===============================================================
# 🔥 Settings 인스턴스 생성
# ---------------------------------------------------------------
# - FastAPI startup 시 단 한 번 실행
# - settings.DB_USER, settings.SECRET_KEY 처럼 접근 가능
# ===============================================================
settings = Settings()
