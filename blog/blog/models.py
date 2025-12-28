from django.conf import settings
from django.db import models
from django.urls import reverse
from utils.model import TimestampModel


class Blog(TimestampModel):
    CATEGORY_CHOICES = (
        ("FREE", "자유게시판"),
        ("EMOTION", "감성글귀"),
    )

    category = models.CharField(
        "카테고리",
        max_length=10,
        choices=CATEGORY_CHOICES,
        default="FREE",
    )
    title = models.CharField("제목", max_length=100)
    content = models.TextField("본문")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="작성자",
        related_name="blogs",
    )

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title[:10]}"

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"blog_pk": self.pk})

    class Meta:
        verbose_name = "블로그"
        verbose_name_plural = "블로그 목록"


class Comment(TimestampModel):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="블로그",
    )
    content = models.CharField("본문", max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="작성자",
    )

    def __str__(self):
        return f"{self.blog.title} 댓글"

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        ordering = ('-created_at', '-id')


# models.CASEDE = 같이 삭제
# models.PROTECT = 삭제가 불가능함 (유저가 삭제 하려고 할때 블로그가 있으면 유저 삭제가 불가능)
# models.SET_NULL = NULL값을 넘습니다 (유저 삭제시 블로그가 auth가 null값이 됨)

# 익명,기존사용자 허용
# author = models.ForeignKey(
# settings.AUTH_USER_MODEL,
# on_delete=models.SET_NULL,
# null=True,
# blank=True,
# verbose_name="작성자",
# related_name="blogs"
# )

# mysql로 봤을때 생성되는 테이블
# CREATE TABLE blog_blog (
# id BIGINT AUTO_INCREMENT PRIMARY KEY,
# category VARCHAR(10) NOT NULL,
# title VARCHAR(100) NOT NULL,
# content LONGTEXT NOT NULL,
# created_at DATETIME(6) NOT NULL,
# updated_at DATETIME(6) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


# =========================
# 문자열 표현 (선택)
# =========================
# Admin / Shell에서 객체를 문자열로 볼 때 사용
# def __str__(self):
# return f"[{self.category}] {self.title}"
