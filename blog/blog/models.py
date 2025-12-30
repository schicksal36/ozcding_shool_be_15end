from io import BytesIO
from pathlib import Path
import re
from PIL import Image

from django.conf import settings
from django.core.files import File
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
    image =models.ImageField('이미지', null=True, blank=True,upload_to='blog/%Y/%m/%d')
    thubnail = models.ImageField("썸네일",null=True, blank=True, upload_to='blog/%Y/%m/%d')

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title[:10]}"

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"blog_pk": self.pk})

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        if self.image:
            return self.image.url
        return None

    
   # def save(self,*args,**kwargs):
        #if not self.image:
            #return super(self, *args, **kwargs)

        #image =  Image.open(self.image)
        #image.thumbnail((300,300))     
        #image_path = Path(self.imge.name)
        #thumbnail_name = image_path.stem
        #thumbnail_extension = image_path.suffix
        #thumbnail_filename = f"{thumbnail_name}_thumb{thumbnail_extension}" #databases
        #if thumbnail_extension in ['.jpg','jpeg']:
            #file_type = 'JPEG'
        #elif thumbnail_extension == '.gif':
            #file_type = 'GIF'
        #elif thumbnail_extension == '.png':
            #file_type = 'PNG' 
        #else:
            #return super().save(*args,**kwargs)
        #temp_thmb = BytesIO()
        #image.save(temp_thmb, file_type)
        #temp_thmb.seek(0)
        #self.thumbnail.save(thumbnail_filename,temp_thmb,seve=False)
        #return super().save(*args,**kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.image:
            return

        img = Image.open(self.image)
        img.thumbnail((300, 300))

        image_path = Path(self.image.name)
        ext = image_path.suffix.lower()
        thumb_name = f"{image_path.stem}_thumb{ext}"

        thumb_io = BytesIO()

        if ext in [".jpg", ".jpeg"]:
            img.save(thumb_io, format="JPEG")
        elif ext == ".png":
            img.save(thumb_io, format="PNG")
        elif ext == ".gif":
            img.save(thumb_io, format="GIF")
        else:
            return

        thumb_io.seek(0)

        self.thumbnail.save(
            thumb_name,
            File(thumb_io),
            save=False
        )

        super().save(update_fields=["thumbnail"])




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

    def get_urlabsolute_url(self):
        return reverse('blog:detail', kwargs={'blog_pk':self.pk})



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
