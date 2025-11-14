from flask import Blueprint, render_template, request, redirect, url_for
from ..services.review_service import (
    get_all_reviews, get_average_rating,
    create_review, get_review, update_review, delete_review
)

review_bp = Blueprint("review", __name__)

@review_bp.route("/")
def index():
    reviews = get_all_reviews()
    avg = get_average_rating()
    return render_template("index.html", reviews=reviews, avg=avg)

@review_bp.route("/new", methods=["GET", "POST"])
def new_review():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        rating = int(request.form["rating"])
        create_review(title, content, rating)
        return redirect(url_for("review.index"))
    return render_template("new.html")

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

@review_bp.route("/delete/<int:review_id>")
def delete_review_route(review_id):
    delete_review(review_id)
    return redirect(url_for("review.index"))
