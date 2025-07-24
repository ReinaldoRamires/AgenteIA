# agents/capacity_forecaster.py
from rich.console import Console
from rich.table import Table

from src import models

console = Console()


class CapacityForecaster:
    """
    Analisa a capacidade da equipe versus a demanda das tarefas do projeto.
    """

    def __init__(self, team_capacity: list[dict]):
        self.team_capacity = {
            item["role"]: item["hours_per_week"] for item in team_capacity
        }
        console.print(
            "✅ [Capacity Forecaster] Inicializado com a capacidade da equipe."
        )

    def forecast(self, project: models.Project, tasks: list[models.Task]):
        """
        Compara a carga de trabalho total estimada com a capacidade da equipe.
        """
        console.print(
            f"📊 [Capacity Forecaster] Calculando previsão para: [bold green]{project.name}[/bold green]..."
        )

        # 1. Calcular a demanda total (soma das estimativas das tarefas)
        total_demand_hours = sum(
            task.estimate
            for task in tasks
            if hasattr(task, "estimate") and task.estimate is not None
        )

        # 2. Calcular a capacidade total (soma das horas da equipe)
        total_capacity_hours_per_week = sum(self.team_capacity.values())

        # Para uma análise simples, vamos assumir um projeto de 4 semanas
        project_duration_weeks = 4
        total_capacity_for_project = (
            total_capacity_hours_per_week * project_duration_weeks
        )

        # 3. Apresentar os resultados em uma tabela
        table = Table(
            title="Análise de Capacidade vs. Demanda (Previsão de 4 semanas)",
            show_header=True,
            header_style="bold blue",
        )
        table.add_column("Métrica", style="dim")
        table.add_column("Valor")

        table.add_row("Demanda Total Estimada", f"{total_demand_hours} horas")
        table.add_row(
            "Capacidade Semanal da Equipe",
            f"{total_capacity_hours_per_week} horas/semana",
        )
        table.add_row(
            f"Capacidade Total no Período ({project_duration_weeks} semanas)",
            f"{total_capacity_for_project} horas",
        )

        balance = total_capacity_for_project - total_demand_hours
        balance_str = (
            f"[green]{balance} horas[/green]"
            if balance >= 0
            else f"[red]{balance} horas[/red]"
        )
        table.add_row("Balanço (Capacidade - Demanda)", balance_str)

        console.print(table)

        if balance < 0:
            console.print(
                f"[bold red]ALERTA:[/bold red] A demanda estimada excede a capacidade da equipe em {-balance:.1f} horas."
            )
            console.print(
                "-> Ações recomendadas: renegociar escopo, aumentar prazo ou alocar mais recursos."
            )
        else:
            console.print(
                "[bold green]STATUS:[/bold green] A equipe tem capacidade suficiente para a demanda estimada neste período."
            )
