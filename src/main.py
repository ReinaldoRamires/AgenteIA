"""
Aplicação de linha de comando do AgenteIA.

Esta versão atualiza a inicialização e o uso dos agentes para respeitar as
assinaturas definidas na camada `agents` e no `LLMRouter`.  Os comandos
principais incluem a criação de um novo projeto (com cronograma e
integração stub ao Notion), análise de decisões, mapeamento de
stakeholders e geração de identidade de marca.

Use a opção `--dry-run` nos comandos para inspecionar prompts sem
executar chamadas a modelos ou ao Notion.
"""

import os
import re
import subprocess

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import typer
import yaml

from agents.brand_kit_bot import BrandKitBot
from agents.decision_supporter import DecisionSupporter
from agents.notion_writer import NotionWriter
from agents.schedule_copilot import ScheduleCopilot
from agents.stakeholder_graph_bot import StakeholderGraphBot

import models  # noqa: F401  (mantido para compatibilidade)

# ---------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------
load_dotenv()  # carrega variáveis de ambiente apenas uma vez
console = Console()
app = typer.Typer(help="Productivity Engine – PMO Digital 360°")

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def get_config() -> dict:
    """
    Lê config/config.yaml e, se existirem variáveis de ambiente
    correspondentes, sobrescreve as chaves sensíveis.
    """
    try:
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError:
        console.print("[bold red]Erro:[/bold red] 'config.yaml' não encontrado.")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Erro ao ler config:[/bold red] {e}")
        raise typer.Exit(1)

    # --- Override por .env ---
    env_map = {
        "api_keys.openai": "OPENAI_API_KEY",
        "api_keys.google_gemini": "GEMINI_API_KEY",
        "api_keys.notion": "NOTION_TOKEN",
    }
    for dotted_key, env_var in env_map.items():
        env_val = os.getenv(env_var)
        if env_val:
            ref = cfg
            *parents, leaf = dotted_key.split(".")
            for key in parents:
                ref = ref.setdefault(key, {})
            ref[leaf] = env_val

    return cfg


def get_db_session(db_url: str):
    engine = create_engine(db_url)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()

# ---------------------------------------------------------------------
# Comandos dos Agentes
# ---------------------------------------------------------------------

@app.command(
    help="✨ Cria um novo projeto e seu cronograma de tarefas no DB e Notion."
)
def new_project(
    name: str,
    project_type: str = typer.Option("default", help="Tipo de projeto"),
    country: str = typer.Option("Brasil", help="País"),
    dry_run: bool = typer.Option(False, help="Não chamar APIs (simulação)"),
) -> None:
    console.print(f"✨ Iniciando criação do projeto: [bold green]{name}[/bold green]")
    config = get_config()
    model_mapping = config.get("model_mapping", {})
    db_session = get_db_session(config.get("database_url"))
    slug = re.sub(r"[^\w-]", "", name.lower().replace(" ", "-"))
    project_data = {
        "slug": slug,
        "name": name,
        "project_type": project_type,
        "country": country,
    }
    try:
        writer = NotionWriter(config=config, model_mapping=model_mapping)
        scheduler = ScheduleCopilot(config=config, model_mapping=model_mapping)
        notion_page_id = ""
        if not dry_run:
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

        tasks = scheduler.generate_schedule(project_data, dry_run=dry_run)
        for task_item in tasks:
            if not dry_run:
                writer.create_task_page(task_item, project_relation_id=notion_page_id)
            db_task = models.Task(
                project_id=db_project.id,
                template=task_item["name"],
                dor=task_item["dor"],
                dod=task_item["dod"],
                estimate=task_item.get("estimate", 0),
            )
            db_session.add(db_task)

        db_session.commit()
        console.print(
            f"✅ Projeto '{name}' e tarefas sincronizados com sucesso! "
            f"Slug: [bold cyan]{slug}[/bold cyan]"
        )
    except Exception as e:
        console.print(f"[bold red]Falha na criação do projeto: {e}[/bold red]")
        db_session.rollback()
    finally:
        db_session.close()


@app.command(help="Analisa prós, contras e riscos de uma decisão estratégica.")
def support_decision(
    project_slug: str = typer.Argument(..., help="O 'slug' do projeto."),
    decision: str = typer.Argument(..., help="A decisão a ser analisada."),
    dry_run: bool = typer.Option(False, help="Não chamar modelos (simulação)"),
) -> None:
    config = get_config()
    model_mapping = config.get("model_mapping", {})
    db_session = get_db_session(config.get("database_url"))
    try:
        project = (
            db_session.query(models.Project).filter_by(slug=project_slug).first()
        )
        if not project:
            console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado.")
            return
        # monta o dicionário do projeto para o agente
        project_data = {
            "slug": project.slug,
            "name": project.name,
            "project_type": project.project_type,
            "country": project.country,
        }
        supporter = DecisionSupporter(config=config, model_mapping=model_mapping)
        analysis = supporter.analyze_trade_offs(
            project_data=project_data, decision=decision, dry_run=dry_run
        )
        console.print(
            f"\n--- Análise da Decisão: '{decision}' ---\n{analysis}\n" + "-" * 50
        )
    except Exception as e:
        console.print(f"[bold red]Falha na análise de decisão: {e}[/bold red]")
    finally:
        db_session.close()


@app.command(help="️️ Mapeia os stakeholders de um projeto.")
def map_stakeholders(
    project_slug: str = typer.Argument(..., help="O 'slug' do projeto."),
    dry_run: bool = typer.Option(False, help="Não chamar modelos (simulação)"),
) -> None:
    config = get_config()
    model_mapping = config.get("model_mapping", {})
    db_session = get_db_session(config.get("database_url"))
    try:
        project = (
            db_session.query(models.Project).filter_by(slug=project_slug).first()
        )
        if not project:
            console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado.")
            return
        project_data = {
            "slug": project.slug,
            "name": project.name,
            "project_type": project.project_type,
            "country": project.country,
        }
        mapper = StakeholderGraphBot(config=config, model_mapping=model_mapping)
        stakeholders = mapper.map_stakeholders(project_data, dry_run=dry_run)
        if dry_run:
            return
        table = Table(
            title=f"Stakeholders: {project.name}", show_header=True, header_style="bold green"
        )
        table.add_column("Stakeholder", style="dim", width=25)
        table.add_column("Influência")
        table.add_column("Interesse")
        table.add_column("Estratégia", width=50)
        for sh in stakeholders:
            table.add_row(sh["stakeholder"], sh["influence"], sh["interest"], sh["engagement"])
        console.print(table)
    finally:
        db_session.close()


@app.command(help=" Gera um kit de identidade de marca para um projeto.")
def generate_brand(
    project_slug: str = typer.Argument(..., help="O 'slug' do projeto."),
    dry_run: bool = typer.Option(False, help="Não chamar modelos (simulação)"),
) -> None:
    config = get_config()
    model_mapping = config.get("model_mapping", {})
    db_session = get_db_session(config.get("database_url"))
    try:
        project = (
            db_session.query(models.Project).filter_by(slug=project_slug).first()
        )
        if not project:
            console.print(f"[bold red]Erro:[/bold red] Projeto '{project_slug}' não encontrado.")
            return
        project_data = {
            "slug": project.slug,
            "name": project.name,
            "project_type": project.project_type,
            "country": project.country,
        }
        brander = BrandKitBot(config=config, model_mapping=model_mapping)
        kit = brander.generate_kit(project_data, dry_run=dry_run)
        if dry_run:
            return
        slogan = kit.get("slogan", "N/A")
        mission = kit.get("mission_statement", "N/A")
        palette = kit.get("color_palette", [])
        colors_str = "\n".join(
            f"[{c.split()[0]}]███[/] {c}" if isinstance(c, str) else str(c) for c in palette
        )
        panel = Panel(
            f"[bold]Slogan:[/bold] {slogan}\n\n"
            f"[bold]Missão:[/bold] {mission}\n\n"
            f"[bold]Paleta de Cores:[/bold]\n{colors_str}",
            title=f"Kit de Marca: {project.name}",
            border_style="yellow",
        )
        console.print(panel)
    finally:
        db_session.close()


@app.command(help=" Inicia o dashboard visual de projetos.")
def dashboard() -> None:
    console.print(" Lançando o dashboard de projetos...")
    subprocess.run(["streamlit", "run", "src/dashboard.py"], check=False)


@app.command(help="⚙️  Cria o arquivo de banco de dados e as tabelas.")
def init_db() -> None:
    console.print("⚙️  Inicializando o banco de dados...")
    config = get_config()
    db_url = config.get("database_url")
    engine = create_engine(db_url)
    models.create_db_and_tables(engine)
    console.print("✅ Banco de dados inicializado com sucesso!")


# ---------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    app()
