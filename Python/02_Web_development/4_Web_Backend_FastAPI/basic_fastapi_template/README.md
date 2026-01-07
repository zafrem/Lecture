# FastAPI Base Template

A professional-grade starter template for building robust, high-performance web APIs with FastAPI, Python's modern web framework.

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

</div>

## 📋 Features

- ✅ **Complete REST API** with CRUD operations for a sample resource
- ✅ **Interactive API documentation** with Swagger UI and ReDoc
- ✅ **Data validation** using Pydantic models
- ✅ **CORS middleware** configuration for cross-origin requests
- ✅ **Error handling** with proper HTTP status codes
- ✅ **Health check endpoint** for monitoring
- ✅ **Ready for production** with proper configuration setup
- ✅ **Expansion examples** for databases, authentication, and more

## 🗂️ Project Structure

```
basic_fastapi_template/
├── main.py            # Main FastAPI application file
├── requirements.txt   # Python dependencies
├── .gitignore         # Git ignore file
└── README.md          # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository** (or download the template):

```bash
git clone <repository-url>
cd basic_fastapi_template
```

2. **Create a virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the application**:

```bash
uvicorn main:app --reload
```

5. **Access the API**:

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger UI (API Documentation): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc (Alternative API Documentation): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📡 API Endpoints

| Method | URL           | Description        | Request Body | Response          |
|--------|---------------|--------------------|-------------|-------------------|
| GET    | /             | Welcome message    | None        | {"message": "..."} |
| GET    | /health       | Health check       | None        | {"status": "healthy"} |
| GET    | /items        | List all items     | None        | Array of items    |
| GET    | /items/{id}   | Get a specific item | None       | Item object       |
| POST   | /items        | Create a new item  | Item object | Created item      |
| PUT    | /items/{id}   | Update an item     | Item object | Updated item      |
| DELETE | /items/{id}   | Delete an item     | None        | No content (204)  |

## 🧩 Expanding the Template

### Adding a Database with SQLAlchemy

1. **Install additional dependencies**:
```bash
pip install sqlalchemy alembic
```

2. **Create a `database.py` file**:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
# For PostgreSQL: "postgresql://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

3. **Create models in `models.py`**:
```python
from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class ItemModel(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    is_available = Column(Boolean, default=True)
```

4. **Initialize database in `main.py`**:
```python
from .database import engine, Base
from . import models

# Create tables
Base.metadata.create_all(bind=engine)
```

### Adding JWT Authentication

1. **Create a `security.py` file**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional

# JWT Configuration
SECRET_KEY = "your-secret-key"  # Use a strong key in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # Add user lookup logic here
    # user = get_user(username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user
    
    return token_data
```

### Project Structure with Database and Authentication

```
my_fastapi_app/
├── app/
│   ├── __init__.py
│   ├── main.py          # Main application file
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic models
│   ├── security.py      # Authentication and security
│   ├── config.py        # Configuration settings
│   └── api/             # API endpoints
│       ├── __init__.py
│       ├── deps.py      # Dependencies
│       └── v1/          # API version 1
│           ├── __init__.py
│           ├── endpoints/
│           │   ├── __init__.py
│           │   ├── items.py
│           │   └── users.py
│           └── router.py
├── alembic/            # Database migrations
├── tests/              # Unit tests
├── .gitignore
├── requirements.txt
└── README.md
```

## 🧪 Testing

Run tests using pytest:

```bash
pytest
```

## 🔒 Environment Variables

For production use, sensitive information should be stored in environment variables. Create a `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
```

Then use python-dotenv to load these variables:

```python
from dotenv import load_dotenv
load_dotenv()
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 📄 License

MIT

