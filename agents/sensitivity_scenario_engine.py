# agents/sensitivity_scenario_engine.py
import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class SensitivityScenarioEngine:
    """
    Usa IA para criar análises de cenário (otimista, pessimista) para um modelo financeiro.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [Sensitivity Scenario Engine] Inicializado.")

    def analyze_scenarios(self, project: models.Project) -> str:
        """
        Gera uma análise de sensibilidade financeira.
        """
        console.print(
            f"📉📈 [Sensitivity Engine] Analisando cenários para: [bold green]{project.name}[/bold green]..."
        )

        prompt = f"""
            Aja como um Analista de Risco Financeiro.
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}", 
            crie uma análise de sensibilidade com dois cenários: Otimista e Pessimista.

            Para cada cenário, descreva brevemente:
            1.  **As premissas que mudam:** (ex: "Adoção de usuários 50% mais rápida", "Custo de aquisição 30% maior").
            2.  **O impacto no VPL (Valor Presente Líquido):** Estime qualitativamente o impacto (ex: "Aumento substancial", "Redução significativa").
            3.  **O impacto no Payback:** Estime se o payback seria mais rápido ou mais lento.

            Responda em formato Markdown, com um título para cada cenário.
        """

        with console.status(
            "[bold yellow]Aguardando IA analisar os cenários...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("📉📈 [Sensitivity Engine] Análise de cenários concluída!")
        return response.text
