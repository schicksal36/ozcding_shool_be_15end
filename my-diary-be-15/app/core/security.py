#app\core\security.py
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.models.user import User, TokenBlacklist


# ================================================================
# 🔥 비밀번호 해싱 설정
# ---------------------------------------------------------------
# passlib은 암호 해싱 라이브러리. pbkdf2_sha256은 비교적 안전하며 빠름.
# ================================================================
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],   # 사용할 해싱 알고리즘
)


# ================================================================
# 🔥 HTTPBearer — Authorization 헤더에서 "Bearer <token>" 읽는 역할
# ---------------------------------------------------------------
# FastAPI가 자동으로 token.credentials에 JWT 토큰 문자열만 넣어줌.
# ================================================================
oauth2_scheme = HTTPBearer()


# ================================================================
# 🔥 비밀번호 해싱 함수
# ---------------------------------------------------------------
# DB에는 절대 평문 비밀번호 저장 안 됨.
# pwd_context.hash(password) → 솔트 자동 추가 + 안전한 해싱 저장
# ================================================================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ================================================================
# 🔥 비밀번호 검증 함수
# ---------------------------------------------------------------
# plain(사용자 입력) vs hashed(DB 값) 비교
# 내부적으로 같은 해싱 알고리즘을 사용해 비교함.
# ================================================================
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)



# ================================================================
# 🔥 Access Token 생성 (JWT)
# ---------------------------------------------------------------
# subject = 사용자 ID와 같은 토큰의 주체(subject)
#
# to_encode 내부 구조:
# {
#     "sub": "<user_id>",
#     "exp": <만료시간>
# }
#
# exp는 반드시 UTC 시간 사용해야 표준 JWT 규칙을 충족.
# ================================================================
def create_access_token(subject: str, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(subject),
        "exp": datetime.now(timezone.utc) + expires_delta
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,               # 암호화 키
        algorithm=settings.ALGORITHM       # HS256
    )



# ================================================================
# 🔥 Refresh Token 생성
# ---------------------------------------------------------------
# Access Token과 다른 점:
# - 더 긴 만료시간 사용
# - typ="refresh" 추가 → 나중에 토큰 재발급 여부 체크 가능
# ================================================================
def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(subject),
        "exp": datetime.now(timezone.utc) + expires_delta,
        "typ": "refresh"
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )



# ================================================================
# 🔥 Token Blacklist 조회
# ---------------------------------------------------------------
# TokenBlacklist 테이블:
#   token: TEXT
#
# 로그아웃 시 이 테이블에 JWT를 저장하면
# get_current_user에서 항상 먼저 체크하여 차단 가능.
# ================================================================
async def is_token_blacklisted(token: str) -> bool:
    t = await TokenBlacklist.get_or_none(token=token)
    return t is not None



# ================================================================
# 🔥 현재 사용자 가져오기 (JWT 인증 핵심)
# ---------------------------------------------------------------
# 1) Authorization: Bearer <token> 헤더 읽기
# 2) 블랙리스트 여부 체크
# 3) JWT 디코드하여 sub(user_id) 추출
# 4) DB에서 사용자 조회
# 5) 유효하면 User 객체 반환
#
# 이 함수가 실패하면 무조건 401 Unauthorized 반환됨.
# ================================================================
async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    # 401 에러 템플릿 생성
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},  # Swagger 문서를 위한 헤더
    )

    # HTTPBearer가 가져온 JWT 값
    token_value = token.credentials

    try:
        # 🔥 로그아웃된 토큰인지 확인
        if await is_token_blacklisted(token_value):
            raise credentials_exception

        # 🔥 JWT 디코드
        payload = jwt.decode(
            token_value,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # 페이로드에서 사용자 ID(sub) 추출
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        # 서명 불일치 / 만료 / 변조 등 JWT 오류 발생
        raise credentials_exception

    # 🔥 DB에서 사용자 객체 조회
    user = await User.get_or_none(id=user_id)
    if not user:
        raise credentials_exception

    # 정상 인증된 사용자 반환
    return user
