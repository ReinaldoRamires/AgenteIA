# agents/it_bootstrapper.py
import google.generativeai as genai
from rich.console import Console

from src import models

console = Console()


class ITBootstrapper:
    """
    Usa IA para gerar um checklist de infraestrutura de TI para um novo projeto.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [IT Bootstrapper] Inicializado.")

    def generate_checklist(self, project: models.Project) -> str:
        """
        Gera um checklist de TI com base no tipo de projeto.
        """
        console.print(
            f"💻 [IT Bootstrapper] Gerando checklist de TI para: [bold green]{project.name}[/bold green]..."
        )

        prompt = f"""
            Aja como um Arquiteto de Soluções de TI experiente.
            Para um novo projeto chamado "{project.name}", que é do tipo "{project.project_type}", 
            crie um checklist inicial de bootstrapping de TI em formato Markdown.

            O checklist deve cobrir as seguintes áreas críticas:
            1.  **Infraestrutura em Nuvem (Cloud):** Sugira um provedor principal (AWS, GCP ou Azure) e os serviços essenciais para começar (ex: EC2/VM, S3/Blob Storage, RDS/Cloud SQL).
            2.  **Ferramentas de Comunicação e Colaboração:** Liste ferramentas essenciais (ex: Slack/Teams, Google Workspace/Office 365, Notion/Confluence).
            3.  **Controle de Versão e CI/CD:** Indique a plataforma (ex: GitHub, GitLab) e sugira uma ferramenta de CI/CD (ex: GitHub Actions, Jenkins).
            4.  **Segurança e Acessos:** Liste 3 pontos de ação de segurança fundamentais para o primeiro dia (ex: Ativar MFA, Política de senhas fortes, Gerenciador de senhas).
            5.  **Estratégia de Backup:** Descreva uma estratégia de backup simples e inicial para os dados críticos.
        """

        with console.status(
            "[bold yellow]Aguardando IA montar o checklist de TI...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("💻 [IT Bootstrapper] Checklist de TI gerado com sucesso!")
        return response.text
