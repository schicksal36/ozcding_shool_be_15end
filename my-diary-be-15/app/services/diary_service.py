# app/services/diary_service.py

from app.models.diary import Diary
from fastapi import HTTPException


class DiaryService:
    """
    ===============================================================
    🔥 DiaryService — 다이어리 비즈니스 로직 계층
    ---------------------------------------------------------------
    Router(API 계층)는 입력/출력만 담당하고,
    DB 접근은 Repository 혹은 ORM 모델에게 넘기며,
    권한/예외/검증과 같은 '비즈니스 로직'은 이 서비스 계층에서 담당함.

    FastAPI 구조에서 가장 권장되는 Clean Architecture 패턴을 따름.
    ===============================================================
    """

    # -----------------------------------------------------------
    # 🔥 1) 새로운 다이어리 생성
    # -----------------------------------------------------------
    @staticmethod
    async def create(user, title, content):
        """
        다이어리 생성 로직:

        1) Diary.create()
            - user(FK), title, content 필드로 새 레코드 생성
            - 비동기 ORM이므로 await 필수

        2) 반환값: Diary ORM 객체
            → Router에서 DiaryResponse 스키마로 변환됨(from_attributes=True)
        """
        return await Diary.create(
            user=user,
            title=title,
            content=content
        )

    # -----------------------------------------------------------
    # 🔥 2) 특정 유저의 모든 다이어리 조회
    # -----------------------------------------------------------
    @staticmethod
    async def list_for_user(user):
        """
        SELECT * FROM diaries WHERE user_id = user.id;

        user는 PK(id)를 가진 User ORM 객체이므로
        .filter(user=user) 를 사용하면 자동으로 user_id 비교 수행.

        반환값: QuerySet[List[Diary]]
        """
        return await Diary.filter(user=user).all()

    # -----------------------------------------------------------
    # 🔥 3) 다이어리 1개 조회 (없으면 404)
    # -----------------------------------------------------------
    @staticmethod
    async def get_or_404(diary_id: int):
        """
        Diary.get_or_none(id=diary_id):
            - 있으면 Diary 모델 반환
            - 없으면 None 반환

        없을 때 FastAPI 표준 404 응답 생성.
        """
        diary = await Diary.get_or_none(id=diary_id)

        if not diary:
            raise HTTPException(
                status_code=404,
                detail="Diary not found"
            )

        return diary

    # -----------------------------------------------------------
    # 🔥 4) 다이어리 업데이트 (부분 수정 포함)
    # -----------------------------------------------------------
    @staticmethod
    async def update(diary, data):
        """
        diary: Diary ORM 객체
        data: DiaryUpdate 스키마 객체 (title / content 둘 다 optional)

        수정 로직:
          diary.title   = data.title   or diary.title
          diary.content = data.content or diary.content

        즉, 전달된 값이 None이 아닐 때만 필드 수정.
        (PATCH 스타일 부분 업데이트 가능)

        이후 save() 호출로 DB 업데이트 반영.
        """
        diary.title = data.title or diary.title
        diary.content = data.content or diary.content

        await diary.save()
        return diary

    # -----------------------------------------------------------
    # 🔥 5) 다이어리 삭제
    # -----------------------------------------------------------
    @staticmethod
    async def delete(diary):
        """
        Diary ORM 객체를 직접 delete() → 해당 row 삭제.

        Router에서 이미 권한 체크가 끝난 상태이므로,
        여기서는 삭제만 수행하면 됨.
        """
        await diary.delete()
