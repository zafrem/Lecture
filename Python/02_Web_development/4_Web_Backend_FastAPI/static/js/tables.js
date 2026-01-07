
(() => {
    console.log("tables.js loaded");

    let rawData = [];
    let filteredData = [];
    let currentPage = 1;
    const rowsPerPage = 10;
    let currentSort = { column: null, asc: true };

    const searchInput = document.getElementById("searchInput");
    const searchBtn = document.getElementById("searchBtn");
    const tableBody = document.getElementById("tableBody");
    const pagination = document.getElementById("pagination");
    const noResultsText = document.getElementById("noResults");
    const countDisplay = document.getElementById("dataCount");
    const loadingMessage = document.getElementById("loadingMessage");
    const downloadBtn = document.getElementById("downloadBtn");
    const inputName = document.getElementById("inputName");
    const inputAge = document.getElementById("inputAge");

    try {
        rawData = JSON.parse(document.getElementById("data-json").textContent);
        filteredData = rawData;
    } catch (e) {
        console.error("JSON 파싱 실패:", e);
    }

    function showLoading(show) {
        loadingMessage.style.display = show ? "block" : "none";
    }

    function updateTable() {
        showLoading(true);
        setTimeout(() => {
            const keyword = searchInput.value.toLowerCase();
            currentPage = 1;

            filteredData = rawData.filter(item =>
                Object.values(item).some(val =>
                    String(val).toLowerCase().includes(keyword)
                )
            );

            noResultsText.style.display = filteredData.length === 0 ? "block" : "none";
            countDisplay.textContent = `총 ${filteredData.length}건`;

            renderTable();
            renderPagination();
            showLoading(false);
        }, 200);
    }

    function renderTable() {
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const slice = filteredData.slice(start, end);

        tableBody.innerHTML = "";
        slice.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `<td>${item.id}</td><td>${item.Host}</td><td>${item.VaultPath}</td>`;
            tableBody.appendChild(row);
        });
    }

    function renderPagination() {
        const pageCount = Math.ceil(filteredData.length / rowsPerPage);
        pagination.innerHTML = "";

        for (let i = 1; i <= pageCount; i++) {
            const btn = document.createElement("button");
            btn.textContent = i;
            btn.className = i === currentPage ? "active" : "";
            btn.onclick = () => {
                currentPage = i;
                renderTable();
                renderPagination();
            };
            pagination.appendChild(btn);
        }
    }

    function sortBy(column) {
        if (currentSort.column === column) {
            currentSort.asc = !currentSort.asc;
        } else {
            currentSort.column = column;
            currentSort.asc = true;
        }

        filteredData.sort((a, b) => {
            const aVal = a[column];
            const bVal = b[column];
            return typeof aVal === "number"
                ? (currentSort.asc ? aVal - bVal : bVal - aVal)
                : (currentSort.asc ? String(aVal).localeCompare(String(bVal)) : String(bVal).localeCompare(String(aVal)));
        });

        renderTable();
    }

    function downloadCSV() {
        const headers = ["번호", "이름", "나이"];
        const csvRows = [headers.join(",")];

        filteredData.forEach(item => {
            csvRows.push([item.id, item.name, item.age].join(","));
        });

        const blob = new Blob([csvRows.join("\n")], { type: "text/csv;charset=utf-8;" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "lists.csv";
        link.click();
    }

    searchBtn.addEventListener("click", updateTable);
    searchInput.addEventListener("keypress", e => {
        if (e.key === "Enter") updateTable();
    });

    document.querySelectorAll("thead th").forEach((th, idx) => {
        const key = ["id", "Host", "VaultPath"][idx];
        th.style.cursor = "pointer";
        th.addEventListener("click", () => sortBy(key));
    });

    downloadBtn.addEventListener("click", downloadCSV);
    updateTable();

    const addDataBtn = document.getElementById("addDataBtn");
    const addDataForm = document.getElementById("addDataForm");


    addDataBtn.addEventListener("click", () => {
        const isVisible = addDataForm.classList.toggle("show");
        const visible = addDataForm.style.display === "block";

        addDataBtn.textContent = isVisible ? "추가 모드" : "추가 닫기";
        addDataForm.style.display = visible ? "none" : "block";
        //addDataForm.style.display = justify-content ? "none" : "block";
    });


    submitBtn.addEventListener("click", async () => {
        const name = inputName.value.trim();
        const age = parseInt(inputAge.value, 10);

        if (!name || isNaN(age)) {
            alert("이름과 나이를 올바르게 입력하세요.");
            return;
        }

        const res = await fetch("/table_add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, age })
        });

        if (res.ok) {
            alert("저장되었습니다!");
            inputName.value = "";
            inputAge.value = "";
            updateTable(); // 새로고침
        } else {
            alert("저장에 실패했습니다.");
        }
    });
})();
