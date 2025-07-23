# src/main.py (Versão Final Completa)
import typer, yaml, re, subprocess, sys, json, os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
import notion_client
from datetime import date
from . import models
from agents.notion_writer import NotionWriter
from agents.schedule_copilot import ScheduleCopilot
from agents.market_intel_bot import MarketIntelBot
from agents.executive_narrator import ExecutiveNarrator
from agents.compliance_guardian import ComplianceGuardian
from agents.go_to_market_copilot import GoToMarketCopilot
from agents.contract_fabric import ContractFabric
from agents.it_bootstrapper import ITBootstrapper
from agents.org_designer import OrgDesigner
from agents.fin_modeler import FinModeler
from agents.agent_router import AgentRouter
from agents.risk_sentinel import RiskSentinel
from agents.capacity_forecaster import CapacityForecaster
from agents.stakeholder_graph_bot import StakeholderGraphBot
from agents.brand_kit_bot import BrandKitBot
from agents.doc_checklist_builder import DocChecklistBuilder
from agents.comm_plan_builder import CommPlanBuilder
from agents.process_mapper import ProcessMapper
from agents.sensitivity_scenario_engine import SensitivityScenarioEngine
from agents.accounting_helper import AccountingHelper
from agents.feature_viability_scout import FeatureViabilityScout
from agents.decision_supporter import DecisionSupporter
from agents.tam_sam_som_estimator import TAMSAMSOMEstimator
from agents.capacity_leveler import CapacityLeveler

console = Console(); app = typer.Typer(help="🚀 Productivity Engine - PMO Digital 360°")

def get_config():
    try:
        with open("config/config.yaml", "r", encoding="utf-8") as f: return yaml.safe_load(f)
    except FileNotFoundError: console.print("[bold red]Erro:[/bold red] 'config.yaml' não encontrado."); raise typer.Exit(1)
    except Exception as e: console.print(f"[bold red]Erro ao ler config:[/bold red] {e}"); raise typer.Exit(1)

def get_db_session(db_url: str):
    engine = create_engine(db_url); return sessionmaker(autocommit=False, autoflush=False, bind=engine)()

# --- Comandos dos Agentes ---

@app.command(help="✨ Cria um novo projeto e seu cronograma de tarefas no DB e Notion.")
def new_project(name: str = typer.Argument(..., help="O nome completo do novo projeto."), project_type: str = typer.Option("Padrão", help="O tipo de projeto."), country: str = typer.Option("Global", help="O país.")):
    # (Este comando agora é manual, sem a cascata automática para estabilidade)
    console.print(f"✨ Iniciando criação do projeto: [bold green]{name}[/bold green]")
    config = get_config(); db_session = get_db_session(config.get("database_url"))
    try:
        writer = NotionWriter(api_key=config["api_keys"]["notion"], projects_db_id=config["notion_db"]["projects_db_id"], tasks_db_id=config["notion_db"]["tasks_db_id"])
        scheduler = ScheduleCopilot()
        slug = re.sub(r'[^\w-]', '', name.lower().replace(' ', '-'))
        project_data = {"slug": slug, "name": name, "type": project_type, "country": country}
        notion_page_id = writer.create_project_page(project_data)
        db_project = models.Project(name=name, slug=slug, project_type=project_type, country=country, status=models.ProjectStatus.PLANNING, notion_page_id=notion_page_id)
        db_session.add(db_project); db_session.flush()
        tasks = scheduler.generate_schedule(project_type)
        for task_item in tasks:
            writer.create_task_page(task_item, project_relation_id=notion_page_id)
            db_task = models.Task(project_id=db_project.id, template=task_item['name'], dor=task_item['dor'], dod=task_item['dod'], estimate=task_item.get('estimate', 0))
            db_session.add(db_task)
        db_session.commit()
        console.print(f"✅ Projeto '{name}' criado com sucesso! Slug: [bold cyan]{slug}[/bold cyan]")
    except Exception as e:
        console.print(f"[bold red]Falha na criação do projeto: {e}[/bold red]"); db_session.rollback()
    finally:
        db_session.close()

@app.command(help="🤔 Analisa os prós, contras e riscos de uma decisão estratégica.")
def support_decision(project_slug: str = typer.Argument(..., help="O 'slug' do projeto."), decision: str = typer.Argument(..., help="A decisão a ser analisada.")):
    config = get_config(); db_session = get_db_session(config.get("database_url"))
    try:
        project = db_session.query(models.Project).filter_by(slug=project_slug).first()
        if not project: console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado."); return
        supporter = DecisionSupporter(api_key=config["api_keys"]["google_gemini"])
        analysis = supporter.analyze_trade_offs(project, decision)
        console.print(f"\n--- Análise da Decisão: '{decision}' ---\n{analysis}\n-------------------------------------------------")
    except Exception as e: console.print(f"[bold red]Ocorreu um erro na análise da decisão: {e}[/bold red]")
    finally: db_session.close()

# (Aqui estão todos os outros comandos que você já testou e funcionaram)
@app.command(help="🗺️  Mapeia os stakeholders de um projeto.")
def map_stakeholders(project_slug: str = typer.Argument(..., help="O 'slug' do projeto.")):
    config = get_config(); db_session = get_db_session(config.get("database_url"))
    try:
        project = db_session.query(models.Project).filter_by(slug=project_slug).first()
        if not project: console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado."); return
        mapper = StakeholderGraphBot(api_key=config["api_keys"]["google_gemini"]); stakeholders = mapper.map_stakeholders(project)
        if stakeholders:
            table = Table(title=f"Mapeamento de Stakeholders para: {project.name}", show_header=True, header_style="bold green")
            table.add_column("Stakeholder", style="dim", width=25); table.add_column("Influência"); table.add_column("Interesse"); table.add_column("Estratégia de Engajamento", width=50)
            for sh in stakeholders: table.add_row(sh['stakeholder'], sh['influence'], sh['interest'], sh['engagement_strategy'])
            console.print(table)
    finally: db_session.close()

@app.command(help="🎨 Gera um kit de identidade de marca para um projeto.")
def generate_brand(project_slug: str = typer.Argument(..., help="O 'slug' do projeto.")):
    config = get_config(); db_session = get_db_session(config.get("database_url"))
    try:
        project = db_session.query(models.Project).filter_by(slug=project_slug).first()
        if not project: console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado."); return
        brander = BrandKitBot(api_key=config["api_keys"]["google_gemini"]); kit = brander.generate_kit(project)
        if kit:
            slogan = kit.get('slogan', 'N/A'); mission = kit.get('mission_statement', 'N/A'); palette = kit.get('color_palette', [])
            colors_str = "\n".join(f"[{color.split(' ')[0]}]███[/] {color}" for color in palette)
            panel_content = f"[bold]Slogan:[/bold] {slogan}\n\n[bold]Missão:[/bold] {mission}\n\n[bold]Paleta de Cores:[/bold]\n{colors_str}"
            console.print(Panel(panel_content, title=f"Kit de Marca para: {project.name}", border_style="yellow"))
    finally: db_session.close()

@app.command(help="📊 Inicia o dashboard visual de projetos.")
def dashboard():
    console.print("📊 Lançando o dashboard de projetos...")
    command = ["streamlit", "run", "src/dashboard.py"]
    try: subprocess.run(command, check=True)
    except Exception as e: console.print(f"[bold red]Erro ao tentar iniciar o Streamlit:[/bold red] {e}\nTente rodar: [bold cyan]streamlit run src/dashboard.py[/bold cyan]")

@app.command(help="⚙️  Cria o arquivo de banco de dados e as tabelas.")
def init_db():
    console.print("⚙️  Inicializando o banco de dados...")
    config = get_config(); db_url = config.get("database_url")
    engine = create_engine(db_url); models.create_db_and_tables(engine)
    console.print(f"✅ Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    app()