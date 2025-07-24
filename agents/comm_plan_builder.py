from typing import Any, Dict
from .base_agent import BaseAgent

class CommPlanBuilder(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("comm_plan_builder", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return "Crie um plano de comunicação interna e externa para o projeto."
