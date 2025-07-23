# agents/org_designer.py
import google.generativeai as genai
from rich.console import Console
from src import models

console = Console()

class OrgDesigner:
    """
    Usa IA para desenhar uma estrutura organizacional inicial para um projeto.
    """
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        console.print("✅ [Org Designer] Inicializado.")

    def design_team_structure(self, project: models.Project) -> str:
        """
        Gera uma sugestão de estrutura de equipe para o projeto.
        """
        console.print(f"👥 [Org Designer] Desenhando estrutura de equipe para: [bold green]{project.name}[/bold green]...")

        prompt = f"""
            Aja como um consultor de RH e desenvolvimento organizacional.
            Para um novo projeto chamado "{project.name}", que é do tipo "{project.project_type}", 
            desenhe uma estrutura de equipe inicial enxuta (lean team).

            Responda em formato Markdown com:
            1.  Um título "Estrutura de Equipe Sugerida".
            2.  Uma breve introdução sobre a filosofia da equipe (ex: ágil, multifuncional).
            3.  Uma lista dos 3 a 5 papéis essenciais para a fase inicial do projeto.
            4.  Para cada papel, descreva suas 2 ou 3 principais responsabilidades.
        """

        with console.status("[bold yellow]Aguardando IA desenhar a equipe...[/bold yellow]"):
            response = self.model.generate_content(prompt)

        console.print("👥 [Org Designer] Estrutura da equipe desenhada com sucesso!")
        return response.text