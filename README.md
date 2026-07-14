# mini-projeto

Projeto base em Python.

## Requisitos

- Python 3.10+

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

pip install -e ".[dev]"
```

## Uso

```bash
mini-projeto
# ou
python -m mini_projeto
```

## Testes

```bash
pytest
```

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
