# Apresentação — Agente Gerador de Relatórios Técnicos

Até 2 slides (critério 4 / seção 5.1 do enunciado).

---

## Slide 1 — Problema, processo e agente

### Problema

Dados técnicos (logs de deploy, métricas, incidentes, notas de sprint) ficam espalhados em arquivos. Produzir um relatório claro, estruturado e acionável demora e fica inconsistente.

### Processo automatizado

1. Receber o ID/tipo da fonte (ex.: `DEPLOY-001`, `INCIDENTE-002`).
2. Validar a entrada.
3. Ler mocks da fonte + métricas.
4. Analisar com LLM (ou fallback heurístico).
5. Consultar template/regras via ferramenta real.
6. Gerar e gravar o relatório técnico em `output/`.

### Proposta do agente

**Agente Gerador de Relatórios Técnicos** — orquestra o fluxo com **LangGraph**, mantém estado/contexto entre os nós, usa ferramenta de I/O real sobre arquivos mockados e entrega um relatório útil (não um prompt isolado).

---

## Slide 2 — Entrada, saída, ferramenta e fluxo

### Entrada

- ID da fonte **ou** path em `data/mocks/fontes/` (ex.: `DEPLOY-003`).
- Tipo opcional: `deploy` | `incidente` | `sprint` (inferido pelo prefixo se omitido).

### Saída

Relatório em `output/` (Markdown + JSON): sumário, contexto, análise, riscos, recomendações e metadados.

### Ferramenta

`read_mock_file` / `write_report` — leem e gravam de verdade no disco (mocks em `data/mocks/`; saída em `output/`).

### Fluxo LangGraph (10 fontes mockadas)

```text
validate_input → load_context → analyze_data → use_tool → generate_report
```

Fontes: `DEPLOY-001`…`004`, `INCIDENTE-001`…`003`, `SPRINT-001`…`003` (+ métricas e template).
