from fastapi import APIRouter, Depends
from sqlmodel import select
from ..database import get_session, init_db
from ..models import Subject
from ..deps import require_admin

router = APIRouter()

@router.on_event("startup")
def on_startup():
    init_db()

@router.get("/subjects")
def list_subjects(session=Depends(get_session)):
    return session.exec(select(Subject)).all()

@router.post("/subjects", dependencies=[Depends(require_admin)])
def create_subject(data: dict, session=Depends(get_session)):
    s = Subject(name=data.get("name"), code=data.get("code"))
    session.add(s)
    session.commit()
    session.refresh(s)
    return s
