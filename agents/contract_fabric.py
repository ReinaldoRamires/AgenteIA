from typing import Any, Dict
from .base_agent import BaseAgent

class ContractFabric(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("contract_fabric", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return "Gere um esqueleto de contrato para fornecedores/partners."
