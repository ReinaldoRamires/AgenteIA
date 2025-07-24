# tests/test_cli.py

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from src.main import app

runner = CliRunner()


@patch("src.main.NotionWriter")
@patch("src.main.get_db_session")
def test_new_project_command_success(
    mock_get_db_session, mock_notion_writer_class, test_db_session
):
    """
    Testa o comando new-project em total isolamento, usando um DB em memória.
    """
    # Configura o mock do NotionWriter
    mock_writer_instance = MagicMock()
    mock_writer_instance.create_project_page.return_value = "mock-page-id-123"
    mock_notion_writer_class.return_value = mock_writer_instance

    # Configura o mock do Banco de Dados
    mock_get_db_session.return_value = test_db_session

    # Roda o comando CLI
    result = runner.invoke(
        app,
        [
            "new-project",
            "Projeto Teste Isolado",
            "--project-type",
            "Software",
        ],
    )

    # Verifica os resultados
    assert result.exit_code == 0

    # AQUI ESTÁ A CORREÇÃO: Verificações mais robustas
    # 1. Verifica se o nome do projeto está na saída
    assert "Projeto Teste Isolado" in result.stdout
    # 2. Verifica se a parte final da mensagem de sucesso está lá, ignorando quebras de linha
    assert "sincronizados com sucesso!" in result.stdout.replace("\n", " ")

    # Verifica se os mocks foram chamados
    mock_notion_writer_class.assert_called_once()
    mock_get_db_session.assert_called_once()
