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

"""
✅ 이 파일은 "Django가 요청을 받았을 때 어떤 함수를 실행할지(라우팅)" + "그 함수가 무엇을 응답할지(view)"
를 한 곳에 모아둔 예시 코드다.

📌 Django 동작 큰 흐름
1) 브라우저가 URL로 요청 보냄  (예: GET /movie/ )
2) Django는 ROOT_URLCONF(보통 config/settings.py에 설정된 urls.py)를 읽음
3) urlpatterns에서 요청 URL과 일치하는 path를 찾음
4) 매칭된 path에 연결된 view 함수(index, movies 등)를 실행
5) view 함수가 HttpResponse를 리턴하면, 그게 브라우저 화면에 그대로 표시됨
"""
from django.http import HttpResponse, Http404
from django.contrib import admin
from django.urls import path
from django.shortcuts import render


movie_list = [
    {'title': '귀멸의 칼날', 'director': 'ufotable'},
    {'title': '주토피아 2', 'director': 'Disney'},
    {'title': '사무라이 참프루', 'director': 'Manglobe'},
    {'title': '허니와 클로버', 'director': 'J.C.STAFF'},
]


def index(request):
    return HttpResponse('hello?')


def book_list(request):
    #book_text = ''
    #for i in range(10):
        #book_text += f'book{i}<br>'
    return render(request,'book_list.html',{'range': range(0,10)})


def book(request, num):
    return render(request,'book_detali.html',{'num':num})


def language(request, lang):
    return HttpResponse(f'<h1>{lang} 언어 페이지 입니다.</h1>')


def python(request):
    return HttpResponse('python 페이지 입니다.')


def movies(request):
    return render(
        request,
        'movies.html',
        {'movie_list':movie_list}
        )


def movie_detail(request, index):
    if index > len(movie_list) - 1:
        raise Http404

    movie = movie_list[index]

    context = {
        'movie_list': movie_list, 
        'index': index}

    return render(request,'movie.html',context)

def gugu(request, num) : 

    context =  {
        'num': num,
        'results' : [num * i for i in range(1,10)]
    }
    return render(
        request,
        'gugu.html',
        context )



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('book_list/', book_list),
    path('book_list/<int:num>/', book),
    path('language/python/', python),
    path('language/<str:lang>/', language),
    path('movie/', movies),
    path('movie/<int:index>/', movie_detail),
    path('gugu/<int:num>/', gugu),
]
