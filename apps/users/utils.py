"""
유틸리티 함수 모듈

역할:
- 재사용 가능한 유틸리티 함수 제공
- 공통 기능 캡슐화 (코드 생성, 토큰 관리, 날짜/시간 처리)

아키텍처 원칙:
- 단일 책임 원칙(SRP): 각 클래스가 특정 유틸리티 기능만 담당
- 정적 메서드 사용: 인스턴스 생성 없이 사용 가능

사용 예시:
    code = CodeGenerator.generate_verification_code()
    tokens = TokenService.generate_tokens(user)
    expires_at = DateTimeService.get_expiration_time(minutes=10)
"""
import random
import string
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta


class CodeGenerator:
    """
    인증 코드 생성 유틸리티 클래스
    
    역할:
    - 이메일 인증 코드 생성
    - 비밀번호 재설정 코드 생성
    
    동작 원리:
    - random.choices()로 숫자 문자열에서 랜덤 선택
    - 지정된 길이만큼 반복하여 코드 생성
    """
    
    @staticmethod
    def generate_verification_code(length: int = 6) -> str:
        """
        이메일 인증 코드 생성 메서드
        
        동작:
        1. 0-9 숫자 문자열에서 랜덤 선택
        2. 지정된 길이만큼 반복
        3. 문자열로 결합하여 반환
        
        예시:
            generate_verification_code() -> "123456"
            generate_verification_code(4) -> "7890"
        
        :param length: 코드 길이 (기본값: 6)
        :return: 생성된 인증 코드 (문자열)
        """
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def generate_reset_code(length: int = 6) -> str:
        """
        비밀번호 재설정 코드 생성 메서드
        
        동작:
        - generate_verification_code()와 동일한 로직
        - 의미적으로 구분하기 위해 별도 메서드로 분리
        
        :param length: 코드 길이 (기본값: 6)
        :return: 생성된 재설정 코드 (문자열)
        """
        return ''.join(random.choices(string.digits, k=length))


class TokenService:
    """
    JWT 토큰 관련 서비스 클래스
    
    역할:
    - JWT 토큰 생성 (access token, refresh token)
    - 토큰 블랙리스트 관리 (로그아웃 시)
    
    JWT 토큰 구조:
    - Access Token: API 요청 시 사용, 짧은 유효기간 (1시간)
    - Refresh Token: Access Token 갱신용, 긴 유효기간 (7일)
    
    동작 원리:
    1. RefreshToken.for_user()로 사용자에 대한 토큰 생성
    2. access_token은 refresh_token에서 자동 생성
    3. 토큰은 Base64로 인코딩된 JSON 문자열
    """
    
    @staticmethod
    def generate_tokens(user):
        """
        사용자에 대한 JWT 토큰 생성 메서드
        
        동작 과정:
        1. RefreshToken.for_user()로 사용자 정보가 포함된 토큰 생성
        2. 토큰을 문자열로 변환
        3. access_token과 refresh_token을 딕셔너리로 반환
        
        토큰 내용:
        - user_id: 사용자 ID
        - exp: 만료 시간
        - iat: 발급 시간
        - jti: 토큰 고유 ID
        
        :param user: 토큰을 생성할 사용자 객체
        :return: {'refresh': '...', 'access': '...'} 딕셔너리
        """
        # 사용자에 대한 Refresh Token 생성
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),           # Refresh Token (문자열)
            'access': str(refresh.access_token),  # Access Token (문자열)
        }
    
    @staticmethod
    def blacklist_token(refresh_token: str) -> bool:
        """
        토큰을 블랙리스트에 추가하는 메서드
        
        동작 과정:
        1. RefreshToken 객체 생성
        2. blacklist() 메서드로 블랙리스트에 추가
        3. 이후 해당 토큰으로는 재사용 불가능
        
        사용 목적:
        - 로그아웃 시 토큰 무효화
        - 토큰 탈취 시 보안 강화
        
        :param refresh_token: 블랙리스트에 추가할 refresh token
        :return: 성공 시 True, 실패 시 False
        """
        try:
            # RefreshToken 객체 생성
            token = RefreshToken(refresh_token)
            # 블랙리스트에 추가 (데이터베이스에 저장)
            token.blacklist()
            return True
        except Exception:
            # 토큰이 유효하지 않거나 이미 블랙리스트에 있는 경우
            return False


class DateTimeService:
    """
    날짜/시간 관련 유틸리티 클래스
    
    역할:
    - 만료 시간 계산
    - 만료 여부 확인
    
    동작 원리:
    - timezone.now()로 현재 시간 조회 (서버 시간대 기준)
    - timedelta로 시간 더하기/빼기
    """
    
    @staticmethod
    def get_expiration_time(minutes: int = 10) -> timezone.datetime:
        """
        만료 시간 계산 메서드
        
        동작:
        1. 현재 시간 조회 (timezone.now())
        2. 지정된 분만큼 더하기 (timedelta)
        3. 만료 시간 반환
        
        예시:
            get_expiration_time(10) -> 현재 시간 + 10분
            get_expiration_time(30) -> 현재 시간 + 30분
        
        :param minutes: 만료까지의 시간 (분 단위, 기본값: 10)
        :return: 만료 시간 (datetime 객체)
        """
        return timezone.now() + timedelta(minutes=minutes)
    
    @staticmethod
    def is_expired(expires_at) -> bool:
        """
        만료 여부 확인 메서드
        
        동작:
        1. expires_at이 None이면 만료된 것으로 간주 (True 반환)
        2. 현재 시간과 비교하여 만료 여부 확인
        3. expires_at < 현재 시간이면 만료 (True 반환)
        
        예시:
            is_expired(None) -> True
            is_expired(과거 시간) -> True
            is_expired(미래 시간) -> False
        
        :param expires_at: 만료 시간 (datetime 객체 또는 None)
        :return: 만료되었으면 True, 아직 유효하면 False
        """
        if expires_at is None:
            return True
        return expires_at < timezone.now()
