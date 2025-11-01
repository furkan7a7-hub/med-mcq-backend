from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from ..database import get_session
from ..models import Question, Option
from ..deps import require_admin

router = APIRouter()

@router.get("/questions")
def list_questions(subject_id: Optional[int]=None, topic_id: Optional[int]=None, difficulty: Optional[str]=None, limit: int=50, session=Depends(get_session)):
    stmt = select(Question)
    if subject_id is not None:
        stmt = stmt.where(Question.subject_id==subject_id)
    if topic_id is not None:
        stmt = stmt.where(Question.topic_id==topic_id)
    if difficulty is not None:
        stmt = stmt.where(Question.difficulty==difficulty)
    stmt = stmt.limit(limit)
    qs = session.exec(stmt).all()
    out = []
    for q in qs:
        session.refresh(q, attribute_names=["options"])
        out.append({**q.model_dump(), "options":[o.model_dump() for o in q.options]})
    return out

@router.get("/questions/{qid}")
def get_question(qid: int, session=Depends(get_session)):
    q = session.get(Question, qid)
    if not q:
        raise HTTPException(status_code=404, detail="not found")
    session.refresh(q, attribute_names=["options", "explanations"])
    return {**q.model_dump(), "options":[o.model_dump() for o in q.options], "explanations":[e.model_dump() for e in q.explanations]}

@router.post("/questions", dependencies=[Depends(require_admin)])
def create_question(data: dict, session=Depends(get_session)):
    q = Question(
        subject_id=data["subject_id"],
        topic_id=data.get("topic_id"),
        stem=data["stem"],
        difficulty=data.get("difficulty","med"),
        source_ref=data.get("source_ref"),
        year=data.get("year"),
    )
    session.add(q)
    session.commit()
    session.refresh(q)
    options = data.get("options", [])
    for opt in options:
        o = Option(question_id=q.id, label=opt["label"], text=opt["text"], is_correct=opt.get("is_correct", False))
        session.add(o)
    session.commit()
    return get_question(q.id, session)
