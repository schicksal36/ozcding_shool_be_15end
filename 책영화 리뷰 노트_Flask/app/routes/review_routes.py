# app/routes/review_routes.py
# ----------------------------
# 라우팅 담당
# URL → 서비스 호출 → 템플릿 전달
# ----------------------------

from flask import Blueprint, render_template, request, redirect, url_for
from ..services.review_service import (
    get_all_reviews, get_average_rating,
    create_review, get_review, update_review, delete_review
)

# Blueprint 생성 (라우트 그룹)
review_bp = Blueprint("review", __name__)


# 메인 페이지(리뷰 목록 + 평균 별점)
@review_bp.route("/")
def index():
    reviews = get_all_reviews()      # 전체 리뷰
    avg = get_average_rating()       # 평균 별점
    return render_template("index.html", reviews=reviews, avg=avg)


# 새 리뷰 작성 페이지
@review_bp.route("/new", methods=["GET", "POST"])
def new_review():
    if request.method == "POST":
        # 폼 데이터 받아오기
        title = request.form["title"]
        content = request.form["content"]
        rating = int(request.form["rating"])

        # DB 저장
        create_review(title, content, rating)

        # 목록 페이지로 이동
        return redirect(url_for("review.index"))

    # GET 요청 시 작성 폼만 표시
    return render_template("new.html")


# 리뷰 수정
@review_bp.route("/edit/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    review = get_review(review_id)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        rating = int(request.form["rating"])

        update_review(review_id, title, content, rating)

        return redirect(url_for("review.index"))

    return render_template("edit.html", review=review)


# 리뷰 삭제
@review_bp.route("/delete/<int:review_id>")
def delete_review_route(review_id):
    delete_review(review_id)
    return redirect(url_for("review.index"))
