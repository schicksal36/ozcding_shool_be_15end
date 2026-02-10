# Swagger UI 사용 가이드

## Swagger UI 접속 방법

1. Django 서버 실행 확인
   ```bash
   python manage.py runserver
   ```

2. 브라우저에서 Swagger UI 접속
   ```
   http://localhost:8000/api/schema/swagger-ui/
   ```

## API 테스트 방법 (로그인 예시)

### 1단계: API 찾기
- Swagger UI 페이지에서 **"인증"** 태그를 클릭
- **"POST /api/login"** 엔드포인트 찾기

### 2단계: "Try it out" 클릭
- 로그인 API 섹션에서 **"Try it out"** 버튼 클릭

### 3단계: 요청 데이터 입력
Request body에 JSON 형식으로 입력:
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**입력 방법:**
- Swagger UI의 Request body 입력란에 직접 입력
- 또는 예시를 복사해서 수정

### 4단계: "Execute" 클릭
- 입력란 아래의 **"Execute"** 버튼 클릭

### 5단계: 응답 확인
- **Responses** 섹션에서 결과 확인
  - **200**: 로그인 성공
    ```json
    {
      "message": "로그인 성공",
      "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "nickname": "테스트"
      },
      "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
      }
    }
    ```
  - **400**: 입력 데이터 오류
  - **401**: 인증 실패

## 인증이 필요한 API 테스트 방법

### 1단계: 로그인하여 토큰 받기
위의 로그인 방법으로 `access` 토큰을 받습니다.

### 2단계: Swagger UI에서 인증 설정
1. Swagger UI 페이지 상단의 **"Authorize"** 버튼 클릭
2. **"Bearer (JWT)"** 섹션에 토큰 입력
   - 형식: `Bearer {access_token}`
   - 예시: `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
3. **"Authorize"** 버튼 클릭
4. **"Close"** 버튼 클릭

### 3단계: 인증이 필요한 API 테스트
- 이제 인증이 필요한 API(예: `/api/users/me/`)를 테스트할 수 있습니다.
- Swagger UI가 자동으로 Authorization 헤더에 토큰을 포함합니다.

## 주요 API 엔드포인트

### 인증 (인증 불필요)
- `POST /api/users` - 회원가입
- `POST /api/login` - 로그인
- `POST /api/logout` - 로그아웃 (인증 필요)

### 사용자 정보 (인증 필요)
- `GET /api/users/me/` - 내 정보 조회
- `PATCH /api/users/me/` - 내 정보 수정
- `DELETE /api/users/me/` - 회원탈퇴

### 일정 관리 (인증 필요)
- `POST /api/events/` - 일정 생성
- `GET /api/events/` - 일정 목록 조회
- `GET /api/events/{id}/` - 일정 상세 조회
- `PATCH /api/events/{id}/` - 일정 수정
- `DELETE /api/events/{id}/` - 일정 삭제

## 주의사항

1. **JSON 형식 준수**: Request body는 반드시 유효한 JSON 형식이어야 합니다.
2. **필수 필드 확인**: 각 API의 필수 필드를 모두 입력해야 합니다.
3. **토큰 만료**: Access 토큰은 1시간 후 만료됩니다. 만료 시 다시 로그인하거나 Refresh 토큰으로 갱신하세요.
4. **CORS 설정**: 프론트엔드에서 테스트할 때는 CORS 설정이 필요할 수 있습니다.

## 문제 해결

### "Failed to fetch" 오류
- Django 서버가 실행 중인지 확인
- `http://localhost:8000`이 올바른 주소인지 확인

### 400 Bad Request
- Request body의 JSON 형식 확인
- 필수 필드가 모두 입력되었는지 확인

### 401 Unauthorized
- 토큰이 올바르게 입력되었는지 확인
- 토큰이 만료되지 않았는지 확인
- "Authorize" 버튼에서 토큰을 설정했는지 확인

### 405 Method Not Allowed
- 올바른 HTTP 메서드(POST, GET, PATCH, DELETE)를 사용했는지 확인
