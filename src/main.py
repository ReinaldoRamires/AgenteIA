import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict

import yaml
import typer
from dotenv import load_dotenv
load_dotenv()
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agents.agent_router import AgentRouter

console = Console()
app = typer.Typer(help="🚀 PMO 360° - CLI")


# ---------------------------------------------------------------------
# Helpers para configuração e DB
# ---------------------------------------------------------------------
def load_env_vars(project_root: Path) -> None:
    """
    Carrega o arquivo .env da raiz do projeto.
    """
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        console.print("[yellow]Aviso: .env não encontrado na raiz do projeto.[/yellow]")


def load_config(project_root: Path) -> Dict[str, Any]:
    """
    Lê config.yaml e substitui chaves por variáveis de ambiente se existirem.
    """
    cfg_path = project_root / "config" / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

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


def get_db_session(database_url: str):
    """
    Retorna sessão SQLAlchemy simples.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(database_url, future=True)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return Session()


# ---------------------------------------------------------------------
# Comando principal: criação de projeto
# ---------------------------------------------------------------------
@app.command(name="new_project")
def new_project(
    name: str,
    project_type: str = typer.Option("default", help="Tipo de projeto"),
    country: str = typer.Option("Brasil", help="País"),
    dry_run: bool = typer.Option(False, help="Não chamar APIs (simulação)"),
) -> None:
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

    # Mantido run_workflow para compatibilidade com sua versão atual
    router.run_workflow("NEW_PROJECT_CREATED", project_data, dry_run=dry_run)
    typer.echo("Workflow finalizado." + (" (dry-run)" if dry_run else ""))


# ---------------------------------------------------------------------
# Comandos avançados
# ---------------------------------------------------------------------
@app.command(help="🤔 Analisa prós, contras e riscos de uma decisão estratégica.")
def support_decision(
    project_slug: str = typer.Argument(..., help="Slug do projeto"),
    decision: str = typer.Argument(..., help="Decisão a ser analisada"),
) -> None:
    project_root = Path(__file__).resolve().parents[1]
    load_env_vars(project_root)
    cfg = load_config(project_root)
    db = get_db_session(cfg["database_url"])
    try:
        from agents.decision_supporter import DecisionSupporter
        import models
    except ModuleNotFoundError as e:
        console.print(f"[bold red]Erro: módulo não encontrado: {e}[/bold red]")
        return

    project = db.query(models.Project).filter_by(slug=project_slug).first()
    if not project:
        console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado.")
        db.close()
        return

    try:
        supporter = DecisionSupporter(api_key=cfg["gemini_key"])
        analysis = supporter.analyze_trade_offs(project, decision)
        console.print(f"\n--- Análise da Decisão: '{decision}' ---\n{analysis}\n" + "-"*50)
    except Exception as e:
        console.print(f"[bold red]Falha na análise de decisão: {e}[/bold red]")
    finally:
        db.close()


@app.command(help="🗺️  Mapeia os stakeholders de um projeto.")
def map_stakeholders(project_slug: str = typer.Argument(..., help="Slug do projeto")) -> None:
    project_root = Path(__file__).resolve().parents[1]
    load_env_vars(project_root)
    cfg = load_config(project_root)
    db = get_db_session(cfg["database_url"])
    try:
        from agents.stakeholder_graph_bot import StakeholderGraphBot
        import models
    except ModuleNotFoundError as e:
        console.print(f"[bold red]Erro: módulo não encontrado: {e}[/bold red]")
        return

    project = db.query(models.Project).filter_by(slug=project_slug).first()
    if not project:
        console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado.")
        db.close()
        return

    try:
        mapper = StakeholderGraphBot(api_key=cfg["gemini_key"])
        stakeholders = mapper.map_stakeholders(project)
        if stakeholders:
            table = Table(
                title=f"Stakeholders: {project.name}",
                show_header=True,
                header_style="bold green",
            )
            table.add_column("Stakeholder", style="dim", width=25)
            table.add_column("Influência")
            table.add_column("Interesse")
            table.add_column("Estratégia", width=50)
            for sh in stakeholders:
                table.add_row(sh["stakeholder"], sh["influence"], sh["interest"], sh["engagement"])
            console.print(table)
    finally:
        db.close()


@app.command(help="🎨 Gera um kit de identidade de marca para um projeto.")
def generate_brand(project_slug: str = typer.Argument(..., help="Slug do projeto")) -> None:
    project_root = Path(__file__).resolve().parents[1]
    load_env_vars(project_root)
    cfg = load_config(project_root)
    db = get_db_session(cfg["database_url"])
    try:
        from agents.brand_kit_bot import BrandKitBot
        import models
    except ModuleNotFoundError as e:
        console.print(f"[bold red]Erro: módulo não encontrado: {e}[/bold red]")
        return

    project = db.query(models.Project).filter_by(slug=project_slug).first()
    if not project:
        console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado.")
        db.close()
        return

    try:
        brander = BrandKitBot(api_key=cfg["gemini_key"])
        kit = brander.generate_kit(project)
        if kit:
            slogan = kit.get("slogan", "N/A")
            mission = kit.get("mission_statement", "N/A")
            palette = kit.get("color_palette", [])
            colors_str = "\n".join(f"[{c.split()[0]}]███[/] {c}" for c in palette)
            panel = Panel(
                f"[bold]Slogan:[/bold] {slogan}\n\n"
                f"[bold]Missão:[/bold] {mission}\n\n"
                f"[bold]Paleta de Cores:[/bold]\n{colors_str}",
                title=f"Kit de Marca: {project.name}",
                border_style="yellow",
            )
            console.print(panel)
    finally:
        db.close()


# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------
@app.command(name="dashboard")
def dashboard() -> None:
    typer.echo("📊 Abrindo dashboard (Streamlit)...")
    subprocess.run(["streamlit", "run", "src/dashboard.py"], check=False)


# ---------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    app()
