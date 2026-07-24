# AGENTS.md

Instruções para agentes de IA que atuam neste repositório. Leia antes de
editar código ou conteúdo.

## O que é este projeto

Template que gera currículos em DOCX/PDF a partir de YAML. O conteúdo canônico
vive em `data/*.yml`, um manifesto JSON em `manifestos/<empresa>.json` seleciona
o que entra para cada vaga, e `gerar.py` monta e valida o documento.

Pipeline: `manifesto JSON` -> `gerador.montar.montar()` -> `Document` ->
`gerador.validar_docx.validar()` -> DOCX + PDF em `output/<empresa>/`.

## Regras de honestidade (não-negociáveis)

Estas regras são validadas em `data/validate.py` e `gerador/validar_docx.py`.
Elas existem para que o currículo seja defensável em entrevista. Não as contorne.

- **jOOQ só no case Live2U.** A string `jOOQ` só pode aparecer na descrição do
  case `Live2U` em `data/experiencias/iusecase.yml` e na lista de habilidades.
  Nunca em outros cases.
- **Backend de IA declarado como externo.** O case Live2U deve mencionar
  `Sys3` e a palavra `externo`, deixando claro que o backend de IA é operado
  por terceiro.
- **Sem em-dash (—) nem en-dash (–)** em qualquer string do YAML, manifesto,
  código ou DOCX gerado. Use ponto, vírgula ou hífen simples com espaços. Esta
  regra vale também para mensagens de erro e comentários.
- **Verbos no passado** no início de descrições de cases e itens transversais.
  Lista aceita (em `validar_docx.py`): Construí, Modelei, Implementei, Mantive,
  Desenvolvi, Integrei, Estruturei, Participei, Colaborei, Refatorei, Atuei,
  Contribuí, Automatizei, Lidei.
- **Cargo CTPS vs cargo de apresentação.** O cargo formal (CBO) pode diferir do
  cargo real exercido. Mantenha ambos no YAML: `cargo` é o formal, `cargo_apresentacao`
  é o que entra no currículo.

## Estilo ATS (não quebre)

O documento gerado deve ser legível por parsers de ATS:

- **Sem tabelas de layout.** Zero tabelas. Use parágrafos com tab stops
  (`linha_data`) para datas à direita.
- **Uma coluna.** Sem sidebar, sem layout de duas colunas.
- **Contato no cabeçalho.** Telefone e email são checados como presentes no
  DOCX pelo validador quando o perfil é fornecido.
- **Seções em ordem canônica** (fixa em `montar`): cabeçalho, Perfil,
  Habilidades, Experiência, Formação, Cursos, Idiomas (toggle), IA (toggle).
- **Limite de 2 páginas.** `gerar.py` valida a contagem do PDF e falha se
  exceder. Enxugue bullets ou cases, não aumente o limite.

## Dados sensíveis e PII

- `data/perfil.yml` é um **template** com dados fictícios (versionado).
- `data/perfil.real.yml` guarda dados reais e é **gitignored**. Tem precedência
  em runtime via `carregar_tudo()` em `data/validate.py`.
- Nunca hardcode contato (telefone, email, nome) em código. O validador lê do
  perfil quando precisa checar presença.
- Ao adicionar conteúdo, use dados fictícios em exemplos e testes.

## Como fazer mudanças

### Adicionar uma experiência ou case

1. Edite o arquivo correspondente em `data/experiencias/` (ou crie um novo).
2. Registre o arquivo em `data/index.yml` (lista `experiencias`).
3. Rode `python3 data/validate.py` para confirmar que passou nas regras.
4. Se a descrição do case começa com prefixo de produto (ex.: `Consol:`),
   adicione o prefixo em `PREFIXOS_PRODUTO` em `gerador/validar_docx.py` se for
   um produto novo.

### Adicionar uma habilidade ou bucket

1. Edite `data/habilidades.yml`.
2. Se criar um bucket novo, o manifesto precisa referenciar pelo `rotulo`
   exato. Itens em subseleção (`{rotulo, itens}`) devem existir no bucket.

### Adicionar um manifesto de vaga

1. Copie um manifesto existente em `manifestos/`.
2. Preencha os campos (veja README para a referência completa).
3. Rode `python3 gerar.py manifestos/<novo>.json` e confirme 2 páginas.

### Adicionar um perfil

1. Edite `data/perfil.yml`, adicione uma chave em `perfis`.
2. O manifesto referencia via `perfil_chave`.

## Workflow de verificação

Antes de considerar uma mudança pronta:

```bash
# 1. Validar a fonte YAML (regras de honestidade e estilo)
python3 data/validate.py

# 2. Rodar os testes
python3 -m pytest -q

# 3. Gerar um currículo e confirmar 2 páginas, 0 tabelas
python3 gerar.py manifestos/cwi_java.json
```

Se qualquer passo falhar, corrija antes de commitar. Os validadores são
defesa em profundidade: uma falha indica conteúdo ou regressão real.

## Convenções de código

- **Erros explícitos em PT-BR.** `_selecionar_*` em `montar.py` levanta
  `KeyError`/`IndexError` com mensagem descrevendo o que faltava e quais
  valores são válidos. Siga o padrão ao adicionar seleção.
- **Helpers de render sem underscore** são públicos (em `render.py`).
- **Imports**: o projeto roda a partir da raiz. `gerar.py` e `montar.py`
  adicionam a raiz ao `sys.path`. Não assuma cwd diferente.
- **Sem dependências além de `python-docx` e `pyyaml`** em runtime (e
  `pytest` em teste). A contagem de páginas do PDF é feita parseando bytes,
  sem pypdf.

## Commits

- Mensagens no presente do imperativo, em PT-BR, lowercase após prefixo se houver.
- Um commit = uma mudança lógica.
- Stage explícito com `git add <arquivo>`.
- Não inclua artefatos regeneráveis (`*.docx`, `*.pdf`, `output/`).
