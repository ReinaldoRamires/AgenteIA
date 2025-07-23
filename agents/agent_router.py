# agents/agent_router.py
from rich.console import Console

console = Console()

class AgentRouter:
    """
    Recebe eventos e despacha para os agentes especialistas corretos
    com base em fluxos de trabalho definidos em um arquivo de regras.
    """
    def __init__(self, agents: dict, rules: dict, dry_run: bool = False):
        self.agents = agents
        self.workflows = rules.get("event_workflows", {})
        self.dry_run = dry_run
        console.print(f"✅ [Agent Router] Maestro dinâmico pronto. Modo dry_run: {self.dry_run}")

    def _execute_workflow(self, workflow_steps: list, project):
        """
        Executa ou simula uma lista de ações de agentes em sequência.
        """
        title_action = "Simulando" if self.dry_run else "Iniciando"
        total_steps = len(workflow_steps)
        console.rule(f"[bold magenta]{title_action} Cascata de Análise Dinâmica ({total_steps} etapas)[/bold magenta]")

        for i, agent_action in enumerate(workflow_steps, 1):
            console.print(f"\n--- Etapa {i}/{total_steps}: {'Planejando' if self.dry_run else 'Executando'} '{agent_action}' ---")

            if not self.dry_run:
                agent_instance = self.agents.get(agent_action)
                if not agent_instance:
                    console.print(f"[bold red]Aviso:[/bold red] Agente para a ação '{agent_action}' não encontrado.")
                    continue

                action_map = {
                    "analyze_market": "analyze_market_potential", "analyze_compliance": "analyze_compliance_risks",
                    "plan_gtm": "generate_strategy", "analyze_risks": "analyze_risks", "design_org": "design_team_structure",
                }
                method_name = action_map.get(agent_action)
                if not method_name:
                    console.print(f"[bold red]Aviso:[/bold red] Método para a ação '{agent_action}' não mapeado.")
                    continue

                method_to_call = getattr(agent_instance, method_name, None)
                # AQUI ESTÁ A CORREÇÃO DE INDENTAÇÃO:
                if method_to_call and callable(method_to_call):
                    try:
                        method_to_call(project)
                    except Exception as e:
                        console.print(f"[bold red]Falha na execução da ação '{agent_action}': {e}[/bold red]")
                else:
                    console.print(f"[bold red]Aviso:[/bold red] Método '{method_name}' não encontrado no agente.")

        # AQUI ESTÁ A SEGUNDA CORREÇÃO: Esta linha estava dentro do 'for'
        console.rule("[bold magenta]Cascata de Análise Concluída[/bold magenta]")

    def route_event(self, event_type: str, data: dict):
        """
        Recebe um evento e dispara o fluxo de trabalho correspondente das regras.
        """
        console.print(f"🧠 [Agent Router] Evento recebido: [bold yellow]{event_type}[/bold yellow]")
        if event_type in self.workflows:
            workflow_steps = self.workflows[event_type]
            project = data.get('project')
            if project or self.dry_run:
                self._execute_workflow(workflow_steps, project)
            else:
                console.print(f"[bold red]Erro:[/bold red] Dados do projeto ausentes para o evento '{event_type}'.")
        else:
            console.print(f"-> Nenhum fluxo de trabalho definido para o evento '{event_type}'.")