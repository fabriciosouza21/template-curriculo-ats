# Handoff: Currículo Reply (Desenvolvedor Backend Java)

**Created:** 2026-07-21 16:00
**Branch:** master
**Status:** in-progress (bloqueado em ambiente, não em código)

## Goal

Gerar currículo DOCX/PDF específico para vaga "Desenvolvedor(a) Java Backend"
da Reply (multinacional italiana de TI, atuação remota no Brasil), seguindo o
padrão das variantes existentes (`zup/`, `innvo_labs/`): um gerador Python
que produz `reply_curriculo_java_backend.docx` e o PDF derivado via
LibreOffice.

JD Reply exige: Java 17/21, Spring Boot/Micronaut, microserviços e sistemas
distribuídos, bancos relacionais e NoSQL, Kafka, REST, CI/CD, Docker,
Kubernetes, testes unitários, Git, observabilidade, AWS. Desejável Open
Finance.

## What was done

- Criado `/home/usuario/projetos/curriculo/vaga_reply/reply_curriculo_java_backend.py`
  (gerador Python, ~480 linhas, espelhado nas variantes Innovo/Zup).
- Variante canônica `reply/reply_curriculo_java_backend.py` foi criada
  primeiro, mas o usuário reportou que a pasta `reply/` não foi encontrada.
  Recriada em `vaga_reply/`. **Estado da pasta `reply/` original é
  desconhecido** (não foi possível verificar via bash).
- Conteúdo canônico vem de `/home/usuario/projetos/curriculo/briefing_llm_externo.md`.
  Nada inventado. Cargos CTPS, CBOs, datas e stacks validados.
- Keywords da JD cobertas e validadas por assertions inline (`validar()`):
  Java, Java 17, Java 21, Spring Boot, Spring Data JPA, Spring Security,
  JPA, Hibernate, REST, microservicos, sistemas distribuidos, API,
  PostgreSQL, MySQL, Redis, NoSQL, Apache Camel, Kafka, AWS SQS, AWS,
  Git, CI/CD, Docker, Kubernetes, JUnit, Mockito, Testcontainers,
  OpenTelemetry, observabilidade, code review, nuvem, SQL nativo,
  REQUIRES_NEW, Outbox, Event-Driven, Micronaut.
- Honestidade técnica preservada (assertions proíbem "X em produção" para
  Kafka, Kubernetes, Grafana, Micronaut, WireMock, todos marcados como
  estudo).
- Sem em-dashes (—) nem en-dashes (–), conforme regra do AGENTS.md.
- Sem tabelas de layout (ATS-strict).
- Siglas expandidas ao menos uma vez: "Representational State Transfer",
  "OpenID Connect".
- Verbo de ação no início de cada bullet de experiência (Liderei, Modelei,
  Construí, Implementei, Participei etc).

## Current state

- **Arquivo principal:** `/home/usuario/projetos/curriculo/vaga_reply/reply_curriculo_java_backend.py`
  está pronto e funcional (a primeira execução, antes do shell cair, gerou
  DOCX + PDF com sucesso e passou em todas as assertions).
- **Layout:** alinhado às variantes canônicas:
  - Calibri, fonte 10pt corpo / 11pt H2 / 12pt H1 / 16pt nome.
  - Margens 1.2cm, `line_spacing=1.0`.
  - `USE_COR=True`, cor verde `#2E8B57` (mesmo verde da variante Zup),
    aplicada em nome, cargo, cabeçalhos H2 e bordas inferiores dos H2.
  - `_h2` com `space_before=1, space_after=1` e borda inferior.
  - `_paragrafo` com `space_after=2`.
  - `_bullet` com `space_after=0, left_indent=0.5cm`, sem `line_spacing`
    próprio (herda 1.0 do Normal).
- **DOCX/PDF:** foram gerados na primeira execução. Após as últimas edições
  de enxugamento, **não foram regerados** porque o shell `/usr/bin/zsh` do
  ambiente do ZCode desapareceu (`spawn /usr/bin/zsh ENOENT` em todos os
  bash calls, com e sem sandbox).
- **Git:** branch `master`, arquivos novos não commitados. `.gitignore`
  ignora `*.docx`, `*.pdf`, `__pycache__/`, `.superpowers/`.
- **Estado do PDF atual (na máquina do usuário):** 3 páginas. O usuário
  reportou isso após a última rodada. A pasta pode ainda conter a versão
  de 3 páginas.

## Key decisions

1. **Pasta `vaga_reply/` em vez de `reply/`** porque o usuário reportou não
   ter encontrado a `reply/` original. Provável causa: a primeira execução
   bash falhou em criar/persistir a pasta quando o `zsh` quebrou no meio da
   sessão.

2. **Cor verde `#2E8B57`** escolhida pelo usuário explicitamente ("coloque
   o vrde na cor"). É o mesmo verde validado na variante Zup. O vermelho
   institucional Reply `#E30613` foi descartado a pedido do usuário.

3. **Enxugamento de bullets para reduzir páginas** feito em 2 rodadas:
   - Rodada 1: bullets de Habilidades enxutos, parênteses explicativos
     removidos, Soft Skills de 3 para 2 bullets, Perfil compactado.
   - Rodada 2: bullets de experiência da itexto fundidos. "Logística" +
     "Gamificação corporativa" viraram um único bullet "Logistica e
     gamificacao:". Set de prefixos da validação atualizado para casar.
   - **Depois disso** o layout foi revertido ao padrão canônico
     (`line_spacing=1.0`, margens 1.2cm, `FONTE_H1=12`) porque o usuário
     reportou que os bullets estavam "grudados" e a fonte desalinhada das
     outras variantes. Com a reversão, o PDF voltou a 3 páginas.

4. **Honestidade sobre estudo vs produção** é regra de validação
   (assertions bloqueiam "Kafka em produção", "Kubernetes em produção",
   "Micronaut em produção", "Grafana em produção", "WireMock em produção").
   Esses termos aparecem marcados como "em estudo". Não mexer.

5. **jOOQ só no Live2U** é regra de honestidade validada. Não aparece em
   Consol nem Apontamento.

## What's next

1. **Confirmar se a pasta `reply/` original existe ou não.** Se existir,
   decidir entre deletá-la (e usar só `vaga_reply/`) ou renomear
   `vaga_reply/` de volta para `reply/` para consistência com `zup/`,
   `innvo_labs/`, `cwi/`.

2. **Regerar DOCX + PDF** com as últimas edições (apenas possível quando
   o `zsh` voltar):
   ```bash
   cd /home/usuario/projetos/curriculo/vaga_reply
   python3 reply_curriculo_java_backend.py
   rm -f reply_curriculo_java_backend.pdf
   libreoffice --headless --convert-to pdf reply_curriculo_java_backend.docx
   pdfinfo reply_curriculo_java_backend.pdf | grep Pages
   ```

3. **Se ainda 3 páginas**, próximo corte cirúrgico (Opção A acordada com
   o usuário): remover ou fundir mais bullets de experiência secundária.
   Candidatos, em ordem de prioridade de corte (menor impacto em
   keywords da JD):
   - Reduzir "Apontamento" (itexto multi-tenant não carrega keyword única
     da JD que já não esteja em Consol/Fintech).
   - Encolher "Transversais" para 1 linha.
   - Cortar "Formação Complementar" de 5 para 3 bullets.
   Não cortar: Consol, Fintech, Agronegócio (carregam Clean Architecture,
   DDD, Event-Driven, Outbox, Apache Camel, SQL nativo, REQUIRES_NEW).

4. **Antes de cortar, inspecionar onde a página 3 começa:**
   ```bash
   pdftotext -layout reply_curriculo_java_backend.pdf - \
     | awk 'BEGIN{p=1} /\f/{p++; next} {print p": "$0}' | tail -30
   ```
   Sem isso, cortes são no escuro.

5. **Restaurar `zsh` no ambiente** (pré-requisito para o agente voltar a
   executar):
   ```bash
   sudo ln -sf /usr/bin/bash /usr/bin/zsh
   # ou
   sudo apt install -y zsh
   ```

6. **Commit** quando 2 páginas estiver confirmado. Convenção do repo:
   presente do imperativo, sem emoji. Sugestão:
   `add reply/reply_curriculo_java_backend.py vaga java backend reply`

## Blockers / Open questions

- **`/usr/bin/zsh` sumiu do ambiente do ZCode.** Todos os `Bash` calls
  retornam `spawn /usr/bin/zsh ENOENT`. Sem bash, o agente não consegue
  executar o gerador Python, regerar PDF, contar páginas, ou inspecionar
  onde a página 3 corta. Write/Edit/Read funcionam normalmente.
  **Bloqueador crítico.** Usuário precisa restaurar `zsh` ou o agente
  precisa rodar comandos via um shell alternativo (não há fallback hoje).
- **Pasta `reply/` vs `vaga_reply/`.** Estado da `reply/` original é
  desconhecido. Usuário reportou "não encontrei a pasta". Pode ter sido
  perdida quando o `zsh` quebrou no meio da primeira execução, ou pode
  existir com versão desatualizada (3 páginas, vermelho Reply, sem
  enxugamento).
- **Páginas:** 3 confirmadas pelo usuário após reversão ao layout
  canônico. Antes da reversão (com `line_spacing=0.9`, `FONTE_H1=11`,
  margens 1.0cm), já estava mais perto de 2 mas visualmente quebrado
  (bullets grudados, fonte desalinhada).

## How to continue

1. Leia este handoff.
2. Restaure o `zsh` no ambiente (ou confirme que já está restaurado):
   `sudo ln -sf /usr/bin/bash /usr/bin/zsh`.
3. Verifique o estado das duas pastas:
   ```bash
   ls -la /home/usuario/projetos/curriculo/reply/ \
          /home/usuario/projetos/curriculo/vaga_reply/
   ```
4. Rode o gerador em `vaga_reply/` (passo 2 de "What's next").
5. Se 3 páginas, rode o `pdftotext` do passo 4 de "What's next" e use a
   saída para decidir o corte.
6. Não reverter o layout canônico (Calibri 10/11/12/16, margens 1.2cm,
   `line_spacing=1.0`, verde `#2E8B57`). Reduzir volume de texto, não
   compactar espaçamento.

## Key files

- `/home/usuario/projetos/curriculo/vaga_reply/reply_curriculo_java_backend.py`
  - Gerador Python do currículo Reply. Pronto e funcional. Único arquivo
    novo desta sessão.
- `/home/usuario/projetos/curriculo/innvo_labs/innvo_curriculo_java_senior.py`
  - Variante de referência (Innovo Labs, Java Senior). Cópia fiel do
    padrão de layout, fonte e validação. Use como baseline ao comparar.
- `/home/usuario/projetos/curriculo/zup/zup_curriculo_backend.py`
  - Variante de referência (Zup, Backend Java). Mesmo verde `#2E8B57`
    que a Reply agora usa.
- `/home/usuario/projetos/curriculo/briefing_llm_externo.md`
  - Fonte canônica de dados pessoais, experiências, skills e formação.
    Todo conteúdo do currículo sai daqui. Nada inventado.
- `/home/usuario/projetos/curriculo/data/index.yml`, `perfil.yml`,
  `habilidades.yml`
  - Migração em andamento para YAML canônico (ramo paralelo, não
    relacionado a esta vaga). Não mexer nesta sessão.
- `/home/usuario/projetos/curriculo/.gitignore`
  - Ignora `*.docx`, `*.pdf`. Confirmar antes de commitar.
