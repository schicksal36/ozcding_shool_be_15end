from django.http import Http404, HttpResponse
from django.shortcuts import render

def bookmark_list(request):
    return HttpResponse('<h1>북마크 리스트 페이지입니다.</h1>')

def bookmark_detail(request, num):
    return HttpResponse(f'<h1>{num}번 북마크 상세 페이지</h1>')
