"""Testes do nó ``validate_input``."""

from __future__ import annotations

from nodes.validate_input import validate_input


def test_valida_id_canonico() -> None:
    """Aceita ID no formato PREFIXO-NNN e infere o tipo."""
    out = validate_input({"source_id": "DEPLOY-001", "report_type": ""})
    assert out["validation_errors"] == []
    assert out["source_id"] == "DEPLOY-001"
    assert out["report_type"] == "deploy"


def test_valida_path_relativo() -> None:
    """Aceita path relativo para o mock da fonte."""
    out = validate_input(
        {"source_id": "fontes/INCIDENTE-002.json", "report_type": ""}
    )
    assert out["validation_errors"] == []
    assert out["source_id"] == "INCIDENTE-002"
    assert out["report_type"] == "incidente"


def test_rejeita_id_invalido() -> None:
    """Rejeita ID fora do padrão."""
    out = validate_input({"source_id": "FOO-1", "report_type": ""})
    assert out["validation_errors"]
    assert "inválido" in out["validation_errors"][0].lower()


def test_rejeita_tipo_incompativel() -> None:
    """Rejeita tipo explícito diferente do prefixo."""
    out = validate_input(
        {"source_id": "SPRINT-001", "report_type": "deploy"}
    )
    assert out["validation_errors"]
    assert "incompatível" in out["validation_errors"][0]


def test_rejeita_path_absoluto() -> None:
    """Bloqueia path absoluto na fonte."""
    out = validate_input({"source_id": "/tmp/DEPLOY-001.json", "report_type": ""})
    assert out["validation_errors"]
    assert "absoluto" in out["validation_errors"][0].lower()


def test_aceita_tipo_compativel() -> None:
    """Aceita tipo explícito alinhado ao ID."""
    out = validate_input(
        {"source_id": "SPRINT-003", "report_type": "sprint"}
    )
    assert out["validation_errors"] == []
    assert out["report_type"] == "sprint"
