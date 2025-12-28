from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

def sign_up(request):
    """
    회원가입(sign up) 뷰
    - POST 요청이면 전송된 폼 데이터를 바탕으로 UserCreationForm을 생성한다.
    - form이 유효할 때:
        1. form.save()로 새 사용자 객체를 저장
        2. 새 사용자를 로그인(django_login) 처리하여 세션에 등록
        3. 로그인이 끝나면 settings.LOGIN_REDIRECT_URL로 리디렉트
    - form이 유효하지 않거나 GET 요청일 때:
        1. (request.POST or None)으로 빈 폼 혹은 에러 포함 폼을 생성
        2. 회원가입 페이지(templates/registration/signup.html)에 form을 넘겨 렌더링
    """
    form = UserCreationForm(request.POST or None)  # POST 데이터로 폼 생성(없으면 빈 폼)
    if form.is_valid():  # 폼 유효성 검사
        user = form.save()  # 새 사용자를 DB에 저장
        django_login(request, user)  # 방금 만든 사용자로 바로 로그인
        return redirect(settings.LOGIN_REDIRECT_URL)  # 로그인 후 이동
    return render(request, "registration/signup.html", {"form": form})  # 폼과 함께 회원가입 페이지 렌더

def login(request):
    """
    로그인(login) 뷰
    - POST라면, 사용자가 제출한 데이터를 AuthenticationForm에 담는다.
    - form이 유효하면:
        1. get_user()로 인증된 사용자 객체 추출
        2. 해당 사용자로 로그인(django_login)
        3. redirect_to: 로그인 전 가려고 했던 페이지가 있으면 그리로, 없으면 LOGIN_REDIRECT_URL로 리디렉트
    - GET이라면, 빈 AuthenticationForm 생성
    - 로그인 템플릿(templates/registration/login.html)에 form을 넘겨 렌더링
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # POST 데이터로 폼 생성
        if form.is_valid():  # 폼 유효성 검사(아이디/비밀번호 검증)
            user = form.get_user()  # 인증된 유저 정보 가져오기
            django_login(request, user)  # 해당 유저로 로그인(session 등록)
            redirect_to = request.GET.get("next")  # 로그인 직전 원래 가고 싶었던 URL(없으면 None)
            if redirect_to:
                return redirect(redirect_to)  # "next" 값이 있다면 해당 URL로 리디렉트
            return redirect(settings.LOGIN_REDIRECT_URL)  # 아니면 설정된 기본 경로로
    else:
        form = AuthenticationForm(request)  # GET 요청: 빈 로그인 폼 생성
    return render(
        request,
        "registration/login.html",
        {"form": form},
    )

def logout(request):
    """
    로그아웃(logout) 뷰
    - django_logout 함수로 현 사용자를 로그아웃(세션 데이터 제거)
    - 로그아웃 후 설정된 LOGIN_REDIRECT_URL로 리디렉트
    """
    django_logout(request)  # 세션에서 사용자 정보 제거 = 로그아웃
    return redirect(settings.LOGIN_REDIRECT_URL)  # 로그아웃 후 지정된 페이지로 이동
