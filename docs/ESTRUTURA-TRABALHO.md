# Estrutura de Trabalho — Mini-Projeto Avaliativo (Módulo 2)

**Prazo:** 20/07/2026  
**Peso:** 30% da nota do módulo  
**Modalidade:** individual (1 aluno)  
**Stack obrigatória:** LangGraph + pelo menos 1 ferramenta real + estado/contexto + documentação  
**Status do sistema:** Fases 0–3 concluídas; Fases 4–6 pendentes

---

## 1. Proposta do agente

### Nome

Agente Gerador de Relatórios Técnicos

### Problema

Dados técnicos (logs de deploy, métricas, incidentes, notas de sprint) ficam espalhados em arquivos. Produzir um relatório claro, estruturado e acionável demora e é inconsistente.

### Processo automatizado

1. Receber o tipo/ID da fonte (ex.: `DEPLOY-001`, `INCIDENTE-002`, `SPRINT-003`).
2. Validar a entrada (`validate_input`).
3. Ler **arquivos mockados** com os dados brutos da fonte + métricas (`load_context` + `read_mock_file`).
4. Montar contexto/memória no estado do agente (`AgentState` + `messages`).
5. Analisar os dados com o LLM **ou** fallback heurístico (`analyze_data`).
6. Consultar **template/regras mockadas** via ferramenta real (`use_tool` + `read_mock_file`).
7. Validar seções e gravar o **relatório técnico final** em `output/` (`generate_report` + `write_report`).

### Entrada

- ID da fonte **ou** caminho para arquivo em `data/mocks/fontes/` (ex.: `fontes/DEPLOY-003.json`).
- Tipo do relatório (opcional): `deploy`, `incidente`, `sprint` (inferido pelo prefixo do ID se omitido).

### Saída

Relatório técnico em `output/` (Markdown + JSON) contendo, no mínimo:

- sumário executivo
- contexto / fatos relevantes
- análise técnica
- riscos e impactos
- recomendações
- metadados (fonte, data, tipo, `analysis_modo`, versão do template)

### Por que é um agente

Tem objetivo claro, estado compartilhado, fluxo em etapas no LangGraph, usa ferramenta e entrega um relatório útil — não é um único prompt isolado.

### Regras permanentes do sistema

- **Regra dos mocks:** arquivos em `data/mocks/` são **dados fictícios**. A ferramenta **lê/escreve de verdade** no disco (não é “ação só simulada”).
- **Regra do ambiente:** executar sempre com o Python do `.venv` (`source .venv/bin/activate` ou `.venv/bin/python`). Sem isso: `ModuleNotFoundError: No module named 'langgraph'`. Guia completo no `README.md`.
- **Regra do LLM:** com `OPENAI_API_KEY` no `.env` → análise `modo=llm`. Sem chave ou falha de API → fallback `modo=heuristic`.
- **Regra de segurança:** `.env` nunca versionado; `.env.example` só com nomes de variáveis; leitura restrita a `data/mocks/` (bloqueia absoluto e `..`).
- **Regra de documentação:** todo Python em `src/` com Docstrings Google style em português (seção 10). Docs Markdown alinhados ao markdownlint do projeto.

---

## 2. Estrutura de pastas do repositório

```text
modelo-projeto/
├── README.md                           # onboarding completo do colaborador
├── .gitignore                          # .env, .venv, output/*.md|json, .cursor/
├── .env.example                        # OPENAI_API_KEY=, OPENAI_MODEL=
├── .markdownlint.json                  # regras do linter Markdown (IDE)
├── .markdownlint-cli2.jsonc            # ignora output/ e enunciado oficial
├── requirements.txt
├── pytest.ini                          # pythonpath + discovery de testes
│
├── data/
│   └── mocks/                          # OBRIGATÓRIO — dados mockados
│       ├── fontes/                     # 10 fontes (ver seção 4)
│       ├── metricas/
│       │   └── indicadores.json        # KPIs de 6 serviços
│       └── templates/
│           └── relatorio_tecnico.json  # seções obrigatórias / regras
│
├── src/
│   ├── __init__.py
│   ├── main.py                         # CLI: python3 -m src.main --fonte ...
│   ├── config.py                       # paths + get_chat_model()
│   ├── state.py                        # AgentState (TypedDict)
│   ├── graph.py                        # StateGraph + rotas condicionais
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── validate_input.py
│   │   ├── load_context.py
│   │   ├── analyze_data.py             # LLM ou heurística offline
│   │   ├── use_tool.py                 # lê template mockado
│   │   └── generate_report.py          # valida seções + grava output/
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── read_mock_file.py           # lê mocks (path seguro)
│   │   └── write_report.py             # grava MD + JSON em output/
│   └── prompts/
│       └── system.py                   # SYSTEM_PROMPT_ANALYSIS
│
├── output/                             # gerado em runtime (.gitignore em *.md/*.json)
│   └── .gitkeep
│
├── examples/
│   ├── entrada.md                      # CLI + tabela das 10 fontes
│   └── saida.md                        # trechos de relatórios reais
│
├── docs/
│   ├── ESTRUTURA-TRABALHO.md            # este plano (fonte da verdade do processo)
│   ├── CHECKLIST-ENTREGA.md            # checklist do enunciado (§7)
│   ├── Mini-Projeto Avaliativo - Módulo 2 .md
│   ├── prompts.md
│   └── apresentacao/
│       └── slides.md                   # até 2 slides
│
└── tests/                              # 61 testes (pytest)
    ├── conftest.py
    ├── test_validations.py
    ├── test_load_context.py
    ├── test_read_mock_file.py
    ├── test_analyze_data.py
    ├── test_use_tool.py
    ├── test_generate_report.py
    ├── test_fontes_mocks.py            # cobre as 10 fontes
    └── test_graph_e2e.py
```

---

## 3. Fluxo LangGraph (nós) — estado atual

```text
[entrada do usuário]
        ↓
  validate_input      → valida ID/tipo; rejeita entrada inválida
        ↓ (se ok)
  load_context        → lê fonte + métricas; monta estado/memória
        ↓ (se ok)
  analyze_data        → LLM ou heurística → analysis no estado
        ↓
  use_tool            → lê templates/relatorio_tecnico.json
        ↓ (se ok)
  generate_report     → valida seções + write_report → output/
        ↓
     [fim]
```

### Rotas condicionais (interrupção antecipada)

| Após | Segue se | Encerra se |
| --- | --- | --- |
| `validate_input` | sem `validation_errors` | erros de ID/tipo |
| `load_context` | contexto carregado | mock inexistente / path inválido |
| `use_tool` | `tool_result.status == ok` | falha ao ler template |
| `generate_report` | — (nó final) | seções inválidas ou erro de escrita → `validation_errors` |

### Estado compartilhado (`AgentState`)

| Campo | Tipo | Uso |
| --- | --- | --- |
| `source_id` | str | ID canônico (ex.: `DEPLOY-003`) |
| `report_type` | str | `deploy` / `incidente` / `sprint` |
| `raw_source` | dict | Conteúdo do mock da fonte |
| `metrics` | dict | Indicadores de apoio |
| `validation_errors` | list | Falhas de validação / carga / template / saída |
| `analysis` | dict | Resultado LLM/heurística (`modo`, fatos, riscos…) |
| `tool_result` | dict | Template + IDs de seções obrigatórias |
| `final_report` | dict | Relatório + `arquivos` (paths MD/JSON) |
| `messages` | list | Memória acumulada (`add_messages`) |

---

## 4. Arquivos mockados

### `data/mocks/fontes/` (10 arquivos)

| ID | Tipo | Cenário resumido |
| --- | --- | --- |
| `DEPLOY-001` | deploy | Produção parcial — healthcheck timeout (api-pagamentos) |
| `DEPLOY-002` | deploy | Staging OK — rotação JWT (api-auth) |
| `DEPLOY-003` | deploy | Produção com rollback — spike 5xx (gateway) |
| `DEPLOY-004` | deploy | Produção parcial — fila SQS alta (api-notificacoes) |
| `INCIDENTE-001` | incidente | P2 latência checkout — query lenta |
| `INCIDENTE-002` | incidente | P1 gateway — certificado TLS |
| `INCIDENTE-003` | incidente | P3 pagamentos — 401 / JWKS (em investigação) |
| `SPRINT-001` | sprint | Cobranças — entrega 36/42 |
| `SPRINT-002` | sprint | Identity — entrega baixa 21/35 |
| `SPRINT-003` | sprint | Platform — entrega 40/40 |

### `data/mocks/metricas/indicadores.json`

KPIs fictícios por serviço (janela últimos 7 dias) + limites de alerta:

- Serviços: `api-pagamentos`, `api-checkout`, `gateway`, `api-auth`, `api-notificacoes`, `worker-conciliacao`
- Limites: latência p95, taxa de erro, disponibilidade mínima

### `data/mocks/templates/relatorio_tecnico.json`

Seções obrigatórias, tom do texto e regras gerais usadas por `use_tool` / `generate_report`.

**Requisito do enunciado (mínimo):** 3 fontes + 1 métricas + 1 template — **atendido e ampliado (10 fontes).**

---

## 5. Fases de implementação (trabalho individual)

### Fase 0 — Setup do repositório (0,5 dia)

**Objetivo:** base versionada e segura.

- [x] Inicializar Git + branch `main`
- [x] Criar `.gitignore` (`.env`, `output/*.md`, `output/*.json`, `__pycache__`, `.venv`, `.cursor/`)
- [x] Criar `.env.example` (`OPENAI_API_KEY=`, `OPENAI_MODEL=gpt-4o-mini`)
- [x] Criar `requirements.txt` (langgraph, langchain, langchain-openai, python-dotenv, pytest)
- [x] Criar estrutura de pastas
- [x] Commit: `chore: inicializa estrutura do projeto`

**Entrega:** repo clonável, sem secrets.

---

### Fase 1 — Ideia, escopo e slides (0,5 dia)

**Objetivo:** critério 4.

- [x] Fechar o case: **geração de relatórios técnicos**
- [x] Registrar entrada / saída / etapas no README
- [x] Criar até **2 slides** em `docs/apresentacao/`

  - Slide 1: problema + processo + agente
  - Slide 2: entrada, saída, ferramenta, fluxo LangGraph (10 mocks)

- [x] Commit: `docs: adiciona proposta e slides da ideia`

**Entrega:** apresentação pronta.

---

### Fase 2 — Dados mockados e ferramentas de arquivo (1 dia)

**Objetivo:** ferramenta real + mocks (PRIORIDADE).

- [x] Criar JSONs em `data/mocks/` (fontes iniciais, métricas, template)
- [x] Implementar `tools/read_mock_file.py` (lê JSON, valida path)
- [x] Implementar `tools/write_report.py` (grava em `output/` via `config.OUTPUT_DIR`)
- [x] Restringir leitura a `data/mocks/` (segurança)
- [x] Testar leitura/escrita sem LLM
- [x] Commit: `feat: adiciona mocks e ferramentas de leitura/escrita`
- [x] Ampliação posterior: **10 fontes** + métricas dos novos serviços + `tests/test_fontes_mocks.py`

**Entrega:** ferramenta age de verdade sobre arquivos mockados.

---

### Fase 3 — Estado, validação e esqueleto LangGraph (1 dia)

**Objetivo:** critérios 5 e 8 (parcial → depois completado na Fase 4).

- [x] Definir `state.py` (TypedDict + `messages` com `add_messages`)
- [x] Nó `validate_input`
- [x] Nó `load_context` (usa ferramenta de leitura)
- [x] Montar `StateGraph` com edges (stubs iniciais substituídos na Fase 4)
- [x] CLI: `python3 -m src.main --fonte DEPLOY-001`
- [x] Testes: `validate_input`, `load_context`, `read_mock_file`
- [ ] Commit consolidado na Fase 4: `feat: completa fluxo LangGraph com LLM e geracao de relatorios`

**Entrega atual:** esqueleto LangGraph funcional (validate + load reais; analyze/use_tool/generate em stubs).

**Como rodar (sempre com `.venv` ativo):**

```bash
source .venv/bin/activate
which python3   # .../mini-projeto-02/.venv/bin/python3
python3 -m src.main --fonte DEPLOY-001
python3 -m src.main --fonte DEPLOY-003
python3 -m pytest tests/ -v
```

Sem o venv ativo aparece `ModuleNotFoundError: No module named 'langgraph'`.  
Detalhes: `README.md` (seções “Início rápido” e “Problemas comuns”).

---

### Fase 4 — Análise com LLM e geração do relatório (1–1,5 dia)

**Objetivo:** critérios 5, 6 e 8.

- [ ] Nó `analyze_data` com prompt de sistema (`src/prompts/system.py`)
- [ ] Fallback heurístico sem `OPENAI_API_KEY` / falha de API
- [ ] Nó `use_tool` consulta `templates/relatorio_tecnico.json`
- [ ] Manter resultados no estado (`messages` / `analysis` / `tool_result`)
- [ ] Nó `generate_report` consolida, valida seções e grava saída
- [ ] Rota condicional após `use_tool`
- [ ] Execuções demonstráveis (origem: DEPLOY/INCIDENTE/SPRINT-001 com LLM; suite cobre as 10 fontes em modo heurístico)
- [ ] Commit: `feat: completa fluxo LangGraph com LLM e geracao de relatorios`

**Entrega:** agente demonstrável; exemplos em `examples/saida.md` e `output/`.

---

### Fase 5 — Documentação, prompts e exemplos (1 dia)

**Objetivo:** critério 3.

- [ ] `README.md` completo (onboarding, venv, troubleshooting, decisões, limitações)
- [ ] `docs/prompts.md` (planejar, implementar, corrigir/melhorar + prompt de sistema)
- [ ] `examples/entrada.md` e `examples/saida.md` (incluindo tabela das 10 fontes)
- [ ] Revisar `.env.example` e `.gitignore`
- [ ] Revisar Docstrings em todo `src/` (padrão seção 10)
- [ ] Config markdownlint (`.markdownlint.json` + `.markdownlint-cli2.jsonc`)
- [ ] Commit: `docs: completa README, prompts, exemplos e checklist de entrega`
- [ ] Commits de ajuste: `docs: ajusta checklist…`, `docs: marca commits…`

**Entrega:** repo autoexplicativo para novo colaborador.

---

### Fase 6 — Polimento e checklist final (0,5 dia)

**Objetivo:** critérios 1, 2 e 7 + checklist do enunciado.

- [ ] Commits semânticos consistentes (`feat:`, `docs:`, `chore:`)
- [ ] Versionamento na `main` com histórico rastreável
- [ ] Histórico com commits frequentes (contribuição individual)
- [ ] Checklist da seção 7 → `docs/CHECKLIST-ENTREGA.md`
- [ ] Publicar no GitHub (acessível ao professor) — `git push origin main`
- [ ] Submeter link no AVA **antes de 20/07/2026**
- [ ] Após entrega: **não alterar o repo** até a nota

**Commits principais na `main` (histórico):**

- [x] `chore: inicializa estrutura do projeto`
- [x] `docs: adiciona proposta e slides da ideia`
- [x] `feat: adiciona mocks e ferramentas de leitura/escrita`
- [x] `feat: adiciona estado validacao e esqueleto LangGraph`
- [ ] `feat: completa fluxo LangGraph com LLM e geracao de relatorios`
- [ ] `docs: completa README, prompts, exemplos e checklist de entrega`
- [ ] `docs: ajusta checklist de entrega e link no README`
- [ ] `docs: marca commits das fases como resolvidos no checklist`

**Pendências de versão (working tree / a commitar se ainda não versionado):**

- Fase 4: substituir stubs por LLM/heurística, `use_tool` real e `generate_report`
- Fase 5: documentação completa (prompts, exemplos, README onboarding)

**Entrega final:** link submetido no AVA.

---

## 6. Mapa rápido → critérios de avaliação

| Critério | Como esta estrutura cobre |
| --- | --- |
| 1 Versionamento semântico | Commits `feat/docs/chore` no histórico da `main` |
| 2 Contribuição individual | Todo o histórico é do aluno; commits frequentes por fase |
| 3 Docs + prompts | README + `docs/prompts.md` + examples + Docstrings + markdownlint |
| 4 Ideia + slides | Fase 1 — `docs/apresentacao/slides.md` |
| 5 LangGraph | `StateGraph`, nós, edges condicionais (`src/graph.py`) |
| 6 Ferramenta integrada | `read_mock_file` + `write_report` (I/O real em disco) |
| 7 Segurança | `.gitignore`, `.env.example`, path limitado aos mocks |
| 8 Contexto, memória, validação | Estado + `messages` + validação entrada/saída/ferramenta |

---

## 7. Ritmo sugerido (projeto individual)

1. Fases **0–3** — concluídas (estrutura + proposta + mocks + esqueleto LangGraph).
2. Fases **4 → 5** — pendentes (LLM/relatório → docs).
3. Fase **6** — push no GitHub + submissão no AVA (após as fases anteriores).

---

## 8. Ordem de execução imediata (entrega)

1. Concluir Fases 4–5 (LLM/relatório → documentação).
2. Versionar e polir (Fase 6) com commits semânticos na `main`.
3. `git push origin main`.
4. Testar o link do repositório (acesso público ou liberado ao professor).
5. Submeter o link no AVA e congelar o repo até a nota.

---

## 9. Observação sobre arquivos mockados

| O que mockar | O que NÃO fazer |
| --- | --- |
| Fontes (deploy, incidente, sprint), métricas, templates | Ferramenta que finge ler/escrever sem tocar no disco |
| Respostas “de API” salvas em JSON local | Hardcode de secrets no código |
| Exemplos de relatório em `examples/` | Simular tool só no texto do prompt |

**Ferramenta** = função Python real. **Mock** = conteúdo em `data/mocks/`.

---

## 10. Padrão de documentação do código (obrigatório)

O sistema deve estar **documentado em todas as suas partes**. Todo arquivo Python do projeto (`src/`, `tests/` quando fizer sentido) segue o modelo de **Docstrings** (estilo Google).

### O que documentar

| Elemento | Obrigatório |
| --- | --- |
| Módulo (topo do arquivo) | Sim — propósito do arquivo |
| Classe | Sim — responsabilidade e atributos relevantes |
| Função / método público | Sim — o que faz, parâmetros, retorno, exceções |
| Função / método privado (`_`) | Sim — descrição curta (+ Args/Returns se não forem óbvios) |
| Constantes importantes | Comentário ou docstring de módulo explicando o papel |

### Modelo de Docstring (Google style)

```python
def exemplo(fonte: str, tipo: str | None = None) -> dict:
    """Gera o relatório técnico a partir da fonte informada.

    Args:
        fonte: ID da fonte (ex.: ``DEPLOY-001``) ou path relativo do mock.
        tipo: Tipo do relatório. Se omitido, é inferido pelo ID.

    Returns:
        Dicionário com o relatório estruturado e metadados.

    Raises:
        ValueError: Se a fonte for inválida ou o tipo for incompatível.
    """
```

### Regras práticas

- Docstrings em **português** (alinhado ao restante do projeto).
- Preferir explicar o **porquê / o que entrega**, não o óbvio linha a linha.
- Novos arquivos e alterações só entram com docstring completa.
- Regra **já aplicada** nas Fases 3–5; manter em qualquer evolução futura.
- Documentação Markdown do repo deve passar no markdownlint configurado (exceto enunciado oficial e `output/`).

---

## 11. Verificação rápida “sistema ↔ este documento”

| Item real no código | Refletido aqui? |
| --- | --- |
| Estrutura de pastas + `requirements.txt` + `.env.example` (Fase 0) | Sim — concluída |
| Proposta + slides (`README` + `docs/apresentacao/slides.md`) | Sim — Fase 1 |
| 10 fontes mockadas + testes `test_fontes_mocks` | Sim — Fase 2 |
| Ferramentas `read_mock_file` / `write_report` | Sim — Fase 2 |
| Estado + `validate_input` + `load_context` + CLI | Sim — Fase 3 |
| StateGraph com rotas condicionais (stubs Fase 4) | Sim — Fase 3 |
| LLM + fallback heurístico | Planejado (Fase 4) |
| Rotas condicionais no grafo | Planejado (Fases 3–4) |
| `OPENAI_MODEL` / `.env.example` | Sim (Fase 0) |
| Obrigatório usar `.venv` | Sim (regras + Fase 3) |
| README onboarding / troubleshooting | Planejado (Fase 5) |
| Docstrings Google PT | Planejado (Fases 3–5 + seção 10) |
| markdownlint no projeto | Arquivos locais presentes; versionar na Fase 5 |
| Pendência só push + AVA | Não — faltam Fases 4–6 |
