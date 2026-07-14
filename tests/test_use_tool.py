"""Testes do nó ``use_tool``."""

from __future__ import annotations

import importlib

from nodes.use_tool import use_tool

_use_tool_mod = importlib.import_module("nodes.use_tool")


def test_use_tool_le_template() -> None:
    """Carrega o template e expõe IDs das seções obrigatórias."""
    out = use_tool({"validation_errors": []})
    assert out["tool_result"]["status"] == "ok"
    assert out["tool_result"]["template_versao"] == "1.0.0"
    ids = out["tool_result"]["secoes_obrigatorias_ids"]
    assert "sumario_executivo" in ids
    assert "recomendacoes" in ids
    assert "metadados" in ids


def test_use_tool_falha_path(monkeypatch) -> None:
    """Registra erro quando a leitura do template falha."""

    def _boom(_path: str):
        raise FileNotFoundError("mock ausente")

    monkeypatch.setattr(_use_tool_mod, "read_mock_file", _boom)
    out = use_tool({"validation_errors": []})
    assert out["tool_result"]["status"] == "error"
    assert out["validation_errors"]
