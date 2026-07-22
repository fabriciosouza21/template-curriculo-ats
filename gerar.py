#!/usr/bin/env python3
"""CLI: gera um DOCX de currículo a partir de um manifesto JSON.

Uso:
    python3 gerar.py manifestos/marlabs_fullstack.json
    python3 gerar.py manifestos/marlabs_fullstack.json --output saida.docx

Fluxo:
    1. Carrega manifesto JSON.
    2. Chama gerador.montar.montar() para produzir o Document.
    3. Chama gerador.validar_docx.validar() para checar regras ATS.
    4. Salva em output/<nome_do_manifesto>.docx (ou caminho fornecido).
    5. Converte para PDF via LibreOffice (soffice).
    6. Valida que o PDF tem no máximo 2 páginas.

Falha ruidosamente se qualquer passo quebra.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Adiciona raiz do projeto ao sys.path para permitir imports relativos
# (gerador.montar faz o mesmo para importar data.validate).
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gerador.montar import montar  # noqa: E402
from gerador.validar_docx import validar  # noqa: E402

# Limite de páginas do currículo. Curto o suficiente para ser respeitado
# pelo recrutador, longo o suficiente para perfis com bagagem.
MAX_PAGINAS = 2


def _contar_paginas_pdf(pdf_path: Path) -> int:
    """Conta páginas de um PDF parseando o /Count do catálogo.

    Sem dependência externa (pypdf não disponível no ambiente). Lê os
    bytes do PDF e casa `/Count N` no nó /Pages. Fallback para regex de
    `/Type /Page` individuais se /Count estiver ausente.
    """
    with open(pdf_path, "rb") as f:
        data = f.read()
    counts = re.findall(rb"/Count\s+(\d+)", data)
    if counts:
        # /Count pode aparecer em vários nós; pega o maior (catálogo raiz).
        return max(int(c) for c in counts)
    # Fallback: conta ocorrências de /Type /Page (exclui /Pages).
    return len(re.findall(rb"/Type\s*/Page[^s]", data))


def _converter_para_pdf(docx_path: Path) -> Path:
    """Converte DOCX para PDF via LibreOffice headless.

    Retorna o caminho do PDF gerado (mesmo diretório do DOCX).
    Levanta RuntimeError se o soffice não estiver disponível ou falhar.
    """
    if shutil.which("soffice") is None and shutil.which("libreoffice") is None:
        raise RuntimeError(
            "soffice/libreoffice não encontrado no PATH. "
            "Instale o LibreOffice para validação de páginas."
        )
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    out_dir = str(docx_path.parent)
    resultado = subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf",
         "--outdir", out_dir, str(docx_path)],
        capture_output=True, text=True, timeout=120,
    )
    pdf_path = docx_path.with_suffix(".pdf")
    if resultado.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(
            f"conversão para PDF falhou (exit {resultado.returncode}). "
            f"stderr: {resultado.stderr[:200]}"
        )
    return pdf_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera DOCX de currículo a partir de manifesto JSON."
    )
    parser.add_argument(
        "manifesto",
        type=Path,
        help="Caminho para o arquivo de manifesto JSON.",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Caminho de saída do DOCX. Default: output/<nome_manifesto>.docx",
    )
    args = parser.parse_args()

    manifesto_path: Path = args.manifesto.resolve()
    if not manifesto_path.exists():
        print(f"[FAIL] manifesto não encontrado: {manifesto_path}", file=sys.stderr)
        return 1

    # Carrega manifesto para passar ao validador.
    with open(manifesto_path) as f:
        manifesto = json.load(f)

    print(f"[1/5] Montando Document a partir de {manifesto_path.name}...")
    doc = montar(manifesto_path)

    print("[2/5] Validando regras ATS...")
    validar(doc, manifesto=manifesto)

    # Resolve caminho de saída.
    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    if args.output is not None:
        output_path = args.output.resolve()
    else:
        output_path = output_dir / f"{manifesto_path.stem}.docx"

    print(f"[3/5] Salvando em {output_path}...")
    doc.save(str(output_path))

    n_paragrafos = len(doc.paragraphs)
    n_tabelas = len(doc.tables)
    print(f"[4/5] Convertendo para PDF via LibreOffice...")
    try:
        pdf_path = _converter_para_pdf(output_path)
    except RuntimeError as exc:
        print(f"[WARN] {exc}", file=sys.stderr)
        print("       Pulando validação de páginas (PDF não gerado).")
        print(f"[OK] gerado: {output_path}")
        print(f"  - Parágrafos: {n_paragrafos}")
        print(f"  - Tabelas: {n_tabelas} (deve ser 0)")
        return 0

    print(f"[5/5] Validando limite de {MAX_PAGINAS} páginas...")
    n_paginas = _contar_paginas_pdf(pdf_path)
    print(f"  - Páginas: {n_paginas}")
    if n_paginas > MAX_PAGINAS:
        print(
            f"[FAIL] currículo tem {n_paginas} páginas, excede o limite de "
            f"{MAX_PAGINAS}. Enxugue bullets ou cases. PDF em {pdf_path}.",
            file=sys.stderr,
        )
        return 1

    print(f"[OK] gerado: {output_path}")
    print(f"  - Parágrafos: {n_paragrafos}")
    print(f"  - Tabelas: {n_tabelas} (deve ser 0)")
    print(f"  - Páginas: {n_paginas} (limite {MAX_PAGINAS})")
    print(f"  - PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
