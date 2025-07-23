# agents/market_intel_bot.py
import google.generativeai as genai
from rich.console import Console
import json

console = Console()

class MarketIntelBot:
    """
    Usa a API do Google Gemini para realizar análises de mercado.
    """
    def __init__(self, api_key: str):
        if not api_key or "SUA_CHAVE" in api_key:
            raise ValueError("A chave de API do Google Gemini é obrigatória.")
        genai.configure(api_key=api_key)
        # AQUI ESTÁ A CORREÇÃO: Usando um modelo mais recente.
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        console.print("✅ [Market Intel Bot] Conexão com a API do Google Gemini estabelecida.")

    def analyze_market_potential(self, project_name: str, project_type: str) -> dict:
        """
        Gera uma análise de potencial de mercado (TAM, SAM, SOM) para um projeto.
        """
        console.print(f"🤖 [Market Intel Bot] Analisando potencial de mercado para: [bold green]{project_name}[/bold green]...")

        prompt = f"""
            Aja como um analista de negócios sênior.
            Para um projeto chamado "{project_name}", que é do tipo "{project_type}", estime o seguinte:
            1.  **TAM (Total Addressable Market):** O mercado total para essa solução.
            2.  **SAM (Serviceable Available Market):** A fatia do mercado que podemos realisticamente alcançar com nossos canais.
            3.  **SOM (Serviceable Obtainable Market):** A porção do SAM que podemos capturar no curto/médio prazo.

            Forneça uma breve justificativa para cada estimativa.

            Responda APENAS com um objeto JSON válido, sem nenhum texto adicional antes ou depois.
            O formato do JSON deve ser:
            {{
              "tam": {{ "value": "...", "justification": "..." }},
              "sam": {{ "value": "...", "justification": "..." }},
              "som": {{ "value": "...", "justification": "..." }}
            }}
        """

        try:
            with console.status("[bold yellow]Aguardando resposta da IA...[/bold yellow]", spinner="dots"):
                response = self.model.generate_content(prompt)
            
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            
            analysis = json.loads(cleaned_response)
            console.print("🤖 [Market Intel Bot] Análise recebida com sucesso!")
            return analysis

        except Exception as e:
            console.print(f"[bold red]ERRO ao chamar a API do Gemini:[/bold red] {e}")
            raise