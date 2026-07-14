"""Testes do nó ``generate_report``."""

from __future__ import annotations

from pathlib import Path

from nodes.generate_report import generate_report
from nodes.use_tool import use_tool
from tools.read_mock_file import read_mock_file


def _estado_minimo(fonte: str = "DEPLOY-001") -> dict:
    """Monta estado mínimo para geração de relatório."""
    raw = read_mock_file(f"fontes/{fonte}.json")
    tool = use_tool({"validation_errors": []})
    return {
        "source_id": fonte,
        "report_type": raw["tipo"],
        "raw_source": raw,
        "analysis": {
            "modo": "heuristic",
            "sumario": "Sumário de teste.",
            "fatos": ["Fato A", "Fato B"],
            "analise_tecnica": "Análise de teste.",
            "riscos": ["Risco A"],
            "impactos": "Impacto de teste.",
            "recomendacoes": ["Ação 1"],
        },
        "tool_result": tool["tool_result"],
        "validation_errors": [],
    }


def test_generate_report_grava_arquivos(output_dir: Path) -> None:
    """Valida seções e grava MD + JSON em output/."""
    out = generate_report(_estado_minimo("DEPLOY-003"))
    assert out.get("validation_errors") in ([], None) or out["validation_errors"] == []
    final = out["final_report"]
    assert final["status"] == "ok"
    path_md = Path(final["arquivos"]["markdown"])
    path_json = Path(final["arquivos"]["json"])
    assert path_md.exists()
    assert path_json.exists()
    assert path_md.parent == output_dir.resolve()
    assert "DEPLOY-003" in path_md.read_text(encoding="utf-8")


def test_generate_report_rejeita_secao_vazia() -> None:
    """Falha se seção obrigatória estiver vazia."""
    estado = _estado_minimo()
    estado["analysis"]["sumario"] = ""
    out = generate_report(estado)
    assert out["validation_errors"]
    assert out["final_report"]["status"] == "error"
    assert any("sumario_executivo" in e for e in out["validation_errors"])
