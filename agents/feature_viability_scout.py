from typing import Any, Dict
from .base_agent import BaseAgent

class FeatureViabilityScout(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("feature_viability_scout", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        name = project_data.get("name", "")
        return f"Avalie a viabilidade da feature principal do projeto '{name}'."
