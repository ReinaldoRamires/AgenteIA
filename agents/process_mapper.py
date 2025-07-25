from typing import Any, Dict

from .base_agent import BaseAgent


class ProcessMapper(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("process_mapper", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return "Mapeie o fluxo de processos chave do projeto."
