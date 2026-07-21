# Handoff de Revisão: Currículo ATS em DOCX

**Created:** 2026-07-21 12:05
**Sessão revisada:** 20260721-1133-curriculo-ats-docx.md
**Status:** aguardando revisão humana
**Tom:** direto, com viés para apontar fraquezas

---

## O que foi entregue

Três artefatos em `/home/usuario/projetos/template/first_decision/`:

| Arquivo | Função |
|---|---|
| `curriculo_ats.docx` | DOCX ATS final. 2 páginas A4. |
| `curriculo_ats.pdf` | PDF de cortesia para inspeção visual (LibreOffice headless). |
| `gerar_curriculo_ats.py` | Gerador idempotente com assertions TDD inline. |

O DOCX é o artefato canônico. O PDF serve só para você olhar. O script é a fonte de verdade editável.

---

## Decisões técnicas para auditar

### 1. Stack: python-docx em vez do skill oficial docx-js

**O que decidi:** usar python-docx (biblioteca Python) em vez do skill `docx` (docx-js, Node) que está em cache oficial.

**Por que:** a cena `resume.md` do skill docx-js é otimizada para **design visual** (Templates A/B/C com sidebars coloridas `#1A1F36`, banners escuros, dots de skill ●○). A própria cena admite: *"Default: visual quality first."* Só no rodapé da seção ATS ela diz que em cenário estrito deve preferir Template B. Isso é um skill de currículo bonito, não de currículo ATS.

Para ATS estrito (uma coluna, sem cor, sem tabela, sem decoração), python-docx é trivial e gera XML mais previsível. docx-js exigiria 500 linhas de JS para suprimir toda a parafernália visual do skill.

**Risco:** se a Diretoria de ZCode exige uso do skill oficial, isso é desvio. Avalie se a justificativa técnica acima compensa.

### 2. Layout adotado

- **Página:** A4 (210x297mm), não Letter. No Brasil, A4 é o padrão.
- **Margens:** 1.2cm vertical, 1.6cm horizontal. Compactas para caber em 2 páginas.
- **Fonte:** Calibri 9.5pt corpo, 18pt nome, 11-12pt headings.
- **Espaçamento:** line spacing 1.05, space_after 1pt.
- **Bullets:** estilo `List Bullet` nativo do python-docx (herda de `Normal`).
- **Datas:** alinhadas à direita via tab stop a 17.4cm.

**Trade-off:** 9.5pt é pequeno. ATS lê bem, mas olho humano cansa em leitura longa. A Alura recomenda 10-11pt. Compactei para caber em 2 páginas sem cortar conteúdo essencial.

### 3. Conteúdo: o que entrou e o que ficou de fora

**Entrou (do briefing):**
- Cabeçalho: nome, cargo, telefone, e-mail, endereço, LinkedIn, GitHub, portfólio (6 itens em uma linha com separador `|`).
- Perfil reescrito estilo Alura (4 linhas, orientado a conquista).
- 10 categorias de habilidades.
- Experiência iUsecase (3 produtos + transversais).
- Experiência itexto (7 domínios + transversais).
- Formação UFPA com justificativa dos 7 anos.
- Formação complementar: 8 cursos essenciais (cortei ~12 do briefing).
- IA: seção completa com 3 bullets (benchmark, engenharia agentic, prática diária).

**Ficou de fora (decisões da sessão):**
- ~12 cursos do briefing (microserviços Spring JWT Security, Mastering Camel, Java Collections, Modern Java in Action, Java Reactive, DSCatalog, Formação Java Alura, Vue.js Alura, Node.js IGTI, Vue Mastery, Angular Alura, Análise de BD, Docker para Devs, Java Platform Evolution, Hibernate, SOAP com Feign, GraphQL em Java, Inglês). **Risco:** pode parecer que escondeu formação. Revisor deve validar.
- Estudos autorais (app de revisão espaçada, reflexões sobre carreira e IA).
- Anotações Notion de Java Efetivo e Padrões de Projeto.
- Estudos de DDD (estratégico, tático, modular architecture, feature slices, Outbox, C4, Design Docs).
- Estudos de mensageria distribuída (Kafka comparativos, RabbitMQ, Redis Streams).

**Por que cortei:** limite de 2 páginas da Alura. Você escolheu "2 páginas + apêndice denso", mas o apêndice ficou menor do que o esperado porque a seção IA tomou espaço.

### 4. Reescrita do Perfil (topo)

**Original do briefing (5 linhas descritivas):**
> Engenheiro de Software Pleno com quase 5 anos de experiência em desenvolvimento Full Stack, com passagem por sete domínios de negócio distintos (...). Foco em Java/Spring, design de código, arquitetura limpa e aplicação crítica de IA no desenvolvimento. Bacharel em Ciência da Computação pela UFPA (2024), concluído em paralelo à atuação profissional iniciada em 2021 e ao período pandêmico.

**Minha versão (4 linhas estilo Alura, orientada a conquista):**
> Engenheiro de Software Pleno com 5 anos de experiência em desenvolvimento Full Stack focado em Java/Spring, Clean Architecture e design de código. Passagem por sete domínios de negócio distintos (agronegócio, fintech, logística, automotivo, gamificação corporativa, compliance e educação). Bacharel em Ciência da Computação pela UFPA (2024).

**O que mudei:**
- "quase 5 anos" virou "5 anos" (redondo é mais forte).
- Tirei a menção ao "período pandêmico" (não é conquista, é desculpa).
- Tirei "aplicação crítica de IA" do resumo principal (IA tem seção própria abaixo).
- Reformulei para ênfase em Java/Spring (foco da sua candidatura).

**Risco:** a versão original era mais honesta sobre a timeline. Se um recrutador perguntar "por que 7 anos de faculdade?", a resposta está na seção Formação, não no Perfil.

### 5. Telefone

Você forneceu **(00) 00000-0000**. Adicionei ao cabeçalho.

### 6. Em-dashes e en-dashes

**Asserts no script proíbem em-dash (—) e en-dash (–)** por causa da regra de estilo do AGENTS.md. Substituí todos por:
- Dois-pontos em títulos de formação: "Bacharelado em Ciência da Computação: UFPA"
- Hífen com espaços em datas: "Jul 2025 - Atual"

**Risco:** ATS moderno lê ambos sem problema. A regra é estética/profissional, não técnica.

---

## 9 regras de honestidade (auditoria)

O handoff original lista 13 regras. Fiz um checklist do que está honrado no DOCX:

| # | Regra | Status no DOCX |
|---|---|---|
| 1 | Datas UFPA: abr/2017 a jan/2024, colação mar/2024 | ✅ Formação |
| 2 | Datas empregos: itexto 20/10/2021 a 25/04/2025; iUsecase 10/07/2025 a atual | ✅ "Out 2021 - Abr 2025" e "Jul 2025 - Atual" |
| 3 | Cargos CTPS: itexto=Programador (CBO 3171-10), iUsecase=Desenvolvedor Backend Pleno 1 | ✅ Ambos explicitados no texto |
| 4 | jOOQ só no Live2U; Consol=JPA; Apontamento=QueryDSL | ✅ Habilidades diz "jOOQ (Live)"; Consol diz "Spring Data JPA"; Apontamento diz "QueryDSL" |
| 5 | GraphQL é cliente (QR-Capital) | ✅ Habilidades: "GraphQL (cliente via graphql-java-generator)"; Fintech: "como cliente GraphQL" |
| 6 | Spring AI/pgvector/TTS/HLS não são produção | ✅ Não aparecem no DOCX |
| 7 | RAG no Live2U é orquestração frontend, backend externo (Sys3) | ✅ Live2U bullet explicita: "O backend de IA é externo (operado pela Sys3)" |
| 8 | Multi-tenant Apontamento é parcial | ✅ Apontamento bullet: "Refatoração parcial: timelogging migrado, Initiative/Workbook/Sprint ainda pendentes (dívida documentada)" |
| 9 | Suporte itexto = aplicações em produção | ✅ Transversais: "Suporte a aplicações em produção com diagnóstico de defeitos" |
| 10 | Comunicação = técnica estruturada a pares | ⚠️ Não aparece no DOCX. Não inventei soft skills section. |
| 11 | App revisão espaçada = estilo SM-2 (não canônico) | ⚠️ Não aparece (foi cortado com os estudos autorais) |
| 12 | Benchmark = evidência preliminar (n=1) | ✅ IA bullet: "oferecendo evidência preliminar sobre quando delegar a subagents" |
| 13 | Exclusões (SNS, Micronaut, Azure, Iveco, "milhares de usuários", birôs, Gateway, Chain of Responsibility) | ✅ Nenhum desses termos aparece |

**Conclusão da auditoria:** 11/13 honradas. As 2 não aplicadas (10 e 11) foram cortadas por decisão de espaço, não por violação.

---

## Pontos fracos para você questionar

### A. Compactação excessiva em 2 páginas?

A fonte 9.5pt e o line spacing 1.05 são agressivos. Se você preferir mais legibilidade humana (mesmo trocando limite de páginas), dá para ir a 10pt + 1.15 spacing e deixar 3 páginas, ou cortar mais conteúdo.

### B. Corte de cursos foi profundo

Dos ~20 cursos do briefing, só 8 entraram. Cortei:
- Spring JWT Security, Mastering Camel (Spring avançado)
- Java Collections, Modern Java in Action, Java Reactive, DSCatalog, Formação Java Alura
- Vue.js, Vue Mastery, Angular Alura, Node.js IGTI
- Análise de BD, Docker para Devs
- Inglês (curso em andamento)
- Estudos de Java Efetivo, Padrões de Projeto, DDD, Kafka livro

Se algum desses é importante para a vaga específica que você vai tentar, me diz qual e reabro.

### C. Não tem seção de Idiomas

A Alura recomenda. O briefing menciona Inglês em andamento (2025). Cortei. Se quiser, volto com uma linha "Inglês: leitura técnica, curso em andamento (2025)".

### D. Não tem seção de Soft Skills

A Alura recomenda. Você tem material rico no discovery.md (escuta ativa, pensamento metódico, senso crítico, humildade intelectual). Cortei para priorizar conteúdo técnico. Se quiser, volto com 3-4 bullets curtos.

### E. Resumo do Perfil pode estar descalibrado

A versão estilo Alura é mais "vendável" mas menos honesta sobre a timeline. Valide se a omissão do "período pandêmico" no topo não vai te pegar mal em entrevista.

### F. Não validei com análise visual

Tentei usar `analyze_image` nas previews PNG das páginas, mas a API não retornou resultado útil. Minha validação foi estrutural (extração de texto via `pdftotext -layout`), não visual. Você deve abrir o `curriculo_ats.pdf` e confirmar que o layout está visualmente bom.

---

## Como reproduzir

```bash
cd /home/usuario/projetos/template/first_decision
python3 gerar_curriculo_ats.py              # gera o DOCX
libreoffice --headless --convert-to pdf curriculo_ats.docx   # PDF de cortesia
```

O script tem assertions TDD inline que falham ruidosamente se:
- Falta seção obrigatória (PERFIL, HABILIDADES, EXPERIÊNCIA, FORMAÇÃO, FORMAÇÃO COMPLEMENTAR, IA COMO EIXO)
- Tiver tabelas de layout
- Faltar keyword ATS (Java, Spring Boot, PostgreSQL, Clean Architecture, CQRS, UFPA)
- Faltar telefone ou e-mail
- Tiver em-dash ou en-dash

---

## Próximos passos sugeridos (decida)

1. Abrir `curriculo_ats.pdf` e validar visualmente.
2. Decidir se aceita o corte de cursos ou se quer reabrir a lista.
3. Decidir se adiciona seção Idiomas e/ou Soft Skills.
4. Se aprovado, o DOCX está pronto para submeter em portais de RH.

Se quiser ajustar, edite `gerar_curriculo_ats.py` e rode novamente. O script é idempotente.
