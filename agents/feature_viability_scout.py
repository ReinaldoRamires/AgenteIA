# agents/feature_viability_scout.py
import google.generativeai as genai
from rich.console import Console
from src import models

console = Console()

class FeatureViabilityScout:
    """
    Usa IA para fazer uma análise de viabilidade de novas funcionalidades.
    """
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        console.print("✅ [Feature Viability Scout] Inicializado.")

    def scout(self, project: models.Project, feature_description: str) -> str:
        """
        Analisa a viabilidade de uma nova funcionalidade para um projeto.
        """
        console.print(f"🕵️  [Feature Scout] Analisando viabilidade da funcionalidade para: [bold green]{project.name}[/bold green]...")

        prompt = f"""
            Aja como um Gerente de Produto (Product Manager) experiente.
            Para um projeto chamado "{project.name}", do tipo "{project.project_type}", 
            estamos considerando adicionar a seguinte funcionalidade: "{feature_description}".

            Faça uma breve análise de viabilidade em formato Markdown, cobrindo:
            1.  **Análise Competitiva:** Cite 1 ou 2 concorrentes que já possuem uma funcionalidade similar e como eles a implementam.
            2.  **Alinhamento Estratégico:** A funcionalidade está alinhada com o tipo de produto? Agrega valor ao Perfil de Cliente Ideal?
            3.  **Parecer de Viabilidade:** Dê seu parecer (ex: "Alta Viabilidade", "Padrão de Mercado", "Aposta Arriscada") e justifique em uma frase.
        """

        with console.status("[bold yellow]Aguardando IA analisar a funcionalidade...[/bold yellow]"):
            response = self.model.generate_content(prompt)

        console.print("🕵️  [Feature Scout] Análise concluída!")
        return response.text