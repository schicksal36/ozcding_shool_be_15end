// ================================
// 🔐 로그인 상태 확인
// ================================

// 🔹 브라우저 localStorage에 저장된 JWT 토큰을 가져옴
//    로그인 성공 시 auth.js에서 저장한 access_token
const token = localStorage.getItem("access_token");

// 🔹 토큰이 없다는 것은 로그인하지 않은 상태
//    → 내 일기 페이지는 인증 사용자만 접근 가능
//    → 토큰이 없으면 루트(/) 또는 로그인 페이지로 강제 이동
if (!token) location.href = "/";

// 🔹 API 요청 시 사용할 공통 헤더 객체
//    Authorization 헤더에 Bearer 토큰을 담아 서버에 인증 정보 전달
const headers = {
  Authorization: `Bearer ${token}`,
};


// ================================
// 📚 내 일기 목록 로드
// ================================

async function loadDiaries() {
  // 🔹 내 일기 전체 조회 API 호출
  //    서버는 JWT를 통해 "요청한 사용자"의 일기만 반환
  const res = await fetch("/api/v1/diary", { headers });

  // 🔹 응답 데이터를 JSON 형태로 변환
  const diaries = await res.json();

  // 🔹 일기 목록을 출력할 HTML 요소
  //    <div id="diaries"></div> 가 HTML에 있어야 함
  const box = document.getElementById("diaries");

  // 🔹 기존에 표시되어 있던 목록 초기화
  box.innerHTML = "";

  // 🔹 아직 작성한 일기가 하나도 없는 경우
  if (diaries.length === 0) {
    // 사용자에게 안내 메시지와 대시보드 이동 링크 표시
    box.innerHTML = `
      <p>아직 작성한 일기가 없어요.</p>
      <a href="/dashboard">첫 번째 일기 작성하기 →</a>
    `;
    return; // 이후 로직 실행 중단
  }

  // 🔹 조회된 일기 목록을 하나씩 화면에 추가
  diaries.forEach(d => {
    // 각 일기를 감싸는 div 요소 생성
    const div = document.createElement("div");

    // 제목과 내용을 HTML 구조로 삽입
    div.innerHTML = `
      <h3>${d.title}</h3>
      <p>${d.content}</p>
      <hr />
    `;

    // 생성한 div를 일기 목록 영역에 추가
    box.appendChild(div);
  });
}


// ================================
// 🚪 로그아웃
// ================================

function logout() {
  // 🔹 localStorage에 저장된 JWT 토큰 제거
  //    → 인증 정보 완전히 삭제
  localStorage.removeItem("access_token");

  // 🔹 루트(/) 또는 로그인 페이지로 이동
  location.href = "/";
}


// ================================
// 🚀 페이지 최초 로드 시 실행
// ================================

// 🔹 페이지가 열리자마자 내 일기 목록을 서버에서 불러옴
loadDiaries();
