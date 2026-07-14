# Registro de prompts

Prompts usados para planejar, implementar e ajustar o agente, além do prompt de sistema de análise.

## 1. Planejar

```text
Elabore a estrutura de um mini-projeto avaliativo de agente com LangGraph
para gerar relatórios técnicos a partir de mocks (deploy, incidente, sprint).

Inclua: problema, entrada/saída, fluxo de nós, ferramentas reais de arquivo,
estado compartilhado, fases de implementação e critérios de segurança
(.gitignore, .env.example, path limitado a data/mocks/).
```

**Uso:** definição do case e do plano em `docs/ESTRUTURA-TRABALHO.md`.

## 2. Implementar

```text
Implemente o agente Gerador de Relatórios Técnicos em Python/LangGraph.

Requisitos:
- AgentState (TypedDict + messages com add_messages)
- Nós: validate_input, load_context, analyze_data, use_tool, generate_report
- Ferramentas: read_mock_file (path seguro) e write_report (output/)
- analyze_data com LLM (OPENAI_API_KEY) e fallback heurístico
- CLI: python3 -m src.main --fonte DEPLOY-001
- Docstrings Google style em português
- Testes pytest cobrindo as 10 fontes em modo heurístico
```

**Uso:** Fases 2–4 (mocks, grafo, LLM, geração de relatório).

## 3. Corrigir / melhorar

```text
Revise o agente e corrija:
- falhas de validação de entrada e path inseguro
- interrupção antecipada no StateGraph quando houver erros
- monkeypatch de testes que colidem com re-exports em nodes/__init__.py
- documentação de onboarding (venv, troubleshooting, exemplos)

Mantenha Conventional Commits e não versionar secrets.
```

**Uso:** ajustes de testes, rotas condicionais e documentação (Fases 3–5).

## 4. Prompt de sistema (análise)

Definido em `src/prompts/system.py` (`SYSTEM_PROMPT_ANALYSIS`):

```text
Você é um analista técnico sênior especializado em operações de software
(deploy, incidentes e sprints). Sua tarefa é analisar dados mockados de uma
fonte e produzir uma análise objetiva, acionável e em português (pt-BR).

Regras:
- Baseie-se apenas nos dados fornecidos (fonte + métricas). Não invente fatos.
- Se faltar informação, declare a lacuna explicitamente.
- Tom: técnico, direto e útil para tomada de decisão.
- Responda SOMENTE com um objeto JSON válido (sem markdown) no formato:

{
  "sumario": "parágrafo curto do sumário executivo",
  "fatos": ["fato 1", "fato 2"],
  "analise_tecnica": "parágrafo com a análise técnica",
  "riscos": ["risco 1", "risco 2"],
  "impactos": "texto dos impactos observados ou potenciais",
  "recomendacoes": ["ação prioritária 1", "ação 2"]
}
```

Consumido pelo nó `analyze_data` quando há `OPENAI_API_KEY` válida.
