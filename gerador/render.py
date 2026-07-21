"""Helpers de renderização ATS para python-docx.

Extrai e publica os helpers de `gerar_curriculo_ats.py` (linhas 28-124).
Comportamento idêntico ao legado validado em produção: mesmo A4, mesmas
margens 2cm, mesma fonte Calibri 10.5pt, mesmos espaçamentos.

Estilo ATS único: sem cor, sem tabelas de layout, uma coluna, texto puro.
Os nomes são públicos (sem underscore) para consumo limpo por
`gerador.montar` (Task 3 do plano gerador-docx).
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.shared import Pt, Cm, Mm

# Fonte ATS-safe: Calibri (fallback universal). Tamanhos alinhados às
# recomendações da Alura (10-12pt) com margens ~2cm. Aceita até 3 páginas
# para perfis com bagagem.
FONTE = "Calibri"
FONTE_NOME = 18
FONTE_H1 = 12
FONTE_H2 = 11
FONTE_CORPO = 10.5


def style(doc: Document) -> None:
    """Configura A4, margens 2cm e fonte Calibri 10.5pt no estilo Normal."""
    for section in doc.sections:
        section.page_height = Mm(297)
        section.page_width = Mm(210)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)

    normal = doc.styles["Normal"]
    normal.font.name = FONTE
    normal.font.size = Pt(FONTE_CORPO)
    normal.paragraph_format.space_after = Pt(1)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.line_spacing = 1.1


def nome(doc: Document, texto: str) -> None:
    """Nome em maiúsculas, 18pt bold, centralizado."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(texto.upper())
    r.bold = True
    r.font.size = Pt(FONTE_NOME)
    r.font.name = FONTE


def cargo(doc: Document, texto: str) -> None:
    """Cargo logo abaixo do nome, 12pt, centralizado."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(texto)
    r.font.size = Pt(FONTE_H1)
    r.font.name = FONTE


def contato(doc: Document, partes: list[str]) -> None:
    """Linha de contato: partes unidas por ' | ', 10.5pt, centralizada."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(" | ".join(partes))
    r.font.size = Pt(FONTE_CORPO)
    r.font.name = FONTE


def h2(doc: Document, texto: str) -> None:
    """Cabeçalho de seção em maiúsculas, bold, 11pt.

    Sem borda inferior: underline em run separado seria ruído para ATS.
    Mantém apenas bold + caixa alta.
    """
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(texto.upper())
    r.bold = True
    r.font.size = Pt(FONTE_H2)
    r.font.name = FONTE


def paragrafo(doc: Document, texto: str) -> None:
    """Parágrafo de corpo, 10.5pt."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(texto)
    r.font.size = Pt(FONTE_CORPO)
    r.font.name = FONTE


def bullet(doc: Document, texto: str, negrito_prefixo: str = "") -> None:
    """Bullet com prefixo em negrito opcional.

    ATS lê bullet char '-' (estilo List Bullet) bem. Quando
    `negrito_prefixo` é fornecido, gera um run bold seguido de um run
    normal; caso contrário, um único run normal.
    """
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Cm(0.5)
    if negrito_prefixo:
        r1 = p.add_run(negrito_prefixo)
        r1.bold = True
        r1.font.size = Pt(FONTE_CORPO)
        r1.font.name = FONTE
    r2 = p.add_run(texto)
    r2.font.size = Pt(FONTE_CORPO)
    r2.font.name = FONTE


def linha_data(doc: Document, esquerda: str, direita: str) -> None:
    """Linha com cargo a esquerda (bold) e data a direita via tab stop.

    Tab stop à direita em 17cm (limite útil da área de escrita com margens
    de 2cm em A4: 21 - 2 - 2 = 17cm).
    """
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    tab_stops = p.paragraph_format.tab_stops
    tab_stops.add_tab_stop(Cm(17.0), WD_TAB_ALIGNMENT.RIGHT)
    r1 = p.add_run(esquerda)
    r1.bold = True
    r1.font.size = Pt(FONTE_CORPO)
    r1.font.name = FONTE
    r2 = p.add_run("\t" + direita)
    r2.font.size = Pt(FONTE_CORPO)
    r2.font.name = FONTE
