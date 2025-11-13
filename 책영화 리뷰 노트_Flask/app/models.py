# app/models.py
# ----------------------------
# 데이터베이스 모델 정의 파일(ORM)
# Review 테이블 구조 정의
# ----------------------------

from . import db
from datetime import datetime

class Review(db.Model):
    # 기본키(id)
    id = db.Column(db.Integer, primary_key=True)

    # 리뷰 제목
    title = db.Column(db.String(100), nullable=False)

    # 리뷰 내용 (긴 글 가능)
    content = db.Column(db.Text, nullable=False)

    # 별점 (1 ~ 5)
    rating = db.Column(db.Integer, nullable=False)

    # 작성 날짜
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
