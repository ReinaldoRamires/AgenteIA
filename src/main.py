# src/main.py
import os
from pathlib import Path

import typer
import yaml
from dotenv import load_dotenv
from rich.console import Console

from agents.agent_router import AgentRouter

# ---------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------
load_dotenv()
console = Console()
app = typer.Typer(help="🚀 PMO 360° - CLI")

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def load_env_vars(project_root: Path) -> None:
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        console.print("[yellow].env não encontrado na raiz do projeto.[/yellow]")


def load_config(project_root: Path) -> dict:
    cfg_path = project_root / "config" / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    cfg["openai_key"] = os.getenv("OPENAI_API_KEY", cfg.get("openai_key"))
    cfg["gemini_key"] = os.getenv("GEMINI_API_KEY", cfg.get("gemini_key"))
    cfg["notion_token"] = os.getenv("NOTION_TOKEN", cfg.get("notion_token"))
    return cfg


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------
@app.command(name="new_project")
def new_project(
    name: str,
    project_type: str = typer.Option("default"),
    country: str = typer.Option("Brasil"),
) -> None:
    root = Path(__file__).resolve().parents[1]
    load_env_vars(root)
    cfg = load_config(root)
    model_mapping = load_yaml(root / cfg["model_mapping_file"])
    rules = load_yaml(root / cfg["rules_file"])

    router = AgentRouter(cfg, model_mapping, rules)
    router.run_workflow(
        "NEW_PROJECT_CREATED",
        {
            "name": name,
            "project_type": project_type,
            "country": country,
            "team_capacity": cfg.get("team_capacity", []),
        },
    )
    console.print(f"✅ Workflow concluído para projeto '{name}'")


@app.command(name="dashboard")
def dashboard() -> None:
    import subprocess

    console.print("📊 Abrindo dashboard Streamlit…")
    subprocess.run(["streamlit", "run", "src/dashboard.py"], check=False)


if __name__ == "__main__":
    app()
