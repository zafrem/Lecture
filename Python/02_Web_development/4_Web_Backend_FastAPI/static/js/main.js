console.log("✅ main.js loaded");

window.addEventListener("load", () => {
    console.log("✅ window loaded");
    loadContent("welcome");
});

function loadContent(page) {
    fetch("/" + page)
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById("content-area");
            container.innerHTML = html;
            console.log("_loadContent", page);
            if (page === "tables") {
                const existing = document.querySelector('script[src^="/static/js/tables.js"]');
                if (existing) {
                    existing.remove();  // 이전 스크립트 제거
                }

                const script = document.createElement("script");
                script.src = '/static/js/tables.js?v=${Date.now()}';  // 캐시 방지용 버전 파라미터
                script.defer = true;
                document.body.appendChild(script);
            }
        });
}
