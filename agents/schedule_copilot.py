"""
Agente ScheduleCopilot para gerar cronogramas básicos.

Este agente recebe dados de projeto e solicita ao modelo de linguagem a
criação de um cronograma (WBS) com fases, marcos e durações.  O método
`generate_schedule` interpreta a resposta textual e a converte em uma
lista de dicionários com chaves `name`, `dor`, `dod` e `estimate`.

Use `dry_run=True` para inspecionar o prompt sem chamar o modelo.
"""

from typing import Any, Dict, List

from .base_agent import BaseAgent


class ScheduleCopilot(BaseAgent):
    """Agente que cria um cronograma básico para um projeto."""

    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("schedule_copilot", config, model_mapping)

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        project_type = project_data.get("project_type", "default")
        return (
            f"Crie um cronograma básico (WBS) para um projeto do tipo '{project_type}'.\n"
            "Liste fases principais, marcos e durações aproximadas.\n"
            "Responda cada item em uma linha no formato: Tarefa – DoR – DoD – Estimativa (dias).\n"
        )

    def generate_schedule(
        self, project_data: Dict[str, Any], dry_run: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Gera o cronograma básico para o projeto informado.

        :param project_data: dicionário com dados do projeto (project_type etc.).
        :param dry_run: se True, apenas exibe o prompt e retorna lista vazia.
        :return: lista de dicionários com chaves name, dor, dod, estimate.
        """
        prompt = self.build_prompt(project_data)
        if dry_run:
            print(f"[DryRun] {self.name} → prompt gerado:\n{prompt}")
            return []

        text = self.router.generate(self.model, prompt)
        tasks: List[Dict[str, Any]] = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            # Substitui diferentes traços por hífen simples para padronizar
            normalized = line.replace("—", "-").replace("–", "-")
            parts = [p.strip() for p in normalized.split("-")]
            if len(parts) >= 4:
                name, dor, dod, estimate = parts[:4]
                try:
                    est = float(estimate)
                except Exception:
                    est = 0.0
                tasks.append(
                    {
                        "name": name,
                        "dor": dor,
                        "dod": dod,
                        "estimate": est,
                    }
                )
        return tasks
