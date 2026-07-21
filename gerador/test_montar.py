"""Testes do orquestrador gerador.montar.

Padrão TDD: testes escritos antes da implementação. Cada teste monta um
data_dir sintético em `tmp_path` com YAMLs mínimos e um manifesto JSON,
chama `montar()` apontando `data_dir` para o `tmp_path`, e faz assertions
sobre o `Document` retornado.

Cobre o contrato público da Task 3 do plano gerador-docx:
- manifesto sintético mínimo renderiza sem erro e contém nome + produto;
- seleção de cases respeita o manifesto (pede 2, YAML tem 3);
- erros explícitos (KeyError/IndexError) para case, perfil_chave, bucket,
  curso, arquivo de experiência e índice de transversal;
- toggles `idiomas` e `ia` (true/false) ligam/desligam as seções.
"""

import json
from pathlib import Path

import pytest
import yaml
from docx import Document

from gerador.montar import montar


# ---- Helpers para montar data_dir sintético em tmp_path ----

# YAMLs canônicos mínimos. As fixtures reescrevem campos específicos por
# teste quando precisam variar (ex.: 3 cases ao invés de 1).

PERFIL_YML = """
pessoa:
  nome: Pessoa de Teste
  cargo_apresentacao: Cargo de Teste
  contato:
    telefone: "(91) 99999-9999"
    email: teste@example.com
    localizacao: Cidade, UF
    linkedin: linkedin.com/in/teste
    github: github.com/teste
    portfolio: exemplo.com/portfolio
perfis:
  generico: >
    Perfil generico de teste com pelo menos uma frase.
  fullstack: >
    Perfil fullstack de teste com pelo menos uma frase.
"""

HABILIDADES_YML = """
buckets:
  - rotulo: Backend (JVM)
    itens:
      - "Java"
      - "Spring Boot"
  - rotulo: Persistencia
    itens:
      - "PostgreSQL"
"""

INDEX_YML = """
versao: 1
perfil: perfil.yml
habilidades: habilidades.yml
experiencias:
  - experiencias/empresa_a.yml
formacao: formacao.yml
cursos: cursos.yml
idiomas: idiomas.yml
ia: ia.yml
"""

# Experiência com 1 case por default. Testes que precisam de 3 cases
# reescrevem este conteúdo.
EXP_BASE_YML = """
empresa: Empresa A
cargo: Programador
cargo_apresentacao: Cargo de Teste
periodo:
  inicio: 2023-01
  fim: 2024-06
local: Cidade, UF
contexto: >
  Contexto da empresa A.
cases:
  - produto: Produto Alpha
    dominio: dominio alpha
    descricao: >
      Construí o produto Alpha com Java e Spring Boot.
  - produto: Produto Beta
    dominio: dominio beta
    descricao: >
      Implementei o produto Beta com PostgreSQL.
  - produto: Produto Gamma
    dominio: dominio gamma
    descricao: >
      Desenvolvi o produto Gamma com Angular.
transversais:
  - >
    Mantive CI/CD com GitLab e Docker.
  - >
    Colaborei em revisão de código no time.
"""

FORMACAO_YML = """
formacao:
  - curso: Bacharelado de Teste
    instituicao: Universidade de Teste (UT)
    periodo:
      inicio: 2017-01
      fim: 2024-01
    detalhes: >
      Detalhes da formação de teste.
"""

CURSOS_YML = """
cursos:
  - rotulo: Java
    descricao: >
      Curso de Java de teste.
  - rotulo: Spring/Cloud
    descricao: >
      Curso de Spring Cloud de teste.
"""

IDIOMAS_YML = """
idiomas:
  - idioma: Portugues
    nivel: Nativo
  - idioma: Ingles
    nivel: >
      Leitura técnica fluente.
"""

IA_YML = """
itens:
  - rotulo: RAG de teste
    descricao: >
      Item de IA de teste.
"""


def _escrever_data_dir(
    tmp_path: Path,
    *,
    exp_yml: str = EXP_BASE_YML,
    perfil_yml: str = PERFIL_YML,
    habilidades_yml: str = HABILIDADES_YML,
    cursos_yml: str = CURSOS_YML,
    index_yml: str = INDEX_YML,
) -> Path:
    """Escreve os YAMLs canônicos mínimos em tmp_path e retorna tmp_path."""
    (tmp_path / "perfil.yml").write_text(perfil_yml, encoding="utf-8")
    (tmp_path / "habilidades.yml").write_text(habilidades_yml, encoding="utf-8")
    (tmp_path / "formacao.yml").write_text(FORMACAO_YML, encoding="utf-8")
    (tmp_path / "cursos.yml").write_text(cursos_yml, encoding="utf-8")
    (tmp_path / "idiomas.yml").write_text(IDIOMAS_YML, encoding="utf-8")
    (tmp_path / "ia.yml").write_text(IA_YML, encoding="utf-8")
    (tmp_path / "index.yml").write_text(index_yml, encoding="utf-8")
    exp_dir = tmp_path / "experiencias"
    exp_dir.mkdir(exist_ok=True)
    (exp_dir / "empresa_a.yml").write_text(exp_yml, encoding="utf-8")
    return tmp_path


def _escrever_manifesto(tmp_path: Path, manifesto: dict) -> Path:
    """Escreve manifesto.json em tmp_path e retorna o caminho."""
    p = tmp_path / "manifesto.json"
    p.write_text(json.dumps(manifesto, ensure_ascii=False), encoding="utf-8")
    return p


def _texto_doc(doc: Document) -> str:
    return "\n".join(p.text for p in doc.paragraphs)


# Manifesto canônico mínimo (1 bucket, 1 experiência com 1 case, 1 curso,
# idiomas=false, ia=false).
def _manifesto_minimo(**overrides) -> dict:
    base = {
        "vaga": "Teste",
        "perfil_chave": "fullstack",
        "experiencias": [
            {
                "arquivo": "experiencias/empresa_a.yml",
                "cases": ["Produto Alpha"],
                "transversais": [0],
            }
        ],
        "habilidades_buckets": ["Backend (JVM)"],
        "cursos_rotulos": ["Java"],
        "idiomas": False,
        "ia": False,
    }
    base.update(overrides)
    return base


# ---- Teste 1: manifesto sintético mínimo ----

def test_manifesto_minimo_renderiza_documento_com_nome_e_produto(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto_path = _escrever_manifesto(tmp_path, _manifesto_minimo())

    doc = montar(manifesto_path, data_dir=data_dir)

    # Pelo menos 1 parágrafo foi adicionado (além do parágrafo vazio default).
    assert len(doc.paragraphs) >= 1
    texto = _texto_doc(doc)

    # Nome da pessoa aparece (em maiúsculas, conforme helper nome).
    assert "PESSOA DE TESTE" in texto

    # Produto do case aparece (renderizado como bullet com prefixo).
    assert "Produto Alpha" in texto


def test_transversal_renderiza_texto_sem_prefixo(tmp_path):
    """Transversais aparecem no Document, sem prefixo 'Transversais:'.

    Padronização do gerador novo: transversais sempre sem prefixo (ATS-friendly).
    As descrições já são atividades completas começando com verbo no passado.
    """
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(
        experiencias=[
            {
                "arquivo": "experiencias/empresa_a.yml",
                "cases": ["Produto Alpha"],
                "transversais": [0],
            }
        ]
    )
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc)

    # Texto do transversal aparece (literal do fixture empresa_a.yml).
    assert "Mantive CI/CD com GitLab e Docker." in texto
    # Padronização sem prefixo "Transversais:".
    assert "Transversais:" not in texto


# ---- Teste 2: seleção de cases respeita o manifesto ----

def test_selecao_de_cases_filtra_o_que_o_manifesto_pediu(tmp_path):
    # YAML tem 3 cases (Alpha, Beta, Gamma). Manifesto pede só 2.
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(
        experiencias=[
            {
                "arquivo": "experiencias/empresa_a.yml",
                "cases": ["Produto Alpha", "Produto Beta"],
                "transversais": [],
            }
        ]
    )
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc)

    # Os 2 pedidos aparecem.
    assert "Produto Alpha" in texto
    assert "Produto Beta" in texto
    # O terceiro (não pedido) não aparece.
    assert "Produto Gamma" not in texto


# ---- Teste 3: erro explícito - case inexistente ----

def test_case_inexistente_levanta_keyerror_com_nome_do_case(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(
        experiencias=[
            {
                "arquivo": "experiencias/empresa_a.yml",
                "cases": ["Inexistente"],
                "transversais": [],
            }
        ]
    )
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    with pytest.raises(KeyError) as excinfo:
        montar(manifesto_path, data_dir=data_dir)

    # Mensagem menciona o nome do case pedido.
    assert "Inexistente" in str(excinfo.value)


# ---- Teste 4: erro explícito - perfil_chave inexistente ----

def test_perfil_chave_inexistente_levanta_keyerror(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(perfil_chave="inexistente")
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    with pytest.raises(KeyError) as excinfo:
        montar(manifesto_path, data_dir=data_dir)

    assert "inexistente" in str(excinfo.value)


# ---- Teste 5: idiomas true/false ----

def test_idiomas_true_adiciona_secao(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(idiomas=True)
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc).upper()

    assert "IDIOMAS" in texto
    assert "Portugues".upper() in texto


def test_idiomas_false_omite_secao(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(idiomas=False)
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc).upper()

    assert "IDIOMAS" not in texto


# ---- Teste 6: IA true/false ----

def test_ia_true_adiciona_secao(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(ia=True)
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc).upper()

    # Cabeçalho da seção é "IA como Eixo de Estudo e Aplicação".
    assert "IA COMO EIXO" in texto
    assert "RAG de teste".upper() in texto


def test_ia_false_omite_secao(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(ia=False)
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc).upper()

    assert "IA COMO EIXO" not in texto


# ---- Testes adicionais para erros explícitos pedidos no brief ----

def test_bucket_inexistente_levanta_keyerror(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(habilidades_buckets=["Bucket Inexistente"])
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    with pytest.raises(KeyError) as excinfo:
        montar(manifesto_path, data_dir=data_dir)

    assert "Bucket Inexistente" in str(excinfo.value)


def test_curso_inexistente_levanta_keyerror(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(cursos_rotulos=["Curso Inexistente"])
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    with pytest.raises(KeyError) as excinfo:
        montar(manifesto_path, data_dir=data_dir)

    assert "Curso Inexistente" in str(excinfo.value)


def test_arquivo_experiencia_inexistente_levanta_keyerror(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto = _manifesto_minimo(
        experiencias=[
            {
                "arquivo": "experiencias/inexistente.yml",
                "cases": ["Produto Alpha"],
                "transversais": [],
            }
        ]
    )
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    with pytest.raises(KeyError) as excinfo:
        montar(manifesto_path, data_dir=data_dir)

    assert "inexistente.yml" in str(excinfo.value)


def test_indice_transversal_fora_de_range_levanta_indexerror(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    # YAML tem 2 transversais (índices 0 e 1). Pedir índice 5 deve falhar.
    manifesto = _manifesto_minimo(
        experiencias=[
            {
                "arquivo": "experiencias/empresa_a.yml",
                "cases": ["Produto Alpha"],
                "transversais": [5],
            }
        ]
    )
    manifesto_path = _escrever_manifesto(tmp_path, manifesto)

    with pytest.raises(IndexError) as excinfo:
        montar(manifesto_path, data_dir=data_dir)

    # Mensagem deve mencionar o índice E a palavra transversal.
    assert "5" in str(excinfo.value)
    assert "transversal" in str(excinfo.value).lower()


# ---- Testes de formato/canônicos ----

def test_periodo_atual_formatado_com_palavra_atual(tmp_path):
    # Período com fim = "atual" deve renderizar como "Jul 2025 - Atual".
    exp_atual = EXP_BASE_YML.replace(
        "inicio: 2023-01\n  fim: 2024-06",
        "inicio: 2025-07\n  fim: atual",
    )
    data_dir = _escrever_data_dir(tmp_path, exp_yml=exp_atual)
    manifesto_path = _escrever_manifesto(tmp_path, _manifesto_minimo())

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc)

    assert "Jul 2025 - Atual" in texto


def test_periodo_passado_formatado_com_mes_3_letras_portugues(tmp_path):
    # Mês abreviado em português (3 letras, primeira maiúscula).
    # 2023-01 -> Jan, 2024-06 -> Jun.
    data_dir = _escrever_data_dir(tmp_path)
    manifesto_path = _escrever_manifesto(tmp_path, _manifesto_minimo())

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc)

    assert "Jan 2023 - Jun 2024" in texto


def test_secao_habilidades_contem_itens_do_bucket(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto_path = _escrever_manifesto(tmp_path, _manifesto_minimo())

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc)

    # Bucket selecionado tem itens Java e Spring Boot.
    assert "Java" in texto
    assert "Spring Boot" in texto
    # Bucket não selecionado (Persistencia) não entra.
    assert "PostgreSQL" not in texto


def test_secao_formacao_contem_curso_e_instituicao(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto_path = _escrever_manifesto(tmp_path, _manifesto_minimo())

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc)

    assert "Bacharelado de Teste" in texto
    assert "Universidade de Teste" in texto


def test_secao_cursos_contem_rotulo_e_descricao(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto_path = _escrever_manifesto(tmp_path, _manifesto_minimo())

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc)

    # Curso selecionado: Java.
    assert "Java" in texto
    assert "Curso de Java de teste" in texto
    # Curso não selecionado: Spring/Cloud.
    assert "Curso de Spring Cloud" not in texto


def test_cabecalho_contato_tem_partes_do_yaml(tmp_path):
    data_dir = _escrever_data_dir(tmp_path)
    manifesto_path = _escrever_manifesto(tmp_path, _manifesto_minimo())

    doc = montar(manifesto_path, data_dir=data_dir)
    texto = _texto_doc(doc)

    assert "teste@example.com" in texto
    assert "linkedin.com/in/teste" in texto


def test_data_dir_default_resolve_relativo_a_montar_py(tmp_path, monkeypatch):
    """Quando data_dir não é passado, deve resolver para o diretório
    data/ real relativo a gerador/montar.py. Não podemos mockar o
    data_dir real aqui, então testamos apenas que o caminho default
    não é None e aponta para um diretório existente."""
    from gerador import montar as modulo
    default = modulo._default_data_dir()
    assert default.exists()
    assert default.is_dir()
    assert (default / "index.yml").exists()
