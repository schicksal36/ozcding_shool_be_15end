"""
Django Admin 설정 모듈

역할:
- Django Admin 페이지에서 CustomUser 모델 관리
- 사용자 목록 조회, 검색, 필터링
- 사용자 정보 수정, 삭제

동작 원리:
1. @admin.register() 데코레이터로 모델 등록
2. BaseUserAdmin을 상속하여 기본 사용자 관리 기능 사용
3. list_display, list_filter 등으로 화면 커스터마이징

접근 방법:
- URL: /admin/
- 권한: is_staff=True인 사용자만 접근 가능
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    커스텀 사용자 관리자 클래스
    
    역할:
    - Django Admin에서 CustomUser 모델 관리
    - 사용자 목록 표시, 검색, 필터링 설정
    - 사용자 생성/수정 폼 설정
    
    BaseUserAdmin 상속:
    - Django의 기본 사용자 관리 기능 사용
    - 비밀번호 해싱, 권한 관리 등 자동 처리
    """
    
    # 목록 화면에 표시할 필드
    # Admin 페이지에서 사용자 목록을 볼 때 표시되는 컬럼
    list_display = (          # 사용자 아이디
        'email',             # 이메일
        'nickname',          # 닉네임
        'email_verified',    # 이메일 인증 여부
        'is_staff',          # 스태프 여부
        'is_active',         # 활성화 여부
        'date_joined'        # 가입일
    )
    
    # 필터 옵션 (오른쪽 사이드바에 표시)
    # 목록 화면에서 필터링할 수 있는 옵션
    list_filter = (
        'is_staff',          # 스태프 여부로 필터
        'is_superuser',      # 슈퍼유저 여부로 필터
        'is_active',         # 활성화 여부로 필터
        'email_verified',    # 이메일 인증 여부로 필터
        'date_joined'        # 가입일로 필터
    )
    
    # 검색 가능한 필드
    # 검색창에서 검색할 수 있는 필드
    search_fields = (
        'email',     # 이메일로 검색
        'nickname'   # 닉네임으로 검색
    )
    
    # 정렬 기준 (기본 정렬)
    # 목록 화면의 기본 정렬 순서 (-는 내림차순)
    ordering = ('-date_joined',)  # 가입일 내림차순 (최신순)
    
    # 사용자 수정 화면의 필드 그룹 설정
    # 사용자 정보를 수정할 때 보이는 필드 그룹
    fieldsets = (
        # 기본 정보 그룹
        (None, {'fields': ('email', 'password')}),
        
        # 개인 정보 그룹
        ('개인 정보', {
            'fields': ( 'nickname', 'profile_image')
        }),
        
        # 인증 정보 그룹
        ('인증 정보', {
            'fields': (
                'email_verified',
                'email_verification_code',
                'email_verification_code_expires_at'
            )
        }),
        
        # 권한 그룹
        ('권한', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        
        # 중요한 날짜 그룹
        ('중요한 날짜', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # 사용자 생성 화면의 필드 설정
    # 새 사용자를 생성할 때 보이는 필드
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # 넓은 레이아웃
            'fields': (
                'email',      # 이메일 (로그인용, 필수)
                'password1',  # 비밀번호 입력
                'password2'   # 비밀번호 확인
            ),
        }),
    )
