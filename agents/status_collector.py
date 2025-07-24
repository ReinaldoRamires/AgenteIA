# agents/status_collector.py
from datetime import datetime, timedelta

import notion_client
from rich.console import Console

console = Console()


class StatusCollector:
    """Observa o Notion em busca de atualizações de status."""

    def __init__(self, api_key: str, tasks_db_id: str):
        if not api_key or not tasks_db_id:
            raise ValueError("API Key e Tasks DB ID do Notion são obrigatórios.")

        self.notion = notion_client.Client(auth=api_key)
        self.tasks_db_id = tasks_db_id
        console.print(
            "✅ [Status Collector] Conexão com o cliente Notion estabelecida."
        )

    def check_for_updates(self):
        """Busca por tarefas que foram atualizadas no último minuto."""
        one_minute_ago = (datetime.now() - timedelta(minutes=1)).isoformat()

        console.print(
            f"📊 [Status Collector] Verificando tarefas atualizadas desde {one_minute_ago}..."
        )

        try:
            results = self.notion.databases.query(
                database_id=self.tasks_db_id,
                filter={
                    "timestamp": "last_edited_time",
                    "last_edited_time": {"after": one_minute_ago},
                },
            ).get("results")

            if results:
                for page in results:
                    task_name = page["properties"]["Name"]["title"][0]["text"][
                        "content"
                    ]
                    status = page["properties"]["Status"]["status"]["name"]
                    console.print(
                        f"   -> [bold yellow]Atualização Encontrada![/bold yellow] Tarefa '{task_name}' agora está com status '{status}'."
                    )
            else:
                console.print("   -> Nenhuma atualização encontrada.")

        except notion_client.errors.APIResponseError as e:
            console.print(
                f"[bold red]ERRO ao buscar atualizações no Notion:[/bold red] {e}"
            )
