from typing import Any, Dict

from .base_agent import BaseAgent


class ScheduleCopilot(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("schedule_copilot", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        project_type = project_data.get("project_type", "default")
        return (
            f"Crie um cronograma básico (WBS) para um projeto do tipo '{project_type}'.\n"
            "- Fases principais\n- Marcos\n- Durações aproximadas"
        )
