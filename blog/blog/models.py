from django.db import models


class Blog(models.Model):
    """
    =============================================================================
    📌 Blog 모델의 정체
    -----------------------------------------------------------------------------
    - Django ORM 모델 클래스
    - MySQL(DB)에서는 하나의 테이블로 변환됨
    - Python 객체 ↔ SQL Row 를 연결하는 중간 계층
    =============================================================================

    🔹 기본 테이블명 (Django 규칙)
        blog_blog
        (규칙: <app_name>_<model_name 소문자>)

    🔹 MySQL 기준 기본 설정
        ENGINE = InnoDB
        CHARSET = utf8mb4

    🔹 Django의 역할
        - SQL을 직접 쓰지 않아도
        - Python 코드로 CRUD 가능하게 해줌
    =============================================================================
    """


    # ============================================================================
    # 1️⃣ CATEGORY_CHOICES (카테고리 선택지)
    # ============================================================================
    """
    📌 choices의 본질 (아주 중요)

    Django ORM 관점
    ----------------
    - choices는 "제약 조건 + 표시용 메타데이터"
    - Python 튜플(tuple of tuples) 구조
    - 폼(Form), Admin, Validation 단계에서 사용됨

    MySQL(DB) 관점
    ----------------
    ❌ MySQL에는 choices 개념이 없음
    ❌ ENUM 타입으로 자동 변환되지 않음
    ⭕ 그냥 VARCHAR 컬럼에 문자열 저장

    즉,
    - 데이터 무결성 검사는 Django가 담당
    - DB는 문자열 저장만 담당

    🔹 구조 규칙 (필수)
        (
            (실제 저장값, 화면에 보여줄 값),
            ...
        )
    """

    CATEGORY_CHOICES = (
        ("FREE", "자유게시판"),
        ("C", "C"),
        ("PYTHON", "Python"),
        ("JAVA", "Java"),
        ("LINUX", "Linux 명령어"),
    )
    # ⚠️ 기존 코드의 오류 수정:
    # {'Linux','명령어'} ❌  → set 자료형 (choices로 사용 불가)
    # 반드시 (값, 표시값) 형태의 튜플이어야 함


    # ============================================================================
    # 2️⃣ category 필드
    # ============================================================================
    """
    📌 카테고리 필드

    Django ORM
    -----------
    - CharField + choices
    - 유효하지 않은 값은 저장 단계에서 ValidationError 발생

    MySQL 변환 결과
    ----------------
        category VARCHAR(10) NOT NULL

    SQL 개념
    ---------
        `category` varchar(10) NOT NULL

    🔹 실제 DB에 저장되는 값 예시
        'FREE'
        'PYTHON'
        'JAVA'

    🔹 사람이 읽는 값이 필요할 때
        blog.get_category_display()
    """

    category = models.CharField(
        "카테고리",
        max_length=10,
        choices=CATEGORY_CHOICES,
    )


    # ============================================================================
    # 3️⃣ title 필드
    # ============================================================================
    """
    📌 제목 필드

    Django ORM
    -----------
    - CharField(max_length=100)

    MySQL 변환 결과
    ----------------
        title VARCHAR(100) NOT NULL

    특징
    -----
    - 길이 제한은 Django + MySQL 양쪽에서 동시에 적용
    - 초과 시:
        - Django: ValidationError
        - DB: 저장 불가
    """

    title = models.CharField("제목", max_length=100)


    # ============================================================================
    # 4️⃣ content 필드
    # ============================================================================
    """
    📌 본문 필드

    Django ORM
    -----------
    - TextField (대용량 텍스트)

    MySQL 변환 결과
    ----------------
        content LONGTEXT

    특징
    -----
    - 사실상 길이 제한 없음
    - 인덱스 생성 불가 (성능 이슈 주의)
    - 검색용이면 별도 검색 전략 필요
    """

    content = models.TextField("본문")


    # ============================================================================
    # 5️⃣ created_at (작성일)
    # ============================================================================
    """
    📌 작성 시간 필드

    Django ORM
    -----------
    - auto_now_add=True
    - 객체 최초 생성 시 한 번만 자동 설정

    MySQL 변환 결과
    ----------------
        created_at DATETIME(6) NOT NULL

    ⚠️ 핵심 포인트
    --------------
    ❌ MySQL의 DEFAULT CURRENT_TIMESTAMP 사용 안 함
    ⭕ Django가 INSERT 직전에 Python에서 값을 채움

    즉,
    - 시간 관리 책임은 DB ❌
    - Django ORM ⭕
    """

    created_at = models.DateTimeField("작성일자", auto_now_add=True)


    # ============================================================================
    # 6️⃣ updated_at (수정일)
    # ============================================================================
    """
    📌 수정 시간 필드

    Django ORM
    -----------
    - auto_now=True
    - save() 호출 시마다 현재 시간으로 자동 갱신

    MySQL 변환 결과
    ----------------
        updated_at DATETIME(6) NOT NULL

    ⚠️ 주의
    --------
    ❌ MySQL의 ON UPDATE CURRENT_TIMESTAMP 사용 안 함
    ⭕ Django가 UPDATE 직전에 값을 덮어씀
    """

    updated_at = models.DateTimeField("수정일자", auto_now=True)


    # ============================================================================
    # 7️⃣ __str__ 메서드
    # ============================================================================
    """
    📌 객체 문자열 표현

    사용되는 곳
    ------------
    - Django Admin 목록
    - Django shell
    - 디버깅 출력

    get_category_display()
    -----------------------
    - choices의 '표시값'을 반환
    """

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title[:10]}"


    # ============================================================================
    # 8️⃣ Meta 클래스
    # ============================================================================
    """
    📌 모델 메타데이터 설정

    Django 내부에서 사용됨
    -----------------------
    - Admin 화면
    - Model 옵션 처리
    """

    class Meta:
        verbose_name = "블로그"          # 단수 표현
        verbose_name_plural = "블로그 목록"  # 복수 표현


#mysql에 생성되는 테이블
#CREATE TABLE blog_blog (
    #id BIGINT AUTO_INCREMENT PRIMARY KEY,
    #category VARCHAR(10) NOT NULL,
    #title VARCHAR(100) NOT NULL,
    #content LONGTEXT NOT NULL,
    #created_at DATETIME(6) NOT NULL,
    #updated_at DATETIME(6) NOT NULL
#) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

 
  # =========================
    # 문자열 표현 (선택)
    # =========================
    # Admin / Shell에서 객체를 문자열로 볼 때 사용
    #def __str__(self):
        #return f"[{self.category}] {self.title}"