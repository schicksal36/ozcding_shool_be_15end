# app/services/auth_service.py

from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError
from datetime import datetime, timezone
from jose import jwt

from app.core.config import settings
from app.models.user import User, TokenBlacklist
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)


# ======================================================================
# 🔥 AuthService — 인증/인가(Auth) 전용 비즈니스 로직 계층
# ----------------------------------------------------------------------
# Router는 입력/출력만 담당하고,
# 실제 회원가입, 로그인, 토큰 생성, 로그아웃 등의 핵심 로직을 여기에 둔다.
#
# 장점:
#   ✔ Controller(Router) 깔끔해짐
#   ✔ 테스트 가능성 증가
#   ✔ Repository와 역할 분리 명확
# ======================================================================
class AuthService:

    # ==============================================================
    # 🔥 회원가입(Register)
    # ==============================================================    
    @staticmethod
    async def register(username: str, password: str, email: str) -> User:
        """
        회원가입 절차:

        1) 입력받은 비밀번호를 hash_password() 로 해싱
        2) User.create() 로 DB에 저장
        3) username UNIQUE 제약 때문에 중복 발생 시 IntegrityError 발생
        4) FastAPI 클라이언트에게 400 에러 반환

        반환값:
            생성된 User ORM 객체 → Router에서 UserResponse로 변환됨
        """

        hashed = hash_password(password)

        try:
            user = await User.create(
                username=username,
                password_hash=hashed,
                email=email
            )
            return user

        except IntegrityError:
            # username 혹은 email UNIQUE 충돌 시 발생
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )


    # ==============================================================
    # 🔥 로그인(Authentication)
    # ==============================================================
    @staticmethod
    async def authenticate(username: str, password: str) -> User:
        """
        로그인 절차:

        1) username으로 사용자 조회
        2) 없으면 실패
        3) verify_password() 로 해시 비교
        4) 실패하면 400 오류

        반환값:
            로그인 성공한 User 객체
        """

        user = await User.get_or_none(username=username)

        # 사용자 없음 OR 비밀번호 틀림
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=400,
                detail="Incorrect credentials"
            )

        return user


    # ==============================================================
    # 🔥 Access Token + Refresh Token 묶어서 생성
    # ==============================================================    
    @staticmethod
    async def create_tokens_for_user(user: User):
        """
        JWT Access Token + Refresh Token 생성

        ⭐ 주의:
            subject(sub)로 user.username 을 넣고 있음.
            보통 user.id 를 쓰는 것이 더 안전하고 충돌 가능성이 낮음.
            (원하면 user.id 기준으로 변경해드릴 수 있음.)

        반환값 예시:
        {
            "access_token": "ey...",
            "refresh_token": "ey...",
            "token_type": "bearer"
        }
        """

        access = create_access_token(user.username)
        refresh = create_refresh_token(user.username)

        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer"
        }


    # ==============================================================
    # 🔥 로그아웃(토큰 Blacklist 등록)
    # ==============================================================
    @staticmethod
    async def logout(token: str, user: User):
        """
        로그아웃 처리 방식:

        JWT는 원래 '서버가 강제로 무효화할 수 없는' 구조.
        따라서 서버는 다음과 같은 방식을 사용해야 함:

          ✔ 토큰 문자열 자체를 TokenBlacklist 테이블에 저장
          ✔ get_current_user() 호출 시 항상 블랙리스트를 먼저 검사

        절차:
        1) decode 해서 exp(만료시간) 추출 시도
        2) exp를 expired_at 으로 저장 → 나중에 자동 정리 가능
        3) TokenBlacklist(user=..., token=...)
        """

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            # UNIX timestamp → datetime 변환
            exp = payload.get("exp")
            expired_at = datetime.fromtimestamp(exp, tz=timezone.utc) if exp else None

        except Exception:
            # 토큰 구조가 잘못됐거나 변경되었으면 exp 없이 저장
            expired_at = None

        # DB에 블랙리스트 등록 → 즉시 무효 처리
        await TokenBlacklist.create(
            token=token,
            user=user,
            expired_at=expired_at
        )
