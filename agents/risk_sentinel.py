# agents/risk_sentinel.py
from typing import Any, Dict

from .base_agent import BaseAgent


class RiskSentinel(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("risk_sentinel", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        name = project_data.get("name", "")
        return f"""
Você é um analista de riscos corporativos. 
Liste e avalie os principais riscos do projeto "{name}":

- Riscos técnicos, de mercado, financeiros, regulatórios, operacionais
- Probabilidade e impacto (use escala qualitativa: baixo/médio/alto)
- Plano de mitigação recomendado

Formate em tabela ou bullets.
"""
