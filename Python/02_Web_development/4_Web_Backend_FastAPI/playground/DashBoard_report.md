아래는 **FastAPI 대시보드 페이지를 열고, 스크린샷을 찍고, 이메일로 전송하는 전체 Python 코드** 예시야.  
크게 3단계로 나뉘어:

1. **웹페이지 스크린샷 찍기 (Selenium 사용)**
2. **이메일 보내기 (smtplib 사용)**
3. **FastAPI에서 호출할 수 있게 엔드포인트 제공**

---

### 📦 필요한 패키지
```bash
pip install fastapi uvicorn selenium aiofiles python-multipart
```

---

### 🧠 전체 코드 예시

```python
from fastapi import FastAPI, BackgroundTasks
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from email.message import EmailMessage
import smtplib
import ssl
import time
import os

app = FastAPI()

# 1. 대시보드 스크린샷 찍기 함수
def take_screenshot(url: str, output_path: str = "dashboard.png"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 720)
    driver.get(url)
    
    time.sleep(3)  # 페이지 로딩 대기
    driver.save_screenshot(output_path)
    driver.quit()

# 2. 이메일 보내기 함수
def send_email_with_attachment(to_email: str, screenshot_path: str):
    msg = EmailMessage()
    msg["Subject"] = "📊 대시보드 스크린샷"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = to_email
    msg.set_content("첨부된 이미지에서 대시보드를 확인하세요.")

    with open(screenshot_path, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="image", subtype="png", filename="dashboard.png")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login("your_email@gmail.com", "your_app_password")
        smtp.send_message(msg)

# 3. FastAPI 엔드포인트
@app.post("/send-dashboard/")
async def send_dashboard(to: str, background_tasks: BackgroundTasks):
    url = "http://localhost:8000/dashboard"  # 대시보드 URL
    screenshot_path = "dashboard.png"

    # 백그라운드에서 처리
    def job():
        take_screenshot(url, screenshot_path)
        send_email_with_attachment(to, screenshot_path)
        os.remove(screenshot_path)

    background_tasks.add_task(job)
    return {"message": "대시보드 스크린샷 전송 중입니다."}
```

---

### ✅ 사용 예
```bash
curl -X POST "http://localhost:8000/send-dashboard/" -H "Content-Type: application/json" -d '{"to": "받는사람이메일@example.com"}'
```

---

### 💡 참고
- Gmail 사용 시 **앱 비밀번호 생성** 필요.
- Docker나 리눅스 서버에서는 Chrome 드라이버 설정을 추가로 해줘야 해.
- `url`은 실제 대시보드가 열리는 정확한 경로로 바꿔줘야 해.

---

필요하면 ChromeDriver 설치법이나 Docker에서 headless 크롬 설정도 알려줄게!