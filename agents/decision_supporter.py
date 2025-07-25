from typing import Any, Dict

from .base_agent import BaseAgent


class DecisionSupporter(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("decision_supporter", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return "Forneça recomendações de decisão para situações-chave do projeto."
