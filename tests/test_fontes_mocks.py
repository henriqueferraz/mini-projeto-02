"""Cobertura das 10 fontes mockadas em ``data/mocks/fontes/``."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.read_mock_file import read_mock_file

FONTES_ESPERADAS = [
    ("DEPLOY-001", "deploy"),
    ("DEPLOY-002", "deploy"),
    ("DEPLOY-003", "deploy"),
    ("DEPLOY-004", "deploy"),
    ("INCIDENTE-001", "incidente"),
    ("INCIDENTE-002", "incidente"),
    ("INCIDENTE-003", "incidente"),
    ("SPRINT-001", "sprint"),
    ("SPRINT-002", "sprint"),
    ("SPRINT-003", "sprint"),
]


@pytest.mark.parametrize(("fonte_id", "tipo"), FONTES_ESPERADAS)
def test_fonte_mock_existe_e_e_coerente(fonte_id: str, tipo: str) -> None:
    """Cada fonte mockada existe, tem ID/tipo coerentes e campos básicos."""
    dados = read_mock_file(f"fontes/{fonte_id}.json")
    assert dados["id"] == fonte_id
    assert dados["tipo"] == tipo
    assert isinstance(dados.get("titulo"), str) and dados["titulo"]
    assert isinstance(dados.get("resumo"), str) and dados["resumo"]
    assert isinstance(dados.get("tags"), list)


def test_todas_as_fontes_estao_versionadas(mocks_dir: Path) -> None:
    """Garante exatamente as 10 fontes documentadas no plano."""
    arquivos = sorted(p.stem for p in (mocks_dir / "fontes").glob("*.json"))
    esperados = [fid for fid, _ in FONTES_ESPERADAS]
    assert arquivos == esperados
