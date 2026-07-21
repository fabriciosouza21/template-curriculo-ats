# Handoff: Currículo Zup Backend Java

**Created:** 2026-07-21 14:40
**Sessão atual:** revisão completa do currículo direcionado à vaga de Desenvolvedor Backend Java da Zup Innovation
**Status:** currículo pronto para submissão, aguardando validação humana final
**Tom:** direto, com viés para apontar pendências

---

## O que está entregue

Diretório de trabalho: `/home/usuario/projetos/curriculo/`

```
curriculo/
├── briefing_llm_externo.md           # insumo canônico (NÃO editar cego, ver seção "Cuidados")
├── curriculo_ats.{docx,pdf}          # variante ATS genérica (não focada em vaga)
├── gerar_curriculo_ats.py            # gerador idempotente da variante genérica
├── curriculo.html / .pdf / _revisado.md  # versões antigas pré-ATS
├── .handoff/                         # 3 handoffs anteriores (incl. este)
└── zup/
    ├── zup_curriculo_backend.py      # GERADOR CANÔNICO DA VAGA ZUP
    ├── zup_curriculo_backend.docx    # artefato para submeter
    └── zup_curriculo_backend.pdf     # PDF para inspeção visual
```

**O script `zup/zup_curriculo_backend.py` é a fonte de verdade editável.** O DOCX e o PDF são outputs idempotentes. Para mudar qualquer coisa, edita o script e roda.

## Como reproduzir

```bash
cd /home/usuario/projetos/curriculo/zup
python3 zup_curriculo_backend.py                                  # gera DOCX
libreoffice --headless --convert-to pdf zup_curriculo_backend.docx  # gera PDF
```

O script roda assertions TDD inline que falham ruidosamente se algo quebrar.

---

## Estado atual do currículo Zup

**2 páginas A4.** Fonte Calibri 10pt, margens 1.2cm (compromisso ATS), line spacing 1.05, nome 16pt verde-floresta (#2E8B57), headers de seção verdes com linha decorativa fina.

**Seções (em ordem):** Cabeçalho → Perfil → Habilidades → Soft Skills e Idiomas → Experiência → Formação → Formação Complementar.

**Layout:** uma coluna, sem tabela, sem foto, sem sidebar, sem cores no corpo. Verde apenas no nome, cargo e headers.

**Validação atual:**
```
[OK] Validacao ATS + cobertura de keywords da vaga passou.
  - Paragrafos: 44
  - Tabelas: 0
  - Caracteres: 7920
Pages: 2 (A4)
```

---

## Decisões firmes (NÃO reverter sem falar com o usuário)

### 1. Vaga-alvo confirmada como Zup
A vaga "modernização do sistema de comissionamento SAP" que o usuário forneceu **é da Zup Innovation** (confirmado via Greenhouse job-boards.greenhouse.io/zupinnovation e LinkedIn). **SAP é o sistema legado a modernizar, não a empresa.**

### 2. Stack escolhida: python-docx
Skill oficial `docx` (docx-js/Node) é otimizado para design visual, não ATS estrito. python-docx gera XML mais previsível e foi a escolha técnica. Justificativa documentada no handoff anterior `20260721-1133-curriculo-ats-docx.md`.

### 3. Estilo visual: verde-floresta com flag
`USE_COR = True` no topo do script. Aplica verde (#2E8B57) no nome, cargo e headers com linha decorativa. **Se um portal ATS legado barrar**, basta `USE_COR = False` e regenerar: volta ao ATS estrito P&B.

### 4. Compliance com artigos da Alura
Currículo segue os dois artigos da Alura:
- https://www.alura.com.br/artigos/como-fazer-curriculo
- https://www.alura.com.br/artigos/ia-para-fazer-curriculo

Conformidade auditada item a item (ver seção "Auditoria Alura" abaixo).

### 5. Bullets com lead de impacto + stack como apoio
Cada bullet começa com **problema resolvido / impacto** (verbo de ação no passado), seguido da stack técnica como prova. Padrão demandado pelo usuário e endossado pelo segundo artigo da Alura.

### 6. Sem falsa precisão
Usuário pediu para **evitar contagens artificiais** tipo "7 testes", "1h TTL", "32 queries". Mantidas apenas métricas de alto valor: "5 anos", "sete sistemas em três anos e meio", "três produtos", "sete domínios de negócio". Há assertion #3d que proíbe explicitamente 14 termos de falsa precisão.

### 7. Dev Eficiente já foi concluído
Usuário confirmou. O script está com "Dev Eficiente (2025)" sem "(em andamento)".

---

## Auditoria Alura (estado final)

| Recomendação Alura | Status |
|---|---|
| Máximo 2 páginas | ✅ |
| Cabeçalho completo | ✅ |
| Sem foto/documento/estado civil | ✅ |
| Resumo profissional máx 4 linhas | ✅ |
| Experiência em ordem cronológica inversa | ✅ |
| Bullets com verbo de ação | ✅ |
| Hard skills + soft skills | ✅ (fundidas num header "Soft Skills e Idiomas") |
| Keywords da vaga | ✅ |
| Estrutura simples sem tabela/coluna | ✅ |
| Siglas expandidas ao menos uma vez | ✅ (REST, OIDC) |
| Cores com intenção sem exagero | ✅ |

---

## Auditoria de keywords da vaga

Todas as 15 keywords obrigatórias da JD estão presentes:
`Java`, `Spring`, `REST`, `PostgreSQL`, `MySQL`, `Clean Architecture`, `Apache Camel`, `Git`, `CI/CD`, `Docker`, `OAuth`, `API`, `pipelines`, `monitoramento`, `SQL nativo`, `REQUIRES_NEW`, `Testcontainers`.

Keywords da vaga **não cobertas** (por honestidade, não por esquecimento):
- **SAP** (diferencial pedido): usuário não tem experiência real. Não foi inventado.
- **Kubernetes** (diferencial pedido): usuário não tem experiência real. Não foi inventado.

---

## Cuidados com o briefing (importante)

`briefing_llm_externo.md` é o insumo canônico do usuário, **mas tem 3 afirmações que o código-fonte real desmente**. O briefing NÃO deve ser tratado como verdade absoluta. Se um agente futuro for adicionar conteúdo baseado no briefing, valide contra o código real.

Investigação feita em `/home/usuario/usecase/` (3 produtos iUsecase) e `/media/fsm/fsm/backup_fsm_source_only/itexto/` (7 projetos). Achados:

1. **Briefing diz "Redis (cache e pub/sub)"** → Mentira. Nenhum projeto usa `convertAndSend`/`MessageListener`. Redis é só cache. Currículo corrigido para "Redis (cache)".
2. **Briefing diz "WireMock"** → Mentira. Está no pom do Consol mas sem uso real. Removido do currículo.
3. **Briefing sugere mensageria nos 3 produtos iUsecase** → Não tem Rabbit/Kafka/SQS. Events são Spring Application Events in-process via `@TransactionalEventListener`. Apontamento não tem nenhum async.

**Assertion anti-invenção ativa no script:**
```python
proibidos = ["Redis pub/sub", "WireMock"]
proibidos_precisao = [
    "32 queries", "16 repositórios", "7 testes", "TTL 1h",
    "123 commands", "111 queries", "13 métodos", "10 cron",
    "720 classes", "537", "629 classes", "14 rotas", "5 unidades",
    "3 locks",
]
```

Se um agente futuro tentar reinserir qualquer um desses, o script falha na cara.

---

## Pontos fracos / pendências para o próximo agente

### A. Validação visual humana não feita
Usuário deve abrir `zup_curriculo_backend.pdf` e confirmar visualmente antes de submeter. As validações via `analyze_image` em previews PNG confirmaram layout limpo, mas inspeção humana é a última palavra.

### B. Renomear arquivo para submissão
`zup_curriculo_backend.pdf` é nome interno. Para submissão real no portal da Zup (Greenhouse), o padrão ATS-friendly é `Candidato_Nome_Backend_Java.pdf` ou similar com nome do candidato. Decisão pendente do usuário.

### C. Margens 1.2cm são apertadas
A Alura recomenda ~2cm. Foram compactadas para caber 2 páginas com conteúdo denso. Se o usuário preferir respiro visual (aceitando 3 páginas), pode voltar para 1.5cm ou 2cm. Ajuste trivial no `_style()`.

### D. Carta de apresentação não criada
Alura menciona como opcional. Não foi criada por falta de direção explícita do usuário. Se pedir, criar arquivo `carta_apresentacao_zup.md` ou `.docx` no diretório `zup/`.

### E. Idiomas fundido com Soft Skills
Para economizar espaço e caber em 2 páginas, a seção IDIOMAS virou um bullet dentro de "Soft Skills e Idiomas". Se o usuário quiser separar novamente, vai precisar cortar conteúdo em outro lugar para não estourar 2 páginas.

### F. Kubernetes e SAP não cobertos
Diferenciais da vaga. Usuário não tem experiência real. Se quiser apresentar como "estudo em andamento" (não produção), precisa de confirmação do usuário sobre o que de fato estudou.

### G. Não há variantes para outras empresas
Usuário mencionou plano futuro de criar YAMLs estruturados (`experiencia.yml`, `habilidades.yml`, `cursos.yml`) para gerar currículos dinâmicos por empresa. A variante Zup é o primeiro caso. Estrutura de subpastas por empresa (`curriculo/<empresa>/`) já está estabelecida como convenção.

---

## Padrões técnicos do currículo (decisões firmes)

### Bullets seguem este padrão
- Verbo de ação no passado como primeira palavra do corpo (após o prefixo em bold).
- Verbos aceitos (validados por assertion): `Desenvolvi`, `Modelei`, `Integrei`, `Mantive`, `Colaborei`, `Construí`, `Implementei`, `Estruturei`, `Participei`, `Liderei`, `Otimizei`, `Adicionei`, `Orquestrei`, `Usei`.
- Métricas só de alto valor (5 anos, sete sistemas, três produtos, sete domínios).
- Stack técnica aparece como prova do impacto, não como lead.

### Estrutura de cada função no script
- `_style()`: A4, margens, fonte Normal.
- `_nome()`, `_cargo()`, `_contato()`: cabeçalho centralizado com verde opcional.
- `_h2()`: header de seção em caixa alta, verde opcional, com borda inferior.
- `_paragrafo()`, `_bullet()`, `_linha_data()`: conteúdo.
- `_add_borda_inferior()`: injeção XML para borda de parágrafo (python-docx não tem API nativa).
- `construir()`: monta o documento.
- `validar()`: assertions TDD.
- `main()`: construir → validar → salvar.

---

## Resumo da história (para contexto rápido)

1. Usuário começou com currículo genérico ATS em DOCX (já existente, revisado).
2. Pediu criação de diretório dedicado em `Documentos/curriculo/`. Feito.
3. Pediu variante específica para vaga de Backend Java com modernização SAP. Criada.
4. Descobriu-se que a vaga é da **Zup Innovation** (não empresa SAP). Arquivos movidos para `curriculo/zup/` com prefixo `zup_`.
5. Usuário pediu estilo visual com verde, headers marcados. Implementado com `USE_COR = True`.
6. Usuário pediu revisão completa contra os 2 artigos da Alura. Auditoria item a item, 4 violações corrigidas: 2 páginas, soft skills, siglas expandidas, keywords "pipelines" e "monitoramento" literais.
7. Usuário questionou se a experiência estava técnica demais. Decidiu-se reescrever bullets com **lead de impacto + stack como apoio**, e extrair métricas reais do código-fonte do usuário.
8. Investiguei 10 projetos reais (3 iUsecase + 7 itexto) via subagentes. Descobri 3 afirmações falsas no briefing original e corrigi.
9. Usuário pediu para remover falsa precisão (7 testes, 1h, 32 queries). Feito. Mantidas só métricas de alto valor.
10. Usuário confirmou que Dev Eficiente foi concluído. Marcado como tal.

---

## Próximo passo sugerido

**Imediato:** usuário abre `zup_curriculo_backend.pdf`, valida visualmente, renomeia para submissão e envia para a vaga.

**Se for continuar o trabalho:**
1. Confirmar com usuário se quer carta de apresentação.
2. Confirmar se quer variantes para outras empresas (estrutura de subpastas já pronta).
3. Se sim, considerar criar os YAMLs estruturados que o usuário mencionou (`experiencia.yml`, `habilidades.yml`, `cursos.yml`) como fonte única para gerar múltiplas variantes.
4. Qualquer edição no currículo Zup deve ser feita em `zup/zup_curriculo_backend.py`, nunca direto no DOCX.
