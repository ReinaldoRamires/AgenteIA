# agents/accounting_helper.py
import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class AccountingHelper:
    """
    Usa IA para fornecer recomendações contábeis e fiscais iniciais.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [Accounting Helper] Inicializado.")

    def suggest_structure(self, project: models.Project) -> str:
        """
        Sugere um regime tributário e um plano de contas simplificado.
        """
        console.print(
            f"🧾 [Accounting Helper] Sugerindo estrutura contábil para: [bold green]{project.name}[/bold green]..."
        )

        prompt = f"""
            Aja como um Contador Consultor especializado em startups.
            Para um novo projeto no Brasil chamado "{project.name}", do tipo "{project.project_type}",
            forneça recomendações iniciais em formato Markdown sobre:

            1.  **Regime Tributário Sugerido:** Sugira o regime mais provável para uma empresa nascente (Simples Nacional, Lucro Presumido) e justifique brevemente.
            2.  **Plano de Contas Simplificado:** Liste as 5 principais contas de Despesa e 3 de Receita que a empresa deveria monitorar desde o início.
            3.  **Principal Obrigação Acessória:** Cite uma obrigação fiscal/contábil mensal importante para uma empresa de serviços no Brasil.
        """

        with console.status(
            "[bold yellow]Aguardando IA preparar as recomendações contábeis...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("🧾 [Accounting Helper] Recomendações geradas com sucesso!")
        return response.text
