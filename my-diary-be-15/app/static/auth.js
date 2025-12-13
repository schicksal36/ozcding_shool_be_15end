// ================================
// 🔧 API BASE
// ================================
const API_BASE = "/auth";


// ================================
// 🚀 DOM 로딩 완료 후 실행
// ================================
document.addEventListener("DOMContentLoaded", () => {

  const loginTab = document.getElementById("loginTab");
  const signupTab = document.getElementById("signupTab");

  const loginForm = document.getElementById("loginForm");
  const signupForm = document.getElementById("signupForm");

  const error = document.getElementById("error");

  // ================================
  // 🔄 초기 화면 상태
  // ================================
  loginForm.style.display = "block";
  signupForm.style.display = "none";


  // ================================
  // 🔄 탭 전환
  // ================================
  loginTab.addEventListener("click", () => {
    loginTab.classList.add("active");
    signupTab.classList.remove("active");
    loginForm.style.display = "block";
    signupForm.style.display = "none";
    error.innerText = "";
  });

  signupTab.addEventListener("click", () => {
    signupTab.classList.add("active");
    loginTab.classList.remove("active");
    signupForm.style.display = "block";
    loginForm.style.display = "none";
    error.innerText = "";
  });


  // ================================
  // 🔐 로그인 처리 (username 기준)
  // ================================
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    error.innerText = "";

    if (!username || !password) {
      error.innerText = "닉네임과 비밀번호를 입력하세요.";
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) throw new Error();

      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);

      window.location.href = "/dashboard";

    } catch {
      error.innerText = "닉네임 또는 비밀번호가 올바르지 않습니다.";
    }
  });


  // ================================
  // 🆕 회원가입 처리 (UserCreate 스키마 100% 일치)
  // ================================
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("signupUsername").value.trim();
    const email = document.getElementById("signupEmail").value.trim();
    const password = document.getElementById("signupPassword").value;
    const passwordConfirm = document.getElementById("signupPasswordConfirm").value;

    error.innerText = "";

    if (!username || username.length < 3) {
      error.innerText = "닉네임은 3자 이상이어야 합니다.";
      return;
    }

    if (!email) {
      error.innerText = "이메일을 입력하세요.";
      return;
    }

    if (!password || password.length < 3) {
      error.innerText = "비밀번호는 3자 이상이어야 합니다.";
      return;
    }

    if (password !== passwordConfirm) {
      error.innerText = "비밀번호가 일치하지 않습니다.";
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });

      if (!res.ok) throw new Error();

      alert("회원가입 성공! 로그인해주세요.");
      loginTab.click();

    } catch {
      error.innerText = "이미 존재하는 사용자입니다.";
    }
  });

});
// 로그인 성공 후
const data = await res.json();

// 🔥 user 정보도 같이 저장
localStorage.setItem("access_token", data.access_token);
localStorage.setItem("user", JSON.stringify(data.user));

window.location.href = "/dashboard";
