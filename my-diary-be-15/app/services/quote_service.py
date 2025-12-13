import random
from typing import List
from fastapi import HTTPException, status

from app.models.quote import Quote
from app.models.user import User
from app.models.bookmark import Bookmark


# =====================================================================
# 🔥 QuoteService — 명언 자체 조회 기능 담당
# =====================================================================
class QuoteService:
    """
    명언(Quote) 조회 로직 담당.
    Router는 처리 결과를 받아 사용자에게 JSON으로 반환하기만 한다.
    """

    # ---------------------------------------------------------------
    # 🔥 전체 명언 조회
    # ---------------------------------------------------------------
    @staticmethod
    async def get_all() -> List[Quote]:
        """
        전체 명언 리스트 반환.

        현재는 단순 all() 이지만,
        실제 서비스에서는 다음 기능으로 확장 가능:
          - paging (offset, limit)
          - 검색 기능
          - 정렬 옵션

        만약 DB에 명언이 하나도 없다면 빈 리스트 반환.
        """
        quotes = await Quote.all()
        return quotes if quotes else []

    # ---------------------------------------------------------------
    # 🔥 랜덤 명언 1개 반환
    # ---------------------------------------------------------------
    @staticmethod
    async def get_random() -> Quote | None:
        """
        랜덤 명언 조회.

        방법:
          1) 전체 row 개수를 구한다.
          2) random.randint 로 임의 offset 선택
          3) offset(random_index).first() 로 1개 조회

        장점:
          ✔ 대량 데이터에서도 상대적으로 빠름 (ORDER BY RANDOM()보다 적은 부하)

        단점:
          - gap(삭제된 ID)이 많으면 offset 이 비효율적일 수 있음
        """

        count = await Quote.all().count()
        if count == 0:
            return None

        random_index = random.randint(0, count - 1)
        return await Quote.all().offset(random_index).first()



# =====================================================================
# 🔥 QuoteBookmarkService — 북마크 기능 전담 Service
# =====================================================================
class QuoteBookmarkService:
    """
    명언 북마크 기능 담당 서비스.

    기능:
      - 북마크 추가
      - 북마크 중복 방지
      - 북마크 목록 조회
      - 북마크 삭제

    Bookmark 테이블은 User ↔ Quote 관계를 연결하는 N:N 중간 테이블 역할.
    """

    # ---------------------------------------------------------------
    # 🔥 1) 북마크 추가
    # ---------------------------------------------------------------
    @staticmethod
    async def add_bookmark(current_user: User, quote_id: int) -> Bookmark:
        """
        북마크 추가 절차:

        1) 명언 존재 여부 검사
        2) 사용자가 이미 북마크했는지 검사 (중복 방지)
        3) Bookmark.create() 로 추가
        """

        # 1) 명언 존재 확인
        quote = await Quote.get_or_none(id=quote_id)
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quote not found"
            )

        # 2) 중복 북마크 방지
        exists = await Bookmark.filter(user=current_user, quote=quote).exists()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bookmark already exists"
            )

        # 3) 북마크 생성
        return await Bookmark.create(user=current_user, quote=quote)

    # ---------------------------------------------------------------
    # 🔥 2) 북마크 목록 조회
    # ---------------------------------------------------------------
    @staticmethod
    async def get_bookmarks(current_user: User) -> List[Bookmark]:
        """
        현재 로그인한 사용자의 북마크 목록 조회.

        select_related("quote")
            → Bookmark와 연결된 Quote 정보를 JOIN하여 한 번에 가져옴.
              (N+1 문제 방지)

        반환값:
            Bookmark 객체 목록 (각 Bookmark는 .quote 속성을 포함)
        """
        return await Bookmark.filter(user=current_user).select_related("quote")

    # ---------------------------------------------------------------
    # 🔥 3) 북마크 삭제
    # ---------------------------------------------------------------
    @staticmethod
    async def remove_bookmark(current_user: User, quote_id: int) -> None:
        """
        북마크 삭제 로직:

        - 특정 user + 특정 quote 조합만 삭제 (보안상 필요)
        - delete()는 삭제된 개수를 반환
        - 없으면 404 반환
        """

        deleted_count = await Bookmark.filter(
            user=current_user,
            quote_id=quote_id
        ).delete()

        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bookmark not found"
            )
