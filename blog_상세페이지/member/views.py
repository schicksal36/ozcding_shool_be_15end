from django.conf import settings
# settings.py에 정의된 설정값(LOGIN_REDIRECT_URL 등)을 읽기 위해 사용

from django.shortcuts import render, redirect
# render  : HTML 템플릿을 렌더링하여 HttpResponse 반환
# redirect: 다른 URL로 이동시키는 응답 반환 (302 Redirect)

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# UserCreationForm   : Django 기본 회원가입 폼 (아이디/비밀번호 생성 + 검증 포함)
# AuthenticationForm: Django 기본 로그인 폼 (아이디/비밀번호 인증)

from django.contrib.auth import login as django_login
# django_login: 인증 성공한 유저를 세션에 저장하여 로그인 상태로 만듦

from django.contrib.auth import logout as django_logout
# django_logout: 세션을 초기화하여 로그아웃 처리


def sign_up(request):
    """
    [회원가입 기능]
    -------------------------------------------------------------------------
    1. UserCreationForm을 사용하여 회원가입 정보를 입력받음
    2. 입력 데이터가 유효하면 DB에 사용자 계정을 생성
    3. 회원가입 직후 자동 로그인 처리
    4. LOGIN_REDIRECT_URL로 이동
    -------------------------------------------------------------------------
    """

    # POST 요청이면 request.POST 데이터를 폼에 바인딩
    # GET 요청이면 빈 회원가입 폼 생성
    form = UserCreationForm(request.POST or None)

    # 폼 유효성 검사
    # - username 중복 여부
    # - 비밀번호 규칙
    # - 비밀번호 확인 일치 여부
    if form.is_valid():

        # 검증된 데이터를 기반으로 User 객체를 생성하고 DB에 저장
        # (비밀번호는 자동으로 해시 처리됨)
        user = form.save()

        # 생성된 User 객체를 세션에 등록하여 즉시 로그인 처리
        # → request.user가 이 user로 설정됨
        django_login(request, user)

        # settings.py에 정의된 로그인 성공 후 이동 경로로 리다이렉트
        # 기본값은 보통 "/"
        return redirect(settings.LOGIN_REDIRECT_URL)

    # 폼 검증에 실패했거나(GET 요청인 경우)
    # 에러 메시지를 포함한 폼을 다시 템플릿으로 전달
    return render(
        request,
        'registration/signup.html',
        {'form': form}
    )


def login(request):
    """
    [로그인 기능]
    -------------------------------------------------------------------------
    1. AuthenticationForm으로 아이디/비밀번호 인증
    2. 인증 성공 시 세션 로그인 처리
    3. 'next' 파라미터가 있으면 해당 페이지로 이동
    4. 없으면 LOGIN_REDIRECT_URL로 이동
    -------------------------------------------------------------------------
    """

    # POST 요청: 로그인 시도
    if request.method == "POST":

        # AuthenticationForm은 request 객체를 함께 전달해야 함
        # (보안/세션/쿠키 검증용)
        form = AuthenticationForm(request, data=request.POST)

        # 아이디/비밀번호 검증
        if form.is_valid():

            # 인증된 사용자 객체(User)를 가져옴
            user = form.get_user()

            # 사용자 정보를 세션에 저장하여 로그인 상태로 만듦
            django_login(request, user)

            # 로그인 전에 접근하려다 튕긴 페이지가 있는지 확인
            # 예) /blog/create/ → 로그인 페이지 → 로그인 성공 → 다시 /blog/create/
            redirect_to = request.GET.get("next")
            if redirect_to:
                return redirect(redirect_to)

            # 별도 목적지가 없다면 기본 리다이렉트 URL로 이동
            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        # GET 요청: 로그인 페이지 최초 접근
        # 빈 로그인 폼 생성
        form = AuthenticationForm(request)

    # 로그인 실패 또는 GET 요청 시
    # 로그인 폼을 다시 렌더링
    return render(
        request,
        "registration/login.html",
        {"form": form},
    )


def logout(request):
    """
    [로그아웃 기능]
    -------------------------------------------------------------------------
    1. 현재 로그인된 사용자의 세션 정보를 삭제
    2. request.user를 AnonymousUser로 변경
    3. 로그아웃 후 LOGIN_REDIRECT_URL로 이동
    -------------------------------------------------------------------------
    """

    # 세션에서 인증 정보 제거
    # 이후 request.user는 AnonymousUser가 됨
    django_logout(request)

    # 로그아웃 완료 후 메인 페이지 등으로 리다이렉트
    return redirect(settings.LOGIN_REDIRECT_URL)
