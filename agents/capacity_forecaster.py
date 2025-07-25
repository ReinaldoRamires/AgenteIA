from typing import Any, Dict

from .base_agent import BaseAgent


class CapacityForecaster(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("capacity_forecaster", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        team = project_data.get("team_capacity", [])
        return f"Analise a capacidade do time: {team}"
