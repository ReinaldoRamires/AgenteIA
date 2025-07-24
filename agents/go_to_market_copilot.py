# agents/go_to_market_copilot.py
import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class GoToMarketCopilot:
    """
    Usa IA para ajudar a definir a estratégia de Go-to-Market de um projeto.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [Go-to-Market Copilot] Inicializado.")

    def generate_strategy(self, project: models.Project) -> str:
        """
        Gera um esboço da estratégia de Go-to-Market.
        """
        console.print(
            f"📈 [Go-to-Market Copilot] Delineando estratégia para: [bold green]{project.name}[/bold green]..."
        )

        prompt = f"""
            Aja como um Diretor de Estratégia (CSO).
            Para um projeto chamado "{project.name}", que é um "{project.project_type}", 
            crie um esboço de uma estratégia de Go-to-Market em formato Markdown.

            O esboço deve cobrir os seguintes pontos:
            1.  **Perfil de Cliente Ideal (ICP):** Descreva o público-alvo principal em 2-3 frases.
            2.  **Modelo de Precificação (Pricing):** Sugira um modelo de precificação (ex: Assinatura, Freemium, Compra Única) e justifique brevemente.
            3.  **Canais de Aquisição:** Liste 3 canais de aquisição primários para focar no lançamento (ex: Marketing de Conteúdo, Anúncios Pagos, Parcerias).
            4.  **Mensagem Principal (Key Messaging):** Elabore uma frase que resuma o principal valor do produto para o cliente.
        """

        with console.status(
            "[bold yellow]Aguardando IA delinear a estratégia...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("📈 [Go-to-Market Copilot] Esboço da estratégia concluído!")
        return response.text
