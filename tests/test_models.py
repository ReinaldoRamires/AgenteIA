# tests/test_models.py

from src.models import Project, ProjectStatus

def test_create_project_instance():
    """
    Testa a criação de uma instância do modelo Project em memória.
    """
    project = Project(
        name="Projeto Teste Unitário",
        slug="projeto-teste-unitario",
        project_type="Teste",
        country="Brasil",
        status=ProjectStatus.PLANNING
    )

    assert project.name == "Projeto Teste Unitário"
    assert project.slug == "projeto-teste-unitario"
    assert project.status == ProjectStatus.PLANNING
    assert project.country == "Brasil"