"""Testes do validador de YAMLs do curriculo.

Padrão TDD: testes primeiro, validador depois. Cada teste cobre uma
regra do spec docs/superpowers/specs/2026-07-21-curriculo-yaml-design.md.
"""
from pathlib import Path
import pytest
import yaml

from validate import (
    carregar_tudo,
    validar_sintaxe,
    validar_campos_obrigatorios,
    validar_jooq_so_no_live2u,
    validar_backend_ia_externo_live2u,
    validar_divida_apontamento,
    validar_sem_em_dash,
    validar_verbos_passado,
)

DATA_DIR = Path(__file__).parent


def test_carregar_tudo_nao_falha():
    dados = carregar_tudo(DATA_DIR)
    assert set(dados.keys()) == {
        'index', 'perfil', 'habilidades', 'experiencias',
        'formacao', 'cursos', 'idiomas', 'ia',
    }


def test_validar_sintaxe_ok():
    dados = carregar_tudo(DATA_DIR)
    validar_sintaxe(dados)  # não levanta


def test_validar_campos_obrigatorios():
    dados = carregar_tudo(DATA_DIR)
    validar_campos_obrigatorios(dados)  # não levanta


def test_validar_jooq_so_no_live2u():
    dados = carregar_tudo(DATA_DIR)
    validar_jooq_so_no_live2u(dados)  # não levanta


def test_validar_backend_ia_externo_live2u():
    dados = carregar_tudo(DATA_DIR)
    validar_backend_ia_externo_live2u(dados)  # não levanta


def test_validar_divida_apontamento():
    dados = carregar_tudo(DATA_DIR)
    validar_divida_apontamento(dados)  # não levanta


def test_validar_sem_em_dash():
    dados = carregar_tudo(DATA_DIR)
    validar_sem_em_dash(dados)  # não levanta


def test_validar_verbos_passado():
    dados = carregar_tudo(DATA_DIR)
    validar_verbos_passado(dados)  # não levanta
