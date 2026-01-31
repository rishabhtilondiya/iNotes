from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config.db import conn

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []

    for doc in docs:
        newDocs.append({
            "id": str(doc.get("_id")),
            "title": doc.get("title", ""),
            "desc": doc.get("desc", ""),
            "important": doc.get("important", False),
        })

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "newDocs": newDocs
        }
    )


@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    formDict = dict(form)

    formDict["important"] = True if formDict.get("important") == "on" else False

    conn.notes.notes.insert_one(formDict)

    return RedirectResponse(url="/", status_code=303)
