from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from ..database import get_session
from ..models import Question, Option, Explanation
from ..deps import require_admin
from ..ai import generate_explanation
from ..safety import safety_filter

router = APIRouter()

@router.get("/questions/{qid}/explanations")
def list_explanations(qid: int, session=Depends(get_session)):
    exps = session.exec(select(Explanation).where(Explanation.question_id==qid)).all()
    return [e.model_dump() for e in exps]

@router.post("/questions/{qid}/explanations/ai", dependencies=[Depends(require_admin)])
def create_ai_explanation(qid: int, session=Depends(get_session)):
    q = session.get(Question, qid)
    if not q:
        raise HTTPException(status_code=404, detail="question not found")
    opts = session.exec(select(Option).where(Option.question_id==qid)).all()
    correct = next((o for o in opts if o.is_correct), None)
    if not correct:
        raise HTTPException(status_code=400, detail="question has no correct option")
    md = generate_explanation(q.stem, [{"label":o.label, "text":o.text} for o in opts], correct.label, q.source_ref)
    md = safety_filter(md)
    exp = Explanation(question_id=qid, type="ai", content_md=md, references_json=None, created_by="ai")
    session.add(exp)
    session.commit()
    session.refresh(exp)
    return exp
