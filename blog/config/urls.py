"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from blog import views
# ↑ blog 앱의 views.py 파일을 불러옴
#   views.blog_list / views.blog_detail 같은 함수에 접근하기 위함


urlpatterns = [
    # ==========================================
    # 🔐 관리자 페이지 URL
    # ==========================================
path(
    "admin/",              # 📌 관리자 페이지 URL 경로
                           # - 브라우저에서 /admin/ 으로 접속하면 매칭됨
                           # - 예: http://127.0.0.1:8000/admin/

    admin.site.urls        # 📌 Django가 기본 제공하는 관리자(Admin) 사이트
                           # - django.contrib.admin 앱에서 제공
                           # - 모델 등록(admin.py)을 기반으로 CRUD 화면 자동 생성
),

    # 👉 사용자가 브라우저에서
    #    http://127.0.0.1:8000/admin/
    #    로 접속하면
    # 👉 Django가 기본으로 제공하는
    #    관리자(Admin) 사이트가 실행됨


    # ==========================================
    # 📄 블로그 목록 페이지
    # ==========================================
path(
    "blog/",                   # 📌 URL 패턴
                               # - /blog/ 로 접속했을 때 매칭됨
                               # - 블로그 글 목록 페이지의 주소

    views.blog_list,            # 📌 실행될 view 함수
                               # - 요청이 들어오면
                               #   views.blog_list(request) 형태로 호출됨
                               # - DB에서 여러 개의 Blog 객체를 조회해 목록으로 전달

    name="blog_list"            # 📌 URL 이름(name)
                               # - 템플릿에서 {% url 'blog_list' %} 로 사용 가능
                               # - URL을 하드코딩하지 않고 안전하게 링크 생성
),

    # 👉 URL: /blog/
    # 👉 요청 방식: GET
    # 👉 실행 함수: views.blog_list(request)
    #
    # 동작 순서:
    # 1. 사용자가 /blog/ 접속
    # 2. Django URL 라우터가 urlpatterns를 위에서부터 검사
    # 3. "blog/" 와 일치하는 path 발견
    # 4. views.blog_list 함수 호출
    # 5. blog_list 내부에서:
    #    - Blog.objects.all() 로 DB 조회
    #    - blog_list.html 템플릿 렌더링
    # 6. HTML 응답을 브라우저에 반환


    # ==========================================
    # 📄 블로그 상세 페이지
    # ==========================================
path(
    "blog/<int:pk>/",          # 📌 URL 패턴
                               # - blog/숫자/ 형태의 URL만 매칭
                               # - 예: /blog/1/, /blog/10/
                               # - <int:pk>의 숫자는 자동으로 pk 변수에 담김

    views.blog_detail,          # 📌 실행될 view 함수
                               # - 요청이 들어오면
                               #   views.blog_detail(request, pk) 형태로 호출됨

    name="blog_detail"          # 📌 URL 이름(name)
                               # - 템플릿에서 {% url 'blog_detail' blog.pk %} 로 사용
                               # - URL을 하드코딩하지 않게 해주는 핵심 기능
),

    # 👉 URL 예시:
    #    /blog/1/
    #    /blog/5/
    #    /blog/10/
    #
    # 👉 <int:pk> 의미:
    #    - 정수(int) 값만 허용
    #    - 해당 숫자를 pk라는 변수로 view에 전달
    #
    # 예시 동작 흐름:
    # 1. 사용자가 /blog/3/ 접속
    # 2. Django가 <int:pk> 부분에 3을 매칭
    # 3. views.blog_detail(request, pk=3) 호출
    # 4. blog_detail 함수 내부에서:
    #    - get_object_or_404(Blog, pk=3) 실행
    #    - pk=3 인 블로그 객체 조회
    #    - 없으면 자동으로 404 에러 페이지
    # 5. blog_detail.html 템플릿 렌더링
    # 6. 해당 블로그 상세 내용을 브라우저에 반환
]
