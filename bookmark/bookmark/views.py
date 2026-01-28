from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import Bookmark


# ==========================================================
# 🔹 북마크 목록 페이지
# ----------------------------------------------------------
# URL 예:
#   /bookmark/
#
# 역할:
#   - Bookmark 테이블에 저장된 모든 북마크를 조회
#   - bookmark_list.html 템플릿에 전달
#
# SQL 대응:
#   SELECT * FROM bookmark_bookmark;
# ==========================================================
def bookmark_list(request):
    # [1] Bookmark 테이블의 모든 레코드 조회
    bookmarks = Bookmark.objects.filter(id__gte=50)


    # [2] 템플릿으로 전달할 데이터(context)
    context = {
        # ❌ bookmark (존재하지 않는 변수)
        # ✅ bookmarks (QuerySet 객체)
        'bookmarks': bookmarks
    }

    # [3] HTML 템플릿 + 데이터 렌더링
    return render(
        request,
        'bookmark_list.html',
        context
    )


# ==========================================================
# 🔹 북마크 상세 페이지
# ----------------------------------------------------------
# URL 예:
#   /bookmark/<int:pk>/
#
# 역할:
#   - 특정 북마크 1개에 대한 상세 정보 표시
#   - 존재하지 않으면 404 에러 발생
#
# SQL 대응:
#   SELECT * FROM bookmark_bookmark WHERE id = pk;
# ==========================================================
def bookmark_detail(request, pk):
    # [1] URL에서 전달된 pk 값으로 단일 북마크 조회 시도
    #     pk는 URL 패턴 <int:pk> 에서 추출된 값이다.
    try:
        bookmark = Bookmark.objects.get(pk=pk)
        # [동작원리-1]
        #   - ORM이 내부적으로 SQL SELECT 문을 생성해 DB에 질의한다.
        #   - 결과가 1개면 Bookmark 객체로 반환한다.
    except Bookmark.DoesNotExist:
        # [동작원리-2]
        #   - 해당 pk를 가진 행이 없으면
        #   - Django ORM이 Bookmark.DoesNotExist 예외를 발생시킨다.
        raise Http404("Bookmark not found")
        # [동작원리-3]
        #   - raise Http404는 Django에게
        #     "이 요청은 정상적인 404 응답으로 처리하라"고 지시한다.
        #   - 이후 코드는 실행되지 않는다.

    # [2] 템플릿에 전달할 데이터
    context = {
        # 소문자 bookmark:
        #  - 템플릿에서 {{ bookmark.name }}, {{ bookmark.url }} 형태로 접근
        'bookmark': bookmark
    }

    # [3] HTML 템플릿 렌더링
    return render(
        request,
        'bookmark_detail.html',
        context
    )
