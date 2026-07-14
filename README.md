# Agente Gerador de Relatórios Técnicos

Agente em **LangGraph** que transforma dados técnicos mockados (deploys, incidentes e sprints) em relatórios estruturados e acionáveis.

**Repositório:** [github.com/henriqueferraz/mini-projeto-02](https://github.com/henriqueferraz/mini-projeto-02)

> Status: Fases 0–5 concluídas (agente + documentação). Resta polimento/AVA (Fase 6).

## Problema

Logs de deploy, métricas, incidentes e notas de sprint ficam espalhados em arquivos. Escrever um relatório técnico claro, consistente e acionável consome tempo e varia de pessoa para pessoa.

## Objetivo do agente

Automatizar a geração do relatório: validar a entrada, carregar o contexto dos mocks, analisar os dados (LLM ou heurística), consultar o template via ferramenta real e gravar a saída em `output/`.

## Por que é um agente

Tem objetivo claro, estado compartilhado entre nós, fluxo em etapas no LangGraph, usa ferramenta real de arquivo e entrega um relatório útil — não é um único prompt isolado.

## Início rápido

Requisitos: **Python 3.10+**.

```bash
git clone https://github.com/henriqueferraz/mini-projeto-02.git
cd mini-projeto-02

python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -e ".[dev]"
# ou: pip install -r requirements.txt && pip install -e ".[dev]"

cp .env.example .env
# opcional: preencha OPENAI_API_KEY no .env para modo=llm
```

Sempre execute com o Python do `.venv`:

```bash
source .venv/bin/activate
which python3   # deve apontar para .../mini-projeto-02/.venv/bin/python3
```

### Gerar um relatório

```bash
python3 -m src.main --fonte DEPLOY-001
python3 -m src.main --fonte INCIDENTE-002 --tipo incidente
python3 -m src.main --fonte fontes/SPRINT-001.json --json
```

Saída em `output/` (`.md` + `.json`). Trechos versionados: [`examples/saida.md`](examples/saida.md).

### Testes

```bash
pytest
# ou: pytest tests/ -v
```

## Entrada

| Campo | Descrição |
| --- | --- |
| `--fonte` | ID canônico (`DEPLOY-001`) **ou** path relativo (`fontes/DEPLOY-001.json`) |
| `--tipo` | Opcional: `deploy`, `incidente` ou `sprint` (inferido pelo prefixo se omitido) |
| `--json` | Imprime o estado final em JSON (debug) |

Com `OPENAI_API_KEY` no `.env` → análise `modo=llm`. Sem chave ou falha de API → `modo=heuristic`.

Tabela das 10 fontes: [`examples/entrada.md`](examples/entrada.md).

## Saída

Relatório técnico em `output/` contendo:

- sumário executivo
- contexto / fatos relevantes
- análise técnica
- riscos e impactos
- recomendações
- metadados (`fonte`, `data`, `tipo`, `analysis_modo`, `template_versao`)

## Fluxo LangGraph

```text
validate_input → load_context → analyze_data → use_tool → generate_report
```

| Nó | Função |
| --- | --- |
| `validate_input` | Valida ID/tipo; rejeita entrada inválida |
| `load_context` | Lê fonte + métricas via `read_mock_file` |
| `analyze_data` | LLM ou fallback heurístico |
| `use_tool` | Lê `templates/relatorio_tecnico.json` |
| `generate_report` | Valida seções e grava MD + JSON com `write_report` |

Rotas condicionais encerram o fluxo cedo se houver erro de validação, carga ou template.

## Ferramentas

| Ferramenta | Papel |
| --- | --- |
| `read_mock_file` | Lê JSON em `data/mocks/` (bloqueia path absoluto e `..`) |
| `write_report` | Grava relatório em `output/` |

Mocks = dados fictícios. A ferramenta **age de verdade** no disco.

## Estrutura do repositório

```text
data/mocks/          # fontes, métricas, template
src/                 # agente (state, graph, nodes, tools, prompts)
output/              # relatórios gerados em runtime
examples/            # entrada/saída documentadas
docs/                # plano, slides, prompts, checklist
tests/               # pytest
```

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
| --- | --- | --- |
| `OPENAI_API_KEY` | Não | Se vazia → modo heurístico |
| `OPENAI_MODEL` | Não | Padrão: `gpt-4o-mini` |

Use apenas `.env.example` versionado (nomes, sem secrets). O arquivo `.env` está no `.gitignore`.

## Problemas comuns

| Sintoma | Causa provável | Solução |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'langgraph'` | `.venv` não ativo | `source .venv/bin/activate` e confirme com `which python3` |
| `ModuleNotFoundError` em `config` / `nodes` | rodou de outro diretório | execute a partir da raiz do repo: `python3 -m src.main …` |
| Relatório em modo `heuristic` sem querer | sem chave ou API falhou | preencha `OPENAI_API_KEY` no `.env` |
| `FileNotFoundError` / fonte inválida | ID inexistente | use um ID da tabela em `examples/entrada.md` |
| Path rejeitado | absoluto ou com `..` | use ID ou path relativo a `data/mocks/` |

## Decisões de projeto

- **Mocks + I/O real:** dados fictícios em JSON; ferramentas leem/escrevem de verdade.
- **Fallback heurístico:** o agente permanece demonstrável offline / sem crédito de API.
- **Segurança de path:** leitura restrita a `data/mocks/`.
- **Estado LangGraph:** memória em `messages` (`add_messages`) + campos tipados em `AgentState`.
- **Commits na `main`:** projeto individual com histórico semântico por fase.

## Limitações

- Fontes são mockadas (não há integração com APIs reais de deploy/incidente).
- Qualidade da análise LLM depende do modelo e do prompt em `src/prompts/system.py`.
- Heurística é determinística e limitada aos campos estruturados do JSON.
- Relatórios em `output/` não são versionados (apenas exemplos em `examples/`).

## Documentação

| Arquivo | Conteúdo |
| --- | --- |
| [`docs/ESTRUTURA-TRABALHO.md`](docs/ESTRUTURA-TRABALHO.md) | Plano de fases e arquitetura |
| [`docs/prompts.md`](docs/prompts.md) | Registro de prompts (planejar / implementar / corrigir + sistema) |
| [`docs/apresentacao/slides.md`](docs/apresentacao/slides.md) | Slides da proposta (critério 4) |
| [`docs/CHECKLIST-ENTREGA.md`](docs/CHECKLIST-ENTREGA.md) | Checklist do enunciado |
| [`examples/entrada.md`](examples/entrada.md) | Exemplos de entrada + 10 fontes |
| [`examples/saida.md`](examples/saida.md) | Trechos de saída |

## CI/CD e Conventional Commits

GitHub Actions:

- testes em Python 3.10–3.12 em push/PR para `main`;
- commitlint (Conventional Commits);
- validação do título de Pull Requests.

Formato: `<type>(<scope opcional>): <descrição>`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

## Apresentação

Slides: [`docs/apresentacao/slides.md`](docs/apresentacao/slides.md).
