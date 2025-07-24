# agents/doc_checklist_builder.py
import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class DocChecklistBuilder:
    """
    Usa IA para gerar um checklist de documentos necessários para um projeto.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [Doc Checklist Builder] Inicializado.")

    def generate_checklist(self, project: models.Project) -> str:
        """
        Gera um checklist de documentos com base no tipo e país do projeto.
        """
        console.print(
            f"📋 [Doc Checklist Builder] Gerando checklist para: [bold green]{project.name}[/bold green]..."
        )

        prompt = f"""
            Aja como um consultor de projetos experiente.
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}" a ser realizado em "{project.country}",
            crie um checklist em formato Markdown dos principais documentos que serão necessários ao longo do ciclo de vida do projeto.

            Organize o checklist nas seguintes categorias:
            1.  **Documentos de Iniciação e Planejamento:** (ex: Termo de Abertura do Projeto, Plano de Projeto)
            2.  **Documentos Contratuais e Legais:** (ex: Contratos com Fornecedores, NDA com Parceiros)
            3.  **Documentos de Execução e Controle:** (ex: Relatórios de Status, Atas de Reunião)
            4.  **Documentos de Encerramento:** (ex: Termo de Aceite, Lições Aprendidas)
        """

        with console.status(
            "[bold yellow]Aguardando IA gerar o checklist de documentos...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("📋 [Doc Checklist Builder] Checklist gerado com sucesso!")
        return response.text
