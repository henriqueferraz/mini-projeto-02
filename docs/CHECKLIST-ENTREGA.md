# Checklist final de entrega (enunciado §7)

Prazo: **20/07/2026**. Itens de LangGraph/LLM/AVA ficam pendentes até as Fases 3–6.

## Repositório e organização

- [x] Criei o repositório no GitHub e ele está acessível para avaliação.
- [ ] O repositório contém o código-fonte completo do agente (Fases 3–4).
- [x] O projeto está organizado e possui histórico de commits compatível com o desenvolvimento.
- [x] Projeto individual — contribuição rastreável no histórico do aluno.
- [ ] Commits semânticos das fases 0–5 resolvidos na `main`.
- [ ] Push da `main` atualizado após as fases restantes.

## Agente e implementação

- [x] Defini o processo automatizado (geração de relatórios técnicos).
- [x] Objetivo, entrada e saída claramente definidos (README + slides).
- [ ] Agente implementado com **LangGraph**.
- [ ] Fluxo com estado, nós e conexões.
- [ ] Execução funcional com saída estruturada (MD + JSON).

## Ferramentas, contexto e validação

- [x] Ferramenta integrada (`read_mock_file` / `write_report`).
- [x] Ação real em disco (não só simulada).
- [ ] Contexto/memória no estado (`messages`, `raw_source`, `analysis`, etc.).
- [ ] Validação de entrada, path da ferramenta e seções do relatório.
- [x] Sem chaves/tokens versionados (`.env` no `.gitignore`; `.env.example` vazio).

## README.md e prompts

- [x] README com problema, objetivo e funcionamento.
- [ ] README com instruções de execução completas do agente.
- [ ] README com fluxo LangGraph e ferramenta (detalhe pós-implementação).
- [ ] Exemplos de entrada e saída (`examples/` + README).
- [ ] Prompts em `docs/prompts.md`.

## Apresentação

- [x] Até 2 slides em `docs/apresentacao/slides.md`.
- [x] Slides com problema, agente, entrada, saída, ferramenta e fluxo.
- [ ] Submeter slides via AVA **ou** confirmar que versionados no repo bastam (conforme professor).

## Submissão

- [ ] Submeter o link do repositório GitHub no AVA.
- [ ] Conferir se o link está acessível antes da submissão.
- [ ] Entregar antes do prazo.
- [ ] Não modificar o repositório após a entrega até receber a nota.
