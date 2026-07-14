"""Testes do nó ``load_context``."""

from __future__ import annotations

from nodes.load_context import load_context


def test_carrega_fonte_e_metricas() -> None:
    """Carrega mock da fonte e indicadores no estado."""
    out = load_context(
        {
            "source_id": "DEPLOY-001",
            "report_type": "deploy",
            "validation_errors": [],
        }
    )
    assert out["validation_errors"] == []
    assert out["raw_source"]["id"] == "DEPLOY-001"
    assert "servicos" in out["metrics"]
    assert "api-pagamentos" in out["metrics"]["servicos"]


def test_falha_fonte_inexistente() -> None:
    """Registra erro quando o mock da fonte não existe."""
    out = load_context(
        {
            "source_id": "DEPLOY-999",
            "report_type": "deploy",
            "validation_errors": [],
        }
    )
    assert out["validation_errors"]
    assert "raw_source" not in out


def test_falha_sem_source_id() -> None:
    """Exige ``source_id`` para carregar contexto."""
    out = load_context({"validation_errors": []})
    assert out["validation_errors"]
    assert "source_id" in out["validation_errors"][0]
