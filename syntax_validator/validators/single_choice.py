from typing import List, Literal, Optional
from pydantic import BaseModel, Field, model_validator, root_validator


class SingleChoiceAnswer(BaseModel):
    text: str
    correct: bool


class SingleChoiceChoice(BaseModel):
    question: str
    answers: List[SingleChoiceAnswer] = Field(min_length=2)

    @model_validator(mode="after")
    def ensure_single_correct_answer(self):
        answers = self.answers or []
        if sum(answer.correct for answer in answers) != 1:
            raise ValueError("Exactly one answer must be marked as correct")
        return self


class SingleChoiceFeedback(BaseModel):
    positive: str
    negative: str


class SingleChoice(BaseModel):
    title: str
    type: Literal["single_choice"]
    choices: List[SingleChoiceChoice] = Field(min_length=1)
    feedback: SingleChoiceFeedback
    tip: Optional[str]
