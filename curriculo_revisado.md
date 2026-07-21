# CANDIDATO NOME COMPLETO
### Engenheiro de Software Pleno

**CONTATO**
- Endereço: Cidade, UF
- E-mail: candidato.exemplo@dominio.com
- GitHub: github.com/seu-usuario
- LinkedIn: linkedin.com/in/seu-perfil/
- Portfólio: seu-portfolio.com/portfolio/seu-usuario

---

## PERFIL

Engenheiro de Software Pleno com quase 5 anos de experiência em desenvolvimento Full Stack, com passagem por sete domínios de negócio distintos (agronegócio, fintech, logística, automotivo, gamificação corporativa, compliance e educação). Foco em design de código, arquitetura limpa, e aplicação de IA no desenvolvimento com senso crítico. Bacharel em Ciência da Computação pela UFPA (2024), concluído em paralelo à atuação profissional iniciada em 2021 e ao período pandêmico.

---

## HABILIDADES

**Backend:** Java (11/16/17/21), Spring Boot (2.x e 3.x), Spring Data JPA, Spring Cloud (Eureka, Feign), Spring WebFlux.
**Persistência:** PostgreSQL, MySQL, Hibernate/JPA, Hibernate Envers, hibernate-spatial/JTS, Flyway, QueryDSL, jOOQ, SQL nativo.
**Mensageria e Integração:** Apache Camel, AWS SQS, Redis (cache e pub/sub), Valkey, WebSocket (STOMP/SockJS).
**Frontend:** Angular (7/13/15/16/17/20), React (17/18/19), Vue 2, React Native/Expo, Flutter, Vite.
**Auth:** JWT (jjwt), Keycloak (OAuth2/OIDC), AWS Cognito.
**Cloud/DevOps:** AWS (S3, SQS, SES, ECS, ECR, CloudFront, Cognito, Lambda, Elastic Beanstalk, RDS), Cloudinary, Docker, Portainer, Terraform, GitLab CI/CD, Jenkins.
**Testes:** JUnit, Mockito, AssertJ, Testcontainers, WireMock, Cypress, Karma/Jasmine, Vitest, Jest.
**APIs e Contratos:** REST, OpenAPI/Swagger, GraphQL (cliente via graphql-java-generator), SOAP/WSDL.
**Ferramentas de API:** Bruno, Postman, Insomnia (scripts de asserção e encadeamento).
**Metodologia:** Kanban (Redmine, ClickUp).
**Observabilidade:** Sentry, Logstash, OpenTelemetry.
**IA aplicada:** benchmark de modelos de embedding (MRR, Recall@K, nDCG@10), engenharia agentic (Context Engineering, Skills, MCPs, Subagents).

---

## EXPERIÊNCIA

### Engenheiro de Software Pleno — iUsecase Tecnologia e Inovação
*Julho 2025 – atual · Belo Horizonte, MG (remoto)*

Atuação em três produtos com foco em design de código e arquitetura limpa.

- **Consol** (sistema de fiscalização de malha rodoviária) — meu case principal. Spring Boot 3.2 com Java 21 em Clean Architecture e CQRS-lite (leitura por QueryService com `@Cacheable` seletivo, escrita por Commands via ports), Spring Data JPA com hibernate-spatial/JTS para geometria rodoviária, sincronização offline-first no mobile com lock distribuído em Redis, detecção de conflito por timestamp e fallback degradado (consol-sync-api em Node/Express + WebSocket + Valkey). Frontend em React 19 com Vite, React Compiler e mapas em MapLibre, auth em Cognito, mobile em Flutter.
- **Apontamento** (sistema de timesheet multi-tenant) — arquitetura multi-tenant database-driven com policies configuráveis em banco (`policy` → `policy_rule` → `tenant_policy`, com `PolicyRuleLoader` e resolvers `@Cacheable` em Caffeine TTL 1h), em refatoração para eliminar condicionais de cliente (`isConsol`, `CONSOL_CNPJ`) do core: timelogging migrado, Initiative/Workbook/Sprint ainda pendentes. Spring Boot 3.2 com Java 17, QueryDSL e Angular 17.
- **Live2U** (sistema de clínicas e saúde) — orquestração no frontend Angular de um serviço externo de RAG sobre exames, com upload de PDF, jobs assíncronos com polling e respostas com citações atreladas às observações de cada exame. Backend Spring Boot 3.2 com Java 21, jOOQ e integrações com serviços de saúde.

Atividades transversais: desenvolvimento e evolução de features backend, revisão de código no time, CI/CD em GitLab com deploy de imagens ARM64 para ECS via ECR (backend) e S3 com CloudFront (frontend), cultura de testes com Testcontainers, AssertJ e WireMock, e suporte a aplicações em produção com diagnóstico de defeitos.

### Programador Full Stack — itexto Consultoria em Tecnologia
*Outubro 2021 – abril 2025 · Belo Horizonte, MG*

Atuação no ciclo completo de software em sete domínios de negócio (seis Java e um em Go).

- **Agronegócio** — Plataforma Ativus de crédito rural e análise de crédito (Spring Boot 2.3, Java 11, MySQL, Flyway, Angular 13), com gateway de CNDs governamentais orquestrado em Apache Camel e SQS; e sistema de barter agrícola da Corteva, dividido em barter (Spring Boot 2.5, Spring Cloud 2020.0.x com Eureka e Feign, Vue 2, PostgreSQL com Hibernate Envers, Keycloak OIDC) e solo (microsserviços Spring Boot 2.1/Spring Cloud Greenwich, Vue 2).
- **Fintech** — Tokenizadora de ativos (QR-Capital) como cliente GraphQL de API externa (graphql-java-generator + WebClient), com Spring Data JPA + Hibernate Envers sobre PostgreSQL, OAuth2/Keycloak, Spring Boot 2.7/Java 16.
- **Logística** — Marketplace de frete Flex-Frete com cotação, contratação, notas fiscais e mensageria em Camel e SQS; Spring Boot 2.5, PostgreSQL, Redis, React 17.
- **Gamificação corporativa** — Monorepo Weex (bwell) com múltiplos microsserviços, processamento assíncrono em Camel e SQS, geração de certificados em AWS Lambda e IaC com Terraform.
- **Automotivo/industrial** — Plataforma Wirelist (Starcom) de documentação técnica para montadoras, Spring Boot 2.2, MySQL, Elastic Beanstalk, Angular 15.
- **Compliance** — Sistema RRZ de gestão documental com assinatura/endosso e auditoria (Hibernate Envers), Spring Boot 3, Java 17, Angular 16.
- **Educação** — App de quizzes Wikle em Go com Gin e React Native/Expo.

Participação em todas as etapas: coleta de requisitos, planejamento e criação de tarefas, elaboração de contratos de API com Swagger e UML das classes de domínio, desenvolvimento backend e frontend em Angular, React e Vue, integrações com APIs externas e S3, manipulação de planilhas com Apache POI, SQL nativo quando o JPQL não resolvia, testes com JUnit e Mockito, deploy com Docker e Portainer, e suporte a aplicações em produção.

---

## FORMAÇÃO

**Bacharelado em Ciência da Computação** — Universidade Federal do Pará (UFPA)
*Abril 2017 – janeiro 2024 (conclusão); colação de grau em março de 2024*

Concluído em paralelo à atuação profissional iniciada em 2021 na itexto e ao período pandêmico. Ênfase em ferramentas tecnológicas, metodologias computacionais, automação de processos, protocolos de comunicação e modelagem de dados.

---

## CURSOS

- **Desenvolvimento Assistido por IA** — Tech Leads Club (2026, em curso): Context Engineering, Skills, MCPs, padrões de Subagents e Multi-Agents.
- **Go (Golang): Explorando a Linguagem do Google** — Udemy (maio/2024).
- **Microservices do 0 com Spring Cloud, Spring Boot e Docker** — Udemy (outubro/2021): Feign, Eureka, API Gateway, Circuit Breaker, Resilience4j, Config Server, LoadBalancer.
- **Docker para Desenvolvedores** — Udemy (outubro/2021).
- **Desenvolvedor Node.js** — IGTI/XP (novembro/2022): REST API com Express, GraphQL, Jest.
- **Desenvolvedor Frontend** — IGTI/XP (maio/2022): Vue.js, Angular, React, Svelte.
- **Vue Mastery** — vuemastery (setembro/2022): Vue 3, Composition API, Pinia, Vite, Vitest.
- **Angular (Trilha Alura)** — Alura (outubro/2022): formulários, autenticação, lazy loading.
- **Análise de Banco de Dados** — IGTI/XP (setembro/2022): PostgreSQL, SQL Server, Oracle.
- **Java Completo Programação Orientada a Objetos** — Udemy (junho/2021).
- **React e Next** — Udemy (junho/2021).

---

## IA COMO EIXO DE ESTUDO E APLICAÇÃO

- **Benchmark de modelos de embedding** para RAG em português e inglês, com corpus desenhado à mão (40 queries, 45 documentos com hard negatives), métricas de retrieval (MRR, Recall@K, nDCG@10) em múltiplas execuções. Comparação de 7 modelos. Conclusão: e5-small superou qwen3 em MRR com 2,7x menos espaço e 14x mais velocidade.
- **Engenharia agentic**: estudo comparativo solo vs subagents com métricas, Context Engineering (Spec Driven, RPI, Rules, Skills, MCPs).
- **Prática diária de desenvolvimento assistido por IA com revisão crítica**, loop de feedback curto, TDD científico e revisão humana do diff antes de commitar.

Material consolidado em notas próprias (Notion e repositórios de estudo).
