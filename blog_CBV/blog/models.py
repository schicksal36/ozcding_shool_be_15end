from django.conf import settings
from django.db import models
from django.urls import reverse


class Blog(models.Model):
    CATEGORY_CHOICES = (
        ("FREE", "자유게시판"),
        ("C", "C"),
        ("PYTHON", "Python"),
        ("JAVA", "Java"),
        ("LINUX", "Linux 명령어"),
    )

    category = models.CharField("카테고리",max_length=10,choices=CATEGORY_CHOICES, default='free' )
    title = models.CharField("제목", max_length=100)
    content = models.TextField("본문")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="작성자",
        related_name="blogs",
    )
    created_at = models.DateTimeField("작성일자", auto_now_add=True)
    updated_at = models.DateTimeField("수정일자", auto_now=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title[:10]}"
        
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "블로그"
        verbose_name_plural = "블로그 목록"



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
