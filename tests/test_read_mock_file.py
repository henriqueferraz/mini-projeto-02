"""Testes da ferramenta ``read_mock_file`` (leitura segura de mocks)."""

from __future__ import annotations

import pytest

from tools.read_mock_file import read_mock_file


def test_le_fonte_deploy_001() -> None:
    """Lê DEPLOY-001.json e retorna o ID esperado."""
    dados = read_mock_file("fontes/DEPLOY-001.json")
    assert dados["id"] == "DEPLOY-001"
    assert dados["tipo"] == "deploy"
    assert dados["servico"] == "api-pagamentos"


def test_le_metricas_indicadores() -> None:
    """Lê indicadores e valida serviços e limites de alerta."""
    dados = read_mock_file("metricas/indicadores.json")
    assert "servicos" in dados
    assert "api-pagamentos" in dados["servicos"]
    assert dados["limites_alerta"]["disponibilidade_min_pct"] == 99.5


def test_le_template_relatorio() -> None:
    """Lê o template e valida seções obrigatórias."""
    dados = read_mock_file("templates/relatorio_tecnico.json")
    ids = {s["id"] for s in dados["secoes_obrigatorias"]}
    assert "sumario_executivo" in ids
    assert "recomendacoes" in ids
    assert dados["versao"] == "1.0.0"


def test_rejeita_path_absoluto() -> None:
    """Bloqueia path absoluto fora da política de segurança."""
    with pytest.raises(ValueError, match="absoluto"):
        read_mock_file("/etc/passwd")


def test_rejeita_path_com_parent() -> None:
    """Bloqueia escape via ``..``."""
    with pytest.raises(ValueError, match=r"\.\."):
        read_mock_file("../README.md")


def test_rejeita_path_vazio() -> None:
    """Bloqueia caminho vazio."""
    with pytest.raises(ValueError, match="vazio"):
        read_mock_file("   ")


def test_arquivo_inexistente() -> None:
    """Sinaliza mock inexistente com FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_mock_file("fontes/NAO-EXISTE-999.json")
