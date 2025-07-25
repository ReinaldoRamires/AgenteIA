# agents/agent_router.py
from rich.console import Console
from rich.rule import Rule

console = Console()


class AgentRouter:
    """
    Recebe eventos e despacha para os agentes especialistas
    corretos com base em fluxos de trabalho definidos em um arquivo de regras.
    """

    def __init__(self, agents: dict, rules: dict, dry_run: bool = False):
        self.agents = agents
        self.workflows = rules.get("event_workflows", {})
        self.dry_run = dry_run

    def route_event(self, event_type: str, data: dict):
        """
        Roteia um evento pelo workflow configurado.
        """
        console.print(Rule(f" Evento: {event_type} "))
        if event_type in self.workflows:
            for step in self.workflows[event_type]:
                agent_cls = self.agents.get(step)
                if not agent_cls:
                    console.print(f"[red]Agente '{step}' não encontrado[/red]")
                    continue
                agent = agent_cls()
                agent.execute(data, dry_run=self.dry_run)
        else:
            console.print(
                f"[yellow]Nenhum workflow para evento '{event_type}'[/yellow]"
            )
