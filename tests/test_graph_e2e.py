"""Testes de ponta a ponta do fluxo LangGraph completo (Fase 4)."""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

from graph import build_graph, run_agent

_analyze_mod = importlib.import_module("nodes.analyze_data")

FONTES = [
    "DEPLOY-001",
    "DEPLOY-002",
    "DEPLOY-003",
    "DEPLOY-004",
    "INCIDENTE-001",
    "INCIDENTE-002",
    "INCIDENTE-003",
    "SPRINT-001",
    "SPRINT-002",
    "SPRINT-003",
]


def _forcar_heuristica(monkeypatch) -> None:
    """Garante modo heurístico independentemente do ``.env`` local."""
    monkeypatch.setattr(_analyze_mod, "get_chat_model", lambda: None)


def test_fluxo_sucesso_gera_relatorio(monkeypatch, output_dir: Path) -> None:
    """Executa o grafo completo em modo heurístico e grava saída."""
    _forcar_heuristica(monkeypatch)
    estado = run_agent("DEPLOY-001")
    assert estado["validation_errors"] == []
    assert estado["analysis"]["modo"] == "heuristic"
    assert estado["tool_result"]["status"] == "ok"
    assert estado["final_report"]["status"] == "ok"
    arquivos = estado["final_report"]["arquivos"]
    assert Path(arquivos["markdown"]).exists()
    assert Path(arquivos["json"]).exists()
    assert Path(arquivos["markdown"]).parent == output_dir.resolve()


def test_fluxo_interrompe_em_validacao(monkeypatch) -> None:
    """Encerra cedo quando a entrada é inválida."""
    _forcar_heuristica(monkeypatch)
    estado = run_agent("INVALIDO")
    assert estado["validation_errors"]
    assert not estado.get("analysis")


def test_fluxo_interrompe_fonte_inexistente(monkeypatch) -> None:
    """Encerra após load quando o mock não existe."""
    _forcar_heuristica(monkeypatch)
    estado = run_agent("DEPLOY-999")
    assert estado["source_id"] == "DEPLOY-999"
    assert estado["validation_errors"]
    assert not estado.get("analysis")


def test_build_graph_compila() -> None:
    """Garante que o StateGraph compila sem erro."""
    assert build_graph() is not None


@pytest.mark.parametrize("fonte_id", FONTES)
def test_fluxo_heuristico_todas_fontes(fonte_id: str, monkeypatch) -> None:
    """Cobre as 10 fontes mockadas em modo heurístico."""
    _forcar_heuristica(monkeypatch)
    estado = run_agent(fonte_id)
    assert estado["validation_errors"] == []
    assert estado["source_id"] == fonte_id
    assert estado["analysis"]["modo"] == "heuristic"
    assert estado["final_report"]["status"] == "ok"
    assert (
        estado["final_report"]["relatorio"]["metadados"]["analysis_modo"]
        == "heuristic"
    )
