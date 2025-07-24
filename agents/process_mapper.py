# agents/process_mapper.py
import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class ProcessMapper:
    """
    Usa IA para criar um fluxograma em formato Mermaid para um processo do projeto.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [Process Mapper] Inicializado.")

    def generate_flowchart(self, project: models.Project, process_name: str) -> str:
        """
        Gera um fluxograma em código Mermaid.
        """
        console.print(
            f"🌊 [Process Mapper] Mapeando o processo '{process_name}' para: [bold green]{project.name}[/bold green]..."
        )

        prompt = f"""
            Aja como um Analista de Processos de Negócio.
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}", 
            desenhe um fluxograma simples para o processo de "{process_name}".

            Use a sintaxe de fluxograma do Mermaid (graph TD).
            O fluxograma deve ter entre 5 e 8 etapas, mostrando o fluxo lógico do processo.

            Responda APENAS com o bloco de código Mermaid, sem nenhum texto adicional.
            Comece com ```mermaid e termine com ```.
        """

        with console.status(
            "[bold yellow]Aguardando IA desenhar o fluxograma...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("🌊 [Process Mapper] Fluxograma gerado com sucesso!")
        return response.text
