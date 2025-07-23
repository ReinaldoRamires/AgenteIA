# agents/comm_plan_builder.py
import google.generativeai as genai
from rich.console import Console
from src import models

console = Console()

class CommPlanBuilder:
    """
    Usa IA para criar um esboço de um plano de comunicação para um projeto.
    """
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        console.print("✅ [Comm Plan Builder] Inicializado.")

    def generate_plan(self, project: models.Project) -> str:
        """
        Gera um plano de comunicação inicial.
        """
        console.print(f"📡 [Comm Plan Builder] Criando plano de comunicação para: [bold green]{project.name}[/bold green]...")

        prompt = f"""
            Aja como um Gerente de Comunicação.
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}",
            crie um plano de comunicação inicial em formato Markdown.

            O plano deve incluir:
            1.  **Objetivo da Comunicação:** Uma frase clara.
            2.  **Públicos-Alvo:** Liste os 3 principais stakeholders (ex: Equipe Interna, Clientes, Investidores).
            3.  **Canais e Frequência:** Para cada público, sugira o canal (ex: E-mail, Reunião Semanal, Relatório Mensal) e a frequência da comunicação.
            4.  **Mensagens-Chave:** Defina a principal mensagem a ser comunicada para cada público.
        """

        with console.status("[bold yellow]Aguardando IA criar o plano de comunicação...[/bold yellow]"):
            response = self.model.generate_content(prompt)

        console.print("📡 [Comm Plan Builder] Plano gerado com sucesso!")
        return response.text