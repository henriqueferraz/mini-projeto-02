"""Nó final: consolida, valida seções e grava o relatório em ``output/``."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from state import AgentState
from tools.write_report import write_report


def _texto_secao(valor: Any) -> str:
    """Converte valor de análise em texto não vazio para uma seção.

    Args:
        valor: String, lista ou outro valor.

    Returns:
        Texto pronto para a seção (pode ser string vazia se incompleto).
    """
    if valor is None:
        return ""
    if isinstance(valor, list):
        itens = [str(item).strip() for item in valor if str(item).strip()]
        if not itens:
            return ""
        return "\n".join(f"- {item}" for item in itens)
    return str(valor).strip()


def _montar_markdown(relatorio: dict[str, Any], titulos: dict[str, str]) -> str:
    """Gera Markdown do relatório com títulos do template.

    Args:
        relatorio: Relatório estruturado.
        titulos: Mapa ``id_secao -> título``.

    Returns:
        Conteúdo Markdown completo.
    """
    fonte = (relatorio.get("metadados") or {}).get("fonte", "relatorio")
    linhas = [f"# Relatório técnico — {fonte}", ""]

    ordem = [
        "sumario_executivo",
        "contexto",
        "analise_tecnica",
        "riscos_impactos",
        "recomendacoes",
        "metadados",
    ]
    for secao_id in ordem:
        titulo = titulos.get(secao_id, secao_id.replace("_", " ").capitalize())
        linhas.append(f"## {titulo}")
        valor = relatorio.get(secao_id)
        if secao_id == "metadados" and isinstance(valor, dict):
            for chave, item in valor.items():
                linhas.append(f"- **{chave}**: {item}")
        else:
            linhas.append(_texto_secao(valor) if not isinstance(valor, str) else valor)
        linhas.append("")

    return "\n".join(linhas).rstrip() + "\n"


def generate_report(state: AgentState) -> dict[str, Any]:
    """Consolida análise + template, valida seções e grava MD/JSON.

    Args:
        state: Estado com ``analysis`` e ``tool_result`` preenchidos.

    Returns:
        ``final_report`` com paths gerados, ou ``validation_errors``
        se seções obrigatórias faltarem / a escrita falhar.
    """
    erros = list(state.get("validation_errors") or [])
    analysis = dict(state.get("analysis") or {})
    tool_result = dict(state.get("tool_result") or {})
    template = dict(tool_result.get("template") or {})
    source_id = str(state.get("source_id") or "relatorio")
    report_type = str(state.get("report_type") or "")

    secoes = template.get("secoes_obrigatorias") or []
    titulos = {
        str(sec.get("id")): str(sec.get("titulo") or sec.get("id"))
        for sec in secoes
        if isinstance(sec, dict) and sec.get("id")
    }
    ids_obrigatorios = list(tool_result.get("secoes_obrigatorias_ids") or titulos.keys())

    contexto_fatos = _texto_secao(analysis.get("fatos"))
    riscos_txt = _texto_secao(analysis.get("riscos"))
    impactos_txt = _texto_secao(analysis.get("impactos"))
    riscos_impactos = "\n".join(
        parte for parte in [riscos_txt, impactos_txt and f"**Impactos:** {impactos_txt}"] if parte
    )

    metadados = {
        "fonte": source_id,
        "data": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tipo": report_type,
        "analysis_modo": analysis.get("modo"),
        "template_versao": tool_result.get("template_versao")
        or template.get("versao"),
    }
    if analysis.get("fallback_motivo"):
        metadados["fallback_motivo"] = analysis["fallback_motivo"]

    relatorio: dict[str, Any] = {
        "sumario_executivo": _texto_secao(analysis.get("sumario")),
        "contexto": contexto_fatos,
        "analise_tecnica": _texto_secao(analysis.get("analise_tecnica")),
        "riscos_impactos": riscos_impactos,
        "recomendacoes": _texto_secao(analysis.get("recomendacoes")),
        "metadados": metadados,
    }

    for secao_id in ids_obrigatorios:
        valor = relatorio.get(secao_id)
        vazio = valor is None or (isinstance(valor, str) and not valor.strip())
        if isinstance(valor, dict) and not valor:
            vazio = True
        if vazio:
            erros.append(f"Seção obrigatória ausente ou vazia: {secao_id}")

    if erros:
        return {
            "validation_errors": erros,
            "final_report": {
                "status": "error",
                "fonte": source_id,
                "erros": erros,
                "arquivos": {},
            },
            "messages": [
                {
                    "role": "system",
                    "content": "generate_report falhou: " + "; ".join(erros),
                }
            ],
        }

    markdown = _montar_markdown(relatorio, titulos)

    try:
        arquivos = write_report(
            relatorio,
            nome_base=source_id,
            markdown=markdown,
        )
    except (OSError, ValueError) as exc:
        mensagem = f"Falha ao gravar relatório: {exc}"
        erros.append(mensagem)
        return {
            "validation_errors": erros,
            "final_report": {
                "status": "error",
                "fonte": source_id,
                "erros": erros,
                "arquivos": {},
            },
            "messages": [{"role": "system", "content": mensagem}],
        }

    final_report = {
        "status": "ok",
        "fonte": source_id,
        "tipo": report_type,
        "relatorio": relatorio,
        "arquivos": arquivos,
    }

    return {
        "final_report": final_report,
        "validation_errors": [],
        "messages": [
            {
                "role": "assistant",
                "content": (
                    f"Relatório gerado para {source_id}: "
                    f"{arquivos.get('markdown')} | {arquivos.get('json')}"
                ),
            }
        ],
    }
