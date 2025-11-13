# app/config.py
# ----------------------------
# Flask 설정 파일
# SQLite 경로, SECRET_KEY 설정
# ----------------------------

class Config:
    SECRET_KEY = "secret-key-review"  # Flask 세션/폼 보호용
    SQLALCHEMY_DATABASE_URI = "sqlite:///reviews.db"  # SQLite 파일 경로
    SQLALCHEMY_TRACK_MODIFICATIONS = False            # 경고 메시지 비활성화
