"""Montagem do StateGraph LangGraph do agente de relatórios."""

from __future__ import annotations

from typing import Any, Literal

from langgraph.graph import END, START, StateGraph

from nodes.analyze_data import analyze_data
from nodes.generate_report import generate_report
from nodes.load_context import load_context
from nodes.use_tool import use_tool
from nodes.validate_input import validate_input
from state import AgentState


def _tem_erros(state: AgentState) -> bool:
    """Indica se o estado possui erros de validação/carga.

    Args:
        state: Estado atual do agente.

    Returns:
        ``True`` se houver pelo menos um erro.
    """
    erros = state.get("validation_errors") or []
    return bool(erros)


def _rota_apos_validate(
    state: AgentState,
) -> Literal["load_context", "__end__"]:
    """Decide se segue para carga de contexto ou encerra.

    Args:
        state: Estado após ``validate_input``.

    Returns:
        Nome do próximo nó ou ``__end__``.
    """
    return "__end__" if _tem_erros(state) else "load_context"


def _rota_apos_load(
    state: AgentState,
) -> Literal["analyze_data", "__end__"]:
    """Decide se segue para análise ou encerra.

    Args:
        state: Estado após ``load_context``.

    Returns:
        Nome do próximo nó ou ``__end__``.
    """
    return "__end__" if _tem_erros(state) else "analyze_data"


def _rota_apos_use_tool(
    state: AgentState,
) -> Literal["generate_report", "__end__"]:
    """Decide se gera relatório ou encerra após a ferramenta.

    Args:
        state: Estado após ``use_tool``.

    Returns:
        Nome do próximo nó ou ``__end__``.
    """
    resultado = state.get("tool_result") or {}
    if resultado.get("status") == "ok":
        return "generate_report"
    return "__end__"


def build_graph():
    """Constrói e compila o grafo do agente.

    Fluxo completo: validação → contexto → análise (LLM/heurística) →
    template → geração do relatório.

    Returns:
        Grafo compilado pronto para ``invoke`` / ``stream``.
    """
    graph = StateGraph(AgentState)

    graph.add_node("validate_input", validate_input)
    graph.add_node("load_context", load_context)
    graph.add_node("analyze_data", analyze_data)
    graph.add_node("use_tool", use_tool)
    graph.add_node("generate_report", generate_report)

    graph.add_edge(START, "validate_input")
    graph.add_conditional_edges(
        "validate_input",
        _rota_apos_validate,
        {
            "load_context": "load_context",
            "__end__": END,
        },
    )
    graph.add_conditional_edges(
        "load_context",
        _rota_apos_load,
        {
            "analyze_data": "analyze_data",
            "__end__": END,
        },
    )
    graph.add_edge("analyze_data", "use_tool")
    graph.add_conditional_edges(
        "use_tool",
        _rota_apos_use_tool,
        {
            "generate_report": "generate_report",
            "__end__": END,
        },
    )
    graph.add_edge("generate_report", END)

    return graph.compile()


def run_agent(
    fonte: str,
    tipo: str | None = None,
) -> dict[str, Any]:
    """Executa o grafo a partir da fonte informada.

    Args:
        fonte: ID da fonte ou path relativo do mock.
        tipo: Tipo opcional do relatório.

    Returns:
        Estado final retornado pelo grafo.
    """
    app = build_graph()
    estado_inicial: AgentState = {
        "source_id": fonte,
        "report_type": (tipo or "").strip().lower(),
        "validation_errors": [],
        "messages": [
            {
                "role": "user",
                "content": f"Gerar relatório técnico para fonte={fonte!r}.",
            }
        ],
    }
    return app.invoke(estado_inicial)
