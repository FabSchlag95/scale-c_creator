from typing import Any, Dict
from jinja2 import Template


class PromptBuilder():


    def forge_system_prompt(self, config: Dict[str, Any], template="system_base.fidemm.2"):
        with open(f"templates/prompts/{template}.j2", encoding="utf-8", mode="r") as f:
            system_prompt_template = Template(f.read())
        system = system_prompt_template.render(config)
        return system

