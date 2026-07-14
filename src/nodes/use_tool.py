"""Nó que consulta o template/regras mockadas via ferramenta real."""

from __future__ import annotations

from typing import Any

from state import AgentState
from tools.read_mock_file import read_mock_file

TEMPLATE_RELATIVO = "templates/relatorio_tecnico.json"


def use_tool(state: AgentState) -> dict[str, Any]:
    """Lê ``templates/relatorio_tecnico.json`` e registra no estado.

    Args:
        state: Estado atual do agente (contexto já carregado).

    Returns:
        ``tool_result`` com ``status=ok`` ou erro, além de mensagem
        de memória. Em falha, também atualiza ``validation_errors``.
    """
    _ = state
    erros = list(state.get("validation_errors") or [])

    try:
        template = read_mock_file(TEMPLATE_RELATIVO)
    except (FileNotFoundError, ValueError) as exc:
        mensagem = f"Falha ao ler template: {exc}"
        erros.append(mensagem)
        return {
            "validation_errors": erros,
            "tool_result": {
                "status": "error",
                "path": TEMPLATE_RELATIVO,
                "erro": str(exc),
            },
            "messages": [{"role": "system", "content": mensagem}],
        }

    secoes = template.get("secoes_obrigatorias") or []
    secao_ids = [
        str(sec.get("id"))
        for sec in secoes
        if isinstance(sec, dict) and sec.get("id")
    ]

    return {
        "tool_result": {
            "status": "ok",
            "path": TEMPLATE_RELATIVO,
            "template": template,
            "secoes_obrigatorias_ids": secao_ids,
            "template_versao": template.get("versao"),
        },
        "messages": [
            {
                "role": "assistant",
                "content": (
                    f"Template {TEMPLATE_RELATIVO} carregado "
                    f"(versão {template.get('versao')}; "
                    f"{len(secao_ids)} seções obrigatórias)."
                ),
            }
        ],
    }
