from typing import Any, Dict

from .base_agent import BaseAgent


class DocChecklistBuilder(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("doc_checklist_builder", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return "Liste os documentos necessários para o kickoff e entregas do projeto."
