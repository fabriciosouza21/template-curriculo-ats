# data/ - Fonte de verdade do currículo

Conteúdo canônico do currículo em YAML. Agents e geradores DOCX consomem
estes arquivos.

## Fonte canônica

O conteúdo destes YAMLs espelha fielmente os scripts Python legados na
raiz do repo: `gerar_curriculo_ats.py`, `zup/zup_curriculo_backend.py`,
`innvo_labs/innvo_curriculo_java_senior.py`. Esses scripts foram
curados e aprovados em revisões humanas e representam o que
efetivamente entra no currículo. O `briefing_llm_externo.md` é insumo
upstream mais verboso, NÃO canônico: detalhes que estão no briefing mas
foram omitidos dos scripts (por concisão editorial) ficam de fora dos
YAMLs. Para adicionar detalhe do briefing a um case, edite o YAML
diretamente.

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
5. **Sem em-dashes (U+2014) ou en-dashes (U+2013).** Regra de estilo do
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
