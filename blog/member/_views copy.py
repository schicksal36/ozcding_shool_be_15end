from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login, logout as django_logout
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import resolve_url

class SignUpView(FormView):
    """
    [회원가입 기능] - CBV 버전

    ─────────────────────────────────────────────────────────────
    기능 요약:
      - 회원가입 폼(UserCreationForm) 입력값 검증 및 저장
      - 새로운 유저가 생성되면 즉시 로그인 처리
      - 회원가입 성공 후 설정된 리디렉트 URL로 이동
    ─────────────────────────────────────────────────────────────
    동작 원리:
      1. GET 요청 시: 빈 회원가입 폼을 템플릿에 렌더링 (회원가입폼 HTML)
      2. POST 요청 시: 폼 제출 데이터로 유효성 검증
         2-1. 유효하면 → user DB 저장 및 로그인 처리 → success_url로 이동
         2-2. 실패시 → 에러메시지 포함 재출력
    """
    template_name = "registration/signup.html"   # 사용할 템플릿 경로 지정
    form_class = UserCreationForm                # 사용할 폼 클래스 지정
    # success_url: 실제로는 get_success_url() 메서드에서 동적으로 처리함
    success_url = reverse_lazy('login')          # (임시값)

    def form_valid(self, form):
        """
        form_valid: 폼이 유효할 경우 호출됨. 
        회원 계정 생성 및 성공시 즉시 세션 로그인 처리까지 한다. (자동 로그인)
        """
        # 폼의 save(): DB에 User 생성
        user = form.save()
        # 새로 만든 user로 로그인 세션 정보 갱신 (로그인 상태로 전환)
        django_login(self.request, user)
        # 부모(FormView) 메서드를 호출하여 이후 처리 진행 (리다이렉트 등)
        return super().form_valid(form)

    def get_success_url(self):
        """
        회원가입 & 로그인 이후 리디렉트할 URL 반환
        """
        return settings.LOGIN_REDIRECT_URL    # settings.py에 지정된 redirect URL로 이동

class LoginView(FormView):
    """
    [로그인 기능] - CBV 버전

    ─────────────────────────────────────────────────────────────
    기능 요약:
      - 아이디/비밀번호 검증 (AuthenticationForm)
      - 인증 성공시 세션에 로그인 처리
      - next 파라미터가 있으면 해당 URL로, 없으면 기본 로그인 후 리다이렉트 URL로 이동
    ─────────────────────────────────────────────────────────────
    동작 원리:
      1. GET 요청 시: 로그인 폼 렌더링
      2. POST 요청 시: 로그인 검증 (is_valid → form.get_user())
         2-1. 성공 → 세션에 로그인유저 저장 → success_url로 리다이렉트
         2-2. 실패 → 에러 메시지와 폼 재출력
    """
    template_name = "registration/login.html"    # 템플릿 경로
    form_class = AuthenticationForm              # 로그인 폼
    success_url = reverse_lazy('login')          # (임시값, 실제는 하단 get_success_url에서 결정)

    def get_form_kwargs(self):
        """
        AuthenticationForm은 request 객체가 반드시 필요하다.
        (폼 내부에서 request.user 등 접근을 위함)
        """
        # 부모의 get_form_kwargs()로 기본값 셋팅
        kwargs = super().get_form_kwargs()
        # request객체도 kwargs에 추가
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """
        폼이 유효하면 세션에 해당 user로 로그인 처리를 한다.
        (django_login 함수 사용, request와 인증된 유저객체 넘김)
        """
        user = form.get_user()               # 인증된 User 객체 반환
        django_login(self.request, user)     # 로그인 처리 (세션정보 업데이트)
        return super().form_valid(form)      # 이후 기본 프로세스 진행 (리다이렉트 등)

    def get_success_url(self):
        """
        로그인 성공 후 리다이렉트할 URL 결정
        1. 쿼리스트링에 next 파라미터(request.GET['next'])가 있으면 해당 URL로 리다이렉트
           - 단, url_has_allowed_host_and_scheme()로 이 URL이 안전한지 검사 (오픈리다이렉트 방지)
        2. 없으면 settings.LOGIN_REDIRECT_URL로 이동(보통 "/")
        """
        next_url = self.request.GET.get('next')
        # next 파라미터가 있고, 현재 서버 기준으로 허용된 경로라면 → 해당 URL 리턴
        if next_url and url_has_allowed_host_and_scheme(next_url, self.request.get_host()):
            return next_url
        # 아니면 기본 리다이렉트 URL 사용
        return settings.LOGIN_REDIRECT_URL

class LogoutView(RedirectView):
    """
    [로그아웃 기능] - CBV 버전

    ─────────────────────────────────────────────────────────────
    기능 요약:
      - 현재 로그인된 사용자를 로그아웃(세션 삭제)
      - 로그아웃 후, 설정 지정된 URL로 강제 리다이렉트
    ─────────────────────────────────────────────────────────────
    동작 원리:
      1. 사용자가 /logout/ 등의 URL로 접근시 get_redirect_url() 실행
      2. 내부적으로 django_logout(request)로 세션 완전 삭제 (로그인정보 만료)
      3. 최종적으로 LOGIN_REDIRECT_URL로 이동
    """
    pattern_name = None  # 직접 get_redirect_url 오버라이드 방식 사용 (pattern_name 무의미)

    def get_redirect_url(self, *args, **kwargs):
        """
        로그아웃 처리 후 이동할 URL 반환
        """
        django_logout(self.request)                      # 세션 초기화, 로그인 해제
        return resolve_url(settings.LOGIN_REDIRECT_URL)  # 안전하게 지정 위치로 리다이렉트

