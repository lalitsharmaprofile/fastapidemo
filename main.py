import os
from datetime import datetime

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import motor.motor_asyncio

# load .env
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "fastapi_notes")

# async motor client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
notes_collection = db["notes"]

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    # homepage
    cursor = notes_collection.find().sort("created_at", -1)
    notes = []
    async for doc in cursor:
        notes.append(doc)
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})


@app.post("/notes")
async def create_note(request: Request, title: str = Form(...), content: str = Form(...)):
    # save post
    note = {"title": title, "content": content, "created_at": datetime.now()}
    new_id = await notes_collection.insert_one(note)
    # return {"id": str(new_id.inserted_id), "status": 200}
    return RedirectResponse("/", status_code=303)


@app.get("/api/notes")
async def api_notes():
    notes = []
    async for doc in notes_collection.find().sort("created_at", -1):
        doc["_id"] = str(doc["_id"])
        doc["created_at"] = doc["created_at"].isoformat()
        notes.append(doc)
    return notes

