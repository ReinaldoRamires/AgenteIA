from typing import Any, Dict
from .base_agent import BaseAgent

class StakeholderGraphBot(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("stakeholder_graph_bot", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        name = project_data.get("name", "")
        return f"Desenhe grafo de stakeholders para o projeto '{name}'."
