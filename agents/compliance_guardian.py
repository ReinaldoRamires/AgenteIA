# agents/compliance_guardian.py
import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class ComplianceGuardian:
    """
    Usa IA para analisar riscos de conformidade e regulatórios.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [Compliance Guardian] Inicializado.")

    def analyze_compliance_risks(self, project: models.Project) -> str:
        """

        Gera uma análise de riscos de conformidade para um projeto.
        """
        console.print(
            f"🛡️  [Compliance Guardian] Analisando riscos para: [bold green]{project.name}[/bold green]..."
        )

        prompt = f"""
            Aja como um especialista em Compliance e Regulatório.
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}", a ser realizado em "{project.country}", 
            analise e liste os 3 a 5 principais pontos de atenção em conformidade.

            Para cada ponto, mencione a área (ex: Proteção de Dados, AML, ESG) e uma breve descrição do risco ou da exigência.

            Responda em formato Markdown, com um título principal e bullet points para cada item.
        """

        with console.status(
            "[bold yellow]Aguardando IA analisar os riscos...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("🛡️  [Compliance Guardian] Análise de riscos concluída!")
        return response.text
