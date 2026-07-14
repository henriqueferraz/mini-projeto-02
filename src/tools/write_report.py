"""Ferramenta de escrita do relatório técnico em ``output/``.

Grava Markdown e JSON de forma real no disco via ``config.OUTPUT_DIR``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from config import OUTPUT_DIR


def _slugify(valor: str) -> str:
    """Normaliza o identificador para nome de arquivo seguro.

    Args:
        valor: Identificador da fonte ou nome solicitado.

    Returns:
        String segura para uso em nome de arquivo.
    """
    limpo = re.sub(r"[^\w.\-]+", "_", valor.strip(), flags=re.UNICODE)
    return limpo or "relatorio"


def write_report(
    relatorio: dict[str, Any],
    *,
    nome_base: str | None = None,
    markdown: str | None = None,
) -> dict[str, str]:
    """Grava o relatório técnico em Markdown e JSON em ``output/``.

    Args:
        relatorio: Estrutura do relatório (será serializada em JSON).
        nome_base: Prefixo do arquivo (ex.: ``DEPLOY-001``). Se omitido,
            usa ``relatorio.get("metadados", {}).get("fonte")`` ou
            ``relatorio``.
        markdown: Texto Markdown opcional. Se omitido, gera um esboço
            a partir das chaves principais do dicionário.

    Returns:
        Dicionário com caminhos absolutos dos arquivos gerados:
        ``{"markdown": "...", "json": "..."}``.

    Raises:
        ValueError: Se ``relatorio`` estiver vazio ou inválido.
        OSError: Se a gravação em disco falhar.
    """
    if not isinstance(relatorio, dict) or not relatorio:
        raise ValueError("O relatório deve ser um dicionário não vazio.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    metadados = relatorio.get("metadados") or {}
    base = nome_base or metadados.get("fonte") or "relatorio"
    slug = _slugify(str(base))

    path_json = OUTPUT_DIR / f"{slug}.json"
    path_md = OUTPUT_DIR / f"{slug}.md"

    conteudo_md = markdown if markdown is not None else _markdown_padrao(relatorio)

    with path_json.open("w", encoding="utf-8") as handle:
        json.dump(relatorio, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    with path_md.open("w", encoding="utf-8") as handle:
        handle.write(conteudo_md)
        if not conteudo_md.endswith("\n"):
            handle.write("\n")

    return {
        "markdown": str(path_md.resolve()),
        "json": str(path_json.resolve()),
    }


def _markdown_padrao(relatorio: dict[str, Any]) -> str:
    """Monta um Markdown simples a partir do dicionário do relatório.

    Args:
        relatorio: Estrutura do relatório.

    Returns:
        Texto Markdown com seções top-level.
    """
    linhas: list[str] = ["# Relatório técnico", ""]
    metadados = relatorio.get("metadados")
    if isinstance(metadados, dict) and metadados:
        linhas.append("## Metadados")
        for chave, valor in metadados.items():
            linhas.append(f"- **{chave}**: {valor}")
        linhas.append("")

    for chave, valor in relatorio.items():
        if chave == "metadados":
            continue
        titulo = str(chave).replace("_", " ").capitalize()
        linhas.append(f"## {titulo}")
        if isinstance(valor, (list, dict)):
            linhas.append("```json")
            linhas.append(json.dumps(valor, ensure_ascii=False, indent=2))
            linhas.append("```")
        else:
            linhas.append(str(valor))
        linhas.append("")

    return "\n".join(linhas).rstrip() + "\n"
