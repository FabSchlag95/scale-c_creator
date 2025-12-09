import re
from typing import Literal
from pydantic import BaseModel, model_validator


_BOLD_WORD_PATTERN = re.compile(r"\*\*\w+\*\*")


class DragTextSlide(BaseModel):
    title: str
    task_description: str
    type: Literal["drag_text"]
    text_field: str

    @model_validator(mode="after")
    def validate_text(self):
        if len(_BOLD_WORD_PATTERN.findall(self.text_field or "")) < 2:
            raise ValueError("text_field must contain at least two **<word>** placeholders")
        return self
