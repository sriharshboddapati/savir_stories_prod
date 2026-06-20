from fastapi import FastAPI
from utils import show_timeline_from_db


app = FastAPI()

@app.get("/")
def get_all_items_from_db():
    result= []
    Title_Only = show_timeline_from_db()
    for item in Title_Only:
        result.append({"title": item.get("title", "No title"), "date": item.get("date", "No date"), "description": item.get("description", "No description")})
    return result

@app.get("/milestone/")
def get_milestone_by_date():
    Title_Only = show_timeline_from_db()
    return Title_Only

#@app.post("/milestone/")
