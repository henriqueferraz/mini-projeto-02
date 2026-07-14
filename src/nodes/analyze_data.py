"""Nó de análise dos dados da fonte (LLM com fallback heurístico)."""

from __future__ import annotations

import json
import re
from typing import Any

from config import get_chat_model
from prompts.system import SYSTEM_PROMPT_ANALYSIS
from state import AgentState


def _kpi_do_servico(raw_source: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    """Obtém KPIs do serviço associado à fonte, se existir.

    Args:
        raw_source: Conteúdo do mock da fonte.
        metrics: Indicadores carregados.

    Returns:
        Dicionário de KPIs do serviço ou vazio.
    """
    servico = raw_source.get("servico")
    if not isinstance(servico, str):
        return {}
    return dict((metrics.get("servicos") or {}).get(servico) or {})


def _analise_heuristica(
    source_id: str,
    report_type: str,
    raw_source: dict[str, Any],
    metrics: dict[str, Any],
    *,
    motivo_fallback: str | None = None,
) -> dict[str, Any]:
    """Monta análise determinística a partir dos campos do mock.

    Args:
        source_id: ID canônico da fonte.
        report_type: Tipo do relatório.
        raw_source: Dados brutos da fonte.
        metrics: Indicadores de apoio.
        motivo_fallback: Motivo do fallback (sem chave / falha de API).

    Returns:
        Dicionário ``analysis`` com ``modo=heuristic``.
    """
    fatos: list[str] = []
    riscos: list[str] = []
    recomendacoes: list[str] = []

    resumo = str(raw_source.get("resumo") or "").strip()
    titulo = str(raw_source.get("titulo") or source_id)
    impacto = str(raw_source.get("impacto") or "").strip()

    if resumo:
        fatos.append(resumo)

    for evento in raw_source.get("eventos") or []:
        if isinstance(evento, dict):
            msg = evento.get("msg") or evento.get("evento")
            nivel = evento.get("nivel", "")
            if msg:
                prefixo = f"[{nivel}] " if nivel else ""
                fatos.append(f"{prefixo}{msg}")

    for item in raw_source.get("timeline") or []:
        if isinstance(item, dict) and item.get("evento"):
            fatos.append(str(item["evento"]))

    for destaque in raw_source.get("destaques") or []:
        fatos.append(f"Destaque: {destaque}")

    for risco in raw_source.get("riscos") or []:
        riscos.append(str(risco))

    if impacto:
        riscos.append(f"Impacto registrado: {impacto}")

    status = str(raw_source.get("status") or "").lower()
    if status in {"parcial", "rollback", "em_investigacao"}:
        riscos.append(f"Status atual indica atenção: {status}.")

    for acao in raw_source.get("acoes_tomadas") or []:
        recomendacoes.append(str(acao))
    for acao in raw_source.get("acoes_corretivas") or []:
        recomendacoes.append(str(acao))
    for passo in raw_source.get("proximos_passos") or []:
        recomendacoes.append(str(passo))
    for impedimento in raw_source.get("impedimentos") or []:
        riscos.append(f"Impedimento: {impedimento}")

    kpi = _kpi_do_servico(raw_source, metrics)
    limites = metrics.get("limites_alerta") or {}
    if kpi:
        lat = kpi.get("latencia_p95_ms")
        err = kpi.get("taxa_erro_pct")
        disp = kpi.get("disponibilidade_pct")
        if lat is not None and lat > limites.get("latencia_p95_ms", 10**9):
            riscos.append(
                f"Latência p95 do serviço acima do limite "
                f"({lat} ms > {limites.get('latencia_p95_ms')} ms)."
            )
        if err is not None and err > limites.get("taxa_erro_pct", 10**9):
            riscos.append(
                f"Taxa de erro acima do limite "
                f"({err}% > {limites.get('taxa_erro_pct')}%)."
            )
        if disp is not None and disp < limites.get(
            "disponibilidade_min_pct", 0
        ):
            riscos.append(
                f"Disponibilidade abaixo do mínimo "
                f"({disp}% < {limites.get('disponibilidade_min_pct')}%)."
            )
        fatos.append(f"KPIs de apoio do serviço: {kpi}")

    if not fatos:
        fatos.append("Poucos fatos estruturados no mock; revisar a fonte.")
    if not riscos:
        riscos.append("Nenhum risco explícito no mock; monitorar indicadores.")
    if not recomendacoes:
        recomendacoes.append(
            "Revisar a fonte com o time responsável e registrar próximos passos."
        )

    observacoes_metricas = (
        f"KPIs: {kpi}" if kpi else "Sem KPI específico do serviço na janela."
    )

    analysis: dict[str, Any] = {
        "modo": "heuristic",
        "fonte": source_id,
        "tipo": report_type,
        "sumario": (
            f"{titulo}. {resumo}" if resumo else f"Análise heurística de {titulo}."
        ),
        "fatos": fatos[:12],
        "analise_tecnica": (
            f"Análise heurística ({report_type}) com base no mock {source_id}. "
            f"{observacoes_metricas} "
            f"Causa raiz declarada: {raw_source.get('causa_raiz') or 'não informada'}."
        ),
        "riscos": riscos[:10],
        "impactos": impacto or "Impacto não detalhado no mock.",
        "recomendacoes": recomendacoes[:10],
    }
    if motivo_fallback:
        analysis["fallback_motivo"] = motivo_fallback
    return analysis


def _extrair_json(texto: str) -> dict[str, Any]:
    """Extrai o primeiro objeto JSON de uma resposta de LLM.

    Args:
        texto: Conteúdo textual retornado pelo modelo.

    Returns:
        Dicionário parseado.

    Raises:
        ValueError: Se não houver JSON objeto válido.
    """
    bruto = texto.strip()
    if bruto.startswith("```"):
        bruto = re.sub(r"^```(?:json)?\s*", "", bruto)
        bruto = re.sub(r"\s*```$", "", bruto)

    try:
        dados = json.loads(bruto)
        if isinstance(dados, dict):
            return dados
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", bruto, flags=re.DOTALL)
    if not match:
        raise ValueError("Resposta do LLM não contém JSON objeto.")
    dados = json.loads(match.group(0))
    if not isinstance(dados, dict):
        raise ValueError("JSON do LLM não é um objeto.")
    return dados


def _analise_llm(
    source_id: str,
    report_type: str,
    raw_source: dict[str, Any],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    """Executa análise via chat model e normaliza o resultado.

    Args:
        source_id: ID canônico da fonte.
        report_type: Tipo do relatório.
        raw_source: Dados brutos da fonte.
        metrics: Indicadores de apoio.

    Returns:
        Dicionário ``analysis`` com ``modo=llm``.

    Raises:
        RuntimeError: Se o modelo não estiver disponível.
        ValueError: Se a resposta for inválida.
        Exception: Propagada de falhas de API para o chamador tratar.
    """
    model = get_chat_model()
    if model is None:
        raise RuntimeError("OPENAI_API_KEY ausente.")

    from langchain_core.messages import HumanMessage, SystemMessage

    payload = {
        "source_id": source_id,
        "report_type": report_type,
        "raw_source": raw_source,
        "metrics_servico": _kpi_do_servico(raw_source, metrics),
        "limites_alerta": metrics.get("limites_alerta"),
    }
    resposta = model.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT_ANALYSIS),
            HumanMessage(
                content=(
                    "Analise os dados a seguir e responda apenas com JSON:\n"
                    + json.dumps(payload, ensure_ascii=False)
                )
            ),
        ]
    )
    conteudo = getattr(resposta, "content", str(resposta))
    if isinstance(conteudo, list):
        conteudo = "".join(
            parte.get("text", "") if isinstance(parte, dict) else str(parte)
            for parte in conteudo
        )

    dados = _extrair_json(str(conteudo))
    return {
        "modo": "llm",
        "fonte": source_id,
        "tipo": report_type,
        "sumario": str(dados.get("sumario") or "").strip(),
        "fatos": list(dados.get("fatos") or []),
        "analise_tecnica": str(dados.get("analise_tecnica") or "").strip(),
        "riscos": list(dados.get("riscos") or []),
        "impactos": str(dados.get("impactos") or "").strip(),
        "recomendacoes": list(dados.get("recomendacoes") or []),
    }


def analyze_data(state: AgentState) -> dict[str, Any]:
    """Analisa a fonte com LLM ou fallback heurístico.

    Com ``OPENAI_API_KEY`` tenta ``modo=llm``. Sem chave ou em falha de API,
    usa ``modo=heuristic`` sem interromper o fluxo.

    Args:
        state: Estado com ``raw_source`` e ``metrics`` carregados.

    Returns:
        Atualização com ``analysis`` e mensagem de memória.
    """
    source_id = str(state.get("source_id") or "")
    report_type = str(state.get("report_type") or "")
    raw_source = dict(state.get("raw_source") or {})
    metrics = dict(state.get("metrics") or {})

    model = get_chat_model()
    if model is None:
        analysis = _analise_heuristica(
            source_id,
            report_type,
            raw_source,
            metrics,
            motivo_fallback="OPENAI_API_KEY ausente",
        )
    else:
        try:
            analysis = _analise_llm(source_id, report_type, raw_source, metrics)
        except Exception as exc:  # noqa: BLE001 — fallback intencional
            analysis = _analise_heuristica(
                source_id,
                report_type,
                raw_source,
                metrics,
                motivo_fallback=f"falha LLM: {exc}",
            )

    return {
        "analysis": analysis,
        "messages": [
            {
                "role": "assistant",
                "content": (
                    f"Análise concluída em modo={analysis.get('modo')} "
                    f"para {source_id}."
                ),
            }
        ],
    }
