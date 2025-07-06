# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS so frontend can access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data store (dictionary of month to entries list)
expense_data = {}

# Pydantic model for entries
class Expense(BaseModel):
    id: str
    date: str
    type: str  # 'advance' or 'payment'
    particulars: str
    amount: float
    remarks: str

@app.get("/")
def home():
    return {"message": "Expense API is running."}

@app.get("/expenses/{month}", response_model=List[Expense])
def get_expenses(month: str):
    return expense_data.get(month, [])

@app.post("/expenses/{month}")
def add_expense(month: str, entry: Expense):
    if month not in expense_data:
        expense_data[month] = []
    expense_data[month].append(entry)
    return {"message": "Entry added successfully."}

@app.delete("/expenses/{month}/{entry_id}")
def delete_expense(month: str, entry_id: str):
    if month in expense_data:
        expense_data[month] = [e for e in expense_data[month] if e.id != entry_id]
        return {"message": "Entry deleted."}
    raise HTTPException(status_code=404, detail="Entry not found")
