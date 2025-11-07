document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("signupForm");

  form.addEventListener("submit", (e) => {
    e.preventDefault(); // 페이지 새로고침 방지

    const id = document.getElementById("userid").value.trim();
    const pw = document.getElementById("password").value.trim();
    const pw2 = document.getElementById("password2").value.trim();
    const name = document.getElementById("username").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const email = document.getElementById("email").value.trim();

    // ✅ 1. 필수항목 확인
    if (!id || !pw || !pw2 || !name || !phone || !email) {
    alert("⚠️ 모든 항목을 입력해주세요!");
    return;
}

    // ✅ 2. 비밀번호 길이 체크
    if (pw.length < 8) {
    alert("⚠️ 비밀번호는 8자 이상이어야 합니다!");
    return;
}

    // ✅ 3. 비밀번호 확인 일치 검사
    if (pw !== pw2) {
    alert("⚠️ 비밀번호가 일치하지 않습니다!");
    return;
}

    // ✅ 4. 이메일 형식 검사
    if (!email.includes("@") || !email.includes(".")) {
    alert("⚠️ 이메일 형식이 올바르지 않습니다!");
    return;
    }

    // ✅ 5. 전화번호 형식 검사 (기본적인 예: 010-0000-0000)
    const phoneRegex = /^010-\d{4}-\d{4}$/;
    if (!phoneRegex.test(phone)) {
    alert("⚠️ 전화번호 형식은 010-0000-0000 이어야 합니다!");
    return;
}

    // ✅ 6. 가입 완료 메시지
    alert(`✅ 회원가입 완료!\n\n아이디: ${id}\n이름: ${name}\n이메일: ${email}`);

 // ✅ 7. 확인 후 자동 복귀
    window.location.href = "index.html";
});
});