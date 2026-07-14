# Exemplos de entrada

## CLI

Com o `.venv` ativo, na raiz do repositório:

```bash
# ID canônico
python3 -m src.main --fonte DEPLOY-001

# ID + tipo explícito
python3 -m src.main --fonte INCIDENTE-002 --tipo incidente

# Path relativo ao mock
python3 -m src.main --fonte fontes/SPRINT-003.json

# Estado final em JSON (debug)
python3 -m src.main --fonte DEPLOY-003 --json
```

## Entradas inválidas (devem falhar na validação)

```bash
python3 -m src.main --fonte INVALIDO
python3 -m src.main --fonte /tmp/DEPLOY-001.json
python3 -m src.main --fonte SPRINT-001 --tipo deploy
```

## Fontes mockadas (`data/mocks/fontes/`)

| ID | Tipo | Cenário resumido |
| --- | --- | --- |
| `DEPLOY-001` | deploy | Produção parcial — healthcheck timeout (`api-pagamentos`) |
| `DEPLOY-002` | deploy | Staging OK — rotação JWT (`api-auth`) |
| `DEPLOY-003` | deploy | Produção com rollback — spike 5xx (`gateway`) |
| `DEPLOY-004` | deploy | Produção parcial — fila SQS alta (`api-notificacoes`) |
| `INCIDENTE-001` | incidente | P2 latência checkout — query lenta |
| `INCIDENTE-002` | incidente | P1 gateway — certificado TLS |
| `INCIDENTE-003` | incidente | P3 pagamentos — 401 / JWKS (em investigação) |
| `SPRINT-001` | sprint | Cobranças — entrega 36/42 |
| `SPRINT-002` | sprint | Identity — entrega baixa 21/35 |
| `SPRINT-003` | sprint | Platform — entrega 40/40 |

Apoio: `data/mocks/metricas/indicadores.json` e `data/mocks/templates/relatorio_tecnico.json`.
