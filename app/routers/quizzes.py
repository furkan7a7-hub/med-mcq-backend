from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from ..database import get_session
from ..models import Quiz, QuizItem, Question, Option

router = APIRouter()

@router.post("/quizzes")
def create_quiz(data: dict, session=Depends(get_session)):
    qz = Quiz(user_id=data.get("user_id"), subject_id=data.get("subject_id"), mode=data.get("mode","practice"))
    session.add(qz)
    session.commit()
    session.refresh(qz)
    return qz

@router.post("/quizzes/{quiz_id}/answer")
def answer_question(quiz_id: int, data: dict, session=Depends(get_session)):
    question_id = data.get("question_id")
    user_answer = data.get("user_answer")
    if not question_id or not user_answer:
        raise HTTPException(status_code=400, detail="question_id and user_answer required")
    # check correct
    correct = session.exec(select(Option).where(Option.question_id==question_id).where(Option.is_correct==True)).first()
    is_correct = (correct.label == user_answer) if correct else False
    qi = QuizItem(quiz_id=quiz_id, question_id=question_id, user_answer=user_answer, is_correct=is_correct, time_spent_sec=data.get("time_spent_sec"))
    session.add(qi)
    session.commit()
    return {"is_correct": is_correct, "correct_label": correct.label if correct else None}

@router.post("/quizzes/{quiz_id}/finish")
def finish_quiz(quiz_id: int, session=Depends(get_session)):
    items = session.exec(select(QuizItem).where(QuizItem.quiz_id==quiz_id)).all()
    if not items:
        return {"quiz_id": quiz_id, "total": 0, "accuracy": None}
    total = len(items)
    acc = sum(1 for i in items if i.is_correct) / total
    return {"quiz_id": quiz_id, "total": total, "accuracy": acc}
