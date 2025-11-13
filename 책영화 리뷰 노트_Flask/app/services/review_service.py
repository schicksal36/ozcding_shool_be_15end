# app/services/review_service.py
# ----------------------------
# 서비스 계층 (Business Logic)
# - DB에 접근하고 결과를 리턴하는 함수들 모음
# ----------------------------

from ..models import Review
from .. import db
from sqlalchemy import func


# 전체 리뷰 불러오기 (최신순)
def get_all_reviews():
    return Review.query.order_by(Review.created_at.desc()).all()


# 평균 별점 계산
def get_average_rating():
    avg = db.session.query(func.avg(Review.rating)).scalar()  # 평균 계산
    return round(avg, 2) if avg else 0                        # 평균 없으면 0


# 리뷰 생성
def create_review(title, content, rating):
    new_review = Review(title=title, content=content, rating=rating)
    db.session.add(new_review)
    db.session.commit()


# 특정 리뷰 조회 (수정/삭제용)
def get_review(review_id):
    return Review.query.get(review_id)


# 리뷰 수정
def update_review(review_id, title, content, rating):
    review = Review.query.get(review_id)
    review.title = title
    review.content = content
    review.rating = rating
    db.session.commit()


# 리뷰 삭제
def delete_review(review_id):
    review = Review.query.get(review_id)
    db.session.delete(review)
    db.session.commit()
