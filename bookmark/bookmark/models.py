from django.db import models
from django.utils import timezone
# Model = DB의 테이블
# Field = DB의 컬럼

# 북마크 모델
# name : 북마크 이름 (VARCHAR)
# url  : 북마크 주소 (VARCHAR)
class Bookmark(models.Model):
    # ==========================================================
    # [0] 이 클래스가 “DB 테이블”이 되는 원리
    # ==========================================================
    # Django는 models.Model을 상속한 클래스를 발견하면
    # 1) 앱 로딩 시점에 “모델 레지스트리(App registry)”에 등록하고,
    # 2) 이 모델의 필드 정보를 모아서 “스키마(테이블 구조)”를 정의하며,
    # 3) 마이그레이션(migrations)을 통해 실제 DB에 테이블을 생성/수정한다.
    #
    # 즉, Bookmark 클래스 = “파이썬 클래스”이면서 동시에
    # ORM 관점에서 “bookmark_bookmark 같은 DB 테이블”의 설계도 역할을 한다.
    #
    # ※ 실제 테이블 생성은:
    #    python manage.py makemigrations
    #    python manage.py migrate
    # 를 해야 DB에 반영된다.
    # ==========================================================

    # ==========================================================
    # [1] name 필드: CharField = VARCHAR 계열 문자열 컬럼
    # ==========================================================
    # name = models.CharField(...) 한 줄이 의미하는 것:
    # 1) Bookmark 테이블에 "name" 컬럼을 만든다.
    # 2) Django Form / Admin에서 이 필드가 입력 폼으로 자동 생성된다.
    # 3) max_length=100은
    #    - DB 스키마(VARCHAR(100))에 반영되고,
    #    - Django 유효성 검사(Validation)에도 사용된다.
    #
    # 'Name' (verbose_name)은:
    # - Admin 화면에서 필드 라벨로 보이고,
    # - 에러 메시지에서도 “Name”으로 표시될 수 있다.
    name = models.CharField('Name', max_length=100)

    # ==========================================================
    # [2] url 필드: URLField = URL 검증이 포함된 문자열 컬럼
    # ==========================================================
    # URLField는 내부적으로 CharField 기반이지만,
    # 폼/관리자에서 입력값을 받을 때 “URL 형식인지” 검증(validation)을 추가로 한다.
    #
    # 즉 DB는 결국 문자열이지만,
    # Django 레벨에서 "http(s)://..." 같은 형식 체크를 더 해준다.
    url = models.URLField('URL')

    # ==========================================================
    # [3] created_at: auto_now_add=True (생성 시각 고정)
    # ==========================================================
    # auto_now_add=True 동작 원리:
    # - 객체가 DB에 “처음 저장될 때(INSERT)”만 현재 시간을 자동으로 넣는다.
    # - 이후 save()로 수정(UPDATE)해도 created_at은 바뀌지 않는다.
    #
    # 주의:
    # - created_at 값을 직접 지정해서 저장하려 하면(일반적인 save) 덮어쓰는 경우가 많다.
    # - 생성 시각(로그/감사 컬럼)으로 많이 쓴다.
    created_at = models.DateTimeField('생성일시', auto_now_add=True)

    # ==========================================================
    # [4] updated_at: auto_now=True (저장할 때마다 갱신)
    # ==========================================================
    # auto_now=True 동작 원리:
    # - 객체가 저장될 때마다(INSERT든 UPDATE든)
    #   “현재 시간”으로 자동 갱신한다.
    #
    # 즉:
    # - 처음 만들 때도 찍히고
    # - 수정할 때마다 계속 최신으로 바뀐다.
    #
    # “마지막 수정 시각” 추적용으로 표준이다.
    updated_at = models.DateTimeField('수정일시', auto_now=True)

    # ==========================================================
    # [5] __str__: Admin/쉘/디버깅에서 “객체를 사람이 읽기 좋게” 바꿔주는 곳
    # ==========================================================
    # Django Admin 목록에서:
    # - Bookmark object (1) 같은 기본 표시 대신
    # - __str__의 반환값을 사용해서 보여준다.
    #
    # 동작 원리:
    # 1) 파이썬에서 str(obj) 호출하면 obj.__str__()가 호출된다.
    # 2) Admin은 객체를 출력할 때 기본적으로 str(obj)를 사용한다.
    # 3) 그래서 __str__이 있으면 그게 그대로 화면 표시가 된다.
    #
    # 왜 예전엔 "Bookmark object (1)"이었나?
    # - __str__이 없으면 models.Model 기본 구현이 실행되고,
    # - 그 기본 구현이 “<ModelName> object (<pk>)” 형태를 만든다.
    def __str__(self):
        # 여기서 반드시 “문자열(str)”을 반환해야 한다.
        # name이 빈 문자열이면 화면에 빈 값처럼 보일 수 있음.
        return self.name

    # ==========================================================
    # [6] Meta: “테이블 구조”가 아니라 “표현/동작 설정” 영역
    # ==========================================================
    # Meta 안의 값들은 주로:
    # - Admin에서 어떻게 표시할지
    # - 기본 정렬(ordering)을 어떻게 할지
    # - 테이블 이름(db_table)을 어떻게 할지
    # 같은 “부가 설정”을 담당한다.
    #
    # ※ IMPORTANT:
    # Meta 안에 __str__을 넣으면 안 된다.
    # __str__은 모델 클래스의 메서드여야 ORM/ADMIN이 인식한다.
    class Meta:
        # Admin에서 모델 단수 이름 표시
        verbose_name = '북마크'

        # Admin에서 모델 복수 이름(사이드바 목록 제목 등) 표시
        verbose_name_plural = '북마크 목록'

        # (참고) 이런 것도 Meta에 자주 넣음:
        # ordering = ['-created_at']  # 기본 정렬: 최신 생성순
        # db_table = 'bookmark'       # 실제 DB 테이블명 강제 지정

# makemigrations
# → 모델 변경 사항을 분석해서 migration.py 파일을 생성함
# → 실제 DB에는 아직 아무 영향 없음
# → Git commit 대상 (설계도 생성 단계)

# migrate
# → migrations 폴더 안의 migration 파일들을 실제 DB에 적용
# → 실제 테이블 생성/수정/삭제가 발생
# → DB 상태가 변경됨

# makemigrations = DB 설계도 생성
# migrate = 설계도를 실제 DB에 반영

# makemigrations → commit → github
# migrate → 로컬/서버 DB에 적용 ->git의 push

