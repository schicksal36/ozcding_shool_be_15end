#app\api\v1\diary.py
from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.quote import QuoteBookmarkResponse, QuoteResponse
from app.scraping.quote_scraper import scrape_and_save_quotes
from app.services.quote_service import QuoteBookmarkService, QuoteService


# ---------------------------------------------------------
# 🔸 /quotes로 시작하는 모든 엔드포인트를 담당하는 Router
# Swagger 문서에서는 Quotes 그룹으로 묶임
# ---------------------------------------------------------
router = APIRouter(prefix="/quotes", tags=["Quotes"])



"""
===============================================================
🔥 1) 명언 스크래핑 — POST /quotes/scrape
===============================================================
"""
@router.post(
    "/scrape",
    summary="명언 스크래핑",
    description="saramro.com에서 명언을 스크래핑하여 DB에 저장",
)
async def scrape_quotes(
    pages: int = Query(default=10, ge=1, le=100, description="스크래핑할 페이지 수"),
):
    """
    🔥 동작 원리:
    1) Query(...)  
        - pages는 URL 파라미터 값  
        - 기본값 10, 최소 1, 최대 100 → FastAPI가 자동으로 검증

    2) scrape_and_save_quotes(pages)
        - saramro.com 사이트에서 HTML 가져오기
        - BeautifulSoup 등으로 명언 추출
        - Quote 중복 여부 체크 후 DB 저장

    3) 스크래핑 결과(총 저장 개수 등) 반환
    """
    result = await scrape_and_save_quotes(pages)
    return result



"""
===============================================================
🔥 2) 전체 명언 조회 — GET /quotes
===============================================================
"""
@router.get(
    "",
    response_model=list[QuoteResponse],
    summary="전체 명언 조회",
    description="DB에 저장된 모든 명언 조회",
)
async def get_all_quotes():
    """
    🔥 동작 원리:
    1) QuoteService.get_all() 실행
        - SELECT * FROM quotes ORDER BY id ASC
        - Quote 모델 리스트 반환
    2) FastAPI가 QuoteResponse 스키마로 자동 변환해 응답
    """
    quotes = await QuoteService.get_all()
    return quotes



"""
===============================================================
🔥 3) 랜덤 명언 조회 — GET /quotes/random
===============================================================
"""
@router.get(
    "/random",
    response_model=QuoteResponse,
    summary="랜덤 명언 조회",
    description="DB에서 랜덤으로 명언 1개 조회",
)
async def get_random_quote():
    """
    🔥 동작 원리:
    1) QuoteService.get_random()
        - DB에서 ORDER BY RANDOM() LIMIT 1 실행
        - 명언 1개만 가져옴
    2) 없다면 404 반환
    """
    quote = await QuoteService.get_random()
    if not quote:
        raise HTTPException(status_code=404, detail="No quotes found")
    return quote



"""
================================================================
🔥 4) 명언 북마크 추가 — POST /quotes/{quote_id}/bookmark
================================================================
"""
@router.post(
    "/{quote_id}/bookmark",
    response_model=QuoteBookmarkResponse,
    summary="명언 북마크 추가",
    description="명언을 북마크에 추가 (중복x)",
)
async def add_bookmark(
    quote_id: int,
    current_user: User = Depends(get_current_user),  # 🔐 JWT 인증 필수
):
    """
    🔥 동작 원리:
    1) JWT 인증된 사용자(current_user) 정보를 가져옴
         - get_current_user가 Authorization 헤더에서 JWT 파싱
         - User 객체 반환

    2) QuoteBookmarkService.add_bookmark(user, quote_id)
         - 해당 명언 존재 여부 확인
         - 북마크 중복 여부 확인
         - (user_id, quote_id) 조합으로 북마크 생성

    3) bookmark.fetch_related("quote")
         - ManyToOne 관계에서 quote 객체를 포함해 반환
         - 별도 join 없이 Tortoise ORM이 자동 lazy load
    """
    bookmark = await QuoteBookmarkService.add_bookmark(current_user, quote_id)
    await bookmark.fetch_related("quote")  # 응답에 quote 내용 포함
    return bookmark



"""
================================================================
🔥 5) 내 북마크 목록 조회 — GET /quotes/bookmarks
================================================================
"""
@router.get(
    "/bookmarks",
    response_model=list[QuoteBookmarkResponse],
    summary="내 북마크 목록 조회",
    description="로그인한 사용자의 북마크 목록 조회",
)
async def get_my_bookmarks(
    current_user: User = Depends(get_current_user),
):
    """
    🔥 동작 원리:
    1) get_current_user → JWT 인증으로 사용자 정보 획득
    2) QuoteBookmarkService.get_bookmarks(current_user)
         - SELECT * FROM quote_bookmarks WHERE user_id = current_user.id
         - JOIN quote 포함해서 응답 구조 맞춰줌
    """
    bookmarks = await QuoteBookmarkService.get_bookmarks(current_user)
    return bookmarks



"""
================================================================
🔥 6) 북마크 삭제 — DELETE /quotes/{quote_id}/bookmark
================================================================
"""
@router.delete(
    "/{quote_id}/bookmark",
    summary="북마크 해제",
    description="북마크에서 명언 제거",
)
async def remove_bookmark(
    quote_id: int,
    current_user: User = Depends(get_current_user),
):
    """
    🔥 동작 원리:
    1) JWT 인증된 사용자(current_user)를 기반으로  
       (user_id, quote_id) 조합을 DB에서 검색

    2) 없으면 404 에러
    3) 있으면 delete() 실행하여 북마크 해제

    4) 성공 메시지 반환
    """
    await QuoteBookmarkService.remove_bookmark(current_user, quote_id)
    return {"message": "북마크가 성공적으로 삭제되었습니다"}
