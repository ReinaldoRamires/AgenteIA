from typing import Any, Dict

from rich.console import Console

from .base_agent import BaseAgent

console = Console()


class AccountingHelper(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("accounting_helper", config, model_mapping)
        console.print("✅ [Accounting Helper] Inicializado.")

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return "AccountingHelper stub: sem uso de LLM."
