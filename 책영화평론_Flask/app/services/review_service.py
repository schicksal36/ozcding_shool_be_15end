from ..models import Review
from .. import db
from sqlalchemy import func

def get_all_reviews():
    return Review.query.order_by(Review.created_at.desc()).all()

def get_average_rating():
    avg = db.session.query(func.avg(Review.rating)).scalar()
    return round(avg, 2) if avg else 0

def create_review(title, content, rating):
    new_review = Review(title=title, content=content, rating=rating)
    db.session.add(new_review)
    db.session.commit()

def get_review(review_id):
    return Review.query.get(review_id)

def update_review(review_id, title, content, rating):
    review = Review.query.get(review_id)
    review.title = title
    review.content = content
    review.rating = rating
    db.session.commit()

def delete_review(review_id):
    review = Review.query.get(review_id)
    db.session.delete(review)
    db.session.commit()
