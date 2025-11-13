# app/__init__.py (수정 후)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config   # 설정 파일 불러오기

# SQLAlchemy 인스턴스 생성
db = SQLAlchemy()


def create_app():
    # 1. instance_relative_config=True 추가
    # 2. template_folder 인자 제거 (기본값인 'app/templates/' 사용)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)  # config.py 적용

    # DB 초기화
    db.init_app(app)

    # 앱 최초 실행 시 DB 파일 생성
    with app.app_context():
        from .models import Review  # 모델 불러오기
        db.create_all()             # reviews.db 파일 생성 (instance/ 폴더 내에)

    # Blueprint 등록
    from .routes.review_routes import review_bp
    app.register_blueprint(review_bp)

    return app