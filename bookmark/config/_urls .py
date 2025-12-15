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
from django.shortcuts import render 
# ↑ HttpResponse : 화면에 문자열/HTML 응답을 보내기 위한 클래스
# ↑ Http404      : 잘못된 URL 접근 시 404 에러를 발생시키는 예외

# -------------------------
# 메모리 기반 영화 데이터
# -------------------------
# DB를 아직 안 쓰고 있기 때문에
# 서버가 실행 중일 때만 살아있는 파이썬 리스트
movie_list = [
    {'title': '귀멸의 칼날', 'director': 'ufotable'},
    {'title': '주토피아 2', 'director': 'Disney'},
    {'title': '사무라이 참프루', 'director': 'Manglobe'},
    {'title': '허니와 클로버', 'director': 'J.C.STAFF'},
]


# -------------------------
# 루트 페이지 (/)
# -------------------------
def index(request):
    # 브라우저에서 "/"로 접속하면 실행되는 함수
    # request 객체에는 요청 정보(GET, POST, 헤더 등)가 들어 있음
    return HttpResponse("<h1>hello</h1>")


# -------------------------
# 책 목록 페이지 (/book_list/)
# -------------------------
def book_list(request):
    book_text = ''
    # range(0, 10) → 0부터 9까지
    for i in range(0, 10):
        book_text += f'book {i}<br>'
    # 문자열을 HTML로 그대로 반환
    return HttpResponse(book_text)


# -------------------------
# 책 상세 페이지 (/book/숫자/)
# -------------------------
def book(request, num):
    # URL에서 받은 num이 그대로 함수 인자로 들어옴
    return HttpResponse(f'<h1>book {num}</h1>')


# -------------------------
# 언어 페이지 (/language/문자열/)
# -------------------------
def language(request, lang):
    # <str:lang> 으로 받은 값이 lang 변수에 들어옴
    return HttpResponse(f'<h1>{lang} 언어페이지 입니다.</h1>')


# -------------------------
# movie 목록 페이지
# (/movie/)
# -------------------------
# movie의 title만 보여줌
def movie(request):
    #movie_titles = [movie['title'] for index, movie in enumerate(movie_list)]
    # ↑ 예전에 생각했던 "title만 따로 뽑는 방식"
    # ↑ 지금은 아래 방식이 더 직관적이라 사용 안 함 (학습용으로 유지)

    #response_text = ''

    # enumerate(movie_list)
    # index → 0,1,2,3 (URL에 사용)
    # movie → {'title': ..., 'director': ...}
    #for index, movie in enumerate(movie_list):
        # 각 제목을 클릭하면 상세 페이지로 이동
        # /movie/0/, /movie/1/ ...
    #    response_text += f'<a href="/movie/{index}/">{movie["title"]}</a><br>'

    # 완성된 HTML 문자열을 브라우저로 반환
    #return HttpResponse(response_text)
    return render(
    request,'movies.html',{'movie_list': movie_list}
)


    #movie_titles =[]
    #for movie in movie_list:
    #    movie_titles.append(movie[titles])
    # ↑ 완전 초기 방식
    # ↑ 리스트 컴프리헨션 이해 전 단계의 사고 흔적 (삭제 ❌)


# -------------------------
# movie 상세 페이지
# (/movie/숫자/)
# -------------------------
def movie_detail(request, index):
    # index는 URL에서 받은 값
    # 예: /movie/2/ → index = 2

    # index 범위 검사
    # 존재하지 않는 번호 접근 시 404 에러 발생
    if index < 0 or index >= len(movie_list):
        raise Http404("Movie not found")

    # 정상 범위면 해당 영화 딕셔너리 꺼냄
    movie = movie_list[index]

    # 제목과 감독을 HTML로 반환
    return HttpResponse(
        f"<h1>{movie['title']}</h1>"
        f"<p>Director: {movie['director']}</p>"
    )


# -------------------------
# URL ↔ View 연결부
# -------------------------
urlpatterns = [
    path('admin/', admin.site.urls),

    # "/" → index 함수 실행
    path('', index),

    # "/book_list/" → book_list 실행
    path('book_list/', book_list),

    # "/book/3/" → book(request, num=3)
    path('book/<int:num>/', book),

    # "/language/python/" → language(request, lang="python")
    path('language/<str:lang>/', language),

    # "/movie/" → movie 목록 페이지
    path('movie/', movie),

    # "/movie/1/" → movie_detail(request, index=1)
    path('movie/<int:index>/', movie_detail),
]

