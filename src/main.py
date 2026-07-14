"""CLI do Agente Gerador de Relatórios Técnicos.

Uso (com ``.venv`` ativo, a partir da raiz do repositório)::

    python3 -m src.main --fonte DEPLOY-001
    python3 -m src.main --fonte fontes/INCIDENTE-002.json --tipo incidente
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _garantir_path_src() -> None:
    """Garante que ``src/`` está no ``sys.path`` para imports flat."""
    src_dir = Path(__file__).resolve().parent
    src_str = str(src_dir)
    if src_str not in sys.path:
        sys.path.insert(0, src_str)


_garantir_path_src()

from graph import run_agent  # noqa: E402


def _montar_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da CLI.

    Returns:
        Parser configurado com ``--fonte`` e ``--tipo``.
    """
    parser = argparse.ArgumentParser(
        prog="python3 -m src.main",
        description=(
            "Agente Gerador de Relatórios Técnicos (LangGraph). "
            "Fase 3: validação + carga de contexto; análise/relatório em stubs."
        ),
    )
    parser.add_argument(
        "--fonte",
        required=True,
        help="ID da fonte (DEPLOY-001) ou path relativo (fontes/DEPLOY-001.json).",
    )
    parser.add_argument(
        "--tipo",
        choices=["deploy", "incidente", "sprint"],
        default=None,
        help="Tipo do relatório (opcional; inferido pelo prefixo do ID).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprime o estado final em JSON (útil para debug).",
    )
    return parser


def _resumo_estado(estado: dict[str, Any]) -> str:
    """Monta um resumo legível do estado final.

    Args:
        estado: Estado retornado por ``run_agent``.

    Returns:
        Texto formatado para stdout.
    """
    erros = estado.get("validation_errors") or []
    linhas = [
        f"fonte: {estado.get('source_id', '-')}",
        f"tipo: {estado.get('report_type', '-')}",
    ]

    if erros:
        linhas.append("status: ERRO")
        linhas.append("erros:")
        for err in erros:
            linhas.append(f"  - {err}")
        return "\n".join(linhas)

    raw = estado.get("raw_source") or {}
    analysis = estado.get("analysis") or {}
    tool = estado.get("tool_result") or {}
    final = estado.get("final_report") or {}

    linhas.extend(
        [
            "status: OK",
            f"titulo: {raw.get('titulo', '-')}",
            f"analysis.modo: {analysis.get('modo', '-')}",
            f"tool_result.status: {tool.get('status', '-')}",
            f"final_report.status: {final.get('status', '-')}",
            f"mensagens: {len(estado.get('messages') or [])}",
        ]
    )
    return "\n".join(linhas)


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada da CLI.

    Args:
        argv: Lista de argumentos (usa ``sys.argv`` se omitido).

    Returns:
        Código de saída (0 sucesso, 1 erro de validação/carga).
    """
    parser = _montar_parser()
    args = parser.parse_args(argv)

    estado = run_agent(fonte=args.fonte, tipo=args.tipo)

    if args.json:
        serializavel = {
            k: v
            for k, v in estado.items()
            if k != "messages"
        }
        serializavel["messages_count"] = len(estado.get("messages") or [])
        print(json.dumps(serializavel, ensure_ascii=False, indent=2, default=str))
    else:
        print(_resumo_estado(estado))

    erros = estado.get("validation_errors") or []
    return 1 if erros else 0


if __name__ == "__main__":
    raise SystemExit(main())
