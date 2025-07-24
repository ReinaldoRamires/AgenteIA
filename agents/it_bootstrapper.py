from typing import Any, Dict
from .base_agent import BaseAgent

class ITBootstrapper(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("it_bootstrapper", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return "Descreva os passos para bootstrap de infraestrutura (rede, servidores, etc)."
