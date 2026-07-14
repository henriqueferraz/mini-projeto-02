"""Testes de integração leve das ferramentas sem LLM."""

from __future__ import annotations

from pathlib import Path

from tools.read_mock_file import read_mock_file
from tools.write_report import write_report


def test_pipeline_leitura_escrita_sem_llm(output_dir: Path) -> None:
    """Lê fonte + template e grava um relatório mínimo em disco."""
    fonte = read_mock_file("fontes/DEPLOY-003.json")
    template = read_mock_file("templates/relatorio_tecnico.json")
    metricas = read_mock_file("metricas/indicadores.json")

    secoes = {s["id"]: f"Conteúdo gerado para {s['titulo']}." for s in template["secoes_obrigatorias"]}
    relatorio = {
        **secoes,
        "metadados": {
            "fonte": fonte["id"],
            "tipo": fonte["tipo"],
            "analysis_modo": "heuristic",
            "template_versao": template["versao"],
            "servico_fonte": fonte.get("servico"),
            "metricas_servico": metricas["servicos"].get(fonte.get("servico", ""), {}),
        },
    }

    caminhos = write_report(
        relatorio,
        nome_base=fonte["id"],
        markdown=(
            f"# Relatório técnico — {fonte['id']}\n\n"
            f"{fonte['resumo']}\n"
        ),
    )

    path_md = Path(caminhos["markdown"])
    path_json = Path(caminhos["json"])
    assert path_md.exists()
    assert path_json.exists()
    assert fonte["id"] in path_md.read_text(encoding="utf-8")
