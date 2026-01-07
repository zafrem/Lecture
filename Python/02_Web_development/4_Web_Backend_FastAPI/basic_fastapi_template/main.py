from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Base Template",
    description="A base template for FastAPI applications",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define data models using Pydantic
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# Mock database
items_db = []
item_id_counter = 1

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Base Template"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# CRUD operations for items

# Create item
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    global item_id_counter
    item.id = item_id_counter
    item_id_counter += 1
    items_db.append(item)
    return item

# Read all items
@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100):
    return items_db[skip: skip + limit]

# Read single item
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Update item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            updated_item.id = item_id
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete item
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Item not found")

# Error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Add static files mounting if needed
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Run the application if executed directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
