"""Nó que carrega fonte e métricas mockadas no estado do agente."""

from __future__ import annotations

from typing import Any

from state import AgentState
from tools.read_mock_file import read_mock_file


def load_context(state: AgentState) -> dict[str, Any]:
    """Lê a fonte e os indicadores, montando contexto/memória.

    Usa a ferramenta real ``read_mock_file`` para I/O em disco.

    Args:
        state: Estado com ``source_id`` já validado.

    Returns:
        Atualização com ``raw_source``, ``metrics``, possíveis
        ``validation_errors`` e mensagem de memória.
    """
    erros = list(state.get("validation_errors") or [])
    source_id = str(state.get("source_id") or "").strip()

    if not source_id:
        erros.append("source_id ausente para carregar o contexto.")
        return {
            "validation_errors": erros,
            "messages": [
                {
                    "role": "system",
                    "content": "Falha em load_context: source_id ausente.",
                }
            ],
        }

    caminho_fonte = f"fontes/{source_id}.json"

    try:
        raw_source = read_mock_file(caminho_fonte)
        metrics = read_mock_file("metricas/indicadores.json")
    except (FileNotFoundError, ValueError) as exc:
        erros.append(str(exc))
        return {
            "validation_errors": erros,
            "messages": [
                {
                    "role": "system",
                    "content": f"Falha ao carregar contexto: {exc}",
                }
            ],
        }

    servico = raw_source.get("servico")
    trecho_metricas = ""
    if isinstance(servico, str):
        kpi = (metrics.get("servicos") or {}).get(servico)
        if kpi is not None:
            trecho_metricas = f" KPIs de {servico} disponíveis."

    return {
        "raw_source": raw_source,
        "metrics": metrics,
        "validation_errors": erros,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"Contexto carregado: {caminho_fonte} "
                    f"({raw_source.get('titulo', source_id)})."
                    f"{trecho_metricas}"
                ),
            }
        ],
    }
