# Checklist final de entrega (enunciado §7)

Prazo: **20/07/2026**. Itens de LLM/AVA ficam pendentes até as Fases 4–6.

## Repositório e organização

- [x] Criei o repositório no GitHub e ele está acessível para avaliação.
- [ ] O repositório contém o código-fonte completo do agente (Fase 4).
- [x] O projeto está organizado e possui histórico de commits compatível com o desenvolvimento.
- [x] Projeto individual — contribuição rastreável no histórico do aluno.
- [ ] Commits semânticos das fases 0–5 resolvidos na `main`.
- [ ] Push da `main` atualizado após as fases restantes.

## Agente e implementação

- [x] Defini o processo automatizado (geração de relatórios técnicos).
- [x] Objetivo, entrada e saída claramente definidos (README + slides).
- [x] Agente implementado com **LangGraph** (esqueleto; stubs na análise/relatório).
- [x] Fluxo com estado, nós e conexões.
- [ ] Execução funcional com saída estruturada (MD + JSON) — Fase 4.

## Ferramentas, contexto e validação

- [x] Ferramenta integrada (`read_mock_file` / `write_report`).
- [x] Ação real em disco (não só simulada).
- [x] Contexto/memória no estado (`messages`, `raw_source`, etc.).
- [x] Validação de entrada e path da ferramenta (seções do relatório na Fase 4).
- [x] Sem chaves/tokens versionados (`.env` no `.gitignore`; `.env.example` vazio).

## README.md e prompts

- [x] README com problema, objetivo e funcionamento.
- [x] README com instruções de execução do esqueleto.
- [ ] README com fluxo LangGraph e ferramenta (detalhe pós-Fase 4/5).
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
