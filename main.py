from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Guestbook entries stored in-memory for simplicity (not suitable for production)
guestbook_entries = []

# Serve static files from the "static" directory under the "/static" path
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="templates")

class GuestbookEntry(BaseModel):
    name: str
    message: str

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "entries": guestbook_entries})

@app.post("/add_entry/", response_class=HTMLResponse)
async def add_entry(request: Request, name: str = Form(...), message: str = Form(...)):
    try:
        entry = f"{name}: {message}"
        guestbook_entries.append(entry)
        return templates.TemplateResponse("index.html", {"request": request, "entries": guestbook_entries})
    except Exception as e:
        print(f"Error adding entry: {e}")
        raise
