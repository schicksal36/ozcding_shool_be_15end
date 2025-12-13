#app\api\v1\diary.py
from fastapi import APIRouter, Depends, HTTPException, status

# 🔹 요청/응답 데이터 검증용 Schema
from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate

# 🔹 Service 계층: 실제 DB 로직을 수행하는 곳
from app.services.diary_service import DiaryService

# 🔹 JWT 인증 후 현재 사용자 반환
from app.core.security import get_current_user


# --------------------------------------------------------------------
# 🔸 APIRouter 설정
# prefix="/api/v1/diaries" → 모든 엔드포인트 앞에 자동으로 붙음
# tags=["Diaries"] → Swagger UI 문서에서 ‘Diaries’ 그룹으로 묶임
# --------------------------------------------------------------------
router = APIRouter(prefix="/api/v1/diaries", tags=["Diaries"])



# ================================================================
# 🔥 1) 다이어리 생성 — POST /api/v1/diaries
# ================================================================
@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED,
             description="create new diary")
async def create_diary(payload: DiaryCreate, current_user=Depends(get_current_user)):
    """
    🔥 동작 원리:
    1) get_current_user → JWT 검증 후 현재 사용자(User) 객체 반환
    2) payload.title, payload.content → 입력값 검증(DiaryCreate 스키마)
    3) DiaryService.create(...)
         - DB에 diary row 생성
         - user_id=current_user.id 로 연결되어 저장됨
    4) 생성된 Diary 모델을 DiaryResponse 형태로 반환
    """

    diary = await DiaryService.create(
        current_user,
        payload.title,
        payload.content
    )
    return diary



# ================================================================
# 🔥 2) 사용자 다이어리 목록 조회 — GET /api/v1/diaries
# ================================================================
@router.get("/", response_model=list[DiaryResponse], description="get all diaries")
async def list_diaries(current_user=Depends(get_current_user)):
    """
    🔥 동작 원리:
    1) 인증된 사용자(current_user)를 가져온 뒤
    2) DiaryService.list_for_user(current_user)
         - SELECT * FROM diaries WHERE user_id = current_user.id
    3) 본인 다이어리만 목록으로 반환됨 (다른 사람 다이어리는 절대 안 보임)
    """

    return await DiaryService.list_for_user(current_user)



# ================================================================
# 🔥 3) 단일 다이어리 조회 — GET /api/v1/diaries/{diary_id}
# ================================================================
@router.get("/{diary_id}", response_model=DiaryResponse, description="get a diary by id")
async def get_diary(diary_id: int, current_user=Depends(get_current_user)):
    """
    🔥 동작 원리:
    1) DiaryService.get_or_404(diary_id)
         - diary가 없으면 자동으로 404 발생
    2) 권한 체크
         - diary.user_id != current_user.id → 403 Forbidden
         - 즉, 다른 사람 다이어리는 절대 조회 불가
    """

    diary = await DiaryService.get_or_404(diary_id)

    # 소유자 권한 체크
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return diary



# ================================================================
# 🔥 4) 다이어리 수정 — PUT /api/v1/diaries/{diary_id}
# ================================================================
@router.put("/{diary_id}", response_model=DiaryResponse, description="update a diary by id")
async def update_diary(diary_id: int, payload: DiaryUpdate, current_user=Depends(get_current_user)):
    """
    🔥 동작 원리:
    1) 다이어리 존재 확인 (없으면 404)
    2) 소유자 검증 (user_id mismatch → 403 Forbidden)
    3) DiaryService.update(diary, payload)
         - title/content 중 수정된 항목만 업데이트
    """

    diary = await DiaryService.get_or_404(diary_id)

    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return await DiaryService.update(diary, payload)



# ================================================================
# 🔥 5) 다이어리 삭제 — DELETE /api/v1/diaries/{diary_id}
# ================================================================
@router.delete("/{diary_id}", description="delete a diary by id")
async def delete_diary(diary_id: int, current_user=Depends(get_current_user)):
    """
    🔥 동작 원리:
    1) 다이어리 존재 여부 확인
    2) 소유자 권한 체크 (본인 것만 삭제 가능)
    3) DiaryService.delete(diary)
    4) {"msg": "deleted"} 응답
    """

    diary = await DiaryService.get_or_404(diary_id)

    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    await DiaryService.delete(diary)
    return {"msg": "deleted"}
