"""Ferramenta de leitura segura de arquivos JSON em ``data/mocks/``.

Garante I/O real no disco e bloqueia paths absolutos ou com ``..``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import MOCKS_DIR


def _resolver_path_seguro(caminho_relativo: str) -> Path:
    """Resolve um path relativo dentro de ``MOCKS_DIR`` com validação.

    Args:
        caminho_relativo: Caminho relativo ao diretório de mocks
            (ex.: ``fontes/DEPLOY-001.json``).

    Returns:
        Path absoluto já validado e contido em ``MOCKS_DIR``.

    Raises:
        ValueError: Se o path for absoluto, vazio, contiver ``..`` ou
            escapar de ``data/mocks/``.
    """
    if not caminho_relativo or not str(caminho_relativo).strip():
        raise ValueError("Caminho do mock não pode ser vazio.")

    bruto = str(caminho_relativo).strip().replace("\\", "/")

    if Path(bruto).is_absolute() or bruto.startswith("/"):
        raise ValueError(
            f"Path absoluto não é permitido: {caminho_relativo!r}. "
            "Use um caminho relativo a data/mocks/."
        )

    partes = Path(bruto).parts
    if ".." in partes:
        raise ValueError(
            f"Path com '..' não é permitido: {caminho_relativo!r}."
        )

    candidato = (MOCKS_DIR / bruto).resolve()
    mocks_raiz = MOCKS_DIR.resolve()

    try:
        candidato.relative_to(mocks_raiz)
    except ValueError as exc:
        raise ValueError(
            f"Path fora de data/mocks/: {caminho_relativo!r}."
        ) from exc

    return candidato


def read_mock_file(caminho_relativo: str) -> dict[str, Any]:
    """Lê e interpreta um arquivo JSON mockado em disco.

    Args:
        caminho_relativo: Path relativo a ``data/mocks/``
            (ex.: ``fontes/DEPLOY-001.json``,
            ``metricas/indicadores.json``).

    Returns:
        Dicionário com o conteúdo JSON do arquivo.

    Raises:
        ValueError: Se o path for inválido/inseguro ou o JSON for inválido.
        FileNotFoundError: Se o arquivo não existir dentro de ``data/mocks/``.
    """
    caminho = _resolver_path_seguro(caminho_relativo)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Mock não encontrado: {caminho_relativo!r} "
            f"(resolvido para {caminho})."
        )

    if not caminho.is_file():
        raise ValueError(
            f"O caminho não é um arquivo: {caminho_relativo!r}."
        )

    try:
        with caminho.open(encoding="utf-8") as handle:
            dados = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"JSON inválido em {caminho_relativo!r}: {exc}."
        ) from exc

    if not isinstance(dados, dict):
        raise ValueError(
            f"O mock {caminho_relativo!r} deve ser um objeto JSON (dict)."
        )

    return dados
