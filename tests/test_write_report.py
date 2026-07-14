"""Testes da ferramenta ``write_report`` (gravação real em ``output/``)."""

from __future__ import annotations

import json
from pathlib import Path

from tools.write_report import write_report


def test_grava_markdown_e_json(output_dir: Path) -> None:
    """Grava MD + JSON e confere conteúdo no disco."""
    relatorio = {
        "metadados": {
            "fonte": "TESTE-WRITE-001",
            "tipo": "deploy",
            "analysis_modo": "heuristic",
            "template_versao": "1.0.0",
        },
        "sumario_executivo": "Sumário de teste da Fase 2.",
        "recomendacoes": ["Validar leitura/escrita sem LLM."],
    }

    caminhos = write_report(relatorio, nome_base="TESTE-WRITE-001")

    path_md = Path(caminhos["markdown"])
    path_json = Path(caminhos["json"])

    assert path_md.exists()
    assert path_json.exists()
    assert path_md.parent == output_dir.resolve()
    assert path_json.parent == output_dir.resolve()

    assert "Sumário de teste" in path_md.read_text(encoding="utf-8")

    carregado = json.loads(path_json.read_text(encoding="utf-8"))
    assert carregado["metadados"]["fonte"] == "TESTE-WRITE-001"

    # limpeza dos artefatos de teste
    path_md.unlink(missing_ok=True)
    path_json.unlink(missing_ok=True)


def test_write_report_rejeita_vazio() -> None:
    """Rejeita relatório inválido."""
    import pytest

    with pytest.raises(ValueError):
        write_report({})
