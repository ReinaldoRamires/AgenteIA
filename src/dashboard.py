# src/dashboard.py

import json

import pandas as pd
import plotly.express as px
import streamlit as st
import yaml
from sqlalchemy import create_engine

# --- Configuração da Página ---
st.set_page_config(page_title="PMO 360° Dashboard", page_icon="📊", layout="wide")


# --- Funções de Carregamento de Dados ---
@st.cache_data(ttl=30)
def load_data_from_db():
    """Conecta no DB e carrega todas as tabelas relevantes como DataFrames."""
    try:
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        db_url = config.get("database_url")
        if not db_url:
            st.error("URL do banco de dados não encontrada.")
            return [pd.DataFrame()] * 3

        engine = create_engine(db_url)
        projects_df = pd.read_sql_table("projects", engine)
        tasks_df = pd.read_sql_table("tasks", engine)

        # Tenta carregar a tabela de cache de mercado, se existir
        if (
            "cache_market"
            in pd.read_sql(
                "SELECT name FROM sqlite_master WHERE type='table';", engine
            )["name"].tolist()
        ):
            market_cache_df = pd.read_sql_table("cache_market", engine)
        else:
            market_cache_df = pd.DataFrame()

        return projects_df, tasks_df, market_cache_df

    except Exception as e:
        st.error(f"Erro ao carregar dados do banco de dados: {e}")
        return [pd.DataFrame()] * 3


# --- Carregamento dos Dados ---
projects, tasks, market_cache = load_data_from_db()

# --- Barra Lateral (Sidebar) com Filtros ---
st.sidebar.title("Productivity Engine 360°")
st.sidebar.header("Filtros")

project_types = ["Todos"] + sorted(projects["project_type"].unique().tolist())
selected_type = st.sidebar.selectbox("Filtrar por Tipo de Projeto:", project_types)

if selected_type != "Todos":
    projects_filtered = projects[projects["project_type"] == selected_type].copy()
else:
    projects_filtered = projects.copy()

# --- Título Principal ---
st.title("📊 Dashboard Executivo de Projetos")
st.markdown("Visão geral do portfólio de projetos gerenciado pelo Productivity Engine.")

if projects_filtered.empty:
    st.warning("Nenhum projeto encontrado para os filtros selecionados.")
else:
    # --- Abas para Organização ---
    tab1, tab2 = st.tabs(["Visão Geral", "Detalhes por Projeto"])

    with tab1:
        st.subheader("Métricas Gerais do Portfólio")
        col1, col2, col3 = st.columns(3)
        col1.metric("Projetos Exibidos", len(projects_filtered))
        status_counts = projects_filtered["status"].value_counts()
        col2.metric("Em Planejamento", status_counts.get("PLANNING", 0))
        col3.metric(
            "Total de Tarefas",
            tasks[tasks["project_id"].isin(projects_filtered["id"])].shape[0],
        )

        st.markdown("---")

        st.subheader("Distribuição do Portfólio")
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            if not tasks.empty:
                tasks_per_project = (
                    tasks[tasks["project_id"].isin(projects_filtered["id"])]
                    .groupby("project_id")
                    .size()
                    .reset_index(name="task_count")
                )
                tasks_per_project = tasks_per_project.merge(
                    projects_filtered[["id", "name"]],
                    left_on="project_id",
                    right_on="id",
                )
                fig_bar = px.bar(
                    tasks_per_project,
                    x="name",
                    y="task_count",
                    title="Tarefas por Projeto",
                    labels={"name": "Projeto", "task_count": "Qtd. Tarefas"},
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        with col_chart2:
            status_counts_df = projects_filtered["status"].value_counts().reset_index()
            status_counts_df.columns = ["status", "count"]
            fig_pie = px.pie(
                status_counts_df,
                names="status",
                values="count",
                title="Projetos por Status",
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with st.expander("Ver Tabela de Projetos Completa"):
            st.dataframe(
                projects_filtered[
                    ["name", "slug", "project_type", "country", "status"]
                ],
                use_container_width=True,
            )

    with tab2:
        st.subheader("Análise Detalhada por Projeto")
        selected_project_name = st.selectbox(
            "Selecione um projeto para ver os detalhes:", projects_filtered["name"]
        )

        if selected_project_name:
            project_details = projects_filtered[
                projects_filtered["name"] == selected_project_name
            ].iloc[0]

            # Exibe tarefas do projeto selecionado
            st.write(f"#### Tarefas do Projeto: {project_details['name']}")
            project_tasks = tasks[tasks["project_id"] == project_details["id"]]
            if not project_tasks.empty:
                st.dataframe(
                    project_tasks[["template", "dor", "dod", "estimate"]],
                    use_container_width=True,
                )
            else:
                st.info("Nenhuma tarefa encontrada para este projeto.")

            # Exibe análise de mercado do projeto selecionado (se houver)
            st.write("#### Análise de Mercado (Cache)")

            # Procura no cache uma análise para o tipo e país do projeto
            project_market_analysis = market_cache[
                (market_cache["sector"] == project_details["project_type"])
                & (market_cache["country"] == project_details["country"])
            ]

            if not project_market_analysis.empty:
                # Pega a análise mais recente
                latest_analysis_data = json.loads(
                    project_market_analysis.iloc[-1]["data"]
                )
                st.json(latest_analysis_data)
            else:
                st.info(
                    f"Nenhuma análise de mercado encontrada em cache para o tipo '{project_details['project_type']}' e país '{project_details['country']}'."
                )
