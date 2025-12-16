"""
This script contains most functions that serve as a factory in some way or other.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Type, Union
import uuid
from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel, Field, create_model
from .utils.parsers import render_and_parse_template
from .templates.prompts.structured_output.schemas import (
    AdvancedText, DragTextSlide, SingleChoiceSlide, Metadata)
from .utils.schemas import Modality

FILE_PATH = Path(__file__).resolve()
DIR_PATH = FILE_PATH.parent
TEMPLATE_DIR = DIR_PATH / "templates/"

# load all h5p templates
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR/"h5p"))
h5p_templates = {
    filename[:-3]: env.get_template(filename)
    for filename in os.listdir(TEMPLATE_DIR/"h5p")
    if filename.endswith(".j2")
}

# FORGING THE SYSTEM PROMPT WITH CONTENT RELATED PARAMS
# .........................................................................


def forge_system_prompt(config: Dict[str, Any], template="system_base"):
    # load prompts
    with open(TEMPLATE_DIR / f"prompts/{template}.j2", encoding="utf-8", mode="r") as f:
        system_prompt_template = Template(f.read())
    system = system_prompt_template.render(config)
    return system

# FORGING THE OUTPUT SCHEMA
# .........................................................................


def forge_pydantic_output_schema(modalities: List[Literal["text", "drag_text", "single_choice"]], min_slide_count=4, max_slide_count=50) -> Type[BaseModel]:
    base_map: Dict[str, Type[BaseModel]] = {
        "single_choice": SingleChoiceSlide,
        "drag_text": DragTextSlide,
        "text": AdvancedText,
    }
    final_slide_types: List[Type[BaseModel]] = []

    for m in modalities:
        if m in base_map:
            final_slide_types.append(base_map[m])
        else:
            raise ValueError(f"{m} not in available slide types.")

    SlideUnion = Union[tuple(final_slide_types)]

    LearningUnitType: Type[BaseModel] = create_model(
        "LearningUnit",
        slides=(List[SlideUnion], Field(description=("Ordered list of slides. "
                                                     "Each type must be used at least once."
                                                     "CONSIDER THE SPECIFICATIONS FOR EACH SLIDE TYPE (MODALITY) STATED IN <modalities>."),
                                        min_length=min_slide_count,
                                        max_length=max_slide_count)),
        metadata=Metadata,
        __module__=__name__,
    )

    return LearningUnitType


# FORGING THE OUTPUT SCHEMA
# .........................................................................
def forge_json_output_schema(modalities: List[Modality], min_slide_count=4, max_slide_count=50) -> str:
    with open(TEMPLATE_DIR / "prompts/structured_output/modalities.json", encoding="utf-8") as f:
        base_map: dict[str, Any] = json.load(f, )
    with open(TEMPLATE_DIR / "prompts/structured_output/output_schema_json.j2", encoding="utf-8") as f:
        template = Template(f.read())
    modalities_with_output_structure = []
    for m in modalities:
        format = json.dumps(base_map[m.id], indent=4, ensure_ascii=False)
        modalities_with_output_structure.append(
            {**m.model_dump(), "format": format})
    return template.render(modalities=modalities_with_output_structure, min_slide_count=min_slide_count, max_slide_count=max_slide_count)


# MERGING OUTPUT IN TEMPLATES
# .........................................................................
def parse_model_response(content: dict[str, Any]) -> str:
    final_slides = []

    # get unit tile for cover page
    unit_title = content.get("title", "Unit")

    # render slide content as elements
    for slide in content.get("slides", []):
        slide_title = slide.get("title", "")
        element_config = {"uuid": str(uuid.uuid1()),
                          "text": "",
                          "choices": []
                          }

        # Generate modality specific content based on slide type
        element_config.update(slide)
        match slide.get("type"):
            case "text":
                content_element = render_and_parse_template(h5p_templates["AdvancedText"],
                                                            element_config)
            case "single_choice":
                choices = __create_single_choice_choices(slide["choices"])
                element_config["choices"] = list(choices)
                content_element = render_and_parse_template(h5p_templates["SingleChoiceSet"],
                                                            element_config)
            case "drag_text":
                content_element = render_and_parse_template(h5p_templates["DragText"],
                                                            element_config)
            case "dialog_cards":
                content_element = render_and_parse_template(h5p_templates["DialogCard"],
                                                            element_config)
            # case "learning_goals":
            #     pass
            #     # for o in objectives:
            #     #     pass
            case _:
                content_element = {}
        final_slides.append({"element": content_element,
                            "title": slide_title, "type": slide.get("type", "")})
    final_content = h5p_templates["Content"].render(
        {"slides": final_slides, "title": unit_title})
    return final_content


def __create_single_choice_choices(choices: list[dict]):
    for choice in choices:
        answers = choice["answers"]
        answers.sort(key=lambda a: not (
            a["correct"] is True or
            (isinstance(a["correct"], str)
                and a["correct"].lower() == "true")
        ))
        choice_ = {
            **choice,
            "subContentId": str(uuid.uuid1()),
            "answers": [a["text"] for a in answers]
        }
        yield choice_
