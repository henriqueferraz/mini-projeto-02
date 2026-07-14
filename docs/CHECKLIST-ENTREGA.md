# Checklist final de entrega (enunciado §7)

Prazo: **20/07/2026**. Documentação completa e AVA ficam para as Fases 5–6.

## Repositório e organização

- [x] Criei o repositório no GitHub e ele está acessível para avaliação.
- [x] O repositório contém o código-fonte completo do agente (Fase 4).
- [x] O projeto está organizado e possui histórico de commits compatível com o desenvolvimento.
- [x] Projeto individual — contribuição rastreável no histórico do aluno.
- [ ] Commits semânticos das fases 0–5 resolvidos na `main`.
- [ ] Push da `main` atualizado após as fases restantes.

## Agente e implementação

- [x] Defini o processo automatizado (geração de relatórios técnicos).
- [x] Objetivo, entrada e saída claramente definidos (README + slides).
- [x] Agente implementado com **LangGraph**.
- [x] Fluxo com estado, nós e conexões.
- [x] Execução funcional com saída estruturada (MD + JSON).

## Ferramentas, contexto e validação

- [x] Ferramenta integrada (`read_mock_file` / `write_report`).
- [x] Ação real em disco (não só simulada).
- [x] Contexto/memória no estado (`messages`, `raw_source`, `analysis`, etc.).
- [x] Validação de entrada, path da ferramenta e seções do relatório.
- [x] Sem chaves/tokens versionados (`.env` no `.gitignore`; `.env.example` vazio).

## README.md e prompts

- [x] README com problema, objetivo e funcionamento.
- [x] README com instruções de execução do agente.
- [x] README com fluxo LangGraph e ferramenta.
- [x] Exemplos de saída (`examples/saida.md`); entrada completa na Fase 5.
- [ ] Prompts em `docs/prompts.md` (Fase 5).

## Apresentação

- [x] Até 2 slides em `docs/apresentacao/slides.md`.
- [x] Slides com problema, agente, entrada, saída, ferramenta e fluxo.
- [ ] Submeter slides via AVA **ou** confirmar que versionados no repo bastam (conforme professor).

## Submissão

- [ ] Submeter o link do repositório GitHub no AVA.
- [ ] Conferir se o link está acessível antes da submissão.
- [ ] Entregar antes do prazo.
- [ ] Não modificar o repositório após a entrega até receber a nota.
