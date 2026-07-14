# Exemplos de saída

Trechos gerados pelo agente (`python3 -m src.main --fonte …`).
Arquivos completos em runtime ficam em `output/` (ignorados pelo Git).

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
ainda assim grava MD + JSON em `output/`. A suíte de testes cobre as **10 fontes**
nesse modo.
