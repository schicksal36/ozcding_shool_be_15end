# app/schemas/user.py
from pydantic import BaseModel, Field


# ================================================================
# 🔥 UserCreate — 회원가입 요청(Request Body) 검증 스키마
# ---------------------------------------------------------------
# 클라이언트가 "/auth/register" 로 보낸 JSON을 검증하는 역할
# 예:
# {
#   "username": "bbangdol",
#   "password": "1234",
#   "email": "test@example.com"
# }
# ================================================================
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    """
    username 길이 제한
    FastAPI는 요청이 들어올 때 자동으로 검증(유효성 실패 → 422 반환)
    """

    password: str = Field(min_length=3, max_length=32)
    """
    실제 DB에는 password가 아닌 'hash'가 저장됨.
    서비스 계층에서 hash_password()를 사용하여 저장하도록 구성됨.
    """

    email: str = Field(max_length=255)
    """
    이메일은 필수지만, 형식 검사(email validator)를 원하면
    pydantic EmailStr 타입 사용 가능.
    """


# ================================================================
# 🔥 UserLogin — 로그인 요청(Request Body) 검증 스키마
# ---------------------------------------------------------------
# AuthService.authenticate(username, password) 호출 전에
# 입력값을 검증하는 역할.
# ================================================================
class UserLogin(BaseModel):
    username: str
    """
    username은 길이 제한 없이 그대로 받되,
    AuthService에서 존재 여부 검증.
    """

    password: str
    """
    평문 비밀번호를 받지만,
    인증 과정에서 verify_password()로 해싱된 값과 비교.
    """


# ================================================================
# 🔥 UserResponse — 사용자 정보 응답(Response DTO)
# ---------------------------------------------------------------
# FastAPI가 ORM(User) 모델 → 이 스키마로 변환하여 JSON으로 응답하게 됨.
#
# 예: 로그인 후 /auth/me 등에서 반환되는 형태
#
# {
#   "id": 1,
#   "username": "bbangdol",
#   "email": "abc@test.com"
# }
#
# from_attributes=True → Tortoise ORM 모델 지원(Pydantic v2)
# orm_mode=True → Pydantic v1 하위 호환
# ================================================================
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # Pydantic v2 방식 (ORM 객체 지원)
        orm_mode = True         # v1 호환성 유지 (중복이지만 안전함)
        """
        동작 원리:
        FastAPI는 ORM 모델(User)을 반환하면
            UserResponse.model_validate(user_obj)
        를 수행해 적절히 JSON 구조로 변환함.
        """


# ================================================================
# 🔥 LoginResponse — 로그인 성공 시 반환되는 응답 형태
# ---------------------------------------------------------------
# Access Token + User 정보를 함께 응답
#
# 예시 응답:
# {
#     "access_token": "eyJhbGciOiJIUzI1NiIs...",
#     "user": {
#         "id": 1,
#         "username": "bbangdol",
#         "email": "test@example.com"
#     }
# }
#
# FastAPI의 response_model에 설정되어 Swagger 문서에 자동 반영됨.
# ================================================================
class LoginResponse(BaseModel):
    access_token: str
    """
    JWT Access Token 문자열
    Authorization: Bearer <token> 로 사용
    """

    user: UserResponse
    """
    로그인한 사용자의 기본 정보를 함께 반환
    클라이언트(React/Vue/앱)가 유저 상태 저장하는 데 사용
    """
