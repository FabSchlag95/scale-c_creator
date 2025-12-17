from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field, conlist


class SingleChoiceAnswer(BaseModel):
    text: str
    correct: bool


class SingleChoiceChoice(BaseModel):
    question: str
    answers: List[SingleChoiceAnswer] = Field(min_length=1)


class SingleChoiceSlide(BaseModel):
    title: str
    type: Literal["single_choice"]
    choices: List[SingleChoiceChoice] = Field(min_length=1)


class DragTextSlide(BaseModel):
    title: str
    task_description: str
    type: Literal["drag_text"]
    text_field: str


class TextSlide(BaseModel):
    title: str
    type: Literal["text"]
    text: str


class DialogCard(BaseModel):
    text: str
    answer: str


class DialogCardsSlide(BaseModel):
    title: str
    type: Literal["dialog_cards"]
    dialogs: List[DialogCard] = Field(min_length=1)


# A slide can be exactly one of the allowed modalities
Slide = Union[SingleChoiceSlide, DragTextSlide, TextSlide, DialogCardsSlide]

# OUTPUT VALIDATION
class ParsedResponseModel(BaseModel):
    title: str
    report: str
    slides: List[Slide]


__all__ = [
    "SingleChoiceAnswer",
    "SingleChoiceChoice",
    "SingleChoiceSlide",
    "DragTextSlide",
    "TextSlide",
    "DialogCard",
    "DialogCardsSlide",
    "Slide",
]

