# agents/fin_modeler.py
from typing import Any, Dict
from rich.console import Console

from .base_agent import BaseAgent

console = Console()

class FinModeler(BaseAgent):
    """
    Gera/analisa modelos financeiros (receita, custo, payback, etc).
    Usa o default run() do BaseAgent.
    """

    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("fin_modeler", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        name = project_data.get("name", "Projeto sem nome")
        project_type = project_data.get("project_type", "desconhecido")

        return f"""
Você é um analista financeiro experiente. 
Preciso que construa um resumo de viabilidade financeira para o projeto "{name}" (tipo: {project_type}).

1. Liste hipóteses principais (ex.: preço, CAC, churn).
2. Faça projeções de receita/custo em 12 meses (curto prazo) e 36 meses (médio prazo).
3. Estime indicadores: LTV, CAC Payback, Margem Bruta, Ponto de Equilíbrio.
4. Apresente riscos financeiros e estratégias de mitigação.
5. Formate em tópicos, bem objetivo.

Se precisar assumir valores, seja realista e transparente.
"""
