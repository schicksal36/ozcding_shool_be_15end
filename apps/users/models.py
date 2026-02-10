from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, nickname=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            nickname=nickname or '',
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('슈퍼유저는 is_staff=True여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('슈퍼유저는 is_superuser=True여야 합니다.')
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    커스텀 사용자 모델
    
    상속 구조:
    - AbstractBaseUser: 비밀번호 관리, 인증 관련 메서드 제공
    - PermissionsMixin: Django 권한 시스템 호환 (groups, user_permissions 필드 자동 추가)
    
    동작 원리:
    1. USERNAME_FIELD = 'email': 로그인 시 사용할 필드 지정
    2. REQUIRED_FIELDS = []: createsuperuser 명령 시 추가로 요구하는 필드
    3. objects = CustomUserManager(): 사용자 생성/조회 시 사용할 매니저 지정
    """
    
    # ========== 필수 정보 필드 ==========
    email = models.EmailField(
        unique=True,
        help_text="이메일 주소 (로그인용, 고유값, 이메일 형식 검증 자동 수행)"
    )
    nickname = models.CharField(
        max_length=50,
        blank=True,
        help_text="닉네임 (프로필 별명, 비워둘 수 있음, 최대 50자)"
    )
    
    # ========== 프로필 정보 필드 ==========
    bio = models.TextField(
        blank=True,
        help_text="자기소개 (프로필 메시지, 비워둘 수 있음, 텍스트 길이 제한 없음)"
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        help_text="프로필 이미지 (MEDIA_ROOT/profiles/ 경로에 저장, 비워둘 수 있음)"
    )
    
    # ========== 이메일 인증 관련 필드 ==========
    email_verified = models.BooleanField(
        default=False,
        help_text="이메일 인증 여부 (True: 인증 완료, False: 미인증, 기본값: False)"
    )
    email_verification_code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        help_text="이메일 인증 코드 (6자리 숫자, 인증 완료 후 None으로 변경)"
    )
    email_verification_code_expires_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="인증 코드 만료 시간 (Datetime 객체, 만료 후 None으로 변경)"
    )
    
    # ========== 관리/시스템 관련 필드 ==========
    is_active = models.BooleanField(
        default=True,
        help_text="계정 활성화 여부 (True: 활성, False: 비활성/정지, 기본값: True)"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="스태프(관리자페이지 접근권한) 여부 (True: Django Admin 접근 가능, 기본값: False)"
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text="슈퍼유저(전체 권한) 여부 (True: 모든 권한 보유, 기본값: False)"
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        help_text="가입일 (자동 기록, timezone.now()로 현재 시간 저장)"
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        help_text="마지막 로그인 일시 (자동 기록, 비워둘 수 있음, 로그인 시 업데이트)"
    )
    
    # 사용자 객체 반환 매니저 지정
    objects = CustomUserManager()
    
    # Django 유저 인증시 사용할 필드 지정
    USERNAME_FIELD = 'email'              # 기본 로그인 필드 (email로 로그인)
    REQUIRED_FIELDS = []                  # createsuperuser 명령시 추가로 요구하는 필드 (email만 필요)
    
    class Meta:
        """
        모델 메타데이터 설정
        """
        verbose_name = '사용자'              # 단수형 이름 (Django Admin에서 표시)
        verbose_name_plural = '사용자들'     # 복수형 이름 (Django Admin에서 표시)
        db_table = 'users'                  # 실제 데이터베이스 테이블명 명시
        ordering = ['-date_joined']          # 기본 정렬 순서 (가입일 내림차순, 최신순)
    
    def __str__(self):
        """
        객체를 문자열로 변환할 때 사용 (Django Admin, shell 등에서 표시)
        
        동작:
        - CustomUser 객체를 print()하거나 문자열로 변환할 때 email 반환
        - 예: print(user) -> "test@example.com"
        """
        return self.email
    
    def get_full_name(self):
        """
        전체 이름 반환 메서드
        
        동작:
        - 닉네임이 있으면 닉네임 반환
        - 닉네임이 없으면 email 반환
        
        사용 예시:
        - user.nickname = "홍길동" -> "홍길동" 반환
        - user.nickname = "" -> "test@example.com" 반환
        """
        return self.nickname or self.email
    
    def get_short_name(self):
        """
        짧은 이름 반환 메서드
        
        동작:
        - get_full_name()과 동일하게 동작
        - Django의 일부 기능에서 사용됨
        
        사용 예시:
        - user.nickname = "홍길동" -> "홍길동" 반환
        - user.nickname = "" -> "test@example.com" 반환
        """
        return self.nickname or self.email
