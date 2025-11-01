from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    code: Optional[str] = None
    is_active: bool = True
    topics: List['Topic'] = Relationship(back_populates='subject')
    questions: List['Question'] = Relationship(back_populates='subject')

class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    subject_id: int = Field(foreign_key="subject.id")
    parent_topic_id: Optional[int] = Field(default=None, foreign_key="topic.id")
    subject: Subject = Relationship(back_populates='topics')
    questions: List['Question'] = Relationship(back_populates='topic')

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id")
    topic_id: Optional[int] = Field(default=None, foreign_key="topic.id")
    stem: str
    image_url: Optional[str] = None
    difficulty: str = "med"
    source_ref: Optional[str] = None
    year: Optional[int] = None
    is_active: bool = True

    subject: Subject = Relationship(back_populates='questions')
    topic: Optional[Topic] = Relationship(back_populates='questions')
    options: List['Option'] = Relationship(back_populates='question')
    explanations: List['Explanation'] = Relationship(back_populates='question')

class Option(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    label: str
    text: str
    is_correct: bool = False
    question: Question = Relationship(back_populates='options')

class Explanation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id")
    type: str = "ai"  # manual | ai
    content_md: str
    references_json: Optional[str] = None
    created_by: Optional[str] = None

    question: Question = Relationship(back_populates='explanations')

class Quiz(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = None
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
    mode: str = "practice"  # practice | exam

class QuizItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(foreign_key="quiz.id")
    question_id: int = Field(foreign_key="question.id")
    user_answer: Optional[str] = None
    is_correct: Optional[bool] = None
    time_spent_sec: Optional[int] = None
