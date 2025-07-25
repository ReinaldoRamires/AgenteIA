# agents/go_to_market_copilot.py
from typing import Any, Dict

from .base_agent import BaseAgent


class GoToMarketCopilot(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("go_to_market_copilot", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        name = project_data.get("name", "")
        return f"""
Você é um estrategista de Go-To-Market. 
Monte um plano GTM para o projeto "{name}" contendo:

- Segmentos de clientes prioritários
- Proposta de valor por segmento
- Canais de aquisição (orgânico, pago, parcerias etc)
- Estratégia de pricing inicial
- Métricas de sucesso e primeiros experimentos
"""
