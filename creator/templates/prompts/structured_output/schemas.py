
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Union

##....................................................................
# SINGLE CHOICE SCHEMA

class SingleChoiceQuestion(BaseModel):
    question: str = Field(
        description="The question text, in the target language. Keep it concise and unambiguous."
    )
    answers: List[str] = Field(
        description=(
            "List of possible answer choices. The correct answer must be included, "
            "and distractors should be plausible but incorrect."
        ),
        min_length=3,
    )

class SingleChoiceSlide(BaseModel):
    title: str = Field(
        description="Short, descriptive title for the slide's topic."
    )
    type: Literal["single_choice"] = Field(
        description="Task type identifier. Always 'single_choice' for this slide."
    )
    choices: List[SingleChoiceQuestion] = Field(
        description=(
            "A list of single-choice questions. Each question must have at least "
            "three answer options."
        ),
        min_length=2,
    )

##....................................................................
# DRAG TEXT SCHEMA

class DragTextSlide(BaseModel):
    title: str = Field(
        description="Short, clear title for the exercise in the target language."
    )
    task_description: str = Field(
        description="Instructions for the student. Keep it short, direct, and encouraging."
    )
    type: Literal["drag_text"] = Field(
        description="Task type identifier. Always 'drag_text' for this slide."
    )
    text_field: str = Field(
        description=(
            "The Lückentext content. Mark missing words with '*' before and after each word "
            "(e.g., *Addition*). Ensure the text is coherent, educational, and "
            "aligned with the title's topic."
        )
    )

##....................................................................
# TEXT SCHEMA

class AdvancedText(BaseModel):
    title: str = Field(
        description="Short, clear title for the slide's topic."
    )
    type: Literal["text"] = Field(
        description="Task type identifier. Always 'text' for this slide."
    )
    text: str = Field(
        description=(
            "Main textual content of the slide. Can include bullet points, line breaks, "
            "and inline formatting (e.g., **bold**) as needed. Keep explanations concise, "
            "educational, and aligned with the slide's title topic."
        )
    )


##....................................................................
# DIALOG CARDS SCHEMA


class DialogCard(BaseModel):
    text: str = Field(
        description=(
            "The prompt or question side of the card. Can be plain text or HTML. "
            "If HTML, wrap in <p> tags for paragraphs."
        )
    )
    answer: str = Field(
        description=(
            "The answer side of the card. Can be plain text or HTML. "
            "If HTML, use semantic tags (<p>, <strong>, etc.) and keep structure clean."
        )
    )



#....................................................................
# META SCHEMA

Slide = Union[DragTextSlide, SingleChoiceSlide, AdvancedText]

class Metadata(BaseModel):
    title: str = Field(
        description="The overarching unit or presentation title."
    )

class LearningUnit(BaseModel):
    slides: List[Slide] = Field(
        description="Ordered list of slide objects. Can be of multiple types."
         "Must include at least one of each type."
    )
    metadata: Metadata = Field(
        description="Information about the learning unit."
    )
