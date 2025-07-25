# src/main.py
import os
from pathlib import Path
import yaml
import typer
from dotenv import load_dotenv
load_dotenv()
from rich.console import Console

from agents.agent_router import AgentRouter

console = Console()
app = typer.Typer(help="🚀 PMO 360° - CLI")


# ---------------------------------------------------------------------
# Helpers para configuração
# ---------------------------------------------------------------------
def load_env_vars(project_root: Path):
    """
    Carrega o arquivo .env da raiz do projeto.
    """
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        console.print("[yellow]Aviso: .env não encontrado na raiz do projeto.[/yellow]")


def load_config(project_root: Path) -> dict:
    """
    Lê o config.yaml e substitui chaves por variáveis de ambiente se existirem.
    """
    cfg_path = project_root / "config" / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Sobrescreve com env, se disponíveis
    cfg["openai_key"] = os.getenv("OPENAI_API_KEY", cfg.get("openai_key"))
    cfg["gemini_key"] = os.getenv("GEMINI_API_KEY", cfg.get("gemini_key"))
    cfg["notion_token"] = os.getenv("NOTION_TOKEN", cfg.get("notion_token"))

    # Avisos amigáveis
    if not cfg.get("openai_key"):
        console.print("[yellow]Aviso: OPENAI_API_KEY não definida.[/yellow]")
    if not cfg.get("gemini_key"):
        console.print("[yellow]Aviso: GEMINI_API_KEY não definida.[/yellow]")
    if not cfg.get("notion_token"):
        console.print("[yellow]Aviso: NOTION_TOKEN não definido.[/yellow]")

    return cfg


def load_model_mapping(cfg: dict, project_root: Path) -> dict:
    mapping_path = project_root / cfg["model_mapping_file"]
    with open(mapping_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["model_mapping"]


def load_rules(cfg: dict, project_root: Path) -> dict:
    rules_path = project_root / cfg["rules_file"]
    with open(rules_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------
# Comandos CLI
# ---------------------------------------------------------------------
@app.command(name="new_project")
def new_project(
    name: str,
    project_type: str = typer.Option("default", help="Tipo de projeto"),
    country: str = typer.Option("Brasil", help="País"),
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

    router.run_workflow("NEW_PROJECT_CREATED", project_data)
    typer.echo(f"Workflow finalizado! Projeto: {name}")


@app.command(name="dashboard")
def dashboard():
    import subprocess
    typer.echo("📊 Abrindo dashboard (Streamlit)...")
    subprocess.run(["streamlit", "run", "src/dashboard.py"], check=False)


if __name__ == "__main__":
    app()
