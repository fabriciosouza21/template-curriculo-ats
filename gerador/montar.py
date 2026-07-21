"""Orquestrador do gerador YAML -> DOCX.

Lê um manifesto JSON de seleção e os YAMLs em data/, seleciona itens por
nome ou índice (sem texto livre) e renderiza um `Document` em ordem
canônica usando os helpers de `gerador.render`.

Contrato público:
    montar(manifesto_path, data_dir=None) -> Document

Erros explícitos (PT-BR) quando uma chave pedida no manifesto não existe:
- perfil_chave:           KeyError
- bucket de habilidades:  KeyError
- arquivo de experiência: KeyError (match por nome de arquivo contra index)
- case de experiência:    KeyError
- índice transversal:     IndexError
- rótulo de curso:        KeyError

Sem em-dashes (U+2014) nem en-dashes (U+2013) em qualquer string gerada.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from docx import Document

from gerador.render import (
    style,
    nome,
    cargo,
    contato,
    h2,
    paragrafo,
    bullet,
    linha_data,
)

# ---- Import de carregar_tudo ----
#
# data/ não é um pacote Python (não tem __init__.py), então um import
# limpo `from data.validate import carregar_tudo` só funciona se o
# diretório raiz do projeto estiver no sys.path. Em produção (CLI rodando
# a partir da raiz) isso é verdade. Em testes pytest (que roda da raiz
# também) também é verdade. Para deixar o módulo robusto a qualquer cwd,
# adicionamos o diretório raiz do projeto (parent deste arquivo) ao
# sys.path explicitamente. É a mesma estratégia usada por data/validate.py
# ao ser invocado como script direto.
_RAIZ_PROJETO = Path(__file__).resolve().parent.parent
if str(_RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(_RAIZ_PROJETO))

# Agora data/ é importável como namespace package (PEP 420). O validate.py
# dentro de data/ também é importável.
from data.validate import carregar_tudo  # noqa: E402


# ---- Formatação de datas ----

# Mapa mês-numérico -> abreviação em PT-BR (3 letras, primeira maiúscula),
# conforme contrato canônico do brief: Jan, Fev, Mar, Abr, Mai, Jun, Jul,
# Ago, Set, Out, Nov, Dez.
_MESES_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
    5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
    9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}


def _formatar_periodo(inicio: Any, fim: Any) -> str:
    """Converte um par (inicio, fim) em "<Mmm AAAA> - <Mmm AAAA|Atual>".

    `inicio` e `fim` aceitam:
    - string "YYYY-MM" (formato YAML canônico);
    - string "atual" para `fim` -> vira "Atual";
    - qualquer outro formato passa direto (escape hatch para casos
      especiais; não deve ocorrer na fonte YAML atual).

    Levanta ValueError se o mês estiver fora de 1..12.
    """
    return f"{_formatar_mes_ano(inicio)} - {_formatar_mes_ano(fim)}"


def _formatar_mes_ano(valor: Any) -> str:
    """Formata "YYYY-MM" -> "Mmm AAAA". "atual" -> "Atual".

    Strings que não casam com o padrão são devolvidas inalteradas
    (escape hatch, não deve ocorrer nos YAMLs atuais).
    """
    if valor == "atual":
        return "Atual"
    s = str(valor).strip()
    # Aceita "YYYY-MM". Tolerante a MM com 1 ou 2 dígitos.
    partes = s.split("-")
    if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
        ano = int(partes[0])
        mes = int(partes[1])
        if mes < 1 or mes > 12:
            raise ValueError(f"mês inválido: {valor!r}")
        return f"{_MESES_PT[mes]} {ano}"
    return s


# ---- Helpers internos de seleção ----

def _default_data_dir() -> Path:
    """Diretório data/ relativo a este arquivo (../data).

    Defaults canônico do brief: quando o chamador não passa `data_dir`,
    usamos o `data/` real do projeto, não um caminho relativo ao cwd.
    """
    return _RAIZ_PROJETO / "data"


def _carregar_manifesto(manifesto_path: Path) -> dict:
    with open(manifesto_path, encoding="utf-8") as f:
        return json.load(f)


def _selecionar_experiencia(
    exps_carregadas: list[dict],
    arquivos_index: list[str],
    arquivo_pedido: str,
) -> dict:
    """Seleciona a experiência pelo nome de arquivo (ex.: experiencias/x.yml).

    Matching por nome de arquivo contra a lista de `index.yml.experiencias`.
    A saída de carregar_tudo devolve as experiências já parseadas, mas
    sem o nome do arquivo original. Por isso usamos `arquivos_index`
    (a lista do index.yml) para casar por posição.
    """
    arq_normalizado = arquivo_pedido.replace("\\", "/")
    for i, arq in enumerate(arquivos_index):
        if arq.replace("\\", "/") == arq_normalizado and i < len(exps_carregadas):
            return exps_carregadas[i]
    raise KeyError(
        f"arquivo de experiência não encontrado: {arquivo_pedido!r}. "
        f"Arquivos disponíveis em index.yml: {arquivos_index}"
    )


def _selecionar_case(exp: dict, produto_pedido: str) -> dict:
    """Seleciona um case pelo nome do produto (chave 'produto')."""
    for case in exp.get("cases", []):
        if case.get("produto") == produto_pedido:
            return case
    produtos = [c.get("produto") for c in exp.get("cases", [])]
    raise KeyError(
        f"case {produto_pedido!r} não existe na experiência "
        f"{exp.get('empresa', '?')!r}. Produtos disponíveis: {produtos}"
    )


def _selecionar_transversal(exp: dict, indice: int) -> str:
    """Retorna o texto do transversal no índice dado."""
    transversais = exp.get("transversais", [])
    if indice < 0 or indice >= len(transversais):
        raise IndexError(
            f"índice transversal {indice} fora de range na experiência "
            f"{exp.get('empresa', '?')!r}. "
            f"Transversais disponíveis: 0..{len(transversais) - 1}"
        )
    return str(transversais[indice]).strip()


def _selecionar_bucket(buckets: list[dict], rotulo_pedido: str) -> dict:
    for b in buckets:
        if b.get("rotulo") == rotulo_pedido:
            return b
    rotulos = [b.get("rotulo") for b in buckets]
    raise KeyError(
        f"bucket de habilidades {rotulo_pedido!r} não existe. "
        f"Rótulos disponíveis: {rotulos}"
    )


def _selecionar_curso(cursos: list[dict], rotulo_pedido: str) -> dict:
    for c in cursos:
        if c.get("rotulo") == rotulo_pedido:
            return c
    rotulos = [c.get("rotulo") for c in cursos]
    raise KeyError(
        f"curso {rotulo_pedido!r} não existe. "
        f"Rótulos disponíveis: {rotulos}"
    )


def _selecionar_perfil(perfis: dict, chave_pedido: str) -> str:
    if chave_pedido not in perfis:
        raise KeyError(
            f"perfil_chave {chave_pedido!r} não existe em perfil.yml. "
            f"Chaves disponíveis: {list(perfis.keys())}"
        )
    return str(perfis[chave_pedido]).strip()


# ---- Seções (uma função por seção canônica) ----

def _render_cabecalho(doc: Document, perfil: dict) -> None:
    pessoa = perfil["pessoa"]
    nome(doc, pessoa["nome"])
    cargo(doc, pessoa["cargo_apresentacao"])

    c = pessoa.get("contato", {})
    # Ordem canônica do brief: telefone, email, localizacao, linkedin,
    # github, portfolio. Só inclui chaves presentes.
    chaves = ("telefone", "email", "localizacao", "linkedin", "github", "portfolio")
    partes = [str(c[k]).strip() for k in chaves if c.get(k)]
    contato(doc, partes)


def _render_perfil(doc: Document, perfil: dict, chave: str) -> None:
    texto = _selecionar_perfil(perfil.get("perfis", {}), chave)
    h2(doc, "Perfil")
    paragrafo(doc, texto)


def _render_habilidades(doc: Document, habilidades: dict, rotulos: list[str]) -> None:
    h2(doc, "Habilidades")
    for rotulo in rotulos:
        bucket = _selecionar_bucket(habilidades.get("buckets", []), rotulo)
        itens = bucket.get("itens", [])
        corpo = ", ".join(str(i).strip() for i in itens)
        bullet(doc, corpo, negrito_prefixo=f"{rotulo}: ")


def _render_experiencia(doc: Document, dados: dict, manifesto_exp: dict,
                        arquivos_index: list[str]) -> None:
    arquivo_pedido = manifesto_exp["arquivo"]
    exp = _selecionar_experiencia(dados["experiencias"], arquivos_index, arquivo_pedido)

    # linha_data(empresa, periodo).
    periodo_fmt = _formatar_periodo(
        exp["periodo"]["inicio"], exp["periodo"]["fim"]
    )
    linha_data(doc, exp["empresa"], periodo_fmt)

    # Parágrafo: "<cargo> (cargo CTPS). <contexto>".
    # O cargo formal (CTPS) está em exp['cargo']. O de apresentação fica
    # no cabeçalho e não se repete aqui.
    cargo_ctps = str(exp.get("cargo", "")).strip()
    contexto = str(exp.get("contexto", "")).strip()
    if cargo_ctps:
        linha = f"{cargo_ctps} (cargo CTPS). {contexto}"
    else:
        linha = contexto
    paragrafo(doc, linha)

    # Cases: prefixo "<produto>: " + descricao.
    for produto in manifesto_exp.get("cases", []):
        case = _selecionar_case(exp, produto)
        bullet(
            doc,
            str(case["descricao"]).strip(),
            negrito_prefixo=f"{produto}: ",
        )

    # Transversais: sem prefixo (padrão do legado).
    for indice in manifesto_exp.get("transversais", []):
        texto = _selecionar_transversal(exp, indice)
        bullet(doc, texto)


def _render_formacao(doc: Document, formacao: dict) -> None:
    h2(doc, "Formação")
    for item in formacao.get("formacao", []):
        curso = str(item["curso"]).strip()
        instituicao = str(item["instituicao"]).strip()
        periodo_fmt = _formatar_periodo(
            item["periodo"]["inicio"], item["periodo"]["fim"]
        )
        linha_data(doc, f"{curso}: {instituicao}", periodo_fmt)
        detalhes = str(item.get("detalhes", "")).strip()
        if detalhes:
            paragrafo(doc, detalhes)


def _render_cursos(doc: Document, cursos: dict, rotulos: list[str]) -> None:
    h2(doc, "Formação Complementar")
    for rotulo in rotulos:
        curso = _selecionar_curso(cursos.get("cursos", []), rotulo)
        bullet(
            doc,
            str(curso["descricao"]).strip(),
            negrito_prefixo=f"{rotulo}: ",
        )


def _render_idiomas(doc: Document, idiomas: dict) -> None:
    h2(doc, "Idiomas")
    for item in idiomas.get("idiomas", []):
        idioma = str(item["idioma"]).strip()
        nivel = str(item.get("nivel", "")).strip()
        bullet(doc, nivel, negrito_prefixo=f"{idioma}: ")


def _render_ia(doc: Document, ia: dict) -> None:
    h2(doc, "IA como Eixo de Estudo e Aplicação")
    for item in ia.get("itens", []):
        rotulo = str(item["rotulo"]).strip()
        descricao = str(item["descricao"]).strip()
        bullet(doc, descricao, negrito_prefixo=f"{rotulo}: ")


# ---- API pública ----

def montar(manifesto_path: str | Path, data_dir: str | Path = None) -> Document:
    """Monta um Document a partir do manifesto JSON e dos YAMLs.

    Args:
        manifesto_path: caminho para o manifesto JSON de seleção.
        data_dir: diretório com os YAMLs (default: data/ relativo a este
            arquivo, i.e., ../data a partir de gerador/montar.py).

    Returns:
        Document configurado e populado, pronto para `doc.save()`.

    Raises:
        KeyError: se qualquer chave nomeada (perfil, bucket, case, curso,
            arquivo de experiência) não existir na fonte YAML.
        IndexError: se um índice de transversal estiver fora de range.
        ValueError: se um mês de período estiver fora de 1..12.
    """
    manifesto_path = Path(manifesto_path)
    data_dir_resolved = Path(data_dir) if data_dir is not None else _default_data_dir()

    manifesto = _carregar_manifesto(manifesto_path)
    dados = carregar_tudo(data_dir_resolved)
    arquivos_index = list(dados["index"].get("experiencias", []))

    doc = Document()
    style(doc)

    # 1. Cabeçalho.
    _render_cabecalho(doc, dados["perfil"])

    # 2. Perfil.
    _render_perfil(doc, dados["perfil"], manifesto["perfil_chave"])

    # 3. Habilidades.
    _render_habilidades(doc, dados["habilidades"], manifesto.get("habilidades_buckets", []))

    # 4. Experiência.
    if manifesto.get("experiencias"):
        h2(doc, "Experiência")
        for manifesto_exp in manifesto["experiencias"]:
            _render_experiencia(doc, dados, manifesto_exp, arquivos_index)

    # 5. Formação.
    _render_formacao(doc, dados["formacao"])

    # 6. Cursos (Formação Complementar).
    _render_cursos(doc, dados["cursos"], manifesto.get("cursos_rotulos", []))

    # 7. Idiomas (toggle).
    if manifesto.get("idiomas"):
        _render_idiomas(doc, dados["idiomas"])

    # 8. IA (toggle).
    if manifesto.get("ia"):
        _render_ia(doc, dados["ia"])

    return doc
