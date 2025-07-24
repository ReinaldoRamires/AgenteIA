# agents/executive_narrator.py
import google.generativeai as genai
from rich.console import Console

# Importamos nossos modelos de dados para type hinting
from src import models

console = Console()


class ExecutiveNarrator:
    """
    Usa IA para gerar relatórios e narrativas executivas sobre projetos.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        console.print("✅ [Executive Narrator] Inicializado e pronto para narrar.")

    def generate_report(self, project: models.Project, tasks: list[models.Task]) -> str:
        """
        Gera um relatório executivo em Markdown para um projeto e suas tarefas.
        """
        console.print(
            f"📖 [Executive Narrator] Gerando relatório para: [bold green]{project.name}[/bold green]..."
        )

        # 1. Construir o contexto com os dados que temos
        task_list_str = "\n".join(
            [f"- {task.template} (Status: {task.percent_done}%)" for task in tasks]
        )
        context = f"""
        **Dados do Projeto:**
        - Nome: {project.name}
        - Tipo: {project.project_type}
        - País: {project.country}
        - Status Geral: {project.status.value}
        - Data de Criação: {project.created_at.strftime('%d/%m/%Y')}

        **Lista de Tarefas do Cronograma:**
        {task_list_str}
        """

        # 2. Criar o prompt para a IA
        prompt = f"""
            Aja como um Gerente de Projetos Sênior escrevendo um relatório de status para um executivo.
            Com base nos dados abaixo, escreva um breve relatório de status em formato Markdown.

            O relatório deve ter:
            1.  Um título (## Relatório de Status do Projeto: [Nome do Projeto]).
            2.  Um parágrafo de "Resumo Executivo" com a situação geral.
            3.  Uma seção de "Principais Atividades" em formato de bullet points, baseada na lista de tarefas.
            4.  Uma breve seção de "Próximos Passos".

            Seja conciso, profissional e direto ao ponto.

            ---
            {context}
            ---
        """

        # 3. Chamar a IA e retornar o resultado
        with console.status(
            "[bold yellow]Aguardando IA escrever o relatório...[/bold yellow]"
        ):
            response = self.model.generate_content(prompt)

        console.print("📖 [Executive Narrator] Relatório gerado com sucesso!")
        return response.text
