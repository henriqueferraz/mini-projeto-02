"""Stubs dos nós que serão completados na Fase 4."""

from __future__ import annotations

from typing import Any

from state import AgentState


def analyze_data(state: AgentState) -> dict[str, Any]:
    """Stub de análise (LLM/heurística entram na Fase 4).

    Args:
        state: Estado com contexto carregado.

    Returns:
        ``analysis`` placeholder e mensagem de memória.
    """
    fonte = state.get("source_id", "?")
    return {
        "analysis": {
            "modo": "stub",
            "status": "pending_fase_4",
            "fonte": fonte,
        },
        "messages": [
            {
                "role": "assistant",
                "content": (
                    f"analyze_data (stub): contexto de {fonte} recebido; "
                    "análise completa na Fase 4."
                ),
            }
        ],
    }


def use_tool(state: AgentState) -> dict[str, Any]:
    """Stub da consulta ao template (implementação real na Fase 4).

    Args:
        state: Estado atual do agente.

    Returns:
        ``tool_result`` com ``status=ok`` para não interromper o grafo.
    """
    _ = state
    return {
        "tool_result": {
            "status": "ok",
            "modo": "stub",
            "template": None,
        },
        "messages": [
            {
                "role": "assistant",
                "content": (
                    "use_tool (stub): leitura do template "
                    "relatorio_tecnico.json na Fase 4."
                ),
            }
        ],
    }


def generate_report(state: AgentState) -> dict[str, Any]:
    """Stub da geração/gravação do relatório (Fase 4).

    Args:
        state: Estado atual do agente.

    Returns:
        ``final_report`` placeholder indicando pendência da Fase 4.
    """
    return {
        "final_report": {
            "status": "pending_fase_4",
            "fonte": state.get("source_id"),
            "tipo": state.get("report_type"),
            "arquivos": {},
        },
        "messages": [
            {
                "role": "assistant",
                "content": (
                    "generate_report (stub): validação de seções e "
                    "write_report na Fase 4."
                ),
            }
        ],
    }
