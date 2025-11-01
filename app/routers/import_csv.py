from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import select
import pandas as pd
from ..database import get_session
from ..models import Subject, Topic, Question, Option
from ..deps import require_admin

router = APIRouter()

COLUMNS = ["subject","topic","stem","option_a","option_b","option_c","option_d","option_e","correct_label","difficulty","source_ref","year"]

@router.post("/questions/import", dependencies=[Depends(require_admin)])
async def import_questions(file: UploadFile = File(...), session=Depends(get_session)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV only")
    df = pd.read_csv(file.file)
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing columns: {missing}")
    created = 0
    for _,row in df.iterrows():
        subj = session.exec(select(Subject).where(Subject.name==row["subject"])).first()
        if not subj:
            subj = Subject(name=row["subject"])
            session.add(subj); session.commit(); session.refresh(subj)
        topic = None
        if pd.notna(row.get("topic")) and str(row["topic"]).strip():
            topic = session.exec(select(Topic).where(Topic.name==row["topic"]).where(Topic.subject_id==subj.id)).first()
            if not topic:
                topic = Topic(name=row["topic"], subject_id=subj.id)
                session.add(topic); session.commit(); session.refresh(topic)
        q = Question(subject_id=subj.id, topic_id=(topic.id if topic else None), stem=row["stem"], difficulty=str(row.get("difficulty","med")), source_ref=str(row.get("source_ref")) if pd.notna(row.get("source_ref")) else None, year=int(row["year"]) if pd.notna(row.get("year")) else None)
        session.add(q); session.commit(); session.refresh(q)
        options = []
        for label,col in zip(["A","B","C","D","E"], ["option_a","option_b","option_c","option_d","option_e"]):
            text = row.get(col)
            if pd.notna(text) and str(text).strip():
                options.append(Option(question_id=q.id, label=label, text=str(text), is_correct=(label==str(row["correct_label"]).strip().upper())))
        if not any(o.is_correct for o in options):
            raise HTTPException(status_code=400, detail=f"No correct option for question id temp stem: {row['stem'][:40]}")
        for o in options: session.add(o)
        session.commit()
        created += 1
    return {"imported": created}
