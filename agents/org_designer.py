# agents/org_designer.py
from typing import Any, Dict

from .base_agent import BaseAgent


class OrgDesigner(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("org_designer", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        team_capacity = project_data.get("team_capacity", [])
        return f"""
Você é um consultor de design organizacional.
Dado um time com estes papéis/capacidades: {team_capacity}

- Proponha uma estrutura organizacional mínima para o projeto.
- Defina responsabilidades de cada papel (RACI resumido).
- Sugira processos de comunicação/reporting.
"""
