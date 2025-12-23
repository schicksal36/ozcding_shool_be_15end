# ================================
# Django 기본
# ================================
from django.contrib.auth.decorators import login_required

# 로그인하지 않은 사용자의 접근을 막고,
# 인증되지 않았으면 LOGIN_URL로 자동 리다이렉트함

from django.core.paginator import Paginator

# QuerySet을 페이지 단위로 분리해주는 Django 내장 클래스

from django.http import Http404

# HTTP 404(Not Found) 예외 클래스 (현재는 주석 처리된 코드에서만 사용)

from django.shortcuts import render, get_object_or_404, redirect

# render            : 템플릿을 HTML로 렌더링하여 HttpResponse 반환
# get_object_or_404 : 객체가 없으면 자동으로 404 응답
# redirect          : 다른 URL로 이동시키는 응답 반환

from django.urls import reverse

# URL name을 실제 URL 문자열로 변환하는 함수

from django.views.decorators.http import require_http_methods

# 허용할 HTTP 메서드(GET, POST 등)를 제한하는 데코레이터

# ================================
# Django ORM
# ================================
from django.db.models import Q

# OR 조건 검색을 가능하게 해주는 ORM 객체

# ================================
# 로컬 앱
# ================================
from blog.form import BlogForm

# Blog 모델과 연결된 Form 클래스 (글 생성/수정용)

from .models import Blog

# Blog 테이블과 매핑된 Django ORM 모델


def blog_list(request):
    """
    [블로그 목록 페이지]
    -------------------------------------------------------------------------
    1. 전체 블로그 글을 DB에서 조회
    2. 검색어(qwer)가 있으면 제목/내용/작성자 기준으로 필터링
    3. Paginator를 이용해 페이지네이션 처리
    4. 목록 템플릿으로 데이터 전달
    -------------------------------------------------------------------------
    """

    # Blog 테이블의 모든 데이터를 작성일 기준 오름차순으로 조회
    blogs = Blog.objects.all().order_by("created_at")

    # GET 파라미터에서 검색어(qwer) 추출
    qwer = request.GET.get("qwer")

    # 검색어가 있을 경우 OR 조건으로 필터링
    if qwer:
        blogs = blogs.filter(
            Q(title__icontains=qwer)
            | Q(content__icontains=qwer)
            | Q(author__username__icontains=qwer)
        )

    # 페이지네이션 객체 생성 (한 페이지당 10개씩)
    paginator = Paginator(blogs, 10)

    # 현재 페이지 번호 (?page=숫자)
    page = request.GET.get("page")

    # 잘못된 페이지 번호가 들어와도 자동으로 처리해주는 메서드
    page_object = paginator.get_page(page)

    # visits = int(request.COOKIES.get('visits', 0)) + 1
    # request.session['count'] = request.session.get('count', 0) + 1

    # 템플릿으로 전달할 데이터
    context = {
        "page_object": page_object,
        #'blogs': blogs,
        #'visits': visits,
        #'count': request.session['count'],
    }

    # HTML 템플릿을 렌더링하여 응답 생성
    response = render(request, "blog_list.html", context)

    # response.set_cookie('visits', visits)
    return response


def blog_detail(request, pk):
    """
    [블로그 상세 페이지]
    -------------------------------------------------------------------------
    1. URL로 전달받은 pk에 해당하는 블로그 글 조회
    2. 글이 없으면 자동으로 404 응답
    3. 상세 페이지 템플릿으로 전달
    -------------------------------------------------------------------------
    """

    # pk에 해당하는 Blog 객체를 조회, 없으면 404
    blog = get_object_or_404(Blog, pk=pk)

    context = {
        "blog": blog,
    }

    return render(request, "blog_detail.html", context)


@login_required()
def blog_create(request):
    """
    [블로그 글 작성]
    -------------------------------------------------------------------------
    1. 로그인한 사용자만 접근 가능
    2. BlogForm을 통해 사용자 입력 처리
    3. 작성자를 현재 로그인한 사용자로 설정
    4. 저장 후 상세 페이지로 이동
    -------------------------------------------------------------------------
    """

    # POST 요청이면 데이터 바인딩, GET이면 빈 폼 생성
    form = BlogForm(request.POST or None)

    # 폼 유효성 검사
    if form.is_valid():

        # DB 저장 전 객체만 생성 (author 설정을 위해)
        blog = form.save(commit=False)

        # 현재 로그인한 사용자를 작성자로 지정
        blog.author = request.user

        # DB에 최종 저장
        blog.save()

        # 글 생성 후 해당 글의 상세 페이지로 이동
        return redirect(reverse("blog_detail", kwargs={"pk": blog.pk}))

    context = {
        "form": form,
    }

    return render(request, "blog_create.html", context)


@login_required()
def blog_update(request, pk):
    """
    [블로그 글 수정]
    -------------------------------------------------------------------------
    1. 로그인한 사용자만 접근 가능
    2. 본인이 작성한 글만 수정 가능
    3. 기존 글 데이터를 폼에 바인딩
    4. 수정 완료 후 상세 페이지로 이동
    -------------------------------------------------------------------------
    """

    # pk + author 조건으로 조회 → 남의 글 접근 차단
    blog = get_object_or_404(Blog, pk=pk, author=request.user)

    # 기존 데이터를 instance로 연결하여 수정 폼 생성
    form = BlogForm(request.POST or None, instance=blog)

    if form.is_valid():
        blog = form.save()
        return redirect(reverse("blog_detail", kwargs={"pk": blog.pk}))

    context = {
        "blog": blog,
        "form": form,
    }

    return redirect(reverse, "blog_update.html", context)


@login_required()
@require_http_methods(["POST"])
def blog_delete(request, pk):
    """
    [블로그 글 삭제]
    -------------------------------------------------------------------------
    1. 로그인한 사용자만 접근 가능
    2. POST 요청만 허용
    3. 본인이 작성한 글만 삭제 가능
    4. 삭제 후 목록 페이지로 이동
    -------------------------------------------------------------------------
    """

    # if request.method !='POST':
    # raise Http404

    # pk + author 조건으로 조회 → 권한 없는 삭제 차단
    blog = get_object_or_404(Blog, pk=pk, author=request.user)

    # DB에서 해당 글 삭제
    blog.delete()

    # 삭제 후 블로그 목록 페이지로 이동
    return redirect(reverse("blog_list"))
