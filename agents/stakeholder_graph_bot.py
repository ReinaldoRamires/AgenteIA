# agents/stakeholder_graph_bot.py
import json

import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class StakeholderGraphBot:
    """
    Usa IA para mapear os stakeholders de um projeto e sugerir estratégias de engajamento.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [Stakeholder Graph Bot] Inicializado.")

    def map_stakeholders(self, project: models.Project) -> list[dict]:
        """
        Gera uma lista de stakeholders com análise de influência e interesse.
        """
        console.print(
            f"🗺️  [Stakeholder Graph Bot] Mapeando stakeholders para: [bold green]{project.name}[/bold green]..."
        )

        prompt = f"""
            Aja como um especialista em Gerenciamento de Partes Interessadas (Stakeholder Management).
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}", 
            identifique 4 tipos de stakeholders chave.

            Para cada stakeholder, forneça:
            - "stakeholder": O nome ou tipo do stakeholder (ex: "Usuários Finais", "Investidores", "Equipe Interna").
            - "influence": O nível de influência sobre o projeto (Baixa, Média, Alta).
            - "interest": O nível de interesse no projeto (Baixo, Médio, Alto).
            - "engagement_strategy": Uma estratégia de engajamento concisa para esse stakeholder.

            Responda APENAS com uma lista de objetos JSON, sem nenhum texto adicional.
            O formato deve ser:
            [
              {{
                "stakeholder": "...",
                "influence": "...",
                "interest": "...",
                "engagement_strategy": "..."
              }},
              {{...}}
            ]
        """

        try:
            with console.status(
                "[bold yellow]Aguardando IA mapear os stakeholders...[/bold yellow]"
            ):
                response = self.model.generate_content(prompt)

            cleaned_response = (
                response.text.strip().replace("```json", "").replace("```", "")
            )
            stakeholder_map = json.loads(cleaned_response)

            console.print(
                "🗺️  [Stakeholder Graph Bot] Mapeamento de stakeholders concluído!"
            )
            return stakeholder_map
        except Exception as e:
            console.print(f"[bold red]ERRO ao mapear stakeholders:[/bold red] {e}")
            return []
