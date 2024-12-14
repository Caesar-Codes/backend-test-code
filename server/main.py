from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="FastAPI Backend", description="Backend API for React frontend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class Item(BaseModel):
    id: int
    title: str
    description: str

# Sample data test
sample_data = [
    Item(id=1, title="Item 1", description="Description for item 1"),
    Item(id=2, title="Item 2", description="Description for item 2"),
    Item(id=3, title="Item 3", description="Description for item 3"),
]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend"}

@app.get("/status")
async def read_root():
    return {"message": "Mock test"}

@app.get("/api/data", response_model=List[Item])
async def get_data():
    return sample_data

# Add an item
@app.post("/api/data", response_model=Item)
async def create_item(item: Item):
    sample_data.append(item)
    return item

# Get a specific item
@app.get("/api/data/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in sample_data:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
