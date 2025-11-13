# Vercel에서 Turso로 SQLite 만들고 프로젝트에 연결하기

---
## 🌐 Vercel이란?
- [Vercel](https://vercel.com/)은 프론트엔드 배포로 유명한 서버리스 플랫폼이지만, 최근에는 Python, Go, Ruby 같은 서버 코드도 실행 가능합니다.
- 특징:
  - ✅ GitHub/GitLab/Bitbucket 저장소와 연동 → 푸시하면 자동 배포
  - ✅ 무료 플랜 제공
  - ✅ 서버리스(Serverless) 환경이라 인프라 관리 필요 없음
  - ✅ Edge Functions를 활용해 빠른 응답


## 🌐 Turso란?

- **[Turso](https://turso.tech/)** 는 SQLite를 기반으로 한 **클라우드 데이터베이스 서비스**입니다.
- 원래 SQLite는 파일 기반 DB라서 로컬 개발에는 편리하지만, **클라우드(서버리스 환경)** 에서 쓰면 파일이 휘발되거나 여러 인스턴스에서 동기화 문제가 생길 수 있습니다.
- Turso는 SQLite와 **완벽 호환**되면서도, DB 파일을 네트워크 상에 두고 클라우드에서 안전하게 읽기/쓰기할 수 있도록 해줍니다.
- 장점:
  - ✅ **SQLite 문법 그대로 사용 가능**
  - ✅ **무료 플랜 제공**
  - ✅ **서버리스 환경(Vercel, Cloudflare 등)과 잘 맞음**
  - ✅ **낮은 지연시간** (엣지 DB)

즉, **"로컬 SQLite의 편리함 + 클라우드 DB의 안정성"** 을 결합한 것이 Turso입니다.

---

## ⚙️ Turso를 Vercel에서 생성하기

1. https://vercel.com/ 에서 회원가입 및 로그인을 진행하세요.
2. `Storage` 턉에서 `Turso`를 찾아 `Create` 버튼을 클릭합니다.
3. Get Started가 나왔다면 `Accept and Create` 버튼을 클릭합니다.
4. `Primary Regon`을 `US East(Virginia)`로 설정합니다. 이후 아무것도 건들지 않고 바로 `Continue` 버튼을 클릭합니다.
5. `Database Name`을 원하는 것으로 입력 후, `Create` 버튼을 클릭합니다.
6. 10초 정도 기다리면 데이터베이스가 생성됩니다. `Done`버튼을 누르면, 자동으로 Turso 정보가 담긴 화면으로 넘어갑니다.<br/>`Copy Snippet`을 클릭하여 값을 복사합니다.
7. **⚠️ 6번에서 복사한 값은 외부로 노출 시 해킹의 위협을 받을 수 있습니다. 절대 github에 그대로 올려 노출되지 않게 주의해주세요.**
8. 그럼 이 값을 어떻게 가리고 보관하냐, `env` 파일 및 설정을 이용하면 됩니다. 다음 방법을 참고해주세요.

---

## 🛠️ Flask 코드 수정하기

> 개발 문서가 분산되어 있기 때문에, 정확한 정보는 https://github.com/tursodatabase/sqlalchemy-libsql 여기에서 확인하시길 추천드립니다.

1. 필요한 패키지를 추가 후 requirements.txt를 업데이트 합니다.
   ```bash
   # 패키지 설치
   pip install sqlalchemy-libsql python-dotenv

   # requirements.txt 업데이트
   pip freeze > requirements.txt
   ```

2. 프로젝트 루트에 `.env` 파일을 만드세요. 여기에 복사한 값을 붙여넣기 합니다.<br/>**⚠️ .env를 .gitignore에 반드시 추가해주세요!!**
   ```plaintext
   # .env
   TURSO_DATABASE_URL=libsql://your-db-name.turso.io
   TURSO_AUTH_TOKEN=your-secret-auth-token
   ```

3. sqlite 세팅 코드를 수정합니다.<br/>문제에서 드린 예시 코드 기준으로, `app/config.py`, `app/__init__.py`에서 수정을 진행하시면 됩니다.
    ```python
    # app/config.py

    import os
    from dotenv import load_dotenv

    load_dotenv()

    class Config:
        TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
        TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

    if not TURSO_DATABASE_URL and not TURSO_AUTH_TOKEN:
        # .env에 값이 있을 시에만 Turso를 사용하도록 설정
        SQLALCHEMY_DATABASE_URI = f"sqlite+{TURSO_DATABASE_URL}?secure=true"
        CONNECT_ARGS = {"auth_token": TURSO_AUTH_TOKEN}
    else:
        # Turso 정보가 없거나 에러가 발생한다면 로컬 db를 사용하도록 설정
        print("\n[INFO] No Turso Setup: Use local db...\n")

        # instance 폴더 경로
        INSTANCE_DIR = os.path.join(os.path.dirname(__file__), "..", "instance")

        # 폴더가 없으면 생성
        os.makedirs(INSTANCE_DIR, exist_ok=True)

        SQLALCHEMY_DATABASE_URI = "sqlite:///instance/reviews.db"
        CONNECT_ARGS = {"check_same_thread": False}
    ```

    ```python
    # app/__init__.py

    engine = create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
        echo=True,
        connect_args=Config.CONNECT_ARGS
    )
    ```

4. 서버를 실행 후 잘 작동되는지 확인하세요.

---

## 🚀 Vercel에 프로젝트 배포하기

1. 프로젝트 루트 디렉토리에서 `vercel.json`을 설정해주세요.
   ```json
   {
     "builds": [
       {
         "src": "run.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "/run.py"
       },
       {
         "src": "/static/(.*)",
         "dest": "/run.py"
       }
     ]
   }
   ```
2. `requirements.txt` 파일이 루트 디렉토리에 있는지 꼭 확인하세요. 없으면 `pip freeze > requirements.txt`를 실행해주세요.
3. [Vercel](https://vercel.com)의 메인 페이지에서 `Overview` 탭을 클릭합니다.
4. 오른쪽 위의 `Add New...` > `Project`를 클릭합니다.
5. 프로젝트 repository를 import 합니다.
6. Environment Variables를 설정합니다. `.env`를 참고하세요.
7. `Deploy` 버튼을 눌러 프로젝트를 serverless로 배포합니다.