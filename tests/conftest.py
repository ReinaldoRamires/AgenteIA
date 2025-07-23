# tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base

@pytest.fixture(scope="function")
def test_db_session():
    """
    Cria um banco de dados SQLite em memória para um único teste.
    """
    # Usa um banco de dados em memória
    engine = create_engine("sqlite:///:memory:")

    # Cria todas as nossas tabelas no banco de dados em memória
    Base.metadata.create_all(engine)

    # Cria uma sessão para interagir com o banco de dados
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        # Disponibiliza a sessão para o teste
        yield session
    finally:
        # Fecha a sessão e limpa tudo depois que o teste termina
        session.close()
        Base.metadata.drop_all(engine)