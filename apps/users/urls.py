"""
사용자 앱 URL 라우팅 설정

역할:
- HTTP 요청 URL을 해당하는 뷰로 매핑
- URL 패턴 정의 및 이름 지정

동작 원리:
1. 클라이언트가 HTTP 요청 전송 (예: POST /api/users)
2. Django의 URL 라우터가 urls.py를 순회하며 패턴 매칭
3. 매칭되는 패턴을 찾으면 해당 뷰의 as_view() 메서드 호출
4. 뷰가 요청 처리 후 응답 반환

URL 패턴 구조:
- path('패턴', 뷰.as_view(), name='이름')
- 패턴: 정규식 또는 문자열 패턴
- 뷰: 처리할 뷰 클래스
- name: URL 이름 (reverse() 함수로 사용)

app_name:
- URL 네임스페이스 설정
- 다른 앱과 URL 이름 충돌 방지
- 사용 예: reverse('users:register')
"""
from django.urls import path
from . import views

# URL 네임스페이스 설정 (다른 앱과 이름 충돌 방지)
app_name = 'users'

# URL 패턴 목록 (순서 중요: 위에서부터 매칭 시도)
urlpatterns = [
    # ========== 인증 관련 URL ==========
    
    # 회원가입
    # POST /api/users
    # 인증: 불필요
    path('api/signup/', views.RegisterView.as_view(), name='register'),
    
    # 로그인
    # POST /api/login
    # 인증: 불필요
    path('api/login/', views.LoginView.as_view(), name='login'),
    
    # 로그아웃
    # POST /api/logout
    # 인증: 필요 (JWT 토큰)
    path('api/logout', views.LogoutView.as_view(), name='logout'),
    
    # ========== 사용자 정보 관련 URL ==========
    
    # 유저 정보 조회/수정 (설계서 기준: ProfileView, RetrieveUpdateAPIView)
    # GET /api/users/me/ (조회)
    # PATCH /api/users/me/ (수정)
    # 인증: 필요 (JWT 토큰)
    path('api/users/me/', views.ProfileView.as_view(), name='user-detail'),
    
    # 회원탈퇴 (설계서 기준: UserDeleteView, DestroyAPIView)
    # DELETE /api/users/account/
    # 인증: 필요 (JWT 토큰)
    path('api/users/account/', views.UserDeleteView.as_view(), name='user-delete'),
    
    # 유저 프로필 조회/수정 (설계서 기준: ProfileView, RetrieveUpdateAPIView)
    # GET /api/users/me/profile/ (조회)
    # PATCH /api/users/me/profile/ (수정)
    # 인증: 필요 (JWT 토큰)
    path('api/users/me/profile/', views.UserProfileView.as_view(), name='profile-detail'),
    
    # ========== 이메일 인증 관련 URL ==========
    
    # 이메일 인증 코드 발송 (설계서 기준: EmailView)
    # POST /api/users/email/verify/
    # 인증: 불필요
    path('api/users/email/verify/', views.EmailView.as_view(), name='email-send'),
    
    # 이메일 인증 확인
    # POST /api/users/email/verify/confirm/
    # 인증: 불필요
    path('api/users/email/verify/confirm/', views.EmailVerifyView.as_view(), name='email-verify'),
    
    # 이메일 가입 여부 확인 (설계서 기준: EmailExistCheckView)
    # POST /api/users/find/email/
    # 인증: 불필요
    path('api/users/find/email/', views.EmailExistCheckView.as_view(), name='email-check'),
    
    # ========== 비밀번호 재설정 관련 URL ==========
    
    # 비밀번호 재설정 요청 (설계서 기준: PasswordResetRequestView)
    # POST /api/users/password/reset/
    # 인증: 불필요
    path('api/users/password/reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
    
    # 비밀번호 재설정 완료
    # POST /api/users/password/reset/confirm/
    # 인증: 불필요
    path('api/users/password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]