#app\repositories\quote_repo.py
from typing import List, Optional
from tortoise.expressions import Q

from app.models.quote import Quote, Bookmark


class QuoteRepository:
    """
    명언(Quote) 관련 DB 접근 전용 레이어
    """

    @staticmethod
    async def get_random_quote() -> Optional[Quote]:
        """
        DB에 존재하는 명언 중 랜덤 1개 반환.
        """
        # Tortoise 는 order_by("?") 로 랜덤 정렬 가능
        return await Quote.all().order_by("?").first()

    @staticmethod
    async def get_by_id(quote_id: int) -> Optional[Quote]:
        return await Quote.filter(id=quote_id).first()

    @staticmethod
    async def bulk_create(quotes: List[dict]) -> None:
        """
        스크래핑 등으로 받아온 명언 리스트를 한 번에 저장.
        quotes: [{ "content": "...", "author": "..." }, ...]
        """
        quote_objs = [Quote(**q) for q in quotes]
        await Quote.bulk_create(quote_objs)


class BookmarkRepository:
    """
    명언 북마크 관련 DB 접근 전용 레이어
    """

    @staticmethod
    async def get_by_user_and_quote(user_id: int, quote_id: int) -> Optional[Bookmark]:
        return await Bookmark.filter(user_id=user_id, quote_id=quote_id).first()

    @staticmethod
    async def create(user_id: int, quote_id: int) -> Bookmark:
        return await Bookmark.create(user_id=user_id, quote_id=quote_id)

    @staticmethod
    async def delete(bookmark_id: int, user_id: int) -> int:
        """
        해당 유저가 소유한 북마크만 삭제.
        반환값: 삭제된 row 수 (0 or 1)
        """
        deleted_count = await Bookmark.filter(id=bookmark_id, user_id=user_id).delete()
        return deleted_count

    @staticmethod
    async def list_by_user(user_id: int) -> List[Bookmark]:
        return await Bookmark.filter(user_id=user_id).prefetch_related("quote")
# app/repositories/quote_repo.py

from typing import List, Optional
from tortoise.expressions import Q

from app.models.quote import Quote, Bookmark


# =====================================================================
# 🔥 Repository Layer(저장소 레이어)
# ---------------------------------------------------------------------
# - 서비스(Service) 계층에서 DB 접근 코드를 직접 작성하지 않도록 분리하는 레이어
# - 하나의 책임: "DB에 접근하는 것만 담당"
# - 비즈니스 로직, 검증 등은 Service 계층에서 수행
#
# 장점:
#   ✔ DB 접근 로직과 비즈니스 로직 분리 → 유지보수성 증가
#   ✔ 테스트 용이 → Repository를 Mocking 가능
#   ✔ Service가 깔끔해짐
# =====================================================================


# =====================================================================
# 🔥 QuoteRepository — 명언 테이블 전용 DB 접근 레이어
# =====================================================================
class QuoteRepository:
    """
    명언(Quote) 관련 DB 접근 전용 레이어.
    Service 계층에서는 Query를 직접 만들지 않고,
    오직 Repository의 메서드를 호출해서 DB 조작을 수행한다.
    """

    # ---------------------------------------------------------------
    # 🔸 랜덤 명언 1개 조회
    # ---------------------------------------------------------------
    @staticmethod
    async def get_random_quote() -> Optional[Quote]:
        """
        DB에 존재하는 명언 중 랜덤 1개 반환.

        Tortoise ORM 특징:
            order_by("?") → SQL의 ORDER BY RANDOM() 기능 수행
            first() → LIMIT 1 에 해당

        주의:
            - DB가 커지면 RANDOM()은 성능 이슈가 있을 수 있으나
              명언 정도의 규모에서는 문제 없음.
        """
        return await Quote.all().order_by("?").first()

    # ---------------------------------------------------------------
    # 🔸 id로 단일 명언 조회
    # ---------------------------------------------------------------
    @staticmethod
    async def get_by_id(quote_id: int) -> Optional[Quote]:
        """
        해당 quote_id의 명언 하나 조회.
        없으면 None 반환 → Service 계층에서 처리해야 함.
        """
        return await Quote.filter(id=quote_id).first()

    # ---------------------------------------------------------------
    # 🔸 명언 여러 개 Bulk Create
    # ---------------------------------------------------------------
    @staticmethod
    async def bulk_create(quotes: List[dict]) -> None:
        """
        스크래핑 등으로 받아온 명언 리스트를 한 번에 저장.

        quotes 예시:
            [
                {"content": "명언1", "author": "작가1"},
                {"content": "명언2", "author": "작가2"},
            ]

        동작 방식:
            Quote(**q) → Tortoise 모델 객체 생성
            bulk_create → 여러 레코드를 한 번에 insert (성능 향상)
        """
        quote_objs = [Quote(**q) for q in quotes]
        await Quote.bulk_create(quote_objs)



# =====================================================================
# 🔥 BookmarkRepository — 명언 북마크 전용 DB 접근 레이어
# =====================================================================
class BookmarkRepository:
    """
    명언 북마크 관련 DB 접근 전용 레이어.

    Bookmark 테이블 구조:
        id(PK)
        user_id(FK→User)
        quote_id(FK→Quote)

    즉, User와 Quote 사이의 N:N 관계를 표현하는 중간 테이블.
    """

    # ---------------------------------------------------------------
    # 🔸 유저 + 명언 조합으로 북마크 조회 (중복 체크)
    # ---------------------------------------------------------------
    @staticmethod
    async def get_by_user_and_quote(user_id: int, quote_id: int) -> Optional[Bookmark]:
        """
        특정 유저가 특정 명언을 북마크했는지 조회.
        중복 등록 방지에 활용됨.
        """
        return await Bookmark.filter(user_id=user_id, quote_id=quote_id).first()

    # ---------------------------------------------------------------
    # 🔸 북마크 생성
    # ---------------------------------------------------------------
    @staticmethod
    async def create(user_id: int, quote_id: int) -> Bookmark:
        """
        북마크 하나 생성.
        Tortoise는 create()가 insert와 객체 반환을 동시에 수행함.
        """
        return await Bookmark.create(user_id=user_id, quote_id=quote_id)

    # ---------------------------------------------------------------
    # 🔸 북마크 삭제 (해당 유저의 북마크만 삭제)
    # ---------------------------------------------------------------
    @staticmethod
    async def delete(bookmark_id: int, user_id: int) -> int:
        """
        특정 유저가 소유한 북마크만 삭제.

        WHERE id = bookmark_id AND user_id = user_id 조건으로 삭제되므로
        다른 사람의 북마크는 절대 삭제되지 않음 (보안적 측면).

        반환값:
            삭제된 row 수
            - 0 → 해당 유저의 북마크 아님
            - 1 → 정상 삭제
        """
        deleted_count = await Bookmark.filter(id=bookmark_id, user_id=user_id).delete()
        return deleted_count

    # ---------------------------------------------------------------
    # 🔸 유저가 북마크한 모든 명언 조회
    # ---------------------------------------------------------------
    @staticmethod
    async def list_by_user(user_id: int) -> List[Bookmark]:
        """
        Bookmark 목록 조회 + 명언(quote) join

        prefetch_related("quote")
            → JOIN 효과 (N+1 문제 방지)
            → 북마크마다 quote를 미리 가져와서 API 응답 성능 향상
        """
        return await Bookmark.filter(user_id=user_id).prefetch_related("quote")
