// ================================
// 🚀 DOM 로딩 완료 후 실행
// ================================
document.addEventListener("DOMContentLoaded", () => {

  // ================================
  // 🔐 로그인 상태 확인 & 공통 헤더
  // ================================
  const token = localStorage.getItem("access_token");

  if (!token) {
    location.href = "/login";
    return;
  }

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };


  // ================================
  // 👤 사용자 정보 로드
  // ================================
  async function loadUser() {
    const res = await fetch("/auth/me", { headers });
    if (!res.ok) return;

    const user = await res.json();
    const el = document.getElementById("username");
    if (el) el.innerText = `안녕하세요, ${user.username}`;
  }


  // ================================
  // ❓ 랜덤 질문
  // ================================
  async function loadQuestion() {
    const res = await fetch("/question/random", { headers });
    if (!res.ok) return;

    const data = await res.json();
    const el = document.getElementById("questionText");
    if (el) el.innerText = data.content;
  }
  window.loadQuestion = loadQuestion;


  // ================================
  // 💬 랜덤 명언
  // ================================
  async function loadQuote() {
    const res = await fetch("/quote/random", { headers });
    if (!res.ok) return;

    const data = await res.json();
    const el = document.getElementById("quoteText");
    if (el) el.innerText = `"${data.content}"`;
  }


  // ================================
  // 📝 일기 저장
  // ================================
  async function saveDiary() {
    const titleEl = document.getElementById("title");
    const contentEl = document.getElementById("content");

    if (!titleEl || !contentEl) return;

    const title = titleEl.value.trim();
    const content = contentEl.value.trim();

    if (!title || !content) {
      alert("제목과 내용을 입력하세요");
      return;
    }

    await fetch("/diary", {
      method: "POST",
      headers,
      body: JSON.stringify({ title, content }),
    });

    titleEl.value = "";
    contentEl.value = "";

    loadMyDiaries();
  }
  window.saveDiary = saveDiary;


  // ================================
  // 📚 내 일기 목록
  // ================================
  async function loadMyDiaries() {
    const res = await fetch("/diary?limit=3", { headers });
    if (!res.ok) return;

    const diaries = await res.json();
    const box = document.getElementById("diaryList");
    if (!box) return;

    box.innerHTML = "";

    diaries.forEach(d => {
      const div = document.createElement("div");
      div.innerText = `• ${d.title}`;
      box.appendChild(div);
    });
  }


  // ================================
  // ⭐ 명언 북마크
  // ================================
  async function bookmarkQuote() {
    await fetch("/quote/bookmark", {
      method: "POST",
      headers,
    });
    alert("북마크 완료!");
  }
  window.bookmarkQuote = bookmarkQuote;


  // ================================
  // 🚪 로그아웃
  // ================================
  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    location.href = "/login";
  }
  window.logout = logout;


  // ================================
  // 🚀 최초 실행
  // ================================
  loadUser();
  loadQuestion();
  loadQuote();
  loadMyDiaries();
});
