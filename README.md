# Agente Gerador de Relatórios Técnicos

Agente em **LangGraph** que transforma dados técnicos mockados (deploys, incidentes e sprints) em relatórios estruturados e acionáveis.

> Status: Fases 0–4 concluídas. Agente ponta a ponta com LLM/heurística e saída em `output/`. Próximo: documentação (Fase 5).

## Problema

Logs de deploy, métricas, incidentes e notas de sprint ficam espalhados em arquivos. Escrever um relatório técnico claro, consistente e acionável consome tempo e varia de pessoa para pessoa.

## Objetivo do agente

Automatizar a geração do relatório: validar a entrada, carregar o contexto dos mocks, analisar os dados (LLM ou heurística), consultar o template via ferramenta real e gravar a saída em `output/`.

## Entrada

| Campo | Descrição |
| --- | --- |
| Fonte | ID canônico (ex.: `DEPLOY-001`, `INCIDENTE-002`, `SPRINT-003`) **ou** path relativo em `data/mocks/fontes/` |
| Tipo (opcional) | `deploy`, `incidente` ou `sprint` — se omitido, é inferido pelo prefixo do ID |

Exemplos de CLI:

```bash
source .venv/bin/activate
python3 -m src.main --fonte DEPLOY-001
python3 -m src.main --fonte INCIDENTE-002 --tipo incidente
python3 -m src.main --fonte fontes/SPRINT-001.json
```

Com `OPENAI_API_KEY` no `.env` → análise `modo=llm`. Sem chave ou falha de API → `modo=heuristic`. Trechos de saída em [`examples/saida.md`](examples/saida.md).

## Saída

Relatório técnico em `output/` (Markdown + JSON), contendo no mínimo:

- sumário executivo
- contexto / fatos relevantes
- análise técnica
- riscos e impactos
- recomendações
- metadados (fonte, data, tipo, modo de análise, versão do template)

## Etapas do fluxo (LangGraph)

```text
validate_input → load_context → analyze_data → use_tool → generate_report
```

1. **validate_input** — valida ID/tipo; rejeita entrada inválida.
2. **load_context** — lê fonte + métricas mockadas; monta estado/memória.
3. **analyze_data** — análise via LLM (`OPENAI_API_KEY`) ou fallback heurístico.
4. **use_tool** — lê o template `data/mocks/templates/relatorio_tecnico.json`.
5. **generate_report** — valida seções obrigatórias e grava MD + JSON em `output/`.

## Por que é um agente

Tem objetivo claro, estado compartilhado entre nós, fluxo em etapas no LangGraph, usa ferramenta real de arquivo e entrega um relatório útil — não é um único prompt isolado.

## Apresentação (até 2 slides)

Slides da ideia: [`docs/apresentacao/slides.md`](docs/apresentacao/slides.md).

## Requisitos

- Python 3.10+

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

pip install -e ".[dev]"
```

## Uso (agente)

```bash
source .venv/bin/activate
python3 -m src.main --fonte DEPLOY-001
python3 -m src.main --fonte DEPLOY-003 --json
```

Relatórios gerados em `output/` (Markdown + JSON).

## Testes

```bash
pytest
```

## Documentação do projeto

| Arquivo | Conteúdo |
| --- | --- |
| [`docs/ESTRUTURA-TRABALHO.md`](docs/ESTRUTURA-TRABALHO.md) | Plano de fases e arquitetura |
| [`docs/apresentacao/slides.md`](docs/apresentacao/slides.md) | Slides da proposta (critério 4) |
| [`docs/CHECKLIST-ENTREGA.md`](docs/CHECKLIST-ENTREGA.md) | Checklist do enunciado |

## CI/CD e Conventional Commits

Este repositório usa **GitHub Actions** para:

- executar testes em Python 3.10–3.12 em todo push/PR para `main`;
- validar mensagens de commit com [Conventional Commits](https://www.conventionalcommits.org/);
- validar o título dos Pull Requests no mesmo padrão.

### Formato das mensagens

```
<type>(<scope opcional>): <descrição>
```

Types aceitos: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

Exemplos:

```
feat: adiciona fluxo inicial do agente
fix: corrige falha na validação de entrada
ci: configura commitlint no GitHub Actions
docs: documenta padrão de commits
```

### Fluxo recomendado com branches

```bash
git checkout -b feat/nome-da-feature
# ... alterações ...
git commit -m "feat: descreve a mudança"
git push -u origin HEAD
# abra um Pull Request com título no mesmo padrão
```
