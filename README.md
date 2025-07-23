Markdown

# 🚀 Productivity Engine - PMO Digital 360°

Este projeto é um hub de automação local, orquestrado por linha de comando (CLI) e visualizado através de um dashboard web, para gerenciar o ciclo de vida de projetos complexos de forma automatizada.

O sistema utiliza uma arquitetura de agentes especializados para executar tarefas como criação de projetos, geração de cronogramas, análise de mercado com IA, monitoramento de status e backups automáticos.

## ✨ Funcionalidades Principais

- **Criação Automatizada de Projetos**: Crie um novo projeto e seu cronograma de tarefas padrão no Notion e no banco de dados local com um único comando.
- **Análise de Mercado com IA**: Integre-se com a API do Google Gemini para realizar análises de potencial de mercado (TAM/SAM/SOM) para seus projetos.
- **Dashboard Executivo**: Visualize todos os seus projetos e tarefas em uma interface web interativa construída com Streamlit.
- **Automação em Background**: Um agendador executa tarefas de forma autônoma, como verificar atualizações de status no Notion e realizar backups periódicos.
- **Testes Automatizados**: Uma suíte de testes com `pytest` garante a qualidade e a estabilidade do código.

## 🛠️ Pré-requisitos

- Python 3.11+
- Git

## ⚙️ Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd AgenteIA
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔧 Configuração

1.  Abra o arquivo `config/config.yaml` e preencha as chaves de API (`notion`, `google_gemini`) e os IDs dos databases do Notion, conforme as instruções nos comentários do arquivo.

## ⚡ Uso

Todos os comandos são executados a partir da raiz do projeto.

- **Inicializar o Banco de Dados (faça isso uma vez):**
  ```bash
  python -m src.main init-db
Criar um Novo Projeto:

Bash

python -m src.main new-project "Nome do Meu Projeto" --project-type "Software"
Realizar Análise de Mercado com IA:

Bash

python -m src.main analyze-market "slug-do-meu-projeto"
Iniciar o Dashboard Web:

Bash

streamlit run src/dashboard.py
Iniciar o Agendador de Tarefas (em um terminal separado):

Bash

python -m src.scheduler
📂 Estrutura do Projeto
/agents/: Contém a lógica de cada agente especializado.

/config/: Arquivos de configuração.

/src/: Código fonte principal da aplicação.

/tests/: Testes automatizados.

/backups/: Onde os backups automáticos são salvos.

projects.db: O banco de dados SQLite local.