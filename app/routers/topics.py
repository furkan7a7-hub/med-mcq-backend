from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from ..database import get_session
from ..models import Topic, Subject
from ..deps import require_admin

router = APIRouter()

@router.get("/subjects/{subject_id}/topics")
def list_topics(subject_id: int, session=Depends(get_session)):
    return session.exec(select(Topic).where(Topic.subject_id==subject_id)).all()

@router.post("/topics", dependencies=[Depends(require_admin)])
def create_topic(data: dict, session=Depends(get_session)):
    subject_id = data.get("subject_id")
    name = data.get("name")
    if not subject_id or not name:
        raise HTTPException(status_code=400, detail="subject_id and name are required")
    t = Topic(subject_id=subject_id, name=name, parent_topic_id=data.get("parent_topic_id"))
    session.add(t)
    session.commit()
    session.refresh(t)
    return t
