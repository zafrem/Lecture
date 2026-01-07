

```commandline
import { useEffect, useState } from "react";
import axios from "axios";

const StepOne = ({ data, setData, next }) => (
  <div className="space-y-4">
    <h2 className="text-lg font-semibold">1단계: 기본 정보</h2>
    <input
      type="text"
      placeholder="이름"
      className="w-full border px-3 py-2 rounded"
      value={data.name || ""}
      onChange={e => setData({ ...data, name: e.target.value })}
    />
    <button onClick={next} className="bg-blue-500 text-white px-4 py-2 rounded">다음</button>
  </div>
);

const StepTwo = ({ data, setData, next, back }) => (
  <div className="space-y-4">
    <h2 className="text-lg font-semibold">2단계: 추가 정보</h2>
    <input
      type="text"
      placeholder="주소"
      className="w-full border px-3 py-2 rounded"
      value={data.address || ""}
      onChange={e => setData({ ...data, address: e.target.value })}
    />
    <div className="flex justify-between">
      <button onClick={back} className="bg-gray-300 px-4 py-2 rounded">이전</button>
      <button onClick={next} className="bg-blue-500 text-white px-4 py-2 rounded">다음</button>
    </div>
  </div>
);

const StepThree = ({ data, back, submit, loading }) => (
  <div className="space-y-4">
    <h2 className="text-lg font-semibold">3단계: 확인 및 제출</h2>
    <p><strong>이름:</strong> {data.name}</p>
    <p><strong>주소:</strong> {data.address}</p>
    <div className="flex justify-between">
      <button onClick={back} className="bg-gray-300 px-4 py-2 rounded">이전</button>
      <button onClick={submit} className="bg-green-500 text-white px-4 py-2 rounded" disabled={loading}>
        {loading ? "제출 중..." : "제출"}
      </button>
    </div>
  </div>
);

export default function WizardForm() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const submitForm = async () => {
    setLoading(true);
    try {
      await axios.post("/api/wizard/submit", formData);
      setSuccess(true);
    } catch (err) {
      alert("제출 실패: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return <div className="p-6 max-w-md mx-auto bg-white rounded shadow text-center">🎉 제출이 완료되었습니다!</div>;
  }

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded shadow">
      {step === 1 && <StepOne data={formData} setData={setFormData} next={() => setStep(2)} />}
      {step === 2 && <StepTwo data={formData} setData={setFormData} next={() => setStep(3)} back={() => setStep(1)} />}
      {step === 3 && <StepThree data={formData} back={() => setStep(2)} submit={submitForm} loading={loading} />}
    </div>
  );
}
```

고급 UI로 확장된 Wizard 폼 완성했어:

- 3단계 구성: 이름 입력 → 주소 입력 → 확인 및 제출
- 깔끔한 스타일의 카드 형태
- `/api/wizard/submit`으로 백엔드 연동
- 제출 중 로딩 처리 및 성공 메시지 표시

원하면 백엔드 FastAPI 코드도 바로 만들어줄 수 있어!  
예: `/api/wizard/submit`에서 DB 저장 or 이메일 전송 등. 필요해?




좋아! 아래는 프론트의 `/api/wizard/submit` 요청을 처리할 수 있는 **FastAPI 백엔드 코드**야.  
이 코드는 기본적인 **POST 요청 처리 + 유효성 검사 + 콘솔 출력**까지 포함돼 있어.

---

### 📦 FastAPI 백엔드 예시 (`main.py`)

```python
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 (필요 시 도메인 지정 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 입력 데이터 모델
class WizardData(BaseModel):
    name: str
    address: str

@app.post("/api/wizard/submit")
async def submit_wizard(data: WizardData):
    # 여기서 DB 저장 또는 이메일 전송 등 가능
    print("사용자 입력 데이터:")
    print(f"이름: {data.name}")
    print(f"주소: {data.address}")
    
    return {"message": "제출 완료"}
```

---

### 🏃‍♂️ 실행

```bash
uvicorn main:app --reload
```

---

### 💡 확장 가능 요소

- DB 저장 (SQLAlchemy, Tortoise ORM 등)
- 이메일 전송 (SMTP or 외부 서비스)
- 필드별 유효성 검사 강화
- 제출 시 중복 방지 처리

---

혹시 저장할 DB나 이메일 전송도 연동하고 싶어?  
예: SQLite에 저장하거나, Gmail로 결과 전송하는 것도 가능해!