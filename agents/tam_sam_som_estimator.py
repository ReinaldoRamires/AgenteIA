from typing import Any, Dict

from .base_agent import BaseAgent


class TAMSAMSOMEstimator(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("tam_sam_som_estimator", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        name = project_data.get("name", "")
        return f"Estime TAM, SAM e SOM para o projeto '{name}'."
