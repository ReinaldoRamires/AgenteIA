from typing import Any, Dict

from .base_agent import BaseAgent


class CapacityLeveler(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("capacity_leveler", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return "Balanceie a carga de trabalho entre os membros do time."
