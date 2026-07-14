"""Testes de ponta a ponta do esqueleto LangGraph (Fase 3)."""

from __future__ import annotations

from graph import build_graph, run_agent


def test_fluxo_sucesso_com_stubs() -> None:
    """Executa o grafo completo até o stub de relatório."""
    estado = run_agent("DEPLOY-001")
    assert estado["validation_errors"] == []
    assert estado["source_id"] == "DEPLOY-001"
    assert estado["raw_source"]["id"] == "DEPLOY-001"
    assert estado["analysis"]["modo"] == "stub"
    assert estado["tool_result"]["status"] == "ok"
    assert estado["final_report"]["status"] == "pending_fase_4"
    assert len(estado["messages"]) >= 3


def test_fluxo_interrompe_em_validacao() -> None:
    """Encerra cedo quando a entrada é inválida."""
    estado = run_agent("INVALIDO")
    assert estado["validation_errors"]
    assert "raw_source" not in estado or not estado.get("raw_source")
    assert not estado.get("analysis")


def test_fluxo_interrompe_fonte_inexistente() -> None:
    """Encerra após validate quando o mock não existe."""
    estado = run_agent("DEPLOY-999")
    assert estado["source_id"] == "DEPLOY-999"
    assert estado["validation_errors"]
    assert not estado.get("analysis")


def test_build_graph_compila() -> None:
    """Garante que o StateGraph compila sem erro."""
    app = build_graph()
    assert app is not None
