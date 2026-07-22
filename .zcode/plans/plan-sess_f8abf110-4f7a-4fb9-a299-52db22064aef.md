# Plano: Currículo Stefanini (Desenvolvedor Backend Java SR)

## Decisão de cor (ponto crítico)

O `render.py` atual é "ATS puro, sem cor" (linha 7-8 do docstring). Você pediu `#0B1641`.
Para honrar seu pedido sem quebrar os manifestos existentes (Marlabs), vou tornar a
cor **opcional via manifesto**:

- Manifestos sem chave `cor` → comportamento atual (sem cor, ATS puro). Marlabs inalterado.
- Manifesto com `"cor": "#0B1641"` → cor aplicada em nome, cargo, cabeçalhos H2 e bordas
  inferiores dos H2.

Isso mantém o validador ATS feliz (sem tabelas de layout, uma coluna) e dá identidade visual.

## Mudanças

### 1. `gerador/render.py` - adicionar suporte a cor opcional

- Novo módulo: constante `COR_DEFAULT = None` e helper `_hex_para_rgb(hex_str) -> RGBColor | None`.
- `style(doc, cor=None)`: igual a hoje; cor não afeta o estilo Normal.
- `nome(doc, texto, cor=None)`, `cargo(doc, texto, cor=None)`, `h2(doc, texto, cor=None)`:
  se `cor` não for None, seta `run.font.color.rgb = cor`. Sem cor → inalterado.
- `linha_data`, `bullet`, `paragrafo`, `contato`: **não recebem cor** (corpo fica preto,
  só nome/cargo/H2 recebem destaque, padrão editorial consistente com Zup/Reply).
- H2 com borda inferior quando cor definida (visual de separador), opcional e trivial.

### 2. `gerador/montar.py` - ler `cor` do manifesto e propagar

- Em `montar()`: ler `manifesto.get("cor")`, converter via `_hex_para_rgb`.
- Passar `cor` para `style(doc)` e para cada chamada de `nome`, `cargo`, `h2`.
- `_render_cabecalho`, `_render_perfil`, `_render_habilidades`, `_render_experiencia`,
  `_render_formacao`, `_render_cursos`, `_render_idiomas`, `_render_ia`: recebem `cor`
  e repassam a `h2`/`nome`/`cargo`.
- Default `cor=None` preserva Marlabs.

### 3. `manifestos/stefanini_java_sr.json` - manifesto novo

Perfil `backend`. Buckets priorizados pela JD Stefanini (orqueção):
- Backend (JVM) - Spring Boot, Spring Data JPA, Security, Cloud, WebFlux
- Persistência - PostgreSQL, MySQL, Hibernate/JPA, Flyway, jOOQ, SQL nativo
- Mensageria e Integração - Apache Camel, AWS SQS, Redis
- Testes - JUnit, Mockito, AssertJ, Testcontainers, WireMock
- Cloud/DevOps - AWS, Docker, Jenkins, GitLab CI/CD, Terraform
- APIs e Contratos - REST, OpenAPI/Swagger, SOAP/WSDL
- Auth - JWT, Keycloak
- Observabilidade - Sentry, Logstash, OpenTelemetry
- Metodologia e soft skills - Kanban, Code Review, RCA, mentoria

Cases selecionados (todos com métrica real, nenhum inventado):
- iUsecase: Consol (destaque), Apontamento, Live2U; transversais [0, 1]
- itexto: Weex (destaque), Plataforma Ativus, Corteva; transversais [0]

Cursos: Java, Spring/Cloud, Camel + Spring Boot, Arquitetura, Docker, Effective Java, Segurança.
Idiomas: true. IA: false (vaga backend Java, sem IA na JD).

### 4. Cobertura de keywords da JD Stefanini

| Requisito JD | Onde aparece |
|---|---|
| Java + Spring Boot | Perfil backend + bucket Backend |
| Microsserviços | Weex (~20 microsserviços), Corteva |
| Mensageria Kafka/RabbitMQ | Camel, AWS SQS, Redis pub/sub (Kafka/RabbitMQ não usados em prod, não inventar) |
| Testes JUnit/Mockito/Cucumber | bucket Testes (Cucumber não usado, não listar) |
| Banco relacional + NoSQL | PostgreSQL/MySQL + Redis/Valkey |
| DevOps CI/CD, Jenkins, Docker, pipelines | bucket Cloud/DevOps + transversais iUsecase |
| SOLID, Clean Code, Design Patterns | perfil backend + Arquitetura (Jornada Dev Eficiente) |
| Scrum/Kanban | bucket Metodologia + transversais |

Honestidade preservada: Kafka e RabbitMQ não aparecem como experiência real
(nunca usei em produção). Camel/SQS cobrem o requisito de mensageria. Cucumber idem.

## Verificação (critério de sucesso)

1. `python3 gerar.py manifestos/stefanini_java_sr.json` gera
   `output/stefanini_java_sr.docx` sem erro (validador ATS embutido passa).
2. `python3 -m pytest gerador/` todos verdes (mudança de cor não quebra Marlabs).
3. DOCX tem 2 páginas (máx 3), cor #0B1641 visível em nome/cargo/H2.
4. PDF derivado via LibreOffice (opcional, se `soffice` disponível).

## Fora de escopo (YAGNI)

- Não criar pasta `stefanini/` legada (manifesto canônico cobre).
- Não adicionar Kafka/RabbitMQ/Cucumber à fonte (seria inventar experiência).
- Não alterar manifesto Marlabs.
- Não commitar (apenas gerar; commit só se você pedir).