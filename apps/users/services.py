from django.utils import timezone
from typing import Dict

from .models import CustomUser
from .utils import CodeGenerator, TokenService, DateTimeService
from .exceptions import (
    UserNotFoundError,
    AuthenticationError,
    InvalidVerificationCodeError,
    ExpiredVerificationCodeError,
    InactiveUserError,
    InvalidPasswordError,
    EmailAlreadyExistsError,
)


class UserService:
    """
    사용자 도메인의 핵심 비즈니스 로직을 담당하는 서비스

    책임:
    - 사용자 생성
    - 사용자 조회
    - 사용자 인증
    - 로그인 시간 관리
    """

    @staticmethod
    def create_user(email: str, password: str, nickname: str = '') -> CustomUser:
        """
        신규 사용자 생성

        - CustomUserManager.create_user()를 사용하여
          비밀번호 해싱 및 기본 필드 초기화를 처리한다.
        - 중복 이메일인 경우 EmailAlreadyExistsError 발생
        """
        from django.db import IntegrityError
        
        try:
            return CustomUser.objects.create_user(
                email=email,
                password=password,
                nickname=nickname,
            )
        except IntegrityError:
            raise EmailAlreadyExistsError()

    @staticmethod
    def get_user_by_email(email: str) -> CustomUser:
        """
        이메일을 기준으로 사용자 조회

        - 사용자가 존재하지 않으면 UserNotFoundError 발생
        """
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise UserNotFoundError()

    @staticmethod
    def authenticate_user(email: str, password: str) -> CustomUser:
        """
        이메일 + 비밀번호 기반 사용자 인증

        검증 순서:
        1. 이메일 존재 여부 확인
        2. 비밀번호 검증
        3. 계정 활성화 여부 확인
        """
        # 이메일로 사용자 조회 (대소문자 구분 없이)
        try:
            user = CustomUser.objects.get(email__iexact=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationError()

        if not user.check_password(password):
            raise AuthenticationError()

        if not user.is_active:
            raise InactiveUserError()

        return user

    @staticmethod
    def update_last_login(user: CustomUser) -> None:
        """
        사용자의 마지막 로그인 시간을 현재 시각으로 갱신
        """
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

    @staticmethod
    def check_email_exists(email: str) -> bool:
        """
        이메일 중복 여부 확인

        - 회원가입 시 중복 체크 용도로 사용
        """
        return CustomUser.objects.filter(email=email).exists()


class EmailVerificationService:
    """
    이메일 인증 관련 비즈니스 로직 서비스

    책임:
    - 이메일 인증 코드 발급
    - 이메일 인증 코드 검증
    """

    @staticmethod
    def send_verification_code(email: str) -> str:
        """
        이메일 인증 코드 발급

        - 6자리 인증 코드 생성
        - 인증 코드 및 만료 시간(10분)을 사용자에 저장
        """
        user = UserService.get_user_by_email(email)

        code = CodeGenerator.generate_verification_code()

        user.email_verification_code = code
        user.email_verification_code_expires_at = DateTimeService.get_expiration_time(minutes=10)
        user.save(update_fields=['email_verification_code', 'email_verification_code_expires_at'])

        return code

    @staticmethod
    def verify_code(email: str, code: str) -> None:
        """
        이메일 인증 코드 검증 및 인증 완료 처리

        검증 항목:
        - 코드 일치 여부
        - 코드 만료 여부
        """
        user = UserService.get_user_by_email(email)

        if user.email_verification_code != code:
            raise InvalidVerificationCodeError()

        if DateTimeService.is_expired(user.email_verification_code_expires_at):
            raise ExpiredVerificationCodeError()

        user.email_verified = True
        user.email_verification_code = None
        user.email_verification_code_expires_at = None
        user.save(update_fields=[
            'email_verified',
            'email_verification_code',
            'email_verification_code_expires_at',
        ])


class PasswordResetService:
    """
    비밀번호 재설정 관련 비즈니스 로직 서비스

    책임:
    - 비밀번호 재설정 코드 발급
    - 비밀번호 변경 처리
    """

    @staticmethod
    def request_reset(email: str) -> str:
        """
        비밀번호 재설정 요청 처리

        - 재설정 코드 생성
        - 코드 만료 시간은 30분으로 설정
        """
        user = UserService.get_user_by_email(email)

        code = CodeGenerator.generate_reset_code()

        user.email_verification_code = code
        user.email_verification_code_expires_at = DateTimeService.get_expiration_time(minutes=30)
        user.save(update_fields=['email_verification_code', 'email_verification_code_expires_at'])

        return code

    @staticmethod
    def confirm_reset(email: str, new_password: str) -> None:
        """
        비밀번호 재설정 완료 처리

        - 새 비밀번호를 해싱하여 저장
        - 사용된 인증 코드는 초기화
        """
        user = UserService.get_user_by_email(email)

        user.set_password(new_password)
        user.email_verification_code = None
        user.email_verification_code_expires_at = None
        user.save(update_fields=[
            'password',
            'email_verification_code',
            'email_verification_code_expires_at',
        ])


class AuthService:
    """
    인증 흐름을 조합하는 파사드(Facade) 서비스

    - UserService, TokenService를 조합하여
      로그인 / 회원가입 플로우를 완성한다.
    """

    @staticmethod
    def login(email: str, password: str) -> Dict:
        """
        로그인 처리

        처리 흐름:
        1. 사용자 인증
        2. 마지막 로그인 시간 업데이트
        3. JWT 토큰 발급
        """
        user = UserService.authenticate_user(email, password)

        UserService.update_last_login(user)

        tokens = TokenService.generate_tokens(user)

        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'nickname': user.nickname,
            },
            'tokens': tokens,
        }

    @staticmethod
    def register(email: str, password: str, nickname: str = '') -> Dict:
        """
        회원가입 처리

        - 사용자 생성
        - 즉시 JWT 토큰 발급
        """
        user = UserService.create_user(email, password, nickname)

        tokens = TokenService.generate_tokens(user)

        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'nickname': user.nickname,
            },
            'tokens': tokens,
        }
