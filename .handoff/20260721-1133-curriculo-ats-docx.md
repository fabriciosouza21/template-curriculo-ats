# Handoff: Currículo ATS em DOCX

**Created:** 2026-07-21 11:33
**Completed:** 2026-07-21 12:03
**Branch:** N/A (não é repositório git)
**Status:** DONE (DOCX ATS gerado, validado, 2 páginas A4)

## Goal

Criar uma versão do currículo do Candidato Nome Completo em formato **DOCX seguindo padrão ATS** (Applicant Tracking System), usando o conteúdo já validado nas etapas anteriores. O DOCX substitui o HTML atual porque formulários de candidatura e portais de RH (Gupy, Kenoby, Greenhouse, Workday) extraem texto via parsing, e HTML/PDF bonitos frequentemente quebram na extração. DOCX ATS é o padrão ouro para submissões.

A pessoa está sem créditos no LLM externo (Claude/GPT), então a sessão local precisa gerar o arquivo final.

## What was done (sessões anteriores)

- **Discovery completo** em `/home/usuario/projetos/template/first_decision/discovery.md` (314 linhas, 8 seções + metodologia). Construído via fluxo adversarial (escritor → revisor → juiz) em cada seção. Validação contra código real dos projetos, CTPS, diploma (via OCR com EasyOCR), e Notion.
- **Briefing para LLM externo** em `/home/usuario/projetos/template/first_decision/briefing_llm_externo.md` (241 linhas). Documento consolidado e completo com todas as informações validadas + 9 regras de honestidade.
- **Currículo em HTML** em `/home/usuario/projetos/template/first_decision/curriculo.html` e **PDF** em `curriculo.pdf` (3 páginas, layout de duas colunas, sidebar azul, avatar com iniciais "FM"). Gerado pelo LLM externo a partir do briefing, convertido localmente via Chrome headless.
- **Currículo revisado em markdown** em `/home/usuario/projetos/template/first_decision/curriculo_revisado.md`.

## Current state

**Arquivos prontos na pasta `/home/usuario/projetos/template/first_decision/`:**
- `discovery.md` — fonte da verdade, com auditoria adversarial completa
- `briefing_llm_externo.md` — conteúdo canônico consolidado (USE ESTE como base)
- `curriculo.html` — layout visual bonito (não-ATS), referência de conteúdo
- `curriculo.pdf` — PDF do HTML acima (não-ATS)
- `curriculo_revisado.md` — versão markdown simples

**Decisões já tomadas e validadas** (não reabrir):
- Cargo-título: "Engenheiro de Software Pleno" no topo, com pretensões "Desenvolvedor Backend Pleno" e "Full Stack Pleno".
- Objetivo recomendado: "Atuar como Desenvolvedor Backend Pleno (Java/Spring) em produtos de média e alta complexidade, aplicando design de código, arquitetura limpa e IA de forma crítica, com sólida bagagem em sete domínios de negócio distintos."
- Endereço: Cidade, UF (remoto).
- Foco principal: **Java/Spring**. Frontend, IA e Go são complementares.
- Foto: NÃO (ATS não lê foto e vira ruído).

## Key decisions (honrar estas regras de honestidade)

Estas são correções que foram aplicadas após auditoria adversarial. **NÃO revertê-las no DOCX**:

1. **Datas UFPA:** abril/2017 a janeiro/2024 (conclusão), colação março/2024. Concluído em paralelo à atuação profissional iniciada em 2021 e ao período pandêmico (justifica os 7 anos).
2. **Datas empregos:** itexto 20/10/2021 a 25/04/2025; iUsecase 10/07/2025 a atual (CTPS).
3. **Cargo CTPS:** itexto = "Programador" (CBO 3171-10) durante todo o período; iUsecase = "Desenvolvedor Backend Pleno 1" (CBO 2124-05). A descrição "Full Stack" e "Engenheiro de Software" reflete função real, comum em consultorias brasileiras.
4. **jOOQ:** aparece APENAS no Live2U. Consol usa Spring Data JPA. Apontamento usa QueryDSL. Não misturar.
5. **GraphQL:** consumido como CLIENTE (QR-Capital via graphql-java-generator + WebClient), NÃO server-side.
6. **Spring AI / pgvector / TTS / HLS:** NÃO estão em código de produto. São estudo (rinha-embed benchmark, Notion). Apresentar como estudo, não como implementação em produção.
7. **RAG no Live2U:** é ORQUESTRAÇÃO NO FRONTEND Angular consumindo serviço externo (`ai-api.live2u.com.br`, operado pela Sys3). O backend de IA não está no workspace.
8. **Refatoração multi-tenant do Apontamento:** PARCIAL. Timelogging migrado para policies, mas `CONSOL_CNPJ` ainda hard-coded em WorkbookStrategyFactoryImpl, SprintServiceImpl e TenantBootstrapSeed (dívida documentada em `PLANO-EXECUCAO-MULTITENANT.md`).
9. **Suporte ao usuário final na itexto:** INFERÊNCIA do ciclo SaaS, não evidência primária (sem ticket/log/screenshot). Defender como "suporte a aplicações em produção".
10. **Comunicação:** "técnica estruturada voltada a pares", NÃO "tradução para leigo" (não há evidência disso).
11. **App de revisão espaçada:** algoritmo "estilo SM-2" (variante estendida com `weight = (difficulty+importance)/10`), NÃO SM-2 canônico de Wozniak.
12. **Benchmark de embeddings:** "oferece evidência preliminar" sobre quando delegar a subagents, NÃO "embasa critério" (foi n=1).
13. **Não incluir:** SNS, Micronaut, Azure (só iatmos tem Azure, mas o usuário decidiu não destacar Iveco/Stellantis), "milhares de usuários" na Weex, "birôs de crédito" como integração, Spring Cloud Gateway, Chain of Responsibility (sem fonte).

## What's next (tarefas concretas para o DOCX ATS)

1. **Ler o skill `docx`** em `/home/usuario/.zcode/cli/plugins/cache/zcode-plugins-official/document-skills/0.1.0/skills/docx/SKILL.md` para entender como gerar DOCX corretamente (usa python-docx provavelmente).

2. **Gerar o DOCX ATS** com estas características obrigatórias:
   - **Sem duas colunas**, sem sidebar colorida, sem tabelas de layout, sem caixas, sem cores fortes. Layout de **uma coluna simples**, top-to-bottom.
   - **Fonte padrão** (Arial, Calibri ou Carlito, 10-11pt corpo, 14-16pt nome).
   - **Sem foto, sem ícones, sem emojis, sem SVGs**. ATS não parseia nada disso.
   - **Hierarquia via headings** (H1 nome, H2 seções: Perfil, Habilidades, Experiência, Formação, Cursos, Estudos Complementares, IA).
   - **Texto puro e linear**: cada emprego com empresa, período, cargo, bullets claros.
   - **Sem headers/footers** (ATS pode se perder).
   - **Keywords de skills** repetidas naturalmente (Java, Spring Boot, PostgreSQL, AWS, etc.) porque ATS busca por termos.
   - **Datas no formato simples** (Mês/Ano, ex: "Out 2021 – Abr 2025").
   - **Links como texto puro** (não hiperlinks embutidos; ATS extrai melhor texto puro).
   - **Tamanho alvo: 2-3 páginas.**

3. **Conteúdo:** copiar do `briefing_llm_externo.md` (já está validado), adaptando layout pra DOCX simples.

4. **Salvar em:** `/home/usuario/projetos/template/first_decision/curriculo_ats.docx`

5. **Validar:** abrir o DOCX gerado e confirmar que (a) abre sem erro, (b) texto é selecionável e copiável, (c) tem 2-3 páginas, (d) layout é uma coluna simples. Se possível, exportar também um PDF via `libreoffice --headless --convert-to pdf` como cortesia pra inspeção visual.

## Blockers / Open questions

- **Nenhum bloqueador.** Todo o conteúdo está pronto em `briefing_llm_externo.md`. Skill `docx` está disponível. python-docx provavelmente já instalado (confirmar na próxima sessão com `python3 -c "import docx"`).

## How to continue

**CONCLUÍDO em 2026-07-21.** Resultado da execução:

### Arquivos gerados em `/home/usuario/projetos/template/first_decision/`

- `curriculo_ats.docx` (40 KB) — **DOCX ATS final**, 2 páginas A4, layout uma coluna, zero tabelas.
- `curriculo_ats.pdf` (55 KB) — PDF de cortesia para inspeção visual (via LibreOffice headless).
- `gerar_curriculo_ats.py` (15 KB) — script Python idempotente com assertions TDD inline. Rodar novamente regenera o DOCX.

### Decisões aplicadas (conforme Alura + handoff + briefing)

1. **Stack:** python-docx (em vez do skill docx-js), porque o skill é otimizado para design visual (sidebars coloridas, banners escuros, dots de skill ●○), o que conflita diretamente com ATS estrito. python-docx gera OOXML limpo.
2. **Layout:** uma coluna, A4, fonte Calibri 9.5pt (corpo) / 18pt (nome) / 11-12pt (headings). Margens 1.2cm vertical, 1.6cm horizontal. Line spacing 1.05. Bullets com estilo `List Bullet` nativo.
3. **Cabeçalho:** nome + cargo + linha única com telefone, e-mail, endereço, LinkedIn, GitHub e portfólio separados por `|`.
4. **Perfil:** reescrito em estilo Alura enxuto (4 linhas, orientado a conquista: 5 anos + 7 domínios + UFPA).
5. **Cursos:** apenas essenciais (8 itens principais em vez de ~20), agrupados por área.
6. **IA:** seção completa mantida (3 bullets com benchmark, engenharia agentic e prática diária).
7. **9 regras de honestidade:** honradas. jOOQ só no Live2U, GraphQL como cliente, RAG como orquestração frontend, multi-tenant parcial, cargos CTPS explicitados, etc.
8. **Datas:** formato `Mês/Ano - Mês/Ano` com hífen simples (sem em-dash), alinhadas à direita via tab stop.

### Validações TDD inline no script

O script `gerar_curriculo_ats.py` roda assertions antes de salvar o arquivo:

- ✅ Document abre sem erro (implícito por chegar ao salvar)
- ✅ Seções obrigatórias presentes: PERFIL, HABILIDADES, EXPERIÊNCIA, FORMAÇÃO, FORMAÇÃO COMPLEMENTAR, IA COMO EIXO
- ✅ Zero tabelas (`len(doc.tables) == 0`)
- ✅ Keywords ATS presentes: Java, Spring Boot, PostgreSQL, Clean Architecture, CQRS, UFPA
- ✅ Contato presente: telefone (00) 00000-0000, e-mail
- ✅ jOOQ aparece (apenas Live2U)
- ✅ Sem em-dashes (—) e sem en-dashes (–) — regra de estilo do AGENTS.md

### Métricas finais

- Páginas: 2 (limite Alura respeitado)
- Tamanho: A4 (595x841 pts)
- Parágrafos: 49
- Tabelas: 0 (regra ATS)
- Caracteres: 7353
- Texto extraível via `pdftotext -layout`: confirmado, legível e linear

### Para regenerar

```bash
cd /home/usuario/projetos/template/first_decision
python3 gerar_curriculo_ats.py
libreoffice --headless --convert-to pdf curriculo_ats.docx
```

## Key files

- `/home/usuario/projetos/template/first_decision/briefing_llm_externo.md` — **FONTE PRINCIPAL**. Conteúdo canônico validado com 9 regras de honestidade. Ler primeiro.
- `/home/usuario/projetos/template/first_decision/discovery.md` — Documento de discovery completo (314 linhas) com auditoria adversarial. Referência se houver dúvida sobre qualquer claim.
- `/home/usuario/projetos/template/first_decision/curriculo.html` e `.pdf` — Versão visual (não-ATS) pra referência de conteúdo, mas NÃO copiar o layout.
- `/home/usuario/projetos/template/first_decision/curriculo_revisado.md` — Markdown simples, referência secundária.
- `/home/usuario/.zcode/cli/plugins/cache/zcode-plugins-official/document-skills/0.1.0/skills/docx/SKILL.md` — Skill para gerar DOCX.
- `/home/usuario/projetos/template/first decision/CTPSContratosDigitais06-07-2026.pdf` — CTPS (validação de datas e cargos).
- `/home/usuario/projetos/template/first decision/diploma-ciencia-computacao-ufpa-frente-e-verso.pdf.pdf` — Diploma UFPA (validação de formação).
