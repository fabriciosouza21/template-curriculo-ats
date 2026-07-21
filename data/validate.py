#!/usr/bin/env python3
"""Validador da fonte de verdade YAML do curriculo.

Carrega todos os YAMLs em data/ e valida:
- Sintaxe YAML (via pyyaml).
- Campos obrigatórios por tipo de arquivo.
- Regras de honestidade do spec:
  - jOOQ só no Live2U.
  - Backend de IA externo declarado no Live2U.
  - Dívida documentada no Apontamento.
- Regra de estilo: sem em-dashes (U+2014) ou en-dashes (U+2013).
- Regra de estilo: descrições começam com verbo de ação no passado.

Uso: python3 data/validate.py
Saída: [OK] mensagem + exit 0 se válido; mensagem de erro + exit 1 caso contrário.
"""
from pathlib import Path
import sys
import yaml


def carregar_tudo(data_dir: Path) -> dict:
    """Carrega todos os YAMLs referenciados em index.yml."""
    data_dir = Path(data_dir)
    with open(data_dir / 'index.yml') as f:
        index = yaml.safe_load(f)

    def load(rel):
        with open(data_dir / rel) as f:
            return yaml.safe_load(f)

    return {
        'index': index,
        'perfil': load(index['perfil']),
        'habilidades': load(index['habilidades']),
        'experiencias': [load(rel) for rel in index['experiencias']],
        'formacao': load(index['formacao']),
        'cursos': load(index['cursos']),
        'idiomas': load(index['idiomas']),
        'ia': load(index['ia']),
    }


def validar_sintaxe(dados: dict) -> None:
    """Sintaxe YAML já foi validada ao carregar. Aqui confere tipos básicos."""
    assert isinstance(dados['perfil']['pessoa']['nome'], str)
    assert isinstance(dados['habilidades']['buckets'], list)
    assert isinstance(dados['experiencias'], list) and len(dados['experiencias']) >= 1
    assert isinstance(dados['formacao']['formacao'], list)
    assert isinstance(dados['cursos']['cursos'], list)
    assert isinstance(dados['idiomas']['idiomas'], list)
    assert isinstance(dados['ia']['itens'], list)


def validar_campos_obrigatorios(dados: dict) -> None:
    """Confere campos obrigatórios em cada experiência e perfis."""
    # Perfis: pelo menos generico e fullstack devem existir.
    perfis = dados['perfil'].get('perfis', {})
    for chave in ('generico', 'fullstack'):
        assert chave in perfis, f"perfil '{chave}' ausente em perfil.yml"
    for exp in dados['experiencias']:
        for campo in ('empresa', 'cargo', 'periodo', 'contexto', 'cases'):
            assert campo in exp, f"experiência sem campo obrigatório '{campo}': {exp.get('empresa')}"
        assert 'inicio' in exp['periodo'] and 'fim' in exp['periodo'], \
            f"periodo mal formado em {exp['empresa']}"
        assert len(exp['cases']) >= 1, f"experiência sem cases: {exp['empresa']}"
        for case in exp['cases']:
            for campo in ('produto', 'descricao'):
                assert campo in case, f"case sem campo '{campo}' em {exp['empresa']}"


def validar_jooq_so_no_live2u(dados: dict) -> None:
    """jOOQ só pode aparecer em habilidades e na descrição do case Live2U.

    Regra do spec seção 6.1: 'na descrição do case só pode aparecer em
    Live2U'. Checagem por exclusão: qualquer case cujo produto != 'Live2U'
    não pode ter jOOQ. Cobre cases novos sem precisar atualizar lista.
    """
    for exp in dados['experiencias']:
        for case in exp['cases']:
            if case['produto'] != 'Live2U':
                assert 'jOOQ' not in case['descricao'], \
                    f"jOOQ proibido no case {case['produto']} (só Live2U)"


def validar_backend_ia_externo_live2u(dados: dict) -> None:
    """Case Live2U deve declarar backend de IA externo."""
    for exp in dados['experiencias']:
        for case in exp['cases']:
            if case['produto'] == 'Live2U':
                d = case['descricao'].lower()
                assert 'externo' in d, "Live2U deve mencionar 'externo'"
                assert 'sys3' in d, "Live2U deve mencionar 'Sys3'"


def validar_divida_apontamento(dados: dict) -> None:
    """Case Apontamento deve declarar dívida (pendentes ou dívida)."""
    for exp in dados['experiencias']:
        for case in exp['cases']:
            if case['produto'] == 'Apontamento':
                d = case['descricao'].lower()
                assert 'pendente' in d or 'dívida' in d, \
                    "Apontamento deve declarar pendências"


def validar_sem_em_dash(dados: dict) -> None:
    """Nenhuma string pode conter em-dash (U+2014) ou en-dash (U+2013)."""
    import json
    blob = json.dumps(dados, ensure_ascii=False)
    assert '—' not in blob, "em-dash (—) encontrado"
    assert '–' not in blob, "en-dash (–) encontrado"


def _primeira_palavra(texto: str) -> str:
    """Extrai a primeira palavra não vazia, sem pontuação final."""
    for linha in texto.strip().splitlines():
        linha = linha.strip()
        if not linha:
            continue
        return linha.split()[0].rstrip(',.;:')
    return ''


def validar_verbos_passado(dados: dict) -> None:
    """Descrições de cases e itens transversais começam com verbo no passado."""
    verbos_base = {
        'Construí', 'Modelei', 'Implementei', 'Mantive', 'Desenvolvi',
        'Integrei', 'Estruturei', 'Participei', 'Colaborei', 'Refatorei',
    }
    for exp in dados['experiencias']:
        for case in exp['cases']:
            prim = _primeira_palavra(case['descricao'])
            assert prim in verbos_base, \
                f"case {case['produto']} deve começar com verbo no passado (começa com '{prim}')"
        for tv in exp.get('transversais', []):
            prim = _primeira_palavra(tv)
            assert prim in verbos_base, \
                f"transversal em {exp['empresa']} deve começar com verbo (começa com '{prim}')"


def validar_tudo(data_dir: Path) -> bool:
    """Orquestra todas as validações. Retorna True ou levanta AssertionError."""
    dados = carregar_tudo(data_dir)
    validar_sintaxe(dados)
    validar_campos_obrigatorios(dados)
    validar_jooq_so_no_live2u(dados)
    validar_backend_ia_externo_live2u(dados)
    validar_divida_apontamento(dados)
    validar_sem_em_dash(dados)
    validar_verbos_passado(dados)

    n_cases = sum(len(e['cases']) for e in dados['experiencias'])
    print(f"[OK] validação passou.")
    print(f"  - Experiências: {len(dados['experiencias'])}")
    print(f"  - Cases totais: {n_cases}")
    print(f"  - Buckets de habilidades: {len(dados['habilidades']['buckets'])}")
    print(f"  - Cursos: {len(dados['cursos']['cursos'])}")
    return True


def main() -> int:
    data_dir = Path(__file__).parent
    try:
        validar_tudo(data_dir)
        return 0
    except AssertionError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
