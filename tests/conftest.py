"""Fixtures compartilhadas dos testes do agente."""

from __future__ import annotations

from pathlib import Path

import pytest

from config import MOCKS_DIR, OUTPUT_DIR, ROOT_DIR


@pytest.fixture
def mocks_dir() -> Path:
    """Retorna o diretório de mocks do repositório."""
    return MOCKS_DIR


@pytest.fixture
def output_dir() -> Path:
    """Retorna o diretório de saída do repositório."""
    return OUTPUT_DIR


@pytest.fixture
def root_dir() -> Path:
    """Retorna a raiz do repositório."""
    return ROOT_DIR
