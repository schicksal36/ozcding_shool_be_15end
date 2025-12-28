# ==================== 상세 주석 및 코드 설명 ====================
# 1. 필요한 Django 라이브러리 및 로컬 모듈 임포트
from django.contrib.auth.decorators import login_required  # 로그인 여부 확인
from django.core.paginator import Paginator                # 페이지네이션(글 나누기)
from django.shortcuts import render, get_object_or_404, redirect  # 템플릿 랜더, 객체 조회 등
from django.urls import reverse                            # URL 이름으로 실제 경로 생성
from django.views.decorators.http import require_http_methods  # HTTP 메서드 제한
from django.db.models import Q                             # 복잡한 조건(검색 등) 지원

from blog.forms import BlogForm                             # 폼 기반 글 작성/수정
from .models import Blog                                   # 블로그 모델

# ==================== 1. 블로그 글 목록 ===========================
def blog_list(request):
    """
    블로그 글 목록 화면 (검색 및 페이지네이션 지원).
    """
    # (1) 전체 Blog 객체를 created_at(작성 시간) 기준으로 오름차순 정렬해서 가져온다.
    blogs = Blog.objects.all().order_by("created_at")

    # (2) 주소창에서 전달된 qwer 파라미터(검색어)를 추출한다. (ex: ?qwer=hello)
    qwer = request.GET.get("qwer")

    # (3) 검색어가 있다면 제목/내용/작성자(username)에 해당 단어가 포함된 블로그만 걸러낸다(OR조합).
    if qwer:
        blogs = blogs.filter(
            Q(title__icontains=qwer) |
            Q(content__icontains=qwer) |
            Q(author__username__icontains=qwer)
        )

    # (4) Paginator를 사용해 블로그 목록을 10개씩 분할한다.
    paginator = Paginator(blogs, 10)
    page = request.GET.get("page")         # ?page=2 처럼 전달된 페이지 번호 추출

    # (5) 가져온 page 번호에 해당하는 글목록이 담긴 page_object 생성
    page_object = paginator.get_page(page)

    # (6) 템플릿에 넘겨줄 데이터(Dictionary) 작성
    context = {
        "object_list": page_object.object_list,  # 10개 글의 리스트
        "page_object": page_object,              # 페이지네이션 객체(현재 몇 쪽, 이전/다음 등 정보)
    }

    # (7) 렌더링할 템플릿/데이터와 함께 응답한다.
    return render(request, "blog_list.html", context)


# ==================== 2. 블로그 상세 정보(단일 글) ==================
def blog_detail(request, pk):
    """
    특정 블로그 글 상세 정보 페이지.
    :param pk: 글의 primary key(고유 번호)
    """
    # (1) pk(번호)에 해당하는 Blog 객체 1개를 가져온다. 없으면 404 오류.
    blog = get_object_or_404(Blog, pk=pk)

    # (2) 템플릿에 전달할 데이터 구성
    context = {
        "test": "TEST",  # 샘플 값을 template에 전달 (테스트용)
        "blog": blog,    # 본문에 실제로 쓸 Blog 객체(글 주요내용)
    }

    # (3) 해당 템플릿으로 응답
    return render(request, "blog_detail.html", context)


# ==================== 3. 글 작성(로그인 필수) =======================
@login_required()
def blog_create(request):
    """
    블로그 새 글 작성 (로그인 사용자 전용).
    GET : 빈 폼 보여줌
    POST: 입력데이터 검증 후, 저장 & 상세화면으로 이동
    """
    # (1) 사용자가 폼을 제출(POST)이면 데이터로 폼을 만들고, 아니면 빈 폼
    form = BlogForm(request.POST or None)

    # (2) form 유효성 검사
    if form.is_valid():
        # (2-1) DB에 바로 저장하지 않고, 임시 Blog 객체를 생성
        blog = form.save(commit=False)
        # (2-2) 현재 로그인한 사용자를 작성자로 지정
        blog.author = request.user
        # (2-3) Blog 객체 실제 DB에 저장
        blog.save()
        # (2-4) 작성 완료 후 상세페이지로 이동
        return redirect(reverse("blog_detail", kwargs={"blog_pk": blog.pk}))

    # (3) (처음 들어왔거나, 폼에 오류 있으면) 기존 입력값/폼 에러와 함께 폼 다시 렌더링
    context = {
        "form": form,
    }
    return render(request, "blog_form.html", context)


# ==================== 4. 글 수정(로그인+본인 글만) ===================
@login_required()
def blog_update(request, pk):
    """
    블로그 글 수정(로그인+본인 글만 가능).
    GET : 작성폼에 기존 글 데이터 있어야 함.
    POST: 수정값 유효시 저장.
    """
    # (1) pk에 해당하는 Blog 글을 "본인이 썼는지" 체크해서 가져옴. 아니면 404.
    blog = get_object_or_404(Blog, pk=pk, author=request.user)

    # (2) 요청이 POST이면 새 데이터, 아니면 기존 데이터로 폼 생성
    form = BlogForm(request.POST or None, instance=blog)

    # (3) 폼 유효 검증
    if form.is_valid():
        # (3-1) 수정된 내용을 실제로 저장
        blog = form.save()
        # (3-2) 저장 후 상세화면 이동
        return redirect(reverse("blog_detail", kwargs={"pk": blog.pk}))

    # (4) 폼 입력 미완/에러 시, 현재 데이터와 폼 다시 보여주기
    context = {
        "blog": blog,
        "form": form,
    }
    return render(request, "blog_form.html", context)


# ==================== 5. 글 삭제(로그인+본인 글만, POST만) ===========
@login_required()
@require_http_methods(["POST"])     # POST 요청만 허용 (GET으로 삭제 X)
def blog_delete(request, pk):
    """
    블로그 글 삭제(로그인+본인 글만, POST요청만 가능).
    :param pk: 글 번호
    """
    # (1) 작성자가 '나'인 글만 가져오며, 없으면 404
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    # (2) 실제 DB에서 글 삭제
    blog.delete()
    # (3) 삭제 후 목록 페이지로 이동
    return redirect(reverse("blog_list"))
