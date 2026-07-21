# Briefing para Geração de Currículo — Candidato Nome Completo

> Documento consolidado para envio a LLM externo gerar currículo final.
> Foco: **Desenvolvedor Backend Pleno (Java/Spring)** com perfil full stack.
> Tom: profissional, direto, honesto, sem inflação. Linguagem em português brasileiro.

---

## DADOS PESSOAIS

- **Nome:** Candidato Nome Completo
- **Cargo-alvo:** Engenheiro de Software Pleno (pretensões: Desenvolvedor Backend Pleno e Full Stack Pleno)
- **Endereço:** Cidade, UF
- **E-mail:** candidato.exemplo@dominio.com
- **GitHub:** github.com/seu-usuario
- **LinkedIn:** linkedin.com/in/seu-perfil/
- **Portfólio:** seu-portfolio.com/portfolio/seu-usuario

---

## PERFIL (resumo para o topo)

Engenheiro de Software Pleno com quase 5 anos de experiência em desenvolvimento Full Stack, com passagem por sete domínios de negócio distintos (agronegócio, fintech, logística, automotivo, gamificação corporativa, compliance e educação). Foco em Java/Spring, design de código, arquitetura limpa e aplicação crítica de IA no desenvolvimento. Bacharel em Ciência da Computação pela UFPA (2024), concluído em paralelo à atuação profissional iniciada em 2021 e ao período pandêmico.

---

## FORMAÇÃO ACADÊMICA

**Bacharelado em Ciência da Computação** — Universidade Federal do Pará (UFPA)
- Período: abril de 2017 a janeiro de 2024 (conclusão)
- Colação de grau: março de 2024
- Diploma emitido em julho de 2024 (Belém/PA), registro nº 3.209, Livro ICEN-01/24, Folha 29
- Concluído em paralelo à atuação profissional iniciada em 2021 e ao período pandêmico, o que estendeu o ciclo total para aproximadamente 7 anos.

---

## EXPERIÊNCIA PROFISSIONAL

### Engenheiro de Software Pleno — iUsecase Tecnologia e Inovação
**Julho de 2025 – atual · Belo Horizonte, MG (remoto)**

Atuação em três produtos com foco em design de código e arquitetura limpa.

**Consol — Sistema de fiscalização e vistoria de malha rodoviária (case principal)**
- Backend Spring Boot 3.2 com Java 21 em Clean Architecture com CQRS-lite (leitura por QueryService com `@Cacheable` seletivo, escrita por Commands via ports).
- Spring Data JPA com hibernate-spatial/JTS para geometria rodoviária.
- Sincronização offline-first no mobile com lock distribuído em Redis, detecção de conflito por timestamp e fallback degradado (consol-sync-api em Node/Express + WebSocket + Valkey).
- Frontend em React 19 com Vite, React Compiler e mapas em MapLibre.
- Auth em Cognito, mobile em Flutter.

**Apontamento — Sistema de timesheet multi-tenant**
- Arquitetura multi-tenant database-driven com policies configuráveis em banco (`policy` → `policy_rule` → `tenant_policy`, com `PolicyRuleLoader` e resolvers `@Cacheable` em Caffeine TTL 1h).
- Refatoração em andamento para eliminar condicionais de cliente (`isConsol`, `CONSOL_CNPJ`) do core: módulo de timelogging migrado, Initiative/Workbook/Sprint ainda pendentes.
- Spring Boot 3.2 com Java 17, QueryDSL para queries dinâmicas, Angular 17.

**Live2U — Sistema de clínicas e saúde**
- Orquestração no frontend Angular de um serviço externo de RAG sobre exames, com upload de PDF, jobs assíncronos com polling e respostas com citações atreladas às observações de cada exame (`QuestionResponse.citations` → `examId`/`observationId`).
- Backend Spring Boot 3.2 com Java 21, jOOQ, integrações com serviços de saúde e upload de imagens (Cloudinary).
- O backend da IA (`ai-api.live2u.com.br`, operado pela Sys3) é externo; o trabalho do candidato foi a integração e orquestração no frontend.

**Atividades transversais:**
- Desenvolvimento e evolução de features backend em Spring Boot 3.2 (Java 17/21) com Clean Architecture e separação por camadas.
- Revisão de código no time.
- CI/CD em GitLab com deploy de imagens ARM64 para ECS via ECR (backend) e S3 com CloudFront (frontend).
- Cultura de testes com Testcontainers, AssertJ e WireMock.
- Suporte a aplicações em produção com diagnóstico de defeitos, correção de bugs e evolução de funcionalidades.
- Decisões de arquitetura que participou: seleção de abordagens multi-tenant, escolha entre JPA/QueryDSL/jOOQ por produto, modelagem de domínios complexos (inspeções rodoviárias, exames de saúde, apontamento de horas).

### Programador Full Stack — itexto Consultoria em Tecnologia
**Outubro de 2021 – abril de 2025 · Belo Horizonte, MG**

Atuação no ciclo completo de software em sete domínios de negócio (seis Java e um em Go).

**Agronegócio**
- Plataforma Ativus de crédito rural e análise de crédito (Spring Boot 2.3, Java 11, MySQL, Flyway, Angular 13), com gateway de CNDs governamentais orquestrado em Apache Camel e SQS.
- Sistema de barter agrícola da Corteva, dividido em barter (Spring Boot 2.5, Spring Cloud 2020.0.x com Eureka e Feign, Vue 2, PostgreSQL com Hibernate Envers, Keycloak OIDC) e solo (microsserviços Spring Boot 2.1/Spring Cloud Greenwich, Vue 2).

**Fintech**
- Tokenizadora de ativos (QR-Capital) como cliente GraphQL de API externa (graphql-java-generator + WebClient), com Spring Data JPA + Hibernate Envers sobre PostgreSQL, OAuth2/Keycloak, Spring Boot 2.7/Java 16.

**Logística**
- Marketplace de frete Flex-Frete com cotação, contratação, notas fiscais e mensageria em Camel e SQS; Spring Boot 2.5, PostgreSQL, Redis, React 17.

**Gamificação corporativa**
- Monorepo Weex (bwell) com múltiplos microsserviços, processamento assíncrono em Camel e SQS, geração de certificados em AWS Lambda e IaC com Terraform.

**Automotivo/industrial**
- Plataforma Wirelist (Starcom) de documentação técnica para montadoras (referências a Fiat), Spring Boot 2.2, MySQL, Elastic Beanstalk, Angular 15.

**Compliance**
- Sistema RRZ de gestão documental com assinatura/endosso e auditoria (Hibernate Envers), Spring Boot 3, Java 17, Angular 16.

**Educação**
- App de quizzes Wikle em Go com Gin (backend) e React Native/Expo (frontend).

**Atividades transversais na itexto:**
- Participação em todas as etapas: coleta de requisitos com o cliente, planejamento e criação de tarefas, elaboração de contratos de API com Swagger e UML das classes de domínio.
- Desenvolvimento backend (Java/Spring Boot e também Go) e frontend (Angular, React, Vue), com migrations SQL (PostgreSQL e MySQL), metodologia TDD e Clean Code.
- Integrações com APIs externas e S3, manipulação de planilhas com Apache POI, SQL nativo quando o JPQL não resolvia.
- Testes com JUnit e Mockito, deploy com Docker e Portainer.
- Pensamento crítico durante todo o processo, reportando dúvidas e soluções de comportamentos não mapeados ou desafios encontrados.
- Revisão de código com criticidade.
- Suporte a aplicações em produção com diagnóstico de defeitos.

---

## HABILIDADES TÉCNICAS

**Backend (JVM):** Java (11/16/17/21), Spring Boot (2.x e 3.x), Spring Data JPA, Spring Security, Spring Cloud (Eureka, Feign), Spring WebFlux.

**Persistência:** PostgreSQL, MySQL, Hibernate/JPA, Hibernate Envers (auditoria), hibernate-spatial + JTS (geometria), Flyway (migrations), QueryDSL (queries dinâmicas), jOOQ (Live), SQL nativo.

**Mensageria e Integração:** Apache Camel, AWS SQS, Redis (cache e pub/sub), Valkey, WebSocket (STOMP/SockJS).

**Frontend:** Angular (7/13/15/16/17/20), React (17/18/19), Vue 2, React Native/Expo, Flutter, Vite, Material/PrimeNG/MUI, MapLibre/Leaflet.

**Auth:** JWT (jjwt), Keycloak (OAuth2/OIDC), AWS Cognito.

**Cloud/DevOps:** AWS (S3, SQS, SES, ECS, ECR, CloudFront, Cognito, Lambda, Elastic Beanstalk, RDS), Cloudinary, Docker, Portainer, Terraform, GitLab CI/CD, Jenkins.

**Testes:** JUnit, Mockito, AssertJ, Testcontainers, WireMock, Cypress (E2E), Karma/Jasmine, Vitest, Jest.

**APIs e Contratos:** REST, OpenAPI/Swagger, GraphQL (cliente via graphql-java-generator), SOAP/WSDL.

**Documentos/Dados:** Apache POI (Excel), iText/PDFBox/html2pdf (PDF), OpenCSV, Commons CSV, Velocity (templates).

**Ferramentas de API:** Bruno, Postman, Insomnia (com scripts de asserção e encadeamento).

**Metodologia:** Kanban (Redmine, ClickUp).

**Observabilidade:** Sentry, Logstash, OpenTelemetry.

**IA aplicada:** benchmark de modelos de embedding para RAG (MRR, Recall@K, nDCG@10), engenharia agentic (Context Engineering, Skills, MCPs, Subagents).

---

## TRILHAS DE FORMAÇÃO COMPLEMENTAR

Organizadas por área. Todos os itens abaixo foram estudados de fato e são defensáveis em entrevista.

### Formação Java
- **Java Completo Programação Orientada a Objetos** — Udemy (junho/2021)
- **Java Collections** — Alura (2022)
- **Modern Java in Action** — livro Manning (2023)
- **Java Reactive / Project Reactor** — Udemy (2024)
- **DSCatalog Java REST com Spring** — DevSuperior (2022)
- **Formação Java Alura**: JPA, Spring, JSF (2022)

### Spring e ecossistema
- **Microservices do 0 com Spring Cloud, Spring Boot e Docker** — Udemy (outubro/2021) — Feign, Eureka, API Gateway, Circuit Breaker, Resilience4j, Config Server, LoadBalancer
- **Spring JWT Security** — estudo (2025)
- **Mastering Integration: Camel + Spring Boot** — masterspringboot.com (2022)

### Arquitetura e boas práticas
- **Jornada Dev Eficiente** — Dev Eficiente (2025, em andamento) — DDD, system design, escalabilidade, CDD, resiliência, testes
- **Desbravando SOLID em Java moderno** — livro (2024)
- **Apache Kafka e Spring Boot** — livro (2025, em andamento)
- **Tech Leads Club** (2026, em andamento) — Context Engineering, Skills, MCPs, padrões de Subagents e Multi-Agents
- **Java Efetivo (Effective Java)** — Joshua Bloch (estudo com anotações em Notion por capítulo: criação de objetos, métodos comuns, classes e interfaces)
- **Padrões de Projeto** — livro (estudo em Notion: criacionais, estruturais, comportamentais — Strategy, Chain of Responsibility, Template Method, State, Command, Observer, Adapter)
- **OAuth 2.0** — Casa do Código (livro)

### DDD e Arquitetura de Software (estudo aprofundado, material autoral)
- **DDD Estratégico**: design estratégico, identificação de domínios em código complexo
- **DDD Tático**: rich domain modeling, aggregates, value objects, use cases, domain services. Inclui reflexão sobre os limites do Transaction Script e quando migrar para DDD tático
- **Modular Architecture Principles** e feature folders vs feature modules
- **Feature Slice vs Vertical Slice**
- **Outbox Pattern** (estudo de fluxo)
- **C4 Model** para modelagem e documentação de arquitetura
- **Design Docs** como prática
- **Metrics**: coesão, acoplamento e métricas de código
- **Refatoração com IA** para DDD (plano de migração Transaction Script → DDD tático com memória de longo prazo)

### Mensageria e sistemas distribuídos (estudo)
- **Kafka**: tópicos, partições, consumer groups, offsets, retenção de log. Comparativo Kafka vs SQS/SNS
- **RabbitMQ, AWS SQS/SNS, Redis Streams** como alternativas de message broker
- **Fundamentos da escalabilidade** (estudo autoral em Notion)
- **Performance benchmark** em sistemas distribuídos

### Frontend (complementar)
- **Desenvolvedor Frontend** — IGTI/XP (maio/2022) — Vue.js, Angular, React, Svelte
- **Desenvolvedor Node.js** — IGTI/XP (novembro/2022) — REST API com Express, GraphQL, Jest
- **Vue.js** — Alura (2022)
- **Vue Mastery** — vuemastery (setembro/2022) — Vue 3, Composition API, Pinia, Vite, Vitest
- **Angular (Trilha Alura)** — Alura (outubro/2022)

### Backend Java complementar (anotações em Notion)
- **Java Platform Evolution** (evolução das versões Java)
- **Hibernate** (estudo aprofundado)
- **Apache Camel** (rotas e integrações)
- **SOAP com Feign** (integração legada)
- **GraphQL em Java** (definição de servidor, cliente, schema, consultas)

### Demais
- **Docker para Desenvolvedores** — Udemy (outubro/2021)
- **Análise de Banco de Dados** — IGTI/XP (setembro/2022) — PostgreSQL, SQL Server, Oracle
- **Go (Golang): Explorando a Linguagem do Google** — Udemy (maio/2024, em andamento)
- **Inglês** — curso próprio (2025, em andamento)

### Estudos autorais (textos próprios, não cursos)
- **Reflexões sobre carreira e IA**: "Realidade no uso de IA na programação", "Dívida cognitiva e o uso de IA", "Como a IA impacta o desenvolvimento de habilidades", "LLM Benchmarks: vale combinar múltiplos modelos?", "Fragments" (anotações reflexivas recorrentes).
- **Estudo comparativo Solo vs Subagents** em code review (com métricas).
- **App de revisão espaçada** próprio (algoritmo estilo SM-2 em Bun) com decks sobre Aggregate DDD, Outbox Pattern, Spec-Driven Development, harness engineering e vibe coding.

---

## IA COMO EIXO DE ESTUDO E APLICAÇÃO

- **Benchmark de modelos de embedding para RAG** em português e inglês, com corpus desenhado à mão (40 queries parafraseadas PT/EN, 45 documentos com hard negatives de propósito), qrels e métricas de retrieval (MRR, Recall@K, nDCG@10) em múltiplas execuções para controlar cold start. Comparação de 7 modelos (multilingual-e5 base e small, qwen3-embedding, mpnet, MiniLM, jina-code via llama.cpp, Ollama), testando instruction prefixes (query/passage) e latência. Conclusão documentada: e5-small superou qwen3 em MRR com 2,7x menos espaço e 14x mais velocidade.
- **Engenharia agentic**: estudo comparativo entre revisão solo versus plano e execução com subagents, com métricas (testes passando, iterações, critérios do desafio). Aplicação de Context Engineering (Spec Driven, RPI, Rules, Skills, MCPs) e padrões de Subagents e Multi-Agents.
- **Prática diária de desenvolvimento assistido por IA com revisão crítica**, com loop de feedback curto, TDD científico (caso falhando pelo motivo certo, fix mínimo, revert para confirmar red de novo, baby steps) e revisão humana do diff antes de commitar.

Material consolidado em notas próprias (Notion e repositórios de estudo).

---

## ORIENTAÇÕES PARA O LLM GERADOR

1. **Foco em Java:** o eixo do currículo é Java/Spring. Frontend, IA, Go e demais skills são complementares e não devem roubar a cena.
2. **Tom:** profissional, direto, sem hype. Sem adjetivação vazia ("apaixonado por tecnologia", "visionário", "líder natural").
3. **Honestidade técnica:** NÃO afirmar como implementação em produção o que é estudo. Especificamente:
   - Spring AI / pgvector / TTS / HLS **não** estão em código de produto; são estudo (benchmark de embeddings, Notion).
   - RAG no Live2U é **orquestração no frontend** consumindo serviço externo (ai-api.live2u.com.br, operado pela Sys3), não implementação do backend de IA.
   - GraphQL é consumido como **cliente** (QR-Capital), não implementado server-side.
   - jOOQ aparece apenas no Live; Consol usa Spring Data JPA; Apontamento usa QueryDSL.
   - Refatoração multi-tenant do Apontamento está **parcial**: timelogging migrado, Initiative/Workbook/Sprint ainda pendentes (dívida documentada).
4. **Cargo:** "Engenheiro de Software Pleno" como título no topo, com pretensões "Desenvolvedor Backend Pleno" e "Full Stack Pleno".
5. **Cargo formal na CTPS:** itexto como "Programador" (CBO 3171-10) e iUsecase como "Desenvolvedor Backend Pleno 1" (CBO 2124-05). A descrição de função "Full Stack" e "Engenheiro de Software" reflete o escopo real exercido, comum em consultorias brasileiras onde o cargo formal fica defasado.
6. **Cursos e estudos:** incluir todos os itens das trilhas acima. Marcar "(em andamento)" quando aplicável. Não inventar cursos adicionais. Material de estudo (DDD, mensageria, anotações autorais) pode ser agrupado numa seção "Estudos complementares" ou incorporado às habilidades, desde que não inflado para "experiência em produção".
7. **Layout:** sugerir estrutura em 1 a 2 páginas, com seções claras (Perfil, Habilidades, Experiência, Formação, Cursos, IA). Não incluir foto, idade, estado civil, pretensão salarial.
8. **Idioma:** português brasileiro. Sem em-dashes (usar pontos, vírgulas ou dois-pontos).
9. **Não inventar dados:** datas, nomes de empresa e stacks são reais e foram validados contra código, CTPS, diploma e Notion.

---

## FONTES CONSULTADAS

- **Documentos pessoais:** CTPS digital (datas e cargos), diploma UFPA (transcrição via OCR).
- **Código dos projetos:** `/media/fsm/fsm/backup_fsm_source_only/itexto/` (7 projetos) e `/home/usuario/usecase/` (3 produtos: Consol, Apontamento, Live2U).
- **Estudos locais:** `/home/usuario/Meus-estudos/` (cursos, livros, projetos próprios).
- **Notion (workspace do usuário):** página "💻 Tech" e seus 23 filhos, 3 databases (IA, Desenvolvimento Assistido por IA, Arquitetura evolutivas tech leads), além de páginas autorais sobre carreira, IA e arquitetura.
