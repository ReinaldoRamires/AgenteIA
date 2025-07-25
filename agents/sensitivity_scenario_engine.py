from typing import Any, Dict
from .base_agent import BaseAgent

class SensitivityScenarioEngine(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("sensitivity_scenario_engine", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return "Realize análise de sensibilidade e cenários financeiros."
