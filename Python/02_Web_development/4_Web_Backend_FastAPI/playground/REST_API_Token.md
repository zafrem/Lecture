좋아! FastAPI에서 **API 토큰 인증**을 적용하는 가장 기본적인 방법은 **OAuth2 + Bearer 토큰 방식**을 쓰는 거야. 아래에 **토큰 생성 → API 보호 → 인증 적용** 흐름을 간단하고 명확하게 정리해줄게.

---

## ✅ 1. 필요한 패키지 설치

```bash
pip install python-jose[cryptography]
```

---

## ✅ 2. JWT 토큰 생성 & 검증 함수 만들기 (`auth_token.py`)

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt

# 비밀 키, 알고리즘, 유효시간 설정
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 토큰 생성
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 토큰 검증
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

## ✅ 3. 로그인 시 토큰 발급 (`/token` 엔드포인트)

```python
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
from app.users_db import get_user, verify_password
from app.auth_token import create_access_token

router = APIRouter()

@router.post("/token")
def login_for_token(username: str = Form(...), password: str = Form(...)):
    user = get_user(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀립니다.")
    token = create_access_token({"sub": username})
    return JSONResponse({"access_token": token, "token_type": "bearer"})
```

---

## ✅ 4. API에 토큰 인증 적용

```python
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from app.auth_token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
    return payload["sub"]  # 사용자 이름
```

---

## ✅ 5. 실제 API에 적용 예시

```python
from fastapi import APIRouter, Depends
from app.auth_token import get_current_user

router = APIRouter()

@router.get("/secure-data")
def read_secure_data(current_user: str = Depends(get_current_user)):
    return {"message": f"{current_user}님만 볼 수 있는 데이터입니다!"}
```

---

## ✅ 테스트 방법 (curl 예시)

1. 로그인 → 토큰 받기

```bash
curl -X POST -F "username=test" -F "password=1234" http://localhost:8000/token
```

2. 토큰 받아서 API 요청

```bash
curl -H "Authorization: Bearer <복사한_토큰>" http://localhost:8000/secure-data
```

---

## ✅ 요약

| 단계          | 설명                           |
|---------------|--------------------------------|
| `create_token`| JWT 생성                        |
| `/token`      | 로그인 시 토큰 발급             |
| `verify_token`| 요청 시 토큰 검증               |
| `Depends()`   | 보호된 API에 인증 적용          |

---

JWT 저장을 쿠키에 할 수도 있고, 프론트엔드에 저장해서 요청할 수도 있어.  
더 보안적인 흐름이 필요하면 refresh token도 추가해줄 수 있어. 필요해?