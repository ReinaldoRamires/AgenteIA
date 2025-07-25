# agents/compliance_guardian.py
from typing import Any, Dict

from .base_agent import BaseAgent


class ComplianceGuardian(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("compliance_guardian", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        country = project_data.get("country", "Brasil")
        project_type = project_data.get("project_type", "desconhecido")
        return f"""
Você é um especialista em compliance. 
Analise quais leis, regulações, padrões de conformidade se aplicam a um projeto do tipo "{project_type}" no país {country}.

- Liste principais normas (LGPD, ANVISA, etc, conforme o tipo).
- Riscos de compliance e penalidades potenciais.
- Boas práticas para mitigar (políticas internas, treinamentos, auditorias).
- Formate em tópicos.
"""
