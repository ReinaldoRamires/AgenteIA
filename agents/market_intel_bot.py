# agents/market_intel_bot.py
from typing import Any, Dict

from rich.console import Console

from .base_agent import BaseAgent

console = Console()


class MarketIntelBot(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("market_intel_bot", config, model_mapping)
        console.print(f"✅ [Market Intel Bot] Inicializado usando modelo: {self.model}")

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        name = project_data.get("name", "")
        country = project_data.get("country", "Brasil")
        return f"""
Você é um analista de mercado. 
Faça uma análise de mercado para o projeto "{name}" no país {country}:

- Tamanho do mercado (TAM/SAM/SOM se possível)
- Tendências de crescimento
- Concorrentes relevantes
- Regulamentações/challenges de entrada
- Oportunidades e ameaças

Formate em seções claras e bullets.
"""
