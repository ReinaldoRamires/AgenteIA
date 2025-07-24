# agents/fin_modeler.py
import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class FinModeler:
    """
    Usa IA para criar modelos e análises de viabilidade financeira.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [FinModeler] Inicializado.")

    def analyze_viability(self, project: models.Project, market_analysis: dict) -> str:
        """
        Gera uma análise de viabilidade financeira simplificada.
        """
        console.print(
            f"💰 [FinModeler] Analisando viabilidade financeira para: [bold green]{project.name}[/bold green]..."
        )

        # Usamos a análise de mercado (SOM) que já temos para dar mais contexto à IA
        som_context = market_analysis.get("som", {}).get("value", "não estimado")

        prompt = f"""
            Aja como um Analista Financeiro (CFA).
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}", 
            com um Mercado Obtível (SOM) estimado em "{som_context}", crie uma análise de viabilidade financeira simplificada em formato Markdown.

            Faça as seguintes suposições para um cenário base:
            - Investimento Inicial (CAPEX): Estime um valor razoável para este tipo de projeto.
            - Custo Operacional Anual (OPEX): Estime um valor razoável.
            - Projeção de Receita Anual para 5 anos, começando de forma conservadora e crescendo em direção a uma pequena fatia do SOM.

            Com base nessas suposições, calcule e apresente:
            1.  **Resumo das Premissas:** Liste o CAPEX, OPEX e as receitas anuais projetadas.
            2.  **Fluxo de Caixa Descontado (DCF) Simplificado:** Mostre o fluxo de caixa ano a ano e o Valor Presente Líquido (VPL/NPV), assumindo uma taxa de desconto de 15% a.a.
            3.  **ROI (Retorno sobre o Investimento):** Calcule o ROI ao final de 5 anos.
            4.  **Payback Simples:** Estime em que ano o investimento inicial é pago.
            5.  **Conclusão do Analista:** Dê um parecer breve sobre a viabilidade do projeto com base nos números.
        """

        with console.status(
            "[bold yellow]Aguardando IA calcular a viabilidade...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("💰 [FinModeler] Análise de viabilidade concluída!")
        return response.text
