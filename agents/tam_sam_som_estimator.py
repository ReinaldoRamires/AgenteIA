# agents/tam_sam_som_estimator.py
import json

import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class TAMSAMSOMEstimator:
    """
    Usa IA para uma análise focada em estimar o tamanho do mercado (TAM, SAM, SOM).
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [TAM-SAM-SOM Estimator] Inicializado.")

    def estimate(self, project: models.Project) -> dict:
        """
        Gera uma estimativa detalhada de TAM, SAM, SOM.
        """
        console.print(
            f"📊 [Estimator] Estimando TAM/SAM/SOM para: [bold green]{project.name}[/bold green]..."
        )

        prompt = f"""
            Aja como um Analista de Pesquisa de Mercado.
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}" operando em "{project.country}",
            forneça uma estimativa de TAM (Total Addressable Market), SAM (Serviceable Available Market) e SOM (Serviceable Obtainable Market).

            Para cada um (TAM, SAM, SOM), forneça:
            - "value": Um valor monetário estimado (ex: "US$ 5 Bilhões", "R$ 100 Milhões").
            - "justification": Uma breve justificativa para a sua estimativa, baseada em dados ou premissas lógicas.

            Responda APENAS com um objeto JSON válido, sem nenhum texto adicional.
            O formato deve ser:
            {{
              "tam": {{ "value": "...", "justification": "..." }},
              "sam": {{ "value": "...", "justification": "..." }},
              "som": {{ "value": "...", "justification": "..." }}
            }}
        """

        try:
            with console.status(
                "[bold yellow]Aguardando IA estimar o mercado...[/bold yellow]"
            ):
                response = self.model.generate_content(prompt)

            cleaned_response = (
                response.text.strip().replace("```json", "").replace("```", "")
            )
            market_size = json.loads(cleaned_response)

            console.print("📊 [Estimator] Estimativa de mercado concluída!")
            return market_size
        except Exception as e:
            console.print(f"[bold red]ERRO ao estimar o mercado:[/bold red] {e}")
            return {}
