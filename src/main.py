import os
import subprocess
from pathlib import Path
from typing import Any, Dict

import yaml
import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from agents.agent_router import AgentRouter
from agents.notion_writer import NotionWriter
from agents.schedule_copilot import ScheduleCopilot
from agents.decision_supporter import DecisionSupporter
from agents.stakeholder_graph_bot import StakeholderGraphBot
from agents.brand_kit_bot import BrandKitBot

from src import models  # noqa: F401 — importa src.models corretamente

# ---------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------
load_dotenv()
console = Console()
app = typer.Typer(help="🚀 PMO 360° – CLI")

# ---------------------------------------------------------------------
# Helpers para configuração e DB
# ---------------------------------------------------------------------
def load_env_vars(project_root: Path) -> None:
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    else:
        console.print("[yellow]Aviso: .env não encontrado na raiz do projeto.[/yellow]")


def load_config(project_root: Path) -> Dict[str, Any]:
    cfg_path = project_root / "config" / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Override por ENV
    cfg["openai_key"]   = os.getenv("OPENAI_API_KEY", cfg.get("openai_key"))
    cfg["gemini_key"]   = os.getenv("GEMINI_API_KEY", cfg.get("gemini_key"))
    cfg["notion_token"] = os.getenv("NOTION_TOKEN", cfg.get("notion_token"))

    for key, label in [
        ("openai_key", "OPENAI_API_KEY"),
        ("gemini_key", "GEMINI_API_KEY"),
        ("notion_token", "NOTION_TOKEN"),
    ]:
        if not cfg.get(key):
            console.print(f"[yellow]Aviso: {label} não definido.[/yellow]")

    return cfg


def load_model_mapping(cfg: Dict[str, Any], project_root: Path) -> Dict[str, str]:
    mapping_path = project_root / cfg["model_mapping_file"]
    with open(mapping_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["model_mapping"]


def load_rules(cfg: Dict[str, Any], project_root: Path) -> Dict[str, Any]:
    rules_path = project_root / cfg["rules_file"]
    with open(rules_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_db_session(db_url: str):
    engine = create_engine(db_url, future=True)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return Session()


# ---------------------------------------------------------------------
# Comando principal: NEW_PROJECT_CREATED (fluxo manual)
# ---------------------------------------------------------------------
@app.command(help="✨ Cria um novo projeto e seu cronograma de tarefas no DB e Notion.")
def new_project(
    name: str = typer.Argument(..., help="O nome completo do novo projeto."),
    project_type: str = typer.Option("default", help="O tipo de projeto."),
    country: str = typer.Option("Brasil", help="O país."),
) -> None:
    console.print(f"✨ Iniciando criação do projeto: [bold green]{name}[/bold green]")
    project_root = Path(__file__).resolve().parents[1]
    cfg = load_config(project_root)
    db_session = get_db_session(cfg["database_url"])

    try:
        writer = NotionWriter(
            api_key=cfg["notion_token"],
            projects_db_id=cfg["notion_db"]["projects_db_id"],
            tasks_db_id=cfg["notion_db"]["tasks_db_id"],
        )
        scheduler = ScheduleCopilot()
        slug = re.sub(r"[^\w-]", "", name.lower().replace(" ", "-"))
        project_data = {"slug": slug, "name": name, "type": project_type, "country": country}
        notion_page_id = writer.create_project_page(project_data)

        db_project = models.Project(
            name=name,
            slug=slug,
            project_type=project_type,
            country=country,
            status=models.ProjectStatus.PLANNING,
            notion_page_id=notion_page_id,
        )
        db_session.add(db_project)
        db_session.flush()

        tasks = scheduler.generate_schedule(project_type)
        for task_item in tasks:
            writer.create_task_page(task_item, project_relation_id=notion_page_id)
            db_task = models.Task(
                project_id=db_project.id,
                template=task_item["name"],
                dor=task_item.get("dor", ""),
                dod=task_item.get("dod", ""),
                estimate=task_item.get("estimate", 0),
            )
            db_session.add(db_task)

        db_session.commit()
        console.print(
            f"✅ Projeto '{name}' e tarefas sincronizados com sucesso! "
            f"Slug: [bold cyan]{slug}[/bold cyan]"
        )
    except Exception as e:
        console.print(f"[bold red]Falha na criação do projeto:[/] {e}")
        db_session.rollback()
    finally:
        db_session.close()


# ---------------------------------------------------------------------
# Comando avançado: análise de decisão
# ---------------------------------------------------------------------
@app.command(help="🤔 Analisa prós, contras e riscos de uma decisão estratégica.")
def support_decision(
    project_slug: str = typer.Argument(..., help="Slug do projeto."),
    decision: str    = typer.Argument(..., help="Decisão a ser analisada."),
) -> None:
    cfg = load_config(Path(__file__).resolve().parents[1])
    db_session = get_db_session(cfg["database_url"])
    project = db_session.query(models.Project).filter_by(slug=project_slug).first()
    if not project:
        console.print(f"[bold red]Erro:[/] Projeto '{project_slug}' não encontrado.")
        db_session.close()
        return

    try:
        supp     = DecisionSupporter(api_key=cfg["gemini_key"])
        analysis = supp.analyze_trade_offs(project, decision)
        console.print(f"\n--- Análise da Decisão: '{decision}' ---\n{analysis}\n" + "-"*50)
    except Exception as e:
        console.print(f"[bold red]Erro na análise: {e}[/bold red]")
    finally:
        db_session.close()


# ---------------------------------------------------------------------
# Comando avançado: mapeamento de stakeholders
# ---------------------------------------------------------------------
@app.command(help="🗺️  Mapeia stakeholders de um projeto.")
def map_stakeholders(project_slug: str = typer.Argument(..., help="Slug do projeto")) -> None:
    cfg = load_config(Path(__file__).resolve().parents[1])
    db_session = get_db_session(cfg["database_url"])
    project = db_session.query(models.Project).filter_by(slug=project_slug).first()
    if not project:
        console.print(f"[bold red]Erro:[/] Projeto '{project_slug}' não encontrado.")
        db_session.close()
        return

    try:
        mapper = StakeholderGraphBot(api_key=cfg["gemini_key"])
        sts    = mapper.map_stakeholders(project)
        table  = Table(title=f"Stakeholders: {project.name}", show_header=True, header_style="bold green")
        table.add_column("Stakeholder", style="dim", width=25)
        table.add_column("Influência")
        table.add_column("Interesse")
        table.add_column("Estratégia", width=50)
        for sh in sts:
            table.add_row(sh["stakeholder"], sh["influence"], sh["interest"], sh["engagement_strategy"])
        console.print(table)
    finally:
        db_session.close()


# ---------------------------------------------------------------------
# Comando avançado: kit de marca
# ---------------------------------------------------------------------
@app.command(help="🎨 Gera kit de marca para um projeto.")
def generate_brand(project_slug: str = typer.Argument(..., help="Slug do projeto")) -> None:
    cfg = load_config(Path(__file__).resolve().parents[1])
    db_session = get_db_session(cfg["database_url"])
    project = db_session.query(models.Project).filter_by(slug=project_slug).first()
    if not project:
        console.print(f"[bold red]Erro:[/] Projeto '{project_slug}' não encontrado.")
        db_session.close()
        return

    try:
        bt  = BrandKitBot(api_key=cfg["gemini_key"])
        kit = bt.generate_kit(project)
        slogan  = kit.get("slogan", "N/A")
        mission = kit.get("mission_statement", "N/A")
        palette = kit.get("color_palette", [])
        colors  = "\n".join(f"[{c.split()[0]}]███[/] {c}" for c in palette)
        panel = Panel(
            f"[bold]Slogan:[/bold] {slogan}\n\n"
            f"[bold]Missão:[/bold] {mission}\n\n"
            f"[bold]Paleta de Cores:[/bold] {colors}",
            title=f"Kit de Marca: {project.name}",
            border_style="yellow",
        )
        console.print(panel)
    finally:
        db_session.close()


# ---------------------------------------------------------------------
# Comando: dashboard Streamlit
# ---------------------------------------------------------------------
@app.command(help="📊 Abre dashboard Streamlit.")
def dashboard() -> None:
    console.print("📊 Abrindo dashboard...")
    subprocess.run(["streamlit", "run", "src/dashboard.py"], check=False)


# ---------------------------------------------------------------------
# Comando: inicializa banco de dados
# ---------------------------------------------------------------------
@app.command(help="⚙️  Inicializa banco de dados (SQLite).")
def init_db() -> None:
    console.print("⚙️ Inicializando banco de dados...")
    cfg = load_config(Path(__file__).resolve().parents[1])
    engine = create_engine(cfg["database_url"])
    models.create_db_and_tables(engine)
    console.print("✅ Banco inicializado com sucesso!")


# Entry-point
if __name__ == "__main__":
    app()
