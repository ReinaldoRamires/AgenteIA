# agents/capacity_leveler.py
import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class CapacityLeveler:
    """
    Usa IA para sugerir ações para nivelar a carga de trabalho quando a demanda excede a capacidade.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [Capacity Leveler] Inicializado.")

    def suggest_actions(self, project: models.Project, capacity_deficit: float) -> str:
        """
        Sugere ações para mitigar um déficit de capacidade.
        """
        console.print(
            f"⚖️  [Capacity Leveler] Sugerindo ações para um déficit de {capacity_deficit:.1f} horas..."
        )

        prompt = f"""
            Aja como um Diretor de Operações (COO).
            Em um projeto chamado "{project.name}" (tipo: "{project.project_type}"), 
            identificamos um déficit de capacidade de {capacity_deficit:.1f} horas para o próximo mês.

            Sugira 3 ações estratégicas para resolver este problema, em formato Markdown.
            Para cada ação, explique brevemente o trade-off (o que ganhamos e o que perdemos).

            Exemplos de ações: Repriorizar o backlog, Contratar freelancers, Simplificar o escopo de uma entrega, Pagar horas extras.
        """

        with console.status(
            "[bold yellow]Aguardando IA sugerir ações de nivelamento...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("⚖️  [Capacity Leveler] Sugestões geradas!")
        return response.text
