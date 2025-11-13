# run.py
# ----------------------------
# Flask 실행 엔트리포인트 파일
# create_app()을 불러와서 서버 시작
# ----------------------------

from app import create_app   # app/__init__.py 안의 create_app() 함수

app = create_app()           # Flask 앱 생성

if __name__ == "__main__":
    app.run(debug=True)      # 개발 모드로 실행 (코드 변경 시 자동 리로드)
