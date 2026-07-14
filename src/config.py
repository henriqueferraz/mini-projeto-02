"""Configuração de caminhos e helpers de ambiente do agente.

Define diretórios do repositório usados pelas ferramentas de I/O e,
futuramente, o factory do modelo de chat (Fase 4).
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR: Path = Path(__file__).resolve().parent.parent
"""Raiz do repositório (pai de ``src/``)."""

MOCKS_DIR: Path = ROOT_DIR / "data" / "mocks"
"""Diretório raiz dos dados mockados (única origem permitida para leitura)."""

OUTPUT_DIR: Path = ROOT_DIR / "output"
"""Diretório onde os relatórios gerados (MD + JSON) são gravados."""

OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
"""Modelo padrão da OpenAI quando ``OPENAI_API_KEY`` estiver configurada."""


def get_chat_model():
    """Retorna o chat model da OpenAI ou ``None`` se não houver chave.

    Na Fase 2 apenas o contrato existe; a análise LLM entra na Fase 4.
    Sem ``OPENAI_API_KEY``, o agente usará o fallback heurístico.

    Returns:
        Instância de chat model compatível com LangChain, ou ``None``.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=OPENAI_MODEL, api_key=api_key, temperature=0)
