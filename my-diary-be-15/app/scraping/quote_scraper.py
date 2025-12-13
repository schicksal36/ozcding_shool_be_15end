import httpx
from bs4 import BeautifulSoup
from app.models.quote import Quote


# =====================================================================
# 🔥 scrape_and_save_quotes — saramro.com 명언 스크래핑 후 DB 저장 함수
# ---------------------------------------------------------------------
# FastAPI의 비동기 환경에 최적화되어 있으며,
# httpx.AsyncClient + BeautifulSoup + Tortoise ORM을 조합한 구조.
#
# 동작 요약:
#   1) saramro.com?page=N 형태로 페이지 반복 조회
#   2) HTML 파싱 → 명언 텍스트 & 작가 추출
#   3) DB 중복 여부 확인 (content 기준)
#   4) 새로운 명언만 DB에 저장
#   5) 총 저장 개수, 누적 quote 수 반환
#
# 비동기 구조이므로 메인 서버가 블로킹되지 않아 고성능 유지 가능.
# =====================================================================
async def scrape_and_save_quotes(pages: int = 5):
    base_url = "https://saramro.com/quotes"
    saved_count = 0   # 새로 저장된 명언의 개수

    # -----------------------------------------------------------------
    # 🔥 httpx.AsyncClient()
    # -----------------------------------------------------------------
    # 비동기 요청을 지원하는 HTTP 클라이언트
    # requests와 달리 await 를 사용할 수 있어 FastAPI에 적합함.
    # 세션을 async context로 열어 여러 요청을 효율적으로 처리.
    # -----------------------------------------------------------------
    async with httpx.AsyncClient() as client:

        # ==============================================================
        # 🔥 1) 요청할 페이지 반복
        # ==============================================================
        for page in range(1, pages + 1):
            url = f"{base_url}?page={page}"

            try:
                # -----------------------------------------------------
                # 🔸 HTTP GET 요청
                # -----------------------------------------------------
                response = await client.get(url)

                # 실패 시 스킵
                if response.status_code != 200:
                    continue

                # -----------------------------------------------------
                # 🔸 HTML 파싱 (BeautifulSoup)
                # -----------------------------------------------------
                soup = BeautifulSoup(response.text, "html.parser")

                # saramro.com 의 명언 리스트는 table 구조로 되어 있음
                quote_elements = soup.select("table tbody tr")

                # ======================================================
                # 🔥 2) 테이블 각 row(tr) 에서 명언 추출
                # ======================================================
                for el in quote_elements:

                    # td[colspan="5"] 영역이 실제 명언이 들어있는 곳
                    scraped = el.select_one("td[colspan='5']")
                    if not scraped:
                        continue  # 명언이 아닌 row는 건너뜀

                    # -------------------------------------------------
                    # "명언 내용 - 작가" 형태를 기준으로 split
                    # -------------------------------------------------
                    cont_and_auth = scraped.get_text(strip=True).split("-")

                    content = cont_and_auth[0]               # 명언 본문
                    author = cont_and_auth[1][1:] if len(cont_and_auth) > 1 else None
                    # author[1:] → 앞에 붙어있는 공백 문자 제거

                    # -------------------------------------------------
                    # 🔥 3) DB 중복 검사 (content로 검증)
                    # -------------------------------------------------
                    exists = await Quote.filter(content=content).exists()

                    if not exists:
                        # 새로운 명언만 DB 저장
                        await Quote.create(content=content, author=author)
                        saved_count += 1

            except Exception as e:
                # 페이지 단위 에러는 다른 페이지 진행에 영향을 주지 않도록 처리
                print(f"Error scraping page {page}: {e}")
                continue

    # ==============================================================
    # 🔥 4) 전체 명언 개수 조회 후 반환
    # ==============================================================
    total_count = await Quote.all().count()

    return {
        "message": f"Scraping completed. Saved {saved_count} new quotes.",
        "total_quotes": total_count,
    }


