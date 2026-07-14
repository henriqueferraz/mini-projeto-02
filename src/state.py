"""Estado compartilhado do agente LangGraph.

Centraliza entrada, contexto carregado, análise, resultado de ferramenta
e memória conversacional (``messages`` com reducer ``add_messages``).
"""

from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """Estado do grafo de geração de relatórios técnicos.

    Attributes:
        source_id: ID canônico da fonte (ex.: ``DEPLOY-003``).
        report_type: Tipo do relatório (`deploy` / `incidente` / `sprint`).
        raw_source: Conteúdo JSON do mock da fonte.
        metrics: Indicadores de apoio carregados de ``metricas/``.
        validation_errors: Falhas de validação, carga, template ou saída.
        analysis: Resultado da análise (LLM ou heurística).
        tool_result: Resultado da consulta ao template/regras.
        final_report: Relatório consolidado e paths dos arquivos gerados.
        messages: Memória acumulada do fluxo (reducer ``add_messages``).
    """

    source_id: str
    report_type: str
    raw_source: dict[str, Any]
    metrics: dict[str, Any]
    validation_errors: list[str]
    analysis: dict[str, Any]
    tool_result: dict[str, Any]
    final_report: dict[str, Any]
    messages: Annotated[list, add_messages]
