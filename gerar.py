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

Falha ruidosamente se qualquer passo quebra.
"""
import argparse
import json
import sys
from pathlib import Path

# Adiciona raiz do projeto ao sys.path para permitir imports relativos
# (gerador.montar faz o mesmo para importar data.validate).
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gerador.montar import montar  # noqa: E402
from gerador.validar_docx import validar  # noqa: E402


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

    print(f"[1/3] Montando Document a partir de {manifesto_path.name}...")
    doc = montar(manifesto_path)

    print("[2/3] Validando regras ATS...")
    validar(doc, manifesto=manifesto)

    # Resolve caminho de saída.
    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    if args.output is not None:
        output_path = args.output.resolve()
    else:
        output_path = output_dir / f"{manifesto_path.stem}.docx"

    print(f"[3/3] Salvando em {output_path}...")
    doc.save(str(output_path))

    n_paragrafos = len(doc.paragraphs)
    n_tabelas = len(doc.tables)
    print(f"[OK] gerado: {output_path}")
    print(f"  - Parágrafos: {n_paragrafos}")
    print(f"  - Tabelas: {n_tabelas} (deve ser 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
