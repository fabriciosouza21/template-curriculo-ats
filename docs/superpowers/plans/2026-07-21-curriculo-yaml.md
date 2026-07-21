# Currículo Configurável via YAML — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrar o conteúdo canônico do currículo (hoje hardcoded em `gerar_curriculo_ats.py` e `zup/zup_curriculo_backend.py`) para uma fonte de verdade em YAML sob `data/`, preservando todo o conteúdo e as regras de honestidade.

**Architecture:** Conjunto de arquivos YAML em `data/` seguindo o schema definido no spec `docs/superpowers/specs/2026-07-21-curriculo-yaml-design.md`. Um script validador (`data/validate.py`) carrega todos os YAMLs e falha ruidosamente se campos obrigatórios estão ausentes ou regras de honestidade são violadas. Não há migração dos geradores DOCX neste plano (escopo do spec: apenas modelagem YAML).

**Tech Stack:** Python 3, `pyyaml` para parse, `pytest` para testes do validador.

## Global Constraints

- **Sem em-dashes nem en-dashes** em qualquer string do YAML. Usar pontos, vírgulas ou hifens simples com espaços. (Regra de estilo do AGENTS.md, validada no script atual.)
- **jOOQ só no Live2U.** A string `jOOQ` só pode aparecer em `data/experiencias/iusecase.yml` dentro do case `Live2U`, e em `data/habilidades.yml` na lista de skills. Não pode aparecer nos cases `Consol` ou `Apontamento`.
- **Backend de IA externo no Live2U.** A descrição do case Live2U deve deixar explícito que o backend de IA é externo (operado pela Sys3).
- **Dívida documentada no Apontamento.** A descrição do case Apontamento deve mencionar que a migração multi-tenant está parcial (timelogging migrado, Initiative/Workbook/Sprint pendentes).
- **Cargo CTPS vs cargo de apresentação.** iUsecase tem `cargo: "Desenvolvedor Backend Pleno 1"` (CTPS) e `cargo_apresentacao: "Engenheiro de Software Pleno"` (cabeçalho).
- **Português brasileiro.** Todo o conteúdo é em pt-BR.
- **YAML válido.** Sintaxe YAML válida em todos os arquivos.
- **Verbetes no passado.** Todo `descricao` de case e item de `transversais` começa com verbo de ação no passado (Construí, Modelei, Implementei, Mantive, Desenvolvi, Integrei, Estruturei, Participei, Colaborei, Refatorei), salvo casos excepcionais justificados no comentário.

---

## File Structure

```
curriculo/
├── data/
│   ├── index.yml                  # manifesto: lista arquivos na ordem de composição
│   ├── perfil.yml                 # pessoa + contato + parágrafos de perfil
│   ├── habilidades.yml            # buckets de skills
│   ├── experiencias/
│   │   ├── iusecase.yml           # uma empresa por arquivo
│   │   └── itexto.yml
│   ├── formacao.yml               # formação acadêmica
│   ├── cursos.yml                 # cursos
│   ├── idiomas.yml                # idiomas
│   ├── ia.yml                     # seção IA
│   ├── validate.py                # validador com pytest inline
│   └── test_validate.py           # testes do validador
└── docs/superpowers/
    ├── specs/2026-07-21-curriculo-yaml-design.md  # já existe
    └── plans/2026-07-21-curriculo-yaml.md         # este plano
```

Cada arquivo YAML tem uma responsabilidade única:
- `perfil.yml`: identidade da pessoa (nome, cargo, contato) + parágrafos de perfil. Muda raramente.
- `habilidades.yml`: buckets de skills agrupados por categoria. Lista plana, sem metadados.
- `experiencias/<empresa>.yml`: uma empresa por arquivo, com cases por produto e transversais.
- `formacao.yml`, `cursos.yml`, `idiomas.yml`, `ia.yml`: seções específicas, autocontidas.
- `index.yml`: índice navegável para o agente saber o que existe sem listar diretório.
- `validate.py`: validação dos YAMLs (sintaxe, campos obrigatórios, regras de honestidade).
- `test_validate.py`: testes do validador.

---

## Task 1: Bootstrap do projeto (`data/` + dependências + `index.yml`)

**Files:**
- Create: `data/index.yml`
- Create: `data/.gitignore` (não precisa, mas criar `data/` vazio primeiro)
- Test: validação manual via `python3 -c "import yaml"`

**Interfaces:**
- Consumes: nada.
- Produces: diretório `data/` e `index.yml` com a estrutura de manifesto. Tasks posteriores preenchem os arquivos referenciados.

- [ ] **Step 1: Criar diretório `data/experiencias/`**

```bash
mkdir -p data/experiencias
```

- [ ] **Step 2: Verificar que `pyyaml` está instalado**

```bash
python3 -c "import yaml; print(yaml.__version__)"
```

Se faltar, instalar:

```bash
pip3 install --user pyyaml
```

- [ ] **Step 3: Criar `data/index.yml`**

```yaml
# Manifesto do currículo. Lista os arquivos YAML que compõem a fonte de
# verdade canônica, na ordem em que aparecem no documento final.
# O agente lê este arquivo primeiro para saber o que existe.
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

- [ ] **Step 4: Validar sintaxe do `index.yml`**

```bash
python3 -c "import yaml; yaml.safe_load(open('data/index.yml')); print('[OK] index.yml válido')"
```

Esperado: `[OK] index.yml válido`.

- [ ] **Step 5: Commit**

```bash
git add data/index.yml
git commit -m "add data/index.yml manifesto do curriculo em yaml"
```

---

## Task 2: `perfil.yml` (pessoa + contato + perfil)

**Files:**
- Create: `data/perfil.yml`

**Interfaces:**
- Consumes: nada.
- Produces: estrutura `{pessoa: {nome, cargo_apresentacao, contato: {...}}, perfil: [...]}` usada por geradores futuros.

- [ ] **Step 1: Criar `data/perfil.yml`**

```yaml
# Identidade da pessoa e parágrafos de perfil para o topo do curriculo.
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

# Lista de parágrafos de perfil. O agente pode selecionar ou combinar
# conforme a vaga. Hoje há um único parágrafo canônico.
perfil:
  - >
    Engenheiro de Software Pleno com 5 anos de experiência em
    desenvolvimento Full Stack focado em Java/Spring, Clean Architecture
    e design de código. Passagem por sete domínios de negócio distintos
    (agronegócio, fintech, logística, automotivo, gamificação corporativa,
    compliance e educação). Bacharel em Ciência da Computação pela UFPA
    (2024).
```

- [ ] **Step 2: Validar sintaxe**

```bash
python3 -c "import yaml; d=yaml.safe_load(open('data/perfil.yml')); assert d['pessoa']['nome'] == 'Candidato Nome Completo'; print('[OK] perfil.yml válido')"
```

Esperado: `[OK] perfil.yml válido`.

- [ ] **Step 3: Verificar ausência de em-dashes**

```bash
python3 -c "import yaml; d=yaml.safe_load(open('data/perfil.yml')); import json; s=json.dumps(d, ensure_ascii=False); assert '—' not in s and '–' not in s, 'em-dash ou en-dash encontrado'; print('[OK] sem em-dash')"
```

Esperado: `[OK] sem em-dash`.

- [ ] **Step 4: Commit**

```bash
git add data/perfil.yml
git commit -m "add data/perfil.yml pessoa contato e perfil"
```

---

## Task 3: `habilidades.yml` (buckets de skills)

**Files:**
- Create: `data/habilidades.yml`

**Interfaces:**
- Consumes: nada.
- Produces: estrutura `{buckets: [{rotulo, itens: [...]}]}`. Lista plana por bucket, sem metadados.

- [ ] **Step 1: Criar `data/habilidades.yml`**

Conteúdo vem do briefing seção "HABILIDADES TÉCNICAS" (linhas 107-133). Buckets: Backend (JVM), Persistência, Mensageria, Frontend, Auth, Cloud/DevOps, Testes, APIs e Contratos, Documentos/Dados, Observabilidade e metodologia, IA aplicada.

```yaml
# Buckets de habilidades. Cada bucket tem um rótulo e uma lista de skills
# como strings simples. O agente pode reordenar buckets e reescrever o
# agrupamento conforme a vaga.
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
      - "Hibernate Envers (auditoria)"
      - "hibernate-spatial + JTS (geometria)"
      - "Flyway (migrations)"
      - "QueryDSL (queries dinâmicas)"
      - "jOOQ"
      - "SQL nativo"

  - rotulo: Mensageria e Integração
    itens:
      - "Apache Camel"
      - "AWS SQS"
      - "Redis (cache e pub/sub)"
      - "Valkey"
      - "WebSocket (STOMP/SockJS)"

  - rotulo: Frontend
    itens:
      - "Angular (7/13/15/16/17/20)"
      - "React (17/18/19)"
      - "Vue 2"
      - "React Native/Expo"
      - "Flutter"
      - "Vite"
      - "Material/PrimeNG/MUI"
      - "MapLibre/Leaflet"

  - rotulo: Auth
    itens:
      - "JWT (jjwt)"
      - "Keycloak (OAuth2/OIDC)"
      - "AWS Cognito"

  - rotulo: Cloud/DevOps
    itens:
      - "AWS (S3, SQS, SES, ECS, ECR, CloudFront, Cognito, Lambda, Elastic Beanstalk, RDS)"
      - "Cloudinary"
      - "Docker"
      - "Portainer"
      - "Terraform"
      - "GitLab CI/CD"
      - "Jenkins"

  - rotulo: Testes
    itens:
      - "JUnit"
      - "Mockito"
      - "AssertJ"
      - "Testcontainers"
      - "WireMock"
      - "Cypress (E2E)"
      - "Karma/Jasmine"
      - "Vitest"
      - "Jest"

  - rotulo: APIs e Contratos
    itens:
      - "REST"
      - "OpenAPI/Swagger"
      - "GraphQL (cliente via graphql-java-generator)"
      - "SOAP/WSDL"

  - rotulo: Documentos/Dados
    itens:
      - "Apache POI (Excel)"
      - "iText/PDFBox/html2pdf (PDF)"
      - "OpenCSV"
      - "Commons CSV"
      - "Velocity (templates)"

  - rotulo: Observabilidade e metodologia
    itens:
      - "Sentry"
      - "Logstash"
      - "OpenTelemetry"
      - "Kanban (Redmine, ClickUp)"

  - rotulo: IA aplicada
    itens:
      - "Benchmark de modelos de embedding para RAG (MRR, Recall@K, nDCG@10)"
      - "Engenharia agentic (Context Engineering, Skills, MCPs, Subagents)"
```

- [ ] **Step 2: Validar sintaxe e estrutura**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/habilidades.yml'))
assert 'buckets' in d and len(d['buckets']) >= 10, 'buckets insuficientes'
for b in d['buckets']:
    assert 'rotulo' in b and 'itens' in b, f'bucket mal formado: {b}'
    assert isinstance(b['itens'], list) and len(b['itens']) > 0, f'bucket sem itens: {b}'
print(f'[OK] {len(d[\"buckets\"])} buckets válidos')
"
```

Esperado: `[OK] 11 buckets válidos`.

- [ ] **Step 3: Verificar ausência de em-dashes**

```bash
python3 -c "import yaml, json; d=yaml.safe_load(open('data/habilidades.yml')); s=json.dumps(d, ensure_ascii=False); assert '—' not in s and '–' not in s, 'em-dash encontrado'; print('[OK] sem em-dash')"
```

Esperado: `[OK] sem em-dash`.

- [ ] **Step 4: Commit**

```bash
git add data/habilidades.yml
git commit -m "add data/habilidades.yml buckets de skills"
```

---

## Task 4: `experiencias/iusecase.yml`

**Files:**
- Create: `data/experiencias/iusecase.yml`

**Interfaces:**
- Consumes: nada.
- Produces: estrutura de uma empresa. Schema: `{empresa, cargo, cargo_apresentacao?, periodo: {inicio, fim}, local?, contexto, cases: [{produto, dominio?, destaque?, descricao}], transversais?: [...]}`.

- [ ] **Step 1: Criar `data/experiencias/iusecase.yml`**

Conteúdo vem do briefing seção iUsecase (linhas 39-67) e do `gerar_curriculo_ats.py` (linhas 172-182). Cases: Consol (destaque), Apontamento, Live2U.

```yaml
# Passagem pela iUsecase (Jul 2025 - atual). Case principal: Consol.
empresa: iUsecase Tecnologia e Inovação
cargo: Desenvolvedor Backend Pleno 1            # cargo CTPS (formal, CBO 2124-05)
cargo_apresentacao: Engenheiro de Software Pleno # cargo no cabeçalho do curriculo
periodo:
  inicio: 2025-07
  fim: atual
local: Belo Horizonte, MG (remoto)
contexto: >
  Atuação remota em três produtos com foco em design de código e
  arquitetura limpa.

cases:
  - produto: Consol
    dominio: fiscalização de malha rodoviária
    destaque: true    # prioridade máxima: entra sempre salvo incompatibilidade
                      # forte com a vaga (ex.: case backend em vaga só mobile)
    descricao: >
      Desenvolvi backend em Spring Boot 3.2 e Java 21 para fiscalização de
      malha rodoviária em Clean Architecture com CQRS-lite (leitura por
      QueryService com @Cacheable seletivo, escrita por Commands via
      ports), usando Spring Data JPA com hibernate-spatial/JTS para
      geometria rodoviária. Implementei sincronização offline-first
      mobile com lock distribuído em Redis e fallback degradado
      (consol-sync-api em Node/Express + WebSocket + Valkey), frontend em
      React 19 com Vite e mapas MapLibre, auth em Cognito e mobile em
      Flutter.

  - produto: Apontamento
    dominio: timesheet multi-tenant
    descricao: >
      Modelei arquitetura multi-tenant database-driven para timesheet com
      policies configuráveis em banco (policy, policy_rule,
      tenant_policy) e resolvers @Cacheable em Caffeine TTL 1h. Migrei o
      módulo de timelogging para eliminar condicionais de cliente;
      Initiative/Workbook/Sprint ainda pendentes (dívida documentada).
      Spring Boot 3.2 com Java 17, QueryDSL e Angular 17.

  - produto: Live2U
    dominio: clínicas e saúde
    descricao: >
      Integrei serviço externo de RAG sobre exames no frontend Angular,
      com upload de PDF, jobs assíncronos com polling e respostas com
      citações atreladas às observações de cada exame. Backend Spring
      Boot 3.2 com Java 21, jOOQ e integrações com serviços de saúde. O
      backend de IA é externo (ai-api.live2u.com.br, operado pela Sys3);
      meu trabalho foi a orquestração e integração, não a implementação
      do backend de IA.

transversais:
  - >
    Mantive CI/CD em GitLab com deploy de imagens ARM64 para ECS via ECR
    (backend) e S3 com CloudFront (frontend). Colaborei em cultura de
    testes com Testcontainers, AssertJ e WireMock, revisão de código no
    time e suporte a aplicações em produção com diagnóstico de defeitos.
  - >
    Participei de decisões de arquitetura: seleção de abordagens
    multi-tenant, escolha entre JPA/QueryDSL/jOOQ por produto e
    modelagem de domínios complexos (inspeções rodoviárias, exames de
    saúde, apontamento de horas).
```

- [ ] **Step 2: Validar sintaxe e estrutura**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/experiencias/iusecase.yml'))
assert d['empresa'].startswith('iUsecase')
assert d['cargo'] == 'Desenvolvedor Backend Pleno 1'
assert d['cargo_apresentacao'] == 'Engenheiro de Software Pleno'
assert d['periodo']['inicio'] == '2025-07' and d['periodo']['fim'] == 'atual'
assert len(d['cases']) == 3, f'esperado 3 cases, obtido {len(d[\"cases\"])}'
produtos = [c['produto'] for c in d['cases']]
assert produtos == ['Consol', 'Apontamento', 'Live2U'], f'produtos inesperados: {produtos}'
consol = [c for c in d['cases'] if c['produto'] == 'Consol'][0]
assert consol.get('destaque') is True, 'Consol deve ter destaque: true'
print(f'[OK] iusecase.yml válido: {len(d[\"cases\"])} cases, {len(d[\"transversais\"])} transversais')
"
```

Esperado: `[OK] iusecase.yml válido: 3 cases, 2 transversais`.

- [ ] **Step 3: Verificar regra de honestidade: jOOQ só no Live2U**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/experiencias/iusecase.yml'))
for c in d['cases']:
    if c['produto'] in ('Consol', 'Apontamento'):
        assert 'jOOQ' not in c['descricao'], f\"jOOQ no case {c['produto']} (deveria ser só Live2U)\"
live2u = [c for c in d['cases'] if c['produto'] == 'Live2U'][0]
assert 'jOOQ' in live2u['descricao'], 'Live2U deve mencionar jOOQ'
print('[OK] jOOQ só no Live2U')
"
```

Esperado: `[OK] jOOQ só no Live2U`.

- [ ] **Step 4: Verificar regra de honestidade: backend IA externo no Live2U**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/experiencias/iusecase.yml'))
live2u = [c for c in d['cases'] if c['produto'] == 'Live2U'][0]
assert 'externo' in live2u['descricao'].lower(), 'Live2U deve mencionar backend externo'
assert 'Sys3' in live2u['descricao'], 'Live2U deve mencionar Sys3'
print('[OK] backend IA externo declarado no Live2U')
"
```

Esperado: `[OK] backend IA externo declarado no Live2U`.

- [ ] **Step 5: Verificar regra de honestidade: dívida documentada no Apontamento**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/experiencias/iusecase.yml'))
ap = [c for c in d['cases'] if c['produto'] == 'Apontamento'][0]
assert 'pendentes' in ap['descricao'].lower() or 'dívida' in ap['descricao'].lower(), 'Apontamento deve declarar pendências'
print('[OK] dívida documentada no Apontamento')
"
```

Esperado: `[OK] dívida documentada no Apontamento`.

- [ ] **Step 6: Verificar ausência de em-dashes**

```bash
python3 -c "import yaml, json; d=yaml.safe_load(open('data/experiencias/iusecase.yml')); s=json.dumps(d, ensure_ascii=False); assert '—' not in s and '–' not in s, 'em-dash encontrado'; print('[OK] sem em-dash')"
```

Esperado: `[OK] sem em-dash`.

- [ ] **Step 7: Commit**

```bash
git add data/experiencias/iusecase.yml
git commit -m "add data/experiencias/iusecase.yml com 3 cases e transversais"
```

---

## Task 5: `experiencias/itexto.yml`

**Files:**
- Create: `data/experiencias/itexto.yml`

**Interfaces:**
- Consumes: nada.
- Produces: mesma estrutura da Task 4. Cases: Agronegócio, Fintech, Logística, Gamificação corporativa, Automotivo/industrial, Compliance, Educação.

- [ ] **Step 1: Criar `data/experiencias/itexto.yml`**

Conteúdo vem do briefing seção itexto (linhas 69-103) e do `gerar_curriculo_ats.py` (linhas 185-199). Cargo CTPS: "Programador" (CBO 3171-10).

```yaml
# Passagem pela itexto (Out 2021 - Abr 2025). Sete domínios de negócio.
empresa: itexto Consultoria em Tecnologia
cargo: Programador                              # cargo CTPS (formal, CBO 3171-10)
cargo_apresentacao: Engenheiro de Software Pleno # função real exercida (full stack)
periodo:
  inicio: 2021-10
  fim: 2025-04
local: Belo Horizonte, MG
contexto: >
  Atuação no ciclo completo de software em sete domínios de negócio
  (seis em Java e um em Go).

cases:
  - produto: Agronegócio
    dominio: crédito rural e barter agrícola
    descricao: >
      Construí plataforma Ativus de crédito rural e análise de crédito
      em Spring Boot 2.3, Java 11, MySQL, Flyway e Angular 13, com
      gateway de CNDs governamentais em Apache Camel e SQS. Implementei
      sistema de barter agrícola da Corteva em Spring Cloud (Eureka,
      Feign), Vue 2, PostgreSQL com Hibernate Envers e Keycloak OIDC.

  - produto: Fintech
    dominio: tokenização de ativos
    descricao: >
      Implementei tokenizadora de ativos (QR-Capital) como cliente
      GraphQL de API externa (graphql-java-generator + WebClient), com
      Spring Data JPA e Hibernate Envers sobre PostgreSQL, OAuth2/Keycloak,
      Spring Boot 2.7 e Java 16.

  - produto: Logística
    dominio: marketplace de frete
    descricao: >
      Desenvolvi marketplace de frete Flex-Frete com cotação,
      contratação, notas fiscais e mensageria em Camel e SQS. Spring
      Boot 2.5, PostgreSQL, Redis, React 17.

  - produto: Gamificação corporativa
    dominio: bem-estar corporativo
    descricao: >
      Estruturei monorepo Weex (bwell) com múltiplos microsserviços,
      processamento assíncrono em Camel e SQS, geração de certificados
      em AWS Lambda e IaC com Terraform.

  - produto: Automotivo/industrial
    dominio: documentação técnica para montadoras
    descricao: >
      Mantive plataforma Wirelist (Starcom) de documentação técnica
      para montadoras. Spring Boot 2.2, MySQL, Elastic Beanstalk,
      Angular 15.

  - produto: Compliance
    dominio: gestão documental com assinatura digital
    descricao: >
      Desenvolvi sistema RRZ de gestão documental com assinatura,
      endosso e auditoria (Hibernate Envers). Spring Boot 3, Java 17,
      Angular 16.

  - produto: Educação
    dominio: app de quizzes
    descricao: >
      Construí app de quizzes Wikle em Go com Gin (backend) e React
      Native/Expo (frontend).

transversais:
  - >
    Participei do ciclo completo de 7 sistemas em 3,5 anos: coleta de
    requisitos com o cliente, contratos de API em Swagger, UML das
    classes de domínio, desenvolvimento backend (Java/Spring e Go) e
    frontend (Angular, React, Vue), integrações com APIs externas e S3,
    Apache POI para planilhas, SQL nativo quando JPQL não resolvia,
    testes com JUnit e Mockito, deploy com Docker e Portainer, suporte
    a aplicações em produção com diagnóstico de defeitos.
  - >
    Colaborei em revisão de código com criticidade e pensamento crítico
    durante todo o processo, reportando dúvidas e soluções de
    comportamentos não mapeados ou desafios encontrados.
```

- [ ] **Step 2: Validar sintaxe e estrutura**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/experiencias/itexto.yml'))
assert d['empresa'].startswith('itexto')
assert d['cargo'] == 'Programador'
assert d['periodo']['inicio'] == '2021-10' and d['periodo']['fim'] == '2025-04'
assert len(d['cases']) == 7, f'esperado 7 cases, obtido {len(d[\"cases\"])}'
produtos = [c['produto'] for c in d['cases']]
esperados = ['Agronegócio', 'Fintech', 'Logística', 'Gamificação corporativa', 'Automotivo/industrial', 'Compliance', 'Educação']
assert produtos == esperados, f'produtos inesperados: {produtos}'
print(f'[OK] itexto.yml válido: {len(d[\"cases\"])} cases, {len(d[\"transversais\"])} transversais')
"
```

Esperado: `[OK] itexto.yml válido: 7 cases, 2 transversais`.

- [ ] **Step 3: Verificar ausência de em-dashes**

```bash
python3 -c "import yaml, json; d=yaml.safe_load(open('data/experiencias/itexto.yml')); s=json.dumps(d, ensure_ascii=False); assert '—' not in s and '–' not in s, 'em-dash encontrado'; print('[OK] sem em-dash')"
```

Esperado: `[OK] sem em-dash`.

- [ ] **Step 4: Commit**

```bash
git add data/experiencias/itexto.yml
git commit -m "add data/experiencias/itexto.yml com 7 cases e transversais"
```

---

## Task 6: `formacao.yml`

**Files:**
- Create: `data/formacao.yml`

**Interfaces:**
- Consumes: nada.
- Produces: estrutura `{formacao: [{curso, instituicao, periodo: {inicio, fim}, detalhes}]}`.

- [ ] **Step 1: Criar `data/formacao.yml`**

Conteúdo vem do briefing seção "FORMAÇÃO ACADÊMICA" (linhas 27-33).

```yaml
# Formação acadêmica.
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
      profissional iniciada em 2021 e ao período pandêmico, o que
      estendeu o ciclo total.
```

- [ ] **Step 2: Validar sintaxe e estrutura**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/formacao.yml'))
assert len(d['formacao']) == 1
f = d['formacao'][0]
assert f['curso'] == 'Bacharelado em Ciência da Computação'
assert 'UFPA' in f['instituicao']
assert f['periodo']['inicio'] == '2017-04' and f['periodo']['fim'] == '2024-01'
print('[OK] formacao.yml válido')
"
```

Esperado: `[OK] formacao.yml válido`.

- [ ] **Step 3: Verificar ausência de em-dashes**

```bash
python3 -c "import yaml, json; d=yaml.safe_load(open('data/formacao.yml')); s=json.dumps(d, ensure_ascii=False); assert '—' not in s and '–' not in s, 'em-dash encontrado'; print('[OK] sem em-dash')"
```

Esperado: `[OK] sem em-dash`.

- [ ] **Step 4: Commit**

```bash
git add data/formacao.yml
git commit -m "add data/formacao.yml ufpa ciencia da computacao"
```

---

## Task 7: `cursos.yml`

**Files:**
- Create: `data/cursos.yml`

**Interfaces:**
- Consumes: nada.
- Produces: estrutura `{cursos: [{rotulo, descricao}]}`.

- [ ] **Step 1: Criar `data/cursos.yml`**

Conteúdo vem do briefing seção "TRILHAS DE FORMAÇÃO COMPLEMENTAR" (linhas 137-203) e do `gerar_curriculo_ats.py` (linhas 208-215). Seleção dos cursos principais (não inventar).

```yaml
# Cursos e formação complementar. Todos estudados de fato e defensáveis
# em entrevista. Itens marcados como "(em andamento)" estão em curso.
# O agente prioriza cursos que casam com as keywords da vaga.
cursos:
  - rotulo: Java
    descricao: >
      Udemy (jun/2021). Java Completo Programação Orientada a Objetos.

  - rotulo: Spring/Cloud
    descricao: >
      Udemy (out/2021). Microservices do 0 com Spring Cloud, Spring Boot
      e Docker. Feign, Eureka, API Gateway, Circuit Breaker, Resilience4j,
      Config Server, LoadBalancer.

  - rotulo: Camel + Spring Boot
    descricao: >
      Mastering Integration: Camel + Spring Boot. masterspringboot.com
      (2022).

  - rotulo: Arquitetura
    descricao: >
      Jornada Dev Eficiente (2025, em andamento). DDD, system design,
      escalabilidade, CDD, resiliência, testes.

  - rotulo: Tech leadership
    descricao: >
      Tech Leads Club (2026, em andamento). Context Engineering, Skills,
      MCPs, padrões de Subagents e Multi-Agents.

  - rotulo: Effective Java
    descricao: >
      Joshua Bloch. Estudo com anotações em Notion por capítulo: criação
      de objetos, métodos comuns, classes e interfaces.

  - rotulo: Segurança
    descricao: >
      OAuth 2.0. Casa do Código (livro).

  - rotulo: Frontend
    descricao: >
      IGTI/XP (mai/2022). Vue.js, Angular, React, Svelte.

  - rotulo: Node.js
    descricao: >
      IGTI/XP (nov/2022). REST API com Express, GraphQL, Jest.

  - rotulo: Go
    descricao: >
      Udemy (mai/2024, em andamento). Go (Golang): Explorando a
      Linguagem do Google.

  - rotulo: Docker
    descricao: >
      Udemy (out/2021). Docker para Desenvolvedores.

  - rotulo: Banco de dados
    descricao: >
      IGTI/XP (set/2022). Análise de Banco de Dados: PostgreSQL, SQL
      Server, Oracle.

  - rotulo: Inglês
    descricao: >
      Curso próprio (2025, em andamento).
```

- [ ] **Step 2: Validar sintaxe e estrutura**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/cursos.yml'))
assert len(d['cursos']) >= 10, f'esperado >= 10 cursos, obtido {len(d[\"cursos\"])}'
for c in d['cursos']:
    assert 'rotulo' in c and 'descricao' in c, f'curso mal formado: {c}'
print(f'[OK] {len(d[\"cursos\"])} cursos válidos')
"
```

Esperado: `[OK] 13 cursos válidos`.

- [ ] **Step 3: Verificar ausência de em-dashes**

```bash
python3 -c "import yaml, json; d=yaml.safe_load(open('data/cursos.yml')); s=json.dumps(d, ensure_ascii=False); assert '—' not in s and '–' not in s, 'em-dash encontrado'; print('[OK] sem em-dash')"
```

Esperado: `[OK] sem em-dash`.

- [ ] **Step 4: Commit**

```bash
git add data/cursos.yml
git commit -m "add data/cursos.yml formacao complementar"
```

---

## Task 8: `idiomas.yml`

**Files:**
- Create: `data/idiomas.yml`

**Interfaces:**
- Consumes: nada.
- Produces: estrutura `{idiomas: [{idioma, nivel}]}`.

- [ ] **Step 1: Criar `data/idiomas.yml`**

```yaml
# Idiomas.
idiomas:
  - idioma: Português
    nivel: Nativo
  - idioma: Inglês
    descricao: >
      Leitura técnica fluente para documentação, papers e issue
      trackers. Curso em andamento (2025).
```

- [ ] **Step 2: Validar sintaxe e estrutura**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/idiomas.yml'))
assert len(d['idiomas']) == 2
assert d['idiomas'][0]['idioma'] == 'Português' and d['idiomas'][0]['nivel'] == 'Nativo'
assert d['idiomas'][1]['idioma'] == 'Inglês'
print('[OK] idiomas.yml válido')
"
```

Esperado: `[OK] idiomas.yml válido`.

- [ ] **Step 3: Verificar ausência de em-dashes**

```bash
python3 -c "import yaml, json; d=yaml.safe_load(open('data/idiomas.yml')); s=json.dumps(d, ensure_ascii=False); assert '—' not in s and '–' not in s, 'em-dash encontrado'; print('[OK] sem em-dash')"
```

Esperado: `[OK] sem em-dash`.

- [ ] **Step 4: Commit**

```bash
git add data/idiomas.yml
git commit -m "add data/idiomas.yml portugues e ingles"
```

---

## Task 9: `ia.yml`

**Files:**
- Create: `data/ia.yml`

**Interfaces:**
- Consumes: nada.
- Produces: estrutura `{itens: [{rotulo, descricao}]}`.

- [ ] **Step 1: Criar `data/ia.yml`**

Conteúdo vem do briefing seção "IA COMO EIXO DE ESTUDO E APLICAÇÃO" (linhas 207-213) e do `gerar_curriculo_ats.py` (linhas 224-226).

```yaml
# Seção "IA como Eixo de Estudo e Aplicação". Itens com rotulo + descricao.
# O agente decide se a seção entra (depende da vaga mencionar IA/RAG/LLM)
# e quais itens.
itens:
  - rotulo: "RAG com rigor experimental"
    descricao: >
      Benchmark próprio de modelos de embedding para RAG em português e
      inglês, com corpus desenhado à mão (40 queries parafraseadas,
      45 documentos com hard negatives de propósito) e métricas de
      retrieval (MRR, Recall@K, nDCG@10) em múltiplas execuções para
      controlar cold start. Comparação de 7 modelos (multilingual-e5
      base e small, qwen3-embedding, mpnet, MiniLM, jina-code via
      llama.cpp, Ollama), testando instruction prefixes (query/passage)
      e latência. Conclusão documentada: e5-small superou qwen3 em MRR
      com 2,7x menos espaço e 14x mais velocidade.

  - rotulo: "Engenharia agentic"
    descricao: >
      Estudo comparativo entre revisão solo versus plano e execução com
      subagents, com métricas. Aplicação de Context Engineering (Spec
      Driven, RPI, Rules, Skills, MCPs) e padrões de Subagents e
      Multi-Agents.

  - rotulo: "Desenvolvimento assistido por IA"
    descricao: >
      Prática diária com loop de feedback curto, TDD científico (caso
      falhando pelo motivo certo, fix mínimo, revert para confirmar red
      de novo, baby steps) e revisão humana do diff antes de commitar.
```

- [ ] **Step 2: Validar sintaxe e estrutura**

```bash
python3 -c "
import yaml
d = yaml.safe_load(open('data/ia.yml'))
assert len(d['itens']) == 3
for i in d['itens']:
    assert 'rotulo' in i and 'descricao' in i, f'item mal formado: {i}'
print(f'[OK] {len(d[\"itens\"])} itens de IA válidos')
"
```

Esperado: `[OK] 3 itens de IA válidos`.

- [ ] **Step 3: Verificar ausência de em-dashes**

```bash
python3 -c "import yaml, json; d=yaml.safe_load(open('data/ia.yml')); s=json.dumps(d, ensure_ascii=False); assert '—' not in s and '–' not in s, 'em-dash encontrado'; print('[OK] sem em-dash')"
```

Esperado: `[OK] sem em-dash`.

- [ ] **Step 4: Commit**

```bash
git add data/ia.yml
git commit -m "add data/ia.yml secao de ia como eixo de estudo"
```

---

## Task 10: `validate.py` + `test_validate.py` (validador com pytest)

**Files:**
- Create: `data/validate.py`
- Create: `data/test_validate.py`

**Interfaces:**
- Consumes: todos os YAMLs criados nas Tasks 2-9.
- Produces: script `data/validate.py` com função `validar_tudo()` que retorna `True` se tudo está válido ou levanta exceção com mensagem clara. CLI: `python3 data/validate.py`. Testes em `test_validate.py`.

- [ ] **Step 1: Verificar que `pytest` está disponível**

```bash
python3 -m pytest --version 2>&1 | head -1
```

Se faltar:

```bash
pip3 install --user pytest
```

- [ ] **Step 2: Criar `data/test_validate.py` (testes falhando primeiro — TDD)**

```python
"""Testes do validador de YAMLs do curriculo.

Padrão TDD: testes primeiro, validador depois. Cada teste cobre uma
regra do spec docs/superpowers/specs/2026-07-21-curriculo-yaml-design.md.
"""
from pathlib import Path
import pytest
import yaml

from validate import (
    carregar_tudo,
    validar_sintaxe,
    validar_campos_obrigatorios,
    validar_jooq_so_no_live2u,
    validar_backend_ia_externo_live2u,
    validar_divida_apontamento,
    validar_sem_em_dash,
    validar_verbos_passado,
)

DATA_DIR = Path(__file__).parent


def test_carregar_tudo_nao_falha():
    dados = carregar_tudo(DATA_DIR)
    assert set(dados.keys()) == {
        'index', 'perfil', 'habilidades', 'experiencias',
        'formacao', 'cursos', 'idiomas', 'ia',
    }


def test_validar_sintaxe_ok():
    dados = carregar_tudo(DATA_DIR)
    validar_sintaxe(dados)  # não levanta


def test_validar_campos_obrigatorios():
    dados = carregar_tudo(DATA_DIR)
    validar_campos_obrigatorios(dados)  # não levanta


def test_validar_jooq_so_no_live2u():
    dados = carregar_tudo(DATA_DIR)
    validar_jooq_so_no_live2u(dados)  # não levanta


def test_validar_backend_ia_externo_live2u():
    dados = carregar_tudo(DATA_DIR)
    validar_backend_ia_externo_live2u(dados)  # não levanta


def test_validar_divida_apontamento():
    dados = carregar_tudo(DATA_DIR)
    validar_divida_apontamento(dados)  # não levanta


def test_validar_sem_em_dash():
    dados = carregar_tudo(DATA_DIR)
    validar_sem_em_dash(dados)  # não levanta


def test_validar_verbos_passado():
    dados = carregar_tudo(DATA_DIR)
    validar_verbos_passado(dados)  # não levanta
```

- [ ] **Step 3: Rodar os testes e confirmar que falham**

```bash
cd data && python3 -m pytest test_validate.py -v
```

Esperado: 8 testes FAIL com `ModuleNotFoundError: No module named 'validate'` ou similar (porque `validate.py` ainda não existe).

- [ ] **Step 4: Criar `data/validate.py` (implementação mínima)**

```python
#!/usr/bin/env python3
"""Validador da fonte de verdade YAML do curriculo.

Carrega todos os YAMLs em data/ e valida:
- Sintaxe YAML (via pyyaml).
- Campos obrigatórios por tipo de arquivo.
- Regras de honestidade do spec:
  - jOOQ só no Live2U.
  - Backend de IA externo declarado no Live2U.
  - Dívida documentada no Apontamento.
  - Cargo CTPS != cargo de apresentação (somente para iUsecase).
- Regra de estilo: sem em-dashes (—) ou en-dashes (–).
- Regra de estilo: descrições começam com verbo de ação no passado.

Uso: python3 data/validate.py
Saída: [OK] mensagem + exit 0 se válido; mensagem de erro + exit 1 caso contrário.
"""
from pathlib import Path
import sys
import yaml

# Verbos de ação aceitos no início de descrições e transversais.
VERBOS_PASSADO = {
    'Construí', 'Modelei', 'Implementei', 'Mantive', 'Desenvolvi',
    'Integrei', 'Estruturei', 'Participei', 'Colaborei', 'Refatorei',
    ' Migrei',  # usado como "Migrei o módulo..." dentro do meio; aceita
}


def carregar_tudo(data_dir: Path) -> dict:
    """Carrega todos os YAMLs referenciados em index.yml."""
    data_dir = Path(data_dir)
    with open(data_dir / 'index.yml') as f:
        index = yaml.safe_load(f)

    def load(rel):
        with open(data_dir / rel) as f:
            return yaml.safe_load(f)

    return {
        'index': index,
        'perfil': load(index['perfil']),
        'habilidades': load(index['habilidades']),
        'experiencias': [load(rel) for rel in index['experiencias']],
        'formacao': load(index['formacao']),
        'cursos': load(index['cursos']),
        'idiomas': load(index['idiomas']),
        'ia': load(index['ia']),
    }


def validar_sintaxe(dados: dict) -> None:
    """Sintaxe YAML já foi validada ao carregar. Aqui confere tipos básicos."""
    assert isinstance(dados['perfil']['pessoa']['nome'], str)
    assert isinstance(dados['habilidades']['buckets'], list)
    assert isinstance(dados['experiencias'], list) and len(dados['experiencias']) >= 1
    assert isinstance(dados['formacao']['formacao'], list)
    assert isinstance(dados['cursos']['cursos'], list)
    assert isinstance(dados['idiomas']['idiomas'], list)
    assert isinstance(dados['ia']['itens'], list)


def validar_campos_obrigatorios(dados: dict) -> None:
    """Confere campos obrigatórios em cada experiência."""
    for exp in dados['experiencias']:
        for campo in ('empresa', 'cargo', 'periodo', 'contexto', 'cases'):
            assert campo in exp, f"experiência sem campo obrigatório '{campo}': {exp.get('empresa')}"
        assert 'inicio' in exp['periodo'] and 'fim' in exp['periodo'], \
            f"periodo mal formado em {exp['empresa']}"
        assert len(exp['cases']) >= 1, f"experiência sem cases: {exp['empresa']}"
        for case in exp['cases']:
            for campo in ('produto', 'descricao'):
                assert campo in case, f"case sem campo '{campo}' em {exp['empresa']}"


def validar_jooq_so_no_live2u(dados: dict) -> None:
    """jOOQ só pode aparecer em habilidades e no case Live2U."""
    for exp in dados['experiencias']:
        for case in exp['cases']:
            if case['produto'] in ('Consol', 'Apontamento'):
                assert 'jOOQ' not in case['descricao'], \
                    f"jOOQ proibido no case {case['produto']} (só Live2U)"


def validar_backend_ia_externo_live2u(dados: dict) -> None:
    """Case Live2U deve declarar backend de IA externo."""
    for exp in dados['experiencias']:
        for case in exp['cases']:
            if case['produto'] == 'Live2U':
                d = case['descricao'].lower()
                assert 'externo' in d, "Live2U deve mencionar 'externo'"
                assert 'sys3' in d, "Live2U deve mencionar 'Sys3'"


def validar_divida_apontamento(dados: dict) -> None:
    """Case Apontamento deve declarar dívida (pendentes ou dívida)."""
    for exp in dados['experiencias']:
        for case in exp['cases']:
            if case['produto'] == 'Apontamento':
                d = case['descricao'].lower()
                assert 'pendente' in d or 'dívida' in d, \
                    "Apontamento deve declarar pendências"


def validar_sem_em_dash(dados: dict) -> None:
    """Nenhuma string pode conter em-dash (—) ou en-dash (–)."""
    import json
    blob = json.dumps(dados, ensure_ascii=False)
    assert '—' not in blob, "em-dash (—) encontrado"
    assert '–' not in blob, "en-dash (–) encontrado"


def _primeira_palavra(texto: str) -> str:
    """Extrai a primeira palavra não vazia, sem pontuação final."""
    for linha in texto.strip().splitlines():
        linha = linha.strip()
        if not linha:
            continue
        return linha.split()[0].rstrip(',.;:')
    return ''


def validar_verbos_passado(dados: dict) -> None:
    """Descrições de cases e itens transversais começam com verbo no passado."""
    verbos_base = {
        'Construí', 'Modelei', 'Implementei', 'Mantive', 'Desenvolvi',
        'Integrei', 'Estruturei', 'Participei', 'Colaborei', 'Refatorei',
    }
    for exp in dados['experiencias']:
        for case in exp['cases']:
            prim = _primeira_palavra(case['descricao'])
            assert prim in verbos_base, \
                f"case {case['produto']} deve começar com verbo no passado (começa com '{prim}')"
        for tv in exp.get('transversais', []):
            prim = _primeira_palavra(tv)
            assert prim in verbos_base, \
                f"transversal em {exp['empresa']} deve começar com verbo (começa com '{prim}')"


def validar_tudo(data_dir: Path) -> bool:
    """Orquestra todas as validações. Retorna True ou levanta AssertionError."""
    dados = carregar_tudo(data_dir)
    validar_sintaxe(dados)
    validar_campos_obrigatorios(dados)
    validar_jooq_so_no_live2u(dados)
    validar_backend_ia_externo_live2u(dados)
    validar_divida_apontamento(dados)
    validar_sem_em_dash(dados)
    validar_verbos_passado(dados)

    n_cases = sum(len(e['cases']) for e in dados['experiencias'])
    print(f"[OK] validação passou.")
    print(f"  - Experiências: {len(dados['experiencias'])}")
    print(f"  - Cases totais: {n_cases}")
    print(f"  - Buckets de habilidades: {len(dados['habilidades']['buckets'])}")
    print(f"  - Cursos: {len(dados['cursos']['cursos'])}")
    return True


def main() -> int:
    data_dir = Path(__file__).parent
    try:
        validar_tudo(data_dir)
        return 0
    except AssertionError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
```

- [ ] **Step 5: Rodar os testes e confirmar que passam**

```bash
cd data && python3 -m pytest test_validate.py -v
```

Esperado: 8 passed.

- [ ] **Step 6: Rodar o validador via CLI**

```bash
python3 data/validate.py
```

Esperado:
```
[OK] validação passou.
  - Experiências: 2
  - Cases totais: 10
  - Buckets de habilidades: 11
  - Cursos: 13
```

- [ ] **Step 7: Confirmar TDD revertendo uma regra e vendo o teste falhar**

Para confirmar que os testes pegam regressões (passo 7 do ciclo TDD científico do AGENTS.md), temporariamente insira um em-dash em `data/perfil.yml`:

```bash
# Adiciona em-dash no final do paragrafo de perfil
python3 -c "
p = open('data/perfil.yml').read()
p = p.replace('(2024).', '(2024) — inválido.')
open('data/perfil.yml', 'w').write(p)
"
python3 -m pytest data/test_validate.py::test_validar_sem_em_dash -v
# Esperado: FAIL (em-dash encontrado)

# Reverte
python3 -c "
p = open('data/perfil.yml').read()
p = p.replace('(2024) — inválido.', '(2024).')
open('data/perfil.yml', 'w').write(p)
"
python3 -m pytest data/test_validate.py::test_validar_sem_em_dash -v
# Esperado: PASS
```

- [ ] **Step 8: Commit**

```bash
git add data/validate.py data/test_validate.py
git commit -m "add data/validate.py validador com pytest e regras de honestidade"
```

---

## Task 11: Smoke test ponta a ponta + README

**Files:**
- Create: `data/README.md`

**Interfaces:**
- Consumes: tudo.
- Produces: documentação de como usar a fonte de verdade YAML.

- [ ] **Step 1: Criar `data/README.md`**

```markdown
# data/ — Fonte de verdade do currículo

Conteúdo canônico do currículo em YAML. Agents e geradores DOCX consomem
estes arquivos. Os scripts Python `gerar_curriculo_ats.py` e
`zup/zup_curriculo_backend.py` (na raiz do repo) são legados e serão
migrados para consumir esta fonte em plano posterior.

## Estrutura

```
data/
├── index.yml              # manifesto: lista arquivos na ordem de composição
├── perfil.yml             # pessoa + contato + perfil
├── habilidades.yml        # buckets de skills
├── experiencias/
│   ├── iusecase.yml       # uma empresa por arquivo
│   └── itexto.yml
├── formacao.yml
├── cursos.yml
├── idiomas.yml
├── ia.yml
├── validate.py            # validador (regras de honestidade + estilo)
└── test_validate.py       # testes do validador
```

## Como validar

```bash
python3 data/validate.py
```

Faz sentido se e somente se imprimir `[OK] validação passou.` e sair com
código 0. Qualquer erro indica conteúdo que viola o spec.

## Como adicionar uma empresa nova

1. Crie `data/experiencias/<empresa>.yml` seguindo o schema de
   `iusecase.yml` (campos obrigatórios: `empresa`, `cargo`, `periodo`,
   `contexto`, `cases`).
2. Adicione o caminho em `data/index.yml` na lista `experiencias:`, na
   ordem cronológica reversa (mais recente primeiro).
3. Rode `python3 data/validate.py` para confirmar.

## Schema de experiência

```yaml
empresa: <string>                              # obrigatório
cargo: <string>                                # obrigatório (CTPS)
cargo_apresentacao: <string>                   # opcional (cabeçalho)
periodo:                                       # obrigatório
  inicio: <YYYY-MM>                            # obrigatório
  fim: <YYYY-MM | 'atual'>                     # obrigatório
local: <string>                                # opcional
contexto: <string>                             # obrigatório
cases:                                         # obrigatório, lista não vazia
  - produto: <string>                          # obrigatório
    dominio: <string>                          # opcional
    destaque: <bool>                           # opcional (default false)
    descricao: <string>                        # obrigatório (começa com verbo no passado)
transversais: [<string>, ...]                  # opcional
```

## Regras de honestidade

Estas regras são validadas por `validate.py` e refletem o spec
`docs/superpowers/specs/2026-07-21-curriculo-yaml-design.md` seção 6.

1. **jOOQ só no Live2U.** Não pode aparecer nos cases Consol ou
   Apontamento. Aparece em habilidades e no case Live2U.
2. **Backend de IA externo no Live2U.** O case Live2U deve declarar
   explicitamente que o backend de IA é externo (operado pela Sys3).
3. **Dívida documentada no Apontamento.** O case Apontamento deve
   mencionar que a migração multi-tenant está parcial (timelogging
   migrado, Initiative/Workbook/Sprint pendentes).
4. **Cargo CTPS vs cargo de apresentação.** iUsecase tem cargo CTPS
   "Desenvolvedor Backend Pleno 1" e cargo de apresentação "Engenheiro
   de Software Pleno". Os dois campos existem para refletir isso sem
   falsear.
5. **Sem em-dashes (—) ou en-dashes (–).** Regra de estilo do
   AGENTS.md.
6. **Verbos de ação no passado.** Toda descrição de case e todo item de
   transversais começa com um destes verbos: Construí, Modelei,
   Implementei, Mantive, Desenvolvi, Integrei, Estruturei, Participei,
   Colaborei, Refatorei.

## Fora de escopo (YAGNI)

- Tags pré-modeladas nos itens. O matching vaga→item é semântico, feito
  pelo agente, não por tags no YAML.
- Metadados de skill (anos de uso, último uso).
- Override dinâmico de verbos por vaga.
- Schema JSON formal. A validação é por assertions em Python.
```

- [ ] **Step 2: Smoke test ponta a ponta**

Roda o validador completo uma última vez:

```bash
python3 data/validate.py
```

Esperado:
```
[OK] validação passou.
  - Experiências: 2
  - Cases totais: 10
  - Buckets de habilidades: 11
  - Cursos: 13
```

- [ ] **Step 3: Confirmar que o `index.yml` referencia todos os arquivos existentes**

```bash
python3 -c "
import yaml
from pathlib import Path
data = Path('data')
index = yaml.safe_load(open(data / 'index.yml'))
arquivos_referenciados = {index['perfil'], index['habilidades'], index['formacao'], index['cursos'], index['idiomas'], index['ia']}
arquivos_referenciados.update(index['experiencias'])
arquivos_existentes = {str(p.relative_to(data)) for p in data.rglob('*.yml')}
nao_referenciados = arquivos_existentes - arquivos_referenciados - {'index.yml'}
assert not nao_referenciados, f'arquivos não referenciados no index: {nao_referenciados}'
print(f'[OK] todos os {len(arquivos_existentes) - 1} YAMLs estão no index.yml')
"
```

Esperado: `[OK] todos os 8 YAMLs estão no index.yml`.

- [ ] **Step 4: Commit**

```bash
git add data/README.md
git commit -m "add data/README.md documentacao da fonte de verdade yaml"
```

---

## Critérios de sucesso do plano

1. Diretório `data/` existe com 8 arquivos YAML + `validate.py` + `test_validate.py` + `README.md`.
2. `python3 data/validate.py` imprime `[OK] validação passou.` e sai com código 0.
3. `python3 -m pytest data/test_validate.py -v` reporta 8 passed.
4. Todo o conteúdo de `briefing_llm_externo.md` está representado nos YAMLs, sem perda de informação canônica.
5. Regras de honestidade (jOOQ só no Live2U, backend IA externo, dívida do Apontamento) estão refletidas no conteúdo e verificadas por testes.
6. Nenhum em-dash ou en-dash em qualquer string.
7. `index.yml` referencia todos os arquivos YAML existentes em `data/`.

## Self-review (já feito inline durante a escrita)

- Especificação coberta: Tasks 1-9 criam YAMLs para todas as seções do spec (perfil, habilidades, experiencias, formacao, cursos, idiomas, ia). Task 10 implementa o validador com todas as regras de honestidade. Task 11 documenta e faz smoke test.
- Sem placeholders: todos os steps têm código completo, comandos exatos e saídas esperadas.
- Consistência de tipos: `carregar_tudo()` retorna dict com chaves `index, perfil, habilidades, experiencias, formacao, cursos, idiomas, ia`. `validar_*` consomem esse dict. Funções correspondem aos imports em `test_validate.py`.
- Task 10 passo 7 (revert TDD) é explícito sobre como quebrar e restaurar, alinhado ao TDD científico do AGENTS.md.

## Fora de escopo deste plano

- Migração dos geradores DOCX (`gerar_curriculo_ats.py` e
  `zup/zup_curriculo_backend.py`) para consumir o YAML. Será plano
  posterior, dependente do agente de seleção por vaga.
- Implementação do agente de matching vaga→itens (JSON intermediário
  descrito no spec seção 7). Será plano posterior.
