# agents/decision_supporter.py
import google.generativeai as genai
from rich.console import Console
from src import models

console = Console()

class DecisionSupporter:
    """
    Usa IA para analisar cenários de "what-if" e trade-offs para apoiar a tomada de decisão.
    """
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        console.print("✅ [Decision Supporter] Inicializado.")

    def analyze_trade_offs(self, project: models.Project, decision: str) -> str:
        """
        Analisa os prós, contras e riscos de uma decisão estratégica.
        """
        console.print(f"🤔 [Decision Supporter] Analisando a decisão: '{decision}'...")

        prompt = f"""
            Aja como um Consultor de Estratégia Sênior.
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}", 
            a equipe está considerando a seguinte decisão estratégica: "{decision}".

            Faça uma análise de trade-offs em formato Markdown, incluindo:
            1.  **Prós:** Liste 2 a 3 potenciais benefícios ou vantagens de tomar essa decisão.
            2.  **Contras:** Liste 2 a 3 potenciais desvantagens ou custos.
            3.  **Riscos Associados:** Identifique o principal risco que essa decisão introduz.
            4.  **Recomendação Final:** Dê uma recomendação concisa (ex: "Recomendado com ressalvas", "Não recomendado nesta fase", "Recomendado").
        """

        with console.status("[bold yellow]Aguardando IA analisar os trade-offs...[/bold yellow]"):
            response = self.model.generate_content(prompt)

        console.print("🤔 [Decision Supporter] Análise concluída!")
        return response.text