from typing import Any, Dict
from rich.console import Console
from .base_agent import BaseAgent

console = Console()

class StatusCollector(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("status_collector", config, model_mapping)
        console.print("✅ [Status Collector] Inicializado.")

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return ""

    def run(self, project_data: Dict[str, Any], dry_run: bool = False):
        if dry_run:
            console.print("[DryRun] status_collector → stub coleta status")
            return {}
        console.print("[status_collector] Coleta de status (stub).")
        return {}
