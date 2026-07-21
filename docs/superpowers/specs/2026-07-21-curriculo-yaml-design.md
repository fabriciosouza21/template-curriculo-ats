# Design: Currículo Configurável via YAML

**Data:** 2026-07-21
**Status:** Especificação para aprovação
**Autor:** Candidato Nome Completo + ZCode (brainstorming)

## 1. Problema

Hoje o projeto tem dois scripts Python que duplicam conteúdo:

- `gerar_curriculo_ats.py` — variante ATS genérica
- `zup/zup_curriculo_backend.py` — variante para vaga Zup Backend Java

Cada nova vaga gera um script novo, com texto reescrito à mão. O conteúdo canônico (experiências, skills, cursos) vive hardcoded em cada script, o que produz:

- **Duplicação**: o mesmo bullet do Consol aparece em dois arquivos com pequenas variações.
- **Drift**: correções feitas num script não se propagam para o outro.
- **Atrito**: adaptar o currículo para uma vaga nova exige reescrever Python, não apenas selecionar conteúdo.

## 2. Objetivo

Separar **dados** (fonte de verdade canônica em YAML) de **apresentação** (gerador Python + seleção por vaga). Um agente LLM, dado a descrição de uma vaga, deve conseguir selecionar sozinho quais itens do YAML entram no currículo final e gerar o DOCX.

## 3. Decisões firmadas (das perguntas)

1. **Escopo do YAML**: tudo. Pessoa, perfil, habilidades, experiências, formação, cursos, idiomas e seção de IA. Fonte de verdade completa.
2. **Fluxo do agente**: agente decide tudo a partir da descrição da vaga. Sem pré-aprovação item a item.
3. **Matching**: sem tags pré-modeladas. O agente lê a descrição da vaga, extrai keywords dela e casa contra o texto natural dos itens (descrição do case, nome da skill, etc.).
4. **Verbos nos bullets**: YAML guarda texto final polido, com o verbo já escolhido. Sem override dinâmico. O agente seleciona e ordena, não reescreve.
5. **Habilidades**: lista plana por bucket. Sem metadados (anos de uso, último uso) na primeira versão.

## 4. Estrutura de arquivos (Abordagem C — híbrido)

```
curriculo/
├── data/
│   ├── index.yml              # manifesto: lista arquivos na ordem de composição
│   ├── perfil.yml             # pessoa + contato + parágrafos de perfil
│   ├── habilidades.yml        # buckets de skills
│   ├── cursos.yml             # cursos
│   ├── idiomas.yml            # idiomas
│   ├── formacao.yml           # formação acadêmica
│   ├── ia.yml                 # seção "IA como eixo de estudo"
│   └── experiencias/
│       ├── iusecase.yml       # uma empresa por arquivo
│       └── itexto.yml
├── docs/superpowers/specs/    # este documento
└── [scripts geradores — ver seção 8]
```

**Por que híbrido:**

- Experiências são o núcleo vivo do currículo. Crescem com o tempo, variam entre vagas, e adicionar empresa nova não deve mexer no resto. Por isso ganham diretório próprio, um arquivo por empresa.
- Seções estáveis (pessoa, perfil, formação, idiomas) mudam pouco e ficam em arquivos únicos.
- Habilidades e cursos são listas que crescem mas não têm a complexidade de uma experiência. Arquivo único resolve.
- `index.yml` serve de índice para o agente saber o que existe sem listar diretório.

## 5. Schema detalhado

### 5.1 `data/index.yml`

```yaml
versao: 1
perfil: perfil.yml
habilidades: habilidades.yml
experiencias:
  - experiencias/iusecase.yml
  - experiencias/itexto.yml
formacao: formacao.yml
cursos: cursos.yml
idiomas: idiomas.yml
ia: ia.yml
```

### 5.2 `data/perfil.yml`

```yaml
pessoa:
  nome: Candidato Nome Completo
  cargo_apresentacao: Engenheiro de Software Pleno
  contato:
    telefone: "(00) 00000-0000"
    email: candidato.exemplo@dominio.com
    localizacao: Cidade, UF
    linkedin: linkedin.com/in/seu-perfil/
    github: github.com/seu-usuario
    portfolio: seu-portfolio.com/portfolio/seu-usuario

perfil:
  # Lista de parágrafos. O agente pode selecionar ou combinar.
  - >
    Engenheiro de Software Pleno com 5 anos de experiência em
    desenvolvimento Full Stack focado em Java/Spring, Clean Architecture
    e design de código. Passagem por sete domínios de negócio distintos
    (agronegócio, fintech, logística, automotivo, gamificação corporativa,
    compliance e educação). Bacharel em Ciência da Computação pela UFPA
    (2024).
```

### 5.3 `data/habilidades.yml`

```yaml
# Lista de buckets. Cada bucket tem um rótulo e uma lista de skills
# como strings simples. O agente pode reordenar buckets e reescrever
# o agrupamento conforme a vaga.
buckets:
  - rotulo: Backend (JVM)
    itens:
      - "Java (11/16/17/21)"
      - "Spring Boot (2.x e 3.x)"
      - "Spring Data JPA"
      - "Spring Security"
      - "Spring Cloud (Eureka, Feign)"
      - "Spring WebFlux"

  - rotulo: Persistência
    itens:
      - "PostgreSQL"
      - "MySQL"
      - "Hibernate/JPA"
      - "Hibernate Envers"
      - "hibernate-spatial + JTS"
      - "Flyway"
      - "QueryDSL"
      - "jOOQ"
      - "SQL nativo"

  - rotulo: Mensageria
    itens:
      - "Apache Camel"
      - "AWS SQS"
      - "Redis (cache e pub/sub)"
      - "Valkey"
      - "WebSocket (STOMP/SockJS)"

  # ...demais buckets (Frontend, Auth, Cloud/DevOps, Testes, APIs, Observabilidade)
```

### 5.4 `data/experiencias/iusecase.yml`

Schema canônico para uma empresa:

```yaml
empresa: iUsecase Tecnologia e Inovação
cargo: Desenvolvedor Backend Pleno 1            # cargo CTPS (formal)
cargo_apresentacao: Engenheiro de Software Pleno # cargo no cabeçalho (opcional)
periodo:
  inicio: 2025-07
  fim: atual
local: Belo Horizonte, MG (remoto)
contexto: >
  Atuação remota em três produtos com foco em design de código
  e arquitetura limpa.

cases:
  - produto: Consol
    dominio: fiscalização de malha rodoviária
    destaque: true    # prioridade máxima: entra sempre salvo incompatibilidade
                      # forte com a vaga (ex.: case backend em vaga só mobile)
    descricao: >
      Backend em Spring Boot 3.2 e Java 21 em Clean Architecture com
      CQRS-lite (leitura por QueryService com @Cacheable, escrita por
      Commands via ports), Spring Data JPA com hibernate-spatial/JTS
      para geometria rodoviária. Sincronização offline-first mobile
      com lock distribuído em Redis e fallback degradado (consol-sync-api
      em Node/Express + WebSocket + Valkey). Frontend em React 19 com
      Vite e mapas MapLibre. Auth em Cognito. Mobile em Flutter.

  - produto: Apontamento
    dominio: timesheet multi-tenant
    descricao: >
      Arquitetura multi-tenant database-driven com policies configuráveis
      em banco (policy, policy_rule, tenant_policy) e resolvers @Cacheable
      em Caffeine TTL 1h. Migração do módulo de timelogging para eliminar
      condicionais de cliente. Initiative/Workbook/Sprint ainda pendentes
      (dívida documentada). Spring Boot 3.2 com Java 17, QueryDSL e
      Angular 17.

  - produto: Live2U
    dominio: clínicas e saúde
    descricao: >
      Orquestração no frontend Angular de serviço externo de RAG sobre
      exames, com upload de PDF, jobs assíncronos com polling e respostas
      com citações atreladas às observações de cada exame. Backend Spring
      Boot 3.2 com Java 21, jOOQ e integrações com serviços de saúde.
      Backend de IA externo (Sys3); meu trabalho foi orquestração e
      integração.

transversais:
  - >
    CI/CD em GitLab com deploy de imagens ARM64 para ECS via ECR
    (backend) e S3 com CloudFront (frontend). Colaborei em cultura de
    testes com Testcontainers, AssertJ e WireMock, revisão de código
    no time e suporte a aplicações em produção com diagnóstico de
    defeitos.
```

**Campos obrigatórios por empresa:** `empresa`, `cargo`, `periodo`, `contexto`, `cases`.
**Opcionais:** `cargo_apresentacao`, `local`, `transversais`.
**Campos por case:** `produto`, `descricao` (obrigatórios); `dominio`, `destaque` (opcionais).

### 5.5 `data/experiencias/itexto.yml`

Mesmo schema. Casos: Agronegócio (Ativus + Corteva), Fintech (QR-Capital), Logística (Flex-Frete), Gamificação corporativa (Weex), Automotivo/industrial (Wirelist), Compliance (RRZ), Educação (Wikle). Mais `transversais` com o ciclo completo.

### 5.6 `data/cursos.yml`

```yaml
cursos:
  - rotulo: Java
    descricao: "Udemy (jun/2021). Java Completo Programação Orientada a Objetos."
  - rotulo: "Spring/Cloud"
    descricao: >
      Udemy (out/2021). Microservices do 0 com Spring Cloud, Spring Boot
      e Docker. Feign, Eureka, API Gateway, Circuit Breaker, Resilience4j.
  # ...demais cursos
```

### 5.7 `data/idiomas.yml`

```yaml
idiomas:
  - idioma: Português
    nivel: Nativo
  - idioma: Inglês
    nivel: >
      Leitura técnica fluente para documentação, papers e issue trackers.
      Curso em andamento (2025).
```

### 5.8 `data/formacao.yml`

```yaml
formacao:
  - curso: Bacharelado em Ciência da Computação
    instituicao: Universidade Federal do Pará (UFPA)
    periodo:
      inicio: 2017-04
      fim: 2024-01
    detalhes: >
      Conclusão em janeiro de 2024, colação de grau em março de 2024.
      Diploma emitido em julho de 2024 (Belém/PA), registro nº 3.209,
      Livro ICEN-01/24, Folha 29. Concluído em paralelo à atuação
      profissional iniciada em 2021 e ao período pandêmico.
```

### 5.9 `data/ia.yml`

```yaml
# Seção "IA como Eixo de Estudo e Aplicação".
# Itens com rotulo + descricao. O agente decide se a seção entra
# (depende da vaga mencionar IA) e quais itens.
itens:
  - rotulo: "RAG com rigor experimental"
    descricao: >
      Benchmark próprio de modelos de embedding para RAG em português e
      inglês, com corpus desenhado à mão (40 queries parafraseadas,
      45 documentos com hard negatives de propósito) e métricas de
      retrieval (MRR, Recall@K, nDCG@10) em múltiplas execuções.
      Comparação de 7 modelos. Conclusão: e5-small superou qwen3 em MRR
      com 2,7x menos espaço e 14x mais velocidade.
  # ...demais itens (Engenharia agentic, Desenvolvimento assistido por IA)
```

## 6. Regras de honestidade (vindas do handoff)

O YAML é a fonte de verdade. As regras abaixo sãostraints de conteúdo que precisam valer nos dados, não apenas no gerador:

1. **jOOQ só no Live2U.** A skill "jOOQ" em `habilidades.yml` é legítima, mas na descrição do case só pode aparecer em Live2U. Casos Consol e Apontamento não mencionam jOOQ.
2. **Backend de IA externo no Live2U.** A descrição do case Live2U deixa explícito que o backend de IA é externo (Sys3); meu trabalho foi orquestração.
3. **Dívida documentada no Apontamento.** A migração multi-tenant está parcial: timelogging migrado, Initiative/Workbook/Sprint pendentes.
4. **Cargo CTPS vs cargo de apresentação.** iUsecase: CTPS "Desenvolvedor Backend Pleno 1", cabeçalho "Engenheiro de Software Pleno". Os dois campos existem para refletir isso sem falsear.
5. **Sem em-dashes.** Estilo do AGENTS.md. Aplica no texto do YAML.

## 7. Como o agente usa o YAML

Dado o prompt "gere currículo para vaga X", o agente executa:

1. **Lê a descrição da vaga** e extrai keywords (stack, domínio, senioridade, requeridos vs desejáveis).
2. **Carrega `index.yml`** e a partir dele abre os arquivos relevantes.
3. **Seleciona experiências e cases**: para cada empresa em ordem cronológica reversa, decide:
   - A empresa entra? (se a vaga é backend Java, ambas entram; se é frontend só, talvez só uma.)
   - Quais cases entram? Cases `destaque: true` têm prioridade máxima (entram salvo incompatibilidade forte com a vaga). Os demais entram se casarem com as keywords.
   - Os `transversais` entram? O agente decide caso a caso; não há regra de "pelo menos um".
4. **Seleciona habilidades**: para cada bucket, decide se o bucket entra (alguns podem ser descartados, ex.: Frontend em vaga backend) e em que ordem.
5. **Seleciona cursos**: prioriza os que casam com as keywords.
6. **Decide sobre IA e Idiomas**: se a vaga menciona IA/RAG/LLM, a seção IA entra; senão sai. Idiomas geralmente entra sempre.
7. **Gera o DOCX** via script Python que recebe um manifesto de seleção (JSON intermediário) e renderiza.

**Formato do manifesto de seleção (JSON intermediário):**

```json
{
  "vaga": "Descrição ou identificador da vaga",
  "perfil": ["parágrafo 1 selecionado"],
  "experiencias": [
    {
      "arquivo": "experiencias/iusecase.yml",
      "cases": ["Consol", "Live2U"],
      "transversais": [0]
    }
  ],
  "habilidades": ["Backend (JVM)", "Persistência"],
  "cursos": ["Java", "Spring/Cloud"],
  "idiomas": true,
  "ia": ["RAG com rigor experimental"]
}
```

`transversais: [0]` significa "primeiro item do array transversais da empresa". Índices, não texto, para evitar ambiguidade de paráfrase.

O manifesto é propositalmente auditável. Se o resultado não te agrada, você edita o JSON e regera sem rodar o agente de novo.

## 8. Geradores

Esta spec cobre apenas a modelagem YAML. A migração dos scripts Python existentes para consumir o YAML fica num plano de implementação posterior (skill `writing-plans`).

Decisão prévia para o plano: o gerador vai ser **um único script** parametrizado por manifesto de seleção, substituindo os dois scripts atuais. As variantes por vaga passam a ser manifestos, não scripts.

## 9. Fora de escopo (YAGNI explícito)

- Tags pré-modeladas nos itens. Matching é semântico.
- Metadados de skill (anos de uso, último uso).
- Override dinâmico de verbos por vaga.
- Variantes pré-definidas no YAML (perfil "backend", perfil "fullstack"). O agente cria o perfil sob demanda a partir da vaga.
- Schema JSON formal. O YAML é validado por assertions no gerador (campos obrigatórios, tipos básicos via `pydantic` ou checagens manuais), não por JSON Schema separado. Se a complexidade crescer, introduzimos JSON Schema depois.
- Versionamento semântico do YAML. `versao: 1` no index é informativo.

## 10. Critérios de sucesso

1. Os arquivos YAML em `data/` contêm todo o conteúdo hoje espalhado entre `gerar_curriculo_ats.py` e `zup_curriculo_backend.py`, sem perda.
2. Um humano consegue ler `data/experiencias/iusecase.yml` e entender a passagem pela empresa sem abrir o script Python.
3. Regras de honestidade da seção 6 estão refletidas no conteúdo dos YAMLs.
4. O `index.yml` lista todos os arquivos e serve de índice navegável.
5. O YAML passa num lint básico (sintaxe válida, campos obrigatórios presentes em cada experiência).
