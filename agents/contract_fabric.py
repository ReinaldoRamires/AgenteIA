# agents/contract_fabric.py
import google.generativeai as genai
from rich.console import Console
from datetime import date

console = Console()

class ContractFabric:
    """
    Usa IA para gerar minutas de documentos legais simples.
    """
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        console.print("✅ [Contract Fabric] Inicializado.")

    def generate_nda(self, party_a: str, party_b: str, effective_date: str) -> str:
        """
        Gera uma minuta de um Acordo de Confidencialidade (NDA) simples.
        """
        console.print(f"⚖️  [Contract Fabric] Gerando NDA entre [bold green]{party_a}[/bold green] e [bold green]{party_b}[/bold green]...")

        prompt = f"""
            Aja como um advogado especializado em contratos.
            Gere o texto de um Acordo de Confidencialidade (NDA) mútuo e simples, em português do Brasil.

            Use os seguintes dados:
            - Parte Divulgadora/Receptora A: "{party_a}"
            - Parte Divulgadora/Receptora B: "{party_b}"
            - Data Efetiva: "{effective_date}"

            O documento deve incluir as seguintes seções essenciais:
            1.  Identificação das Partes.
            2.  Definição de "Informação Confidencial".
            3.  Obrigações das Partes.
            4.  Exclusões da Confidencialidade.
            5.  Prazo do Acordo (sugira 5 anos a partir da data efetiva).
            6.  Lei Aplicável e Foro (sugira o foro da comarca de São Paulo, SP).
            7.  Assinaturas.

            O tom deve ser formal e claro. Não inclua nenhuma nota de rodapé ou comentário seu, apenas o texto do contrato.
        """

        with console.status("[bold yellow]Aguardando IA redigir o documento...[/bold yellow]"):
            response = self.model.generate_content(prompt)

        console.print("⚖️  [Contract Fabric] Minuta do NDA gerada com sucesso!")
        return response.text