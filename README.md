# template-curriculo-ats

Template para gerar currículos em DOCX e PDF no formato ATS-friendly a partir
de uma fonte de verdade em YAML. Cada vaga vira um manifesto JSON que seleciona
quais partes do conteúdo canônico entram, sem reescrever texto à mão.

O pipeline é data-driven: o conteúdo vive em `data/*.yml`, um manifesto em
`manifestos/<empresa>.json` escolhe o que entra, e o `gerar.py` monta o DOCX,
converte para PDF e valida regras ATS.

## Por que ATS

Sistemas de triagem (Applicant Tracking Systems) extraem texto do currículo de
forma mecânica. Layouts com duas colunas, tabelas, sidebar colorida ou gráficos
quebram a extração. Este template gera documentos de uma coluna, sem tabelas de
layout, com contato e seções em ordem previsível, para maximizar a leitura
correta por parsers e por recrutadores.

## Pré-requisitos

- Python 3.10+
- `python-docx` e `pyyaml`
- LibreOffice (para converter DOCX em PDF)

Instale as dependências:

```bash
pip install python-docx pyyaml
```

## Estrutura

```
data/                  # fonte de verdade (YAML)
  perfil.yml           # TEMPLATE com dados fictícios (versionado)
  perfil.real.yml      # seus dados reais (gitignored, tem precedência)
  habilidades.yml      # buckets de habilidades
  experiencias/        # uma empresa por arquivo
  formacao.yml         # formação acadêmica
  cursos.yml           # cursos complementares
  idiomas.yml          # idiomas
  ia.yml               # itens de IA
  index.yml            # lista os arquivos que compõem o currículo
  validate.py          # validador da fonte YAML
gerador/               # motor de renderização DOCX
  render.py            # helpers ATS (estilo, nome, bullet, etc.)
  montar.py            # orquestra manifesto + dados em Document
  validar_docx.py      # validador de regras ATS sobre o Document
manifestos/            # um JSON por vaga (a seleção)
output/                # saída gerada (gitignored)
gerar.py               # CLI de entrada
```

## Uso rápido

A partir da raiz do repositório:

```bash
# Gera o currículo para uma vaga (DOCX + PDF em output/<empresa>/)
python3 gerar.py manifestos/cwi_java.json
```

Saída esperada:

```
[OK] gerado: output/cwi/cwi_java.docx
  - Parágrafos: 40
  - Tabelas: 0 (deve ser 0)
  - Páginas: 2 (limite 2)
  - PDF: output/cwi/cwi_java.pdf
```

Para sobrescrever o caminho de saída:

```bash
python3 gerar.py manifestos/cwi_java.json --output ~/Downloads/curriculo_cwi.docx
```

## Configurar seus dados

O `data/perfil.yml` versionado é um template com dados fictícios. Para gerar
currículos com seus dados reais, crie `data/perfil.real.yml`:

```bash
cp data/perfil.yml data/perfil.real.yml
```

Edite `data/perfil.real.yml` com seu nome, telefone, email, localização,
LinkedIn, GitHub e portfolio. Este arquivo é ignorado pelo git (veja
`.gitignore`) e tem precedência sobre o template em tempo de execução.

A mesma lógica se aplica ao conteúdo: edite os YAMLs em `data/` com suas
experiências, habilidades, formação e cursos. As descrições seguem regras de
honestidade validadas em `data/validate.py` (verifique com `python3
data/validate.py`).

## Criar um currículo para uma vaga nova

Um manifesto JSON seleciona o conteúdo para uma vaga específica.

1. Copie um manifesto existente como ponto de partida:

```bash
cp manifestos/cwi_java.json manifestos/minha_vaga.json
```

2. Edite `manifestos/minha_vaga.json`:

```jsonc
{
  "vaga": "Empresa X Desenvolvedor Backend (descrição livre, só metadata)",
  "empresa": "empresa_x",           // vira o subdiretório em output/
  "perfil_chave": "backend",        // chave em data/perfil.yml -> perfis
  "cargo_apresentacao": "Desenvolvedor Backend Pleno",
  "perfil_rotulo": "Desenvolvedor Backend",  // rótulo do H2 da seção Perfil
  "cor": "#0B1641",                 // opcional; default = preto (ATS puro)
  "experiencias": [
    {
      "arquivo": "experiencias/iusecase.yml",
      "cases": ["Consol", "Apontamento", "Live2U"],
      "transversais": [0, 1]        // índices 0-based dos itens transversais
    }
  ],
  "habilidades_buckets": [
    "Backend (JVM)",                // string = bucket inteiro
    {"rotulo": "Cloud/DevOps", "itens": ["Docker", "Terraform"]}  // subseleção
  ],
  "cursos_rotulos": ["Java", "Docker"],
  "idiomas": true,                  // toggle da seção Idiomas
  "ia": true,                       // toggle da seção IA
  "ia_rotulos": ["RAG com rigor experimental"]  // opcional; ausente = todos
}
```

3. Gere:

```bash
python3 gerar.py manifestos/minha_vaga.json
```

Erros de seleção (perfil, bucket, case, curso ou índice inexistente) são
explícitos em PT-BR, apontando o que falta e quais valores são válidos.

## Campos do manifesto

| Campo | Tipo | Descrição |
|---|---|---|
| `vaga` | string | Descrição livre da vaga. Só metadata, não entra no DOCX. |
| `empresa` | string | Slug da empresa. Define o subdiretório em `output/`. |
| `perfil_chave` | string | Chave em `perfil.yml -> perfis` que seleciona o parágrafo de perfil. |
| `cargo_apresentacao` | string | Sobrescreve o cargo do cabeçalho. |
| `perfil_rotulo` | string | Rótulo do H2 da seção Perfil. Default: `Perfil`. |
| `cor` | string hex | Cor de destaque (nome, cargo, H2). Default: preto. |
| `experiencias` | lista | Cada item: `arquivo`, `cases`, `transversais`. |
| `habilidades_buckets` | lista | Cada item: string (bucket inteiro) ou `{rotulo, itens}`. |
| `cursos_rotulos` | lista | Rótulos de cursos em `cursos.yml`. |
| `idiomas` | bool | Liga/desliga a seção Idiomas. |
| `ia` | bool | Liga/desliga a seção IA. |
| `ia_rotulos` | lista | Opcional. Subseleciona itens de IA; ausente = todos. |

## Validação

Dois validadores rodam em camadas.

**Fonte YAML** (regras de honestidade e estilo):

```bash
python3 data/validate.py
```

Verifica: sintaxe, campos obrigatórios, `jOOQ` só no case Live2U, backend de IA
declarado como externo no Live2U, ausência de em-dash/en-dash, e descrições
começando com verbo no passado.

**DOCX gerado** (regras ATS):

```bash
python3 -m gerador.validar_docx output/cwi/cwi_java.docx
```

Checa: sem tabelas de layout, sem em-dashes, seções obrigatórias presentes,
verbos de ação nos bullets, e consistência com o manifesto. O `gerar.py` já
roda esta validação automaticamente antes de salvar.

## Testes

```bash
python3 -m pytest -q
```

Cobre helpers de render, montagem por manifesto e regras de validação ATS.

## Convenções de conteúdo

Mantidas por validadores em duas camadas (YAML e DOCX):

- **Sem em-dash (—) nem en-dash (–)** em qualquer string. Use ponto, vírgula ou
  hífen simples com espaços.
- **Verbos no passado** no início de bullets de experiência e itens
  transversais (Construí, Modelei, Implementei, etc.).
- **Honestidade declarada**: jOOQ aparece apenas onde foi usado de fato;
  backends de terceiros são declarados como externos.

## Licença

Veja o arquivo LICENSE, ou considere este template de uso livre para adaptar ao
seu próprio currículo.
