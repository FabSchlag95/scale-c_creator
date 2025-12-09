from typing import Literal
from pydantic import BaseModel


class TextSlide(BaseModel):
    title: str
    type: Literal["text"]
    text: str