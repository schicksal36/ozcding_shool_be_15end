from django.contrib import admin
from .models import Blog

# 📌 현재 앱(models.py)에 정의된 Blog 모델 import
# - 관리자 페이지에 등록할 대상


# ============================================================================
# 📌 Blog 모델을 Django Admin에 등록
# ============================================================================
@admin.register(Blog)
# 📌 @admin.register(Blog)
# - Blog 모델을 관리자(Admin) 사이트에 등록하는 데코레이터
# - 아래 BlogAdmin 클래스와 Blog 모델을 연결
#
# 내부적으로 아래 코드와 완전히 동일:
# admin.site.register(Blog, BlogAdmin)


class BlogAdmin(admin.ModelAdmin):
    # ============================================================
    # 📌 BlogAdmin 클래스
    #
    # 역할:
    # - 관리자 페이지(/admin/)에서 Blog 모델을
    #   어떻게 보여주고, 어떻게 관리할지 정의
    #
    # 상속:
    # - admin.ModelAdmin을 상속해야 Admin 설정 클래스가 됨
    #
    # 적용 범위:
    # - 목록 화면
    # - 상세 화면
    # - 검색, 필터, 정렬, 표시 필드 등
    # ============================================================

    ...
    # 📌 Ellipsis(...)
    # - 아직 아무 설정도 하지 않았다는 의미의 자리 표시자
    # - 실제 동작은 아래와 동일:
    #
    #   class BlogAdmin(admin.ModelAdmin):
    #       pass
    #
    # 즉,
    # - Blog 모델은 Admin에 "등록은 되어 있음"
    # - 화면은 Django 기본 Admin UI 그대로 사용
