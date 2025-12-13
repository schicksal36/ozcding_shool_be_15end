from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.db.session import init_tortoise
from app.core.config import settings

# API 라우터
from app.api.v1 import auth as auth_router
from app.api.v1 import diary as diary_router
from app.api.v1 import quote as quote_router
from app.api.v1 import question as question_router


# ======================================================================
# 🔥 FastAPI 앱 생성
# ======================================================================
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)


# ======================================================================
# 🔥 CORS 설정
# ======================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================================================================
# 🔥 Tortoise ORM 초기화
# ======================================================================
init_tortoise(app)


# ======================================================================
# 🔥 템플릿 & 정적 파일
# ======================================================================
templates = Jinja2Templates(directory="app/templates")

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


# ======================================================================
# 🔥 HTML 페이지 라우트 (❗ API랑 완전히 분리됨)
# ======================================================================
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/diaries", response_class=HTMLResponse)
def diaries(request: Request):
    return templates.TemplateResponse("diaries.html", {"request": request})


# ======================================================================
# 🔥 API 라우터 등록 (🔥 핵심 수정)
# ======================================================================
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(diary_router.router, prefix="/api/v1")
app.include_router(quote_router.router, prefix="/api/v1")
app.include_router(question_router.router, prefix="/api/v1")


# ======================================================================
# 🔥 헬스 체크
# ======================================================================
@app.get("/", summary="DB 연결 헬스 체크")
async def health_check():
    return {
        "status": "healthy",
        "message": "OK",
    }
