"""Nó de validação da entrada do agente (ID/tipo da fonte)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from state import AgentState

TIPOS_VALIDOS = frozenset({"deploy", "incidente", "sprint"})
PREFIXO_PARA_TIPO = {
    "DEPLOY": "deploy",
    "INCIDENTE": "incidente",
    "SPRINT": "sprint",
}
_PADRAO_ID = re.compile(r"^(DEPLOY|INCIDENTE|SPRINT)-(\d{3})$", re.IGNORECASE)


def _extrair_id_canonico(fonte: str) -> tuple[str | None, list[str]]:
    """Extrai o ID canônico a partir de ID puro ou path relativo.

    Args:
        fonte: Valor informado na CLI (ex.: ``DEPLOY-001`` ou
            ``fontes/DEPLOY-001.json``).

    Returns:
        Tupla ``(source_id, erros)``. ``source_id`` é ``None`` se inválido.
    """
    erros: list[str] = []
    bruto = (fonte or "").strip().replace("\\", "/")

    if not bruto:
        return None, ["Fonte não informada."]

    if bruto.startswith("/") or Path(bruto).is_absolute():
        return None, [
            "Path absoluto não é permitido na fonte. "
            "Use um ID (DEPLOY-001) ou path relativo (fontes/DEPLOY-001.json)."
        ]

    if ".." in Path(bruto).parts:
        return None, ["Path com '..' não é permitido na fonte."]

    nome = Path(bruto).name
    if nome.lower().endswith(".json"):
        nome = nome[:-5]

    match = _PADRAO_ID.fullmatch(nome)
    if not match:
        return None, [
            f"ID de fonte inválido: {fonte!r}. "
            "Use o formato PREFIXO-NNN (ex.: DEPLOY-001, INCIDENTE-002, SPRINT-003)."
        ]

    prefixo = match.group(1).upper()
    numero = match.group(2)
    return f"{prefixo}-{numero}", erros


def validate_input(state: AgentState) -> dict[str, Any]:
    """Valida e normaliza ID/tipo da fonte no estado.

    Aceita ID canônico ou path relativo apontando para o mock em
    ``data/mocks/fontes/``. Infere o tipo pelo prefixo quando omitido.

    Args:
        state: Estado atual (espera ``source_id`` bruto e opcionalmente
            ``report_type``).

    Returns:
        Atualização parcial do estado com ``source_id`` canônico,
        ``report_type``, ``validation_errors`` e mensagem de memória.
    """
    erros: list[str] = []
    fonte_bruta = str(state.get("source_id") or "").strip()
    tipo_informado = str(state.get("report_type") or "").strip().lower()

    source_id, erros_id = _extrair_id_canonico(fonte_bruta)
    erros.extend(erros_id)

    report_type = ""
    if source_id:
        prefixo = source_id.split("-", 1)[0]
        tipo_inferido = PREFIXO_PARA_TIPO[prefixo]

        if tipo_informado:
            if tipo_informado not in TIPOS_VALIDOS:
                erros.append(
                    f"Tipo inválido: {tipo_informado!r}. "
                    f"Use um de: {', '.join(sorted(TIPOS_VALIDOS))}."
                )
            elif tipo_informado != tipo_inferido:
                erros.append(
                    f"Tipo {tipo_informado!r} incompatível com o ID {source_id} "
                    f"(esperado: {tipo_inferido})."
                )
            else:
                report_type = tipo_informado
        else:
            report_type = tipo_inferido

    if erros:
        conteudo = "Validação falhou: " + "; ".join(erros)
    else:
        conteudo = (
            f"Entrada validada: fonte={source_id}, tipo={report_type}."
        )

    atualizacao: dict[str, Any] = {
        "validation_errors": erros,
        "messages": [{"role": "system", "content": conteudo}],
    }
    if source_id:
        atualizacao["source_id"] = source_id
    if report_type:
        atualizacao["report_type"] = report_type

    return atualizacao
