# Exemplos de saída

Trechos gerados pelo agente (`python3 -m src.main --fonte …`).
Arquivos completos em runtime ficam em `output/` (ignorados pelo Git).

## Fontes cobertas

A suíte `tests/test_graph_e2e.py` executa as **10 fontes** em modo heurístico.
Abaixo, trechos demonstráveis com `analysis_modo=llm` (requer `OPENAI_API_KEY`).

| ID | Tipo | Arquivo típico em `output/` |
| --- | --- | --- |
| `DEPLOY-001` | deploy | `output/DEPLOY-001.md` / `.json` |
| `DEPLOY-002` | deploy | `output/DEPLOY-002.md` / `.json` |
| `DEPLOY-003` | deploy | `output/DEPLOY-003.md` / `.json` |
| `DEPLOY-004` | deploy | `output/DEPLOY-004.md` / `.json` |
| `INCIDENTE-001` | incidente | `output/INCIDENTE-001.md` / `.json` |
| `INCIDENTE-002` | incidente | `output/INCIDENTE-002.md` / `.json` |
| `INCIDENTE-003` | incidente | `output/INCIDENTE-003.md` / `.json` |
| `SPRINT-001` | sprint | `output/SPRINT-001.md` / `.json` |
| `SPRINT-002` | sprint | `output/SPRINT-002.md` / `.json` |
| `SPRINT-003` | sprint | `output/SPRINT-003.md` / `.json` |

## DEPLOY-001 (`analysis_modo=llm`)

```markdown
# Relatório técnico — DEPLOY-001

## Sumário executivo
O deploy parcial da versão 2.14.3 do serviço api-pagamentos em produção foi
interrompido devido a um timeout no healthcheck, resultando em aumento de
latência e erros temporários.

## Recomendações
- Investigar e resolver a lentidão no probe do Redis antes de retomar o rollout.
- Monitorar de perto a latência e a taxa de erro ao reiniciar o deploy.

## Metadados
- **fonte**: DEPLOY-001
- **tipo**: deploy
- **analysis_modo**: llm
- **template_versao**: 1.0.0
```

## INCIDENTE-001 (`analysis_modo=llm`)

```markdown
# Relatório técnico — INCIDENTE-001

## Sumário executivo
Incidente de latência elevada no checkout foi mitigado após a criação de um
índice em banco de dados, resultando em normalização da performance.

## Metadados
- **fonte**: INCIDENTE-001
- **tipo**: incidente
- **analysis_modo**: llm
```

## SPRINT-001 (`analysis_modo=llm`)

```markdown
# Relatório técnico — SPRINT-001

## Sumário executivo
A Sprint Cobranças apresentou uma entrega sólida, mas com atraso em dois cards
devido a dependências externas, destacando a necessidade de priorização de
itens pendentes.

## Metadados
- **fonte**: SPRINT-001
- **tipo**: sprint
- **analysis_modo**: llm
```

## Modo heurístico (sem `OPENAI_API_KEY`)

Sem chave (ou com falha de API), o nó `analyze_data` usa `modo=heuristic` e
ainda assim grava MD + JSON em `output/`. Metadados incluem `analysis_modo`
e, quando aplicável, `fallback_motivo`.
