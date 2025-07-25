from typing import Any, Dict
from .base_agent import BaseAgent

class ExecutiveNarrator(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("executive_narrator", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        name = project_data.get("name", "Projeto")
        return (
            f"Como um executivo, faça um resumo narrativo do projeto '{name}'.\n"
            "- Objetivos\n- Principais marcos\n- Métricas de sucesso"
        )
