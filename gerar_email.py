#!/usr/bin/env python3
"""CLI: gera um email de candidatura em Markdown a partir de emails/*.yml.

Uso:
    python3 gerar_email.py emails/actdigital.yml

Fluxo:
    1. Carrega o YAML da vaga.
    2. Carrega perfil e experiências de data/ (perfil real tem precedência).
    3. Valida estrutura, referências de case, em-dash e limite de palavras.
    4. Salva em cartas/<nome_da_vaga>_email.md.

Falha ruidosamente se qualquer passo quebra.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.validate import carregar_tudo  # noqa: E402
from gerador.email import (  # noqa: E402
    carregar_vaga,
    montar_email,
    validar_vaga,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera email de candidatura a partir de YAML da vaga."
    )
    parser.add_argument(
        "vaga",
        type=Path,
        help="Caminho para o YAML da vaga em emails/.",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Caminho de saída. Default: cartas/<nome_da_vaga>_email.md",
    )
    args = parser.parse_args()

    vaga_path: Path = args.vaga.resolve()
    if not vaga_path.exists():
        print(f"[FAIL] YAML da vaga não encontrado: {vaga_path}", file=sys.stderr)
        return 1

    print(f"[1/3] Carregando {vaga_path.name}...")
    vaga = carregar_vaga(vaga_path)
    dados = carregar_tudo(ROOT / "data")

    print("[2/3] Validando estrutura e regras...")
    try:
        validar_vaga(vaga, dados["experiencias"])
    except ValueError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return 1

    print("[3/3] Montando email...")
    email = montar_email(vaga, dados["perfil"])

    output = args.output or (ROOT / "cartas" / f"{vaga_path.stem}_email.md")
    with open(output, "w") as f:
        f.write(email)

    n_palavras = len(email.splitlines())
    print(f"[OK] gerado: {output}")
    print(f"  - Linhas: {n_palavras}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
