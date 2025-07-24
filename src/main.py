# src/main.py
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
from agents.decision_supporter import DecisionSupporter
from agents.stakeholder_graph_bot import StakeholderGraphBot
from agents.brand_kit_bot import BrandKitBot

import models  # noqa: F401

load_dotenv()
console = Console()
app = typer.Typer(help="🚀 PMO 360° – CLI")


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
    cfg["openai_key"] = os.getenv("OPENAI_API_KEY", cfg.get("openai_key"))
    cfg["gemini_key"] = os.getenv("GEMINI_API_KEY", cfg.get("gemini_key"))
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


@app.command(help="✨ Cria um novo projeto e dispara workflow NEW_PROJECT_CREATED.")
def new_project(
    name: str = typer.Argument(..., help="Nome do projeto"),
    project_type: str = typer.Option("default", help="Tipo de projeto"),
    country: str = typer.Option("Brasil", help="País"),
    dry_run: bool = typer.Option(False, help="Simulação (dry-run)"),
):
    project_root = Path(__file__).resolve().parents[1]
    load_env_vars(project_root)
    cfg = load_config(project_root)
    model_mapping = load_model_mapping(cfg, project_root)
    rules = load_rules(cfg, project_root)

    router = AgentRouter(cfg, model_mapping, rules)
    project_data = {
        "name": name,
        "project_type": project_type,
        "country": country,
        "team_capacity": cfg.get("team_capacity", []),
    }
    router.run_workflow("NEW_PROJECT_CREATED", project_data, dry_run=dry_run)
    typer.echo("Workflow finalizado" + (" (dry-run)" if dry_run else ""))


@app.command(help="🤔 Analisa prós, contras e riscos de uma decisão estratégica.")
def support_decision(
    project_slug: str = typer.Argument(..., help="Slug do projeto"),
    decision: str = typer.Argument(..., help="Decisão a ser analisada"),
):
    cfg = load_config(Path(__file__).resolve().parents[1])
    db = get_db_session(cfg["database_url"])
    project = db.query(models.Project).filter_by(slug=project_slug).first()
    if not project:
        console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado.")
        db.close()
        return

    try:
        supp = DecisionSupporter(api_key=cfg["gemini_key"])
        analysis = supp.analyze_trade_offs(project, decision)
        console.print(f"\n--- Análise da Decisão: '{decision}' ---\n{analysis}\n" + "-"*50)
    except Exception as e:
        console.print(f"[bold red]Erro na análise: {e}[/bold red]")
    finally:
        db.close()


@app.command(help="🗺️ Mapeia stakeholders de um projeto.")
def map_stakeholders(project_slug: str = typer.Argument(..., help="Slug do projeto")):
    cfg = load_config(Path(__file__).resolve().parents[1])
    db = get_db_session(cfg["database_url"])
    project = db.query(models.Project).filter_by(slug=project_slug).first()
    if not project:
        console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado.")
        db.close()
        return

    try:
        mapper = StakeholderGraphBot(api_key=cfg["gemini_key"])
        sts = mapper.map_stakeholders(project)
        table = Table(title=f"Stakeholders: {project.name}", show_header=True, header_style="bold green")
        table.add_column("Stakeholder", style="dim", width=25)
        table.add_column("Influência")
        table.add_column("Interesse")
        table.add_column("Estratégia", width=50)
        for sh in sts:
            table.add_row(sh["stakeholder"], sh["influence"], sh["interest"], sh["engagement_strategy"])
        console.print(table)
    finally:
        db.close()


@app.command(help="🎨 Gera kit de marca para um projeto.")
def generate_brand(project_slug: str = typer.Argument(..., help="Slug do projeto")):
    cfg = load_config(Path(__file__).resolve().parents[1])
    db = get_db_session(cfg["database_url"])
    project = db.query(models.Project).filter_by(slug=project_slug).first()
    if not project:
        console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado.")
        db.close()
        return

    try:
        bt = BrandKitBot(api_key=cfg["gemini_key"])
        kit = bt.generate_kit(project)
        slogan = kit.get("slogan", "N/A")
        mission = kit.get("mission_statement", "N/A")
        palette = kit.get("color_palette", [])
        colors = "\n".join(f"[{c.split()[0]}]███[/] {c}" for c in palette)
        panel = Panel(
            f"[bold]Slogan:[/bold] {slogan}\n\n"
            f"[bold]Missão:[/bold] {mission}\n\n"
            f"[bold]Paleta de Cores:[/bold]\n{colors}",
            title=f"Kit de Marca: {project.name}",
            border_style="yellow",
        )
        console.print(panel)
    finally:
        db.close()


@app.command(help="📊 Abre dashboard Streamlit.")
def dashboard():
    console.print("📊 Abrindo dashboard...")
    subprocess.run(["streamlit", "run", "src/dashboard.py"], check=False)


@app.command(help="⚙️ Inicializa o banco de dados (SQLite).")
def init_db():
    console.print("⚙️ Inicializando banco de dados...")
    cfg = load_config(Path(__file__).resolve().parents[1])
    engine = create_engine(cfg["database_url"])
    models.create_db_and_tables(engine)
    console.print("✅ Banco inicalizado com sucesso!")


if __name__ == "__main__":
    app()
