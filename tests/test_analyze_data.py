"""Testes do nó ``analyze_data`` (heurística sem chave de API)."""

from __future__ import annotations

import importlib

from nodes.analyze_data import _analise_heuristica, analyze_data
from tools.read_mock_file import read_mock_file

_analyze_mod = importlib.import_module("nodes.analyze_data")


def test_analyze_heuristic_sem_api_key(monkeypatch) -> None:
    """Sem modelo configurado, usa modo heurístico."""
    monkeypatch.setattr(_analyze_mod, "get_chat_model", lambda: None)
    raw = read_mock_file("fontes/DEPLOY-001.json")
    metrics = read_mock_file("metricas/indicadores.json")
    out = analyze_data(
        {
            "source_id": "DEPLOY-001",
            "report_type": "deploy",
            "raw_source": raw,
            "metrics": metrics,
        }
    )
    assert out["analysis"]["modo"] == "heuristic"
    assert out["analysis"]["sumario"]
    assert out["analysis"]["fatos"]
    assert out["analysis"]["recomendacoes"]


def test_analyze_fallback_em_falha_llm(monkeypatch) -> None:
    """Falha de API cai no fallback heurístico."""

    class _Boom:
        def invoke(self, *_args, **_kwargs):
            raise RuntimeError("API indisponível")

    monkeypatch.setattr(_analyze_mod, "get_chat_model", lambda: _Boom())
    raw = read_mock_file("fontes/INCIDENTE-001.json")
    metrics = read_mock_file("metricas/indicadores.json")
    out = analyze_data(
        {
            "source_id": "INCIDENTE-001",
            "report_type": "incidente",
            "raw_source": raw,
            "metrics": metrics,
        }
    )
    assert out["analysis"]["modo"] == "heuristic"
    assert "fallback_motivo" in out["analysis"]


def test_analise_heuristica_sprint() -> None:
    """Heurística cobre fontes de sprint."""
    raw = read_mock_file("fontes/SPRINT-002.json")
    metrics = read_mock_file("metricas/indicadores.json")
    analysis = _analise_heuristica("SPRINT-002", "sprint", raw, metrics)
    assert analysis["modo"] == "heuristic"
    assert analysis["recomendacoes"]
