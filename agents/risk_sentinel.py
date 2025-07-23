# agents/risk_sentinel.py
import google.generativeai as genai
from rich.console import Console
import json
from src import models

console = Console()

class RiskSentinel:
    """
    Usa IA para identificar e pontuar os principais riscos de um projeto.
    """
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        console.print("✅ [Risk Sentinel] Inicializado.")

    def analyze_risks(self, project: models.Project) -> list[dict]:
        """
        Gera uma lista de riscos potenciais para o projeto.
        """
        console.print(f"🔎 [Risk Sentinel] Identificando riscos para: [bold green]{project.name}[/bold green]...")

        prompt = f"""
            Aja como um Gerente de Riscos (Risk Manager) sênior.
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}" em "{project.country}", 
            identifique os 4 principais riscos.

            Para cada risco, forneça:
            - "risk": Uma descrição concisa do risco.
            - "category": A categoria do risco (Prazo, Custo, Escopo, Regulatório, Técnico, Pessoas).
            - "score": Uma pontuação de impacto de 1 a 10 (onde 10 é o mais alto impacto).
            - "mitigation": Uma sugestão breve de mitigação.

            Responda APENAS com uma lista de objetos JSON, sem nenhum texto adicional.
            O formato deve ser:
            [
              {{
                "risk": "...",
                "category": "...",
                "score": ...,
                "mitigation": "..."
              }},
              {{...}}
            ]
        """

        try:
            with console.status("[bold yellow]Aguardando IA identificar os riscos...[/bold yellow]"):
                response = self.model.generate_content(prompt)

            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            risk_analysis = json.loads(cleaned_response)

            console.print("🔎 [Risk Sentinel] Análise de riscos concluída!")
            return risk_analysis
        except Exception as e:
            console.print(f"[bold red]ERRO ao analisar riscos:[/bold red] {e}")
            # Retorna uma lista vazia em caso de erro para não quebrar o fluxo
            return []