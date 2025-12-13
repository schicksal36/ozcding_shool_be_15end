#app\api\v1\auth.py
from fastapi import APIRouter, Depends

# ✅ User 모델 (Tortoise ORM 모델)
from app.models.user import User

# ✅ Request/Response Schema (Pydantic)
from app.schemas.user import UserCreate, UserLogin, UserResponse, LoginResponse

# ✅ JWT & 인증 관련 헬퍼
from app.core.security import get_current_user, create_access_token, oauth2_scheme

# ✅ 실제 로직을 처리하는 서비스 계층
from app.services.auth_service import AuthService


# --------------------------------------------------------------------
# 🔹 APIRouter 설정
# prefix="/auth" → 모든 엔드포인트 URL 앞에 자동으로 /auth 붙음
# tags=["Auth"] → Swagger UI 문서에서 Auth 그룹으로 표시됨
# --------------------------------------------------------------------
router = APIRouter(prefix="/auth", tags=["Auth"])


# ================================================================
# 🔥 1) 회원가입 API — /auth/register
# ================================================================
@router.post("/register", response_model=UserResponse, description="register new user")
async def register_user(payload: UserCreate):
    """
    🔥 동작 원리:
    1) payload: UserCreate 스키마가 username/password/email 을 검증
    2) AuthService.register(...) 호출
         - 비밀번호를 bcrypt로 해시
         - username 중복 여부 검사
         - email 중복 여부 검사
         - DB에 User 생성
    3) 생성된 User 객체 반환 (단, 비밀번호는 제외)
    """

    # 서비스 계층에 모든 로직 위임 → Router는 '흐름만' 담당
    user = await AuthService.register(
        payload.username,
        payload.password,
        payload.email
    )

    # 반환 형식은 UserResponse 스키마로 자동 변환됨
    return user



# ================================================================
# 🔥 2) 로그인 API — /auth/login
# ================================================================
@router.post("/login", response_model=LoginResponse, description="login user")
async def login(payload: UserLogin):
    """
    🔥 동작 원리:
    1) AuthService.authenticate(username, password)
         - username으로 DB 검색
         - bcrypt로 비밀번호 확인(compare)
         - 실패 시 HTTP 401 Unauthorized 발생
    2) 인증 성공 → JWT 발급
         - create_access_token(user.id)
         - JWT.payload.sub = user.id
         - JWT.secret = ENV.JWT_SECRET
         - JWT.exp = 만료 시간 설정
    3) 클라이언트에게 token + user 정보 반환
    """

    # 사용자 검증
    user = await AuthService.authenticate(payload.username, payload.password)

    # JWT 액세스 토큰 생성
    token = create_access_token(str(user.id))

    # LoginResponse(토큰 + 사용자 정보) 형태로 반환
    return {
        "access_token": token,
        "user": user
    }



# ================================================================
# 🔥 3) 내 정보 조회 API — /auth/me
# ================================================================
@router.get("/me", response_model=UserResponse, description="get user info")
async def get_me(user=Depends(get_current_user)):
    """
    🔥 동작 원리:
    1) Depends(get_current_user)
         - Authorization: Bearer <JWT> 헤더 읽음
         - JWT 디코드하여 user_id 추출
         - DB에서 User 조회
         - 토큰 유효성 검사 (만료 여부 포함)
    2) 유효하면 User 객체 반환
    """

    return user



# ================================================================
# 🔥 4) 로그아웃 API — /auth/logout
# ================================================================
@router.post("/logout", description="logout user")
async def logout(
    current_user: User = Depends(get_current_user),  # 현재 로그인된 사용자
    token: str = Depends(oauth2_scheme)              # Bearer 토큰 직접 얻기
):
    """
    🔥 동작 원리:
    1) Depends(oauth2_scheme)
         - Authorization 헤더에서 JWT 문자열만 추출
         - ex) "Bearer eyJhbGciOi..." → "eyJhbGciOi..."

    2) Depends(get_current_user)
         - JWT 검증 후 실제 User 모델 반환

    3) AuthService.logout(token, current_user)
         - 서버 기반 로그아웃 구현 방식:
            ① 블랙리스트 테이블에 토큰 저장
            ② Redis 등에 토큰을 등록하여 무효 처리
            ③ refresh_token 삭제 (있는 경우)
    4) 정상 로그아웃 메시지 반환
    """

    await AuthService.logout(token, current_user)
    return {"detail": "Successfully logged out"}
