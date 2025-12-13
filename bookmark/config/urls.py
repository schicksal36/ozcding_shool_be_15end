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
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
# [동작원리-0] 위 import들은 "서버가 켜질 때" (python manage.py runserver) 한 번 실행됨.
#             즉, 브라우저 요청이 올 때마다 실행되는 게 아니라,
#             Django가 프로젝트를 로딩할 때 실행되어 준비 상태를 만든다.


# -------------------------
# 메모리 기반 영화 데이터 (DB 대용)
# -------------------------
movie_list = [
    {'title': '귀멸의 칼날', 'director': 'ufotable'},
    {'title': '주토피아 2', 'director': 'Disney'},
    {'title': '사무라이 참프루', 'director': 'Manglobe'},
    {'title': '허니와 클로버', 'director': 'J.C.STAFF'},
]
# [동작원리-1] 이 리스트도 "서버가 켜질 때" 메모리에 로드됨.
#             즉, 서버가 살아있는 동안 movie_list는 계속 유지됨(전역 변수).
#             서버를 재시작하면 movie_list도 다시 초기화된다.


# -------------------------
# 루트 페이지 (/)
# -------------------------
def index(request):
    # [동작원리-2] 아래 함수들은 "요청이 들어올 때만" 실행된다.
    #             (runserver 켤 때 자동 실행 X)
    return HttpResponse("<h1>hello</h1>")
    # [동작원리-3] HttpResponse는 "즉시 문자열을 응답"한다.
    #             템플릿 렌더링 없이 바로 브라우저로 보내는 방식.


# -------------------------
# 책 목록 페이지 (/book_list/)
# -------------------------
def book_list(request):
    return render(
        request,
        'book_list.html',
        {'range': range(0, 10)}
    )
    # [동작원리-4] render()는 3단계를 내부에서 수행한다.
    #   ① templates 폴더에서 'book_list.html' 파일을 찾는다.
    #   ② context 딕셔너리({'range': range(0,10)})를 템플릿에 주입한다.
    #   ③ 완성된 HTML 문자열을 HttpResponse로 감싸서 브라우저에 반환한다.


# -------------------------
# 책 상세 페이지 (/book/숫자/)
# -------------------------
def book(request, num):
    # [동작원리-5] num은 URL 패턴에서 <int:num> 으로 추출된 값.
    #             URL에서 숫자를 뽑아서 view 함수 인자로 꽂아준다.
    return render(
        request,
        'book_detail.html',
        {'num': num}
    )


# -------------------------
# 언어 페이지 (/language/문자열/)
# -------------------------
def language(request, lang):
    # [동작원리-6] lang도 URL에서 <str:lang>으로 추출됨.
    #             예) /language/ko/ → lang="ko"
    return HttpResponse(f'<h1>{lang} 언어페이지 입니다.</h1>')


# -------------------------
# movie 목록 페이지 (/movie/)
# -------------------------
def movie(request):
    return render(
        request,
        'movies.html',
        {'movie_list': movie_list}
    )
    # [동작원리-7] movie_list는 전역 변수라서 view에서 그대로 참조 가능.
    #             템플릿에서는 {% for m in movie_list %} 같은 형태로 사용.


# -------------------------
# movie 상세 페이지 (/movie/숫자/)
# -------------------------
def movie_detail(request, index):
    # [동작원리-8] /movie/<int:index>/ 로 들어오면
    #             Django가 URL에서 index 숫자를 뽑아 여기로 넣는다.
    if index < 0 or index >= len(movie_list):
        # [동작원리-9] raise Http404는 "강제로 404 응답"을 만든다.
        #             즉, 아래 코드를 더 실행하지 않고 중단.
        raise Http404("Movie not found")

    movie = movie_list[index]
    # [동작원리-10] 유효한 index면 해당 영화 dict 1개를 선택.

    return render(request, 'movie.html', {'movie': movie})


# -------------------------
# 구구단 페이지 (/gugu/숫자/)
# -------------------------
def gugu(request, num):
    # [동작원리-11] /gugu/<int:num>/ 로 들어오면 num이 여기로 들어온다.

    if num < 2:
        # [동작원리-12] redirect('gugu', num=2)
        #   - 'gugu'는 아래 urlpatterns에 있는 name='gugu' 를 의미한다.
        #   - Django가 name='gugu'에 해당하는 URL 패턴을 찾아서
        #     num=2를 끼워 URL을 만든 뒤(예: /gugu/2/) 그쪽으로 이동시킨다.
        return redirect('gugu', num=2)

    result = [(i, num * i) for i in range(1, 10)]
    # [동작원리-13] result는 [(1,2), (2,4), ...] 형태의 리스트
    #             템플릿에서 i와 곱 결과를 같이 보여주기 좋게 만든 구조.

    context = {
        'num': num,
        'result': result,
    }
    # [동작원리-14] context 키 이름(num/result)과
    #             템플릿에서 쓰는 {{ num }}, {% for x in result %}가 반드시 일치해야 한다.

    return render(request, 'gugu.html', context)
    # [동작원리-15] 최종적으로 HTML 응답 반환


# -------------------------
# URL ↔ View 연결부 (라우터)
# -------------------------
urlpatterns = [
    path('admin/', admin.site.urls),
    # [동작원리-16] /admin/ 요청이면 Django가 제공하는 admin 사이트로 연결

    path('', index),
    # [동작원리-17] / 요청이면 index(request) 실행

    path('book_list/', book_list),
    # [동작원리-18] /book_list/ 요청이면 book_list(request) 실행

    path('book/<int:num>/', book),
    # [동작원리-19] /book/3/ 요청이면 Django가 3을 뽑아서 book(request, 3) 호출

    path('language/<str:lang>/', language),
    # [동작원리-20] /language/ko/ 요청이면 language(request, "ko") 호출

    path('movie/', movie),
    # [동작원리-21] /movie/ 요청이면 movie(request) 호출

    path('movie/<int:index>/', movie_detail),
    # [동작원리-22] /movie/1/ 요청이면 movie_detail(request, 1) 호출

    path('gugu/', lambda request: redirect('gugu', num=2)),
    # [동작원리-23] /gugu/ 요청은 숫자가 없어서 원래는 매칭이 애매함.
    #             그래서 "기본값 페이지"로 보내기 위해 강제 redirect를 둔 것.
    #             lambda는 "이 자리에서만 쓰는 1회용 view 함수"라고 생각하면 된다.

    path('gugu/<int:num>/', gugu, name='gugu'),
    # [동작원리-24] /gugu/5/ 요청이면 gugu(request, 5) 실행
    #             name='gugu' 덕분에 redirect('gugu', num=2) 같은 "이름 기반 이동"이 가능해진다.
]
# [동작원리-25] urlpatterns 자체는 "서버가 켜질 때" 한 번 로딩되어 URL 매칭표를 만든다.
#             요청이 들어오면 Django는 이 표를 위에서 아래로 순서대로 비교해서
#             "처음으로 매칭되는" path의 view를 실행한다.
