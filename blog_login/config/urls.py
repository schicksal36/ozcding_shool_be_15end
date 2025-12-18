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

# ============================================================
# 🌐 프로젝트 최상위 URL 설정 파일 (config/urls.py)
# ------------------------------------------------------------
# 이 파일의 역할
# 1️⃣ 브라우저에서 들어오는 모든 URL 요청을 가장 먼저 받음
# 2️⃣ 요청 URL에 따라 실행할 view(함수/클래스)를 결정
# 3️⃣ Django의 URL Dispatcher(라우터) 역할 수행
# ============================================================

from django.contrib import admin
# Django 기본 관리자(Admin) 사이트 모듈

from django.urls import path, include
# path    : URL 패턴을 정의
# include : 다른 앱의 urls.py를 포함

from blog import views
# blog 앱의 views.py
# → views.blog_list, views.blog_detail 사용

from member import views as member_views
# member 앱의 views.py
# → member_views.sign_up, member_views.login 사용


# ============================================================
# 📌 urlpatterns
# ------------------------------------------------------------
# Django는 이 리스트를 "위에서 아래로" 순차 검사함
# URL이 처음으로 매칭되는 path가 실행됨
# ============================================================

urlpatterns = [

    # ========================================================
    # 🔐 관리자 페이지
    # ========================================================
    path(
        "admin/",
        admin.site.urls,
    ),
    # 📎 설명:
    # - http://localhost:8000/admin/
    # - Django가 기본 제공하는 관리자 페이지
    # - 모델 관리, 사용자/권한 관리 가능
    # - admin.site.urls 는 "뷰 함수"가 아니라
    #   관리자용 URL 패턴 집합


    # ========================================================
    # 🏠 메인 페이지 (블로그 목록)
    # ========================================================
    path(
        "",
        views.blog_list,
        name="blog_list",
    ),
    # 📎 설명:
    # - 빈 문자열 "" → 루트 URL (/)
    # - http://localhost:8000/
    # - blog_list 뷰 실행
    # - 보통 메인(index) 페이지 역할
    # - name="blog_list":
    #   → {% url 'blog_list' %} 로 템플릿에서 사용


    # ========================================================
    # 📄 블로그 상세 페이지
    # ========================================================
    path(
        "<int:pk>/",
        views.blog_detail,
        name="blog_detail",
    ),
    # 📎 설명:
    # - <int:pk> :
    #   · 정수만 허용
    #   · URL의 숫자 부분을 pk 변수로 전달
    #   · 예) /1/  → pk=1
    # - blog_detail(request, pk) 형태로 호출됨
    # - pk는 보통 Blog 모델의 Primary Key
    # - name="blog_detail":
    #   → {% url 'blog_detail' blog.pk %}


    # ========================================================
    # 🔑 Django 기본 인증(Auth) URL 포함
    # ========================================================
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),
    # 📎 설명:
    # 이 한 줄로 Django가 제공하는 인증 관련 URL들이 자동 등록됨
    #
    # 🔐 포함되는 URL 예시:
    # - /accounts/login/               (로그인)
    # - /accounts/logout/              (로그아웃)
    # - /accounts/password_change/
    # - /accounts/password_change/done/
    # - /accounts/password_reset/
    # - /accounts/password_reset/done/
    # - /accounts/reset/<uidb64>/<token>/
    # - /accounts/reset/done/
    #
    # 🔑 자동 제공되는 name 값:
    # - 'login', 'logout', 'password_change', 'password_reset' 등
    #
    # ⚠️ 주의:
    # - 이 login은 Django 기본 LoginView
    # - 아래에서 직접 만든 login 뷰와 name 충돌 가능


    # ========================================================
    # 📝 회원가입
    # ========================================================
    path(
        "signup/",
        member_views.sign_up,
        name="signup",
    ),
    # 📎 설명:
    # - 회원가입 전용 URL
    # - member/views.py 의 sign_up 함수 실행
    # - {% url 'signup' %} 로 사용 가능


    # ========================================================
    # 🔐 커스텀 로그인
    # ========================================================
    path(
        "login/",
        member_views.login,
        name="custom_login",
    ),
    # 📎 설명:
    # - 직접 구현한 로그인 View
    # - Django 기본 auth.urls 의 'login' 과 구분하기 위해
    #   name을 custom_login으로 지정
    #
    # ✅ 권장:
    # - 템플릿에서는 {% url 'custom_login' %} 사용
    # - 아니면 auth.urls 의 login을 제거하고 하나만 사용
]
