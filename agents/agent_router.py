from rich.console import Console
from rich.rule import Rule
from .base_agent import BaseAgent
from .schedule_copilot import ScheduleCopilot
from .notion_writer import NotionWriter
from .market_intel_bot import MarketIntelBot
from .compliance_guardian import ComplianceGuardian
from .risk_sentinel import RiskSentinel
from .go_to_market_copilot import GoToMarketCopilot
from .org_designer import OrgDesigner
from .fin_modeler import FinModeler
from .executive_narrator import ExecutiveNarrator
from .capacity_forecaster import CapacityForecaster
from .backup_job import BackupJob
from .status_collector import StatusCollector
from .accounting_helper import AccountingHelper

console = Console()

class AgentRouter:
    def __init__(self, config: dict, model_mapping: dict, rules: dict):
        self.config = config
        self.model_mapping = model_mapping
        self.workflows = rules.get("event_workflows", {})
        # Instancia os agentes
        self.agents = {
            "schedule_copilot":        ScheduleCopilot(config, model_mapping),
            "notion_writer":           NotionWriter(config, model_mapping),
            "market_intel_bot":        MarketIntelBot(config, model_mapping),
            "compliance_guardian":     ComplianceGuardian(config, model_mapping),
            "risk_sentinel":           RiskSentinel(config, model_mapping),
            "go_to_market_copilot":    GoToMarketCopilot(config, model_mapping),
            "org_designer":            OrgDesigner(config, model_mapping),
            "fin_modeler":             FinModeler(config, model_mapping),
            "executive_narrator":      ExecutiveNarrator(config, model_mapping),
            "capacity_forecaster":     CapacityForecaster(config, model_mapping),
            "status_collector":        StatusCollector(config, model_mapping),
            "backup_job":              BackupJob(config, model_mapping),
            "accounting_helper":       AccountingHelper(config, model_mapping),
        }
        # Ações -> agentes
        self.action_to_agent = {
            "analyze_market":     "market_intel_bot",
            "analyze_compliance": "compliance_guardian",
            "plan_gtm":           "go_to_market_copilot",
            "analyze_risks":      "risk_sentinel",
            "design_org":         "org_designer",
        }

    def run_workflow(self, event_name: str, project_data: dict, dry_run: bool = False):
        steps = self.workflows.get(event_name, [])
        total = len(steps)
        console.print(Rule(title=f"Workflow: {event_name} ({total} etapas)", characters="─", style="magenta"))
        for idx, action in enumerate(steps, start=1):
            agent_key = self.action_to_agent[action]
            agent = self.agents[agent_key]
            console.print(f"{'[DryRun]' if dry_run else '[Exec]'} Etapa {idx}/{total} → {action}  (agente: {agent_key})")
            try:
                agent.run(project_data, dry_run=dry_run)
            except Exception as e:
                console.print(f"❌ Erro em '{agent_key}': {e}")
        console.print(Rule("Workflow finalizado", style="magenta"))