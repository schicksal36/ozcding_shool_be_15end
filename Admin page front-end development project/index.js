document.addEventListener("DOMContentLoaded", () => {
  // ✅ 기본 상품 데이터
  const product_data = [
    { category: "상의", brand: "Supreme", product: "슈프림 박스로고 후드티", price: "390,000" },
    { category: "하의", brand: "DIESEL", product: "디젤 트랙 팬츠", price: "188,000" },
    { category: "신발", brand: "Nike", product: "에어포스 1", price: "137,000" },
    { category: "패션잡화", brand: "Music&Goods", product: "빵빵이 키링", price: "29,000" },
  ];

  // ✅ 요소 연결
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");
  const categorySelect = document.getElementById("inlineFormSelectPref");
  const darkToggle = document.getElementById("darkToggle");
  const signupBtn = document.getElementById("signupBtn");
  const signupCard = document.getElementById("signupCard");
  const submitSignup = document.getElementById("submitSignup");

  // ✅ DataTable 초기화
  const table = $("#product_data_Table").DataTable({
    data: product_data,
    columns: [
      { data: "category", title: "카테고리" },
      { data: "brand", title: "브랜드" },
      { data: "product", title: "상품명" },
      { data: "price", title: "가격" },
    ],
    pageLength: 5,
    ordering: true,
    searching: true,
    lengthChange: false,
    language: {
      search: "검색:",
      paginate: { previous: "이전", next: "다음" },
      info: "_TOTAL_개 중 _START_–_END_ 표시",
      infoEmpty: "표시할 데이터 없음",
      zeroRecords: "검색 결과가 없습니다.",
    },
    columnDefs: [{ className: "text-center", targets: "_all" }]
  });

  // ✅ 검색 기능
  searchBtn.addEventListener("click", () => {
    const keyword = searchInput.value.trim();
    const category = categorySelect.value;
    const filtered = product_data.filter((item) => {
      const matchCategory = category === "카테고리 선택..." || item.category === category;
      const matchKeyword = keyword === "" || item.product.includes(keyword);
      return matchCategory && matchKeyword;
    });
    table.clear().rows.add(filtered).draw();
  });

  // ✅ 다크모드 토글
  function updateDarkLabel() {
    darkToggle.textContent = document.body.classList.contains("dark-mode")
      ? "☀ 라이트모드"
      : "🌙 다크모드";
  }
  updateDarkLabel();
  darkToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    updateDarkLabel();
  });

  // ✅ 시계
  function updateClock() {
    const n = new Date();
    const days = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];
    const y = n.getFullYear();
    const m = String(n.getMonth() + 1).padStart(2, "0");
    const d = String(n.getDate()).padStart(2, "0");
    const h = String(n.getHours()).padStart(2, "0");
    const min = String(n.getMinutes()).padStart(2, "0");
    const s = String(n.getSeconds()).padStart(2, "0");
    const w = days[n.getDay()];
    document.getElementById("clock").textContent = `🕒 ${y}년 ${m}월 ${d}일 ${h}시${min}분 ${s}초 (${w})`;
  }
  setInterval(updateClock, 1000);
  updateClock();

  // ✅ 회원가입 폼 토글
  signupCard.style.display = "none";
  signupBtn.addEventListener("click", () => {
    const isOpen = signupCard.style.display === "block";
    signupCard.style.display = isOpen ? "none" : "block";
    signupBtn.textContent = isOpen ? "회원가입" : "닫기";
  });

  // ✅ 회원가입 입력 검증
  submitSignup.addEventListener("click", (e) => {
    e.preventDefault();

    const userid = document.getElementById("userid").value.trim();
    const pw = document.getElementById("password").value.trim();
    const pw2 = document.getElementById("password2").value.trim();
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!userid || !pw || !pw2 || !username || !email) {
      alert("⚠️ 모든 항목을 입력해주세요!");
      return;
    }
    if (pw.length < 6) {
      alert("⚠️ 비밀번호는 6자 이상이어야 합니다!");
      return;
    }
    if (pw !== pw2) {
      alert("⚠️ 비밀번호가 일치하지 않습니다!");
      return;
    }
    if (!email.includes("@") || !email.includes(".")) {
      alert("⚠️ 이메일 형식이 올바르지 않습니다!");
      return;
    }

    alert(`✅ 회원가입 완료!\n아이디: ${userid}\n이름: ${username}\n이메일: ${email}`);
    
    // 입력 초기화
    document.querySelectorAll("#signupCard input, #signupCard textarea").forEach(el => el.value = "");
    signupCard.style.display = "none";
    signupBtn.textContent = "회원가입";
  });
});
