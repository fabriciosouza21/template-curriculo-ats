# Gerador YAML→DOCX — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir um gerador Python que lê a fonte de verdade YAML (`data/`) + um manifesto JSON de seleção e produz um DOCX ATS-friendly. Aplica à vaga Marlabs Software Engineer full-stack como primeiro caso real.

**Architecture:** Camadas separadas: `data/` (fonte YAML, só `perfil.yml` muda), `gerador/` (módulo Python com render/montar/validar_docx), `manifestos/` (JSONs por vaga), `gerar.py` (CLI).

**Tech Stack:** Python 3, `python-docx`, `pyyaml`, `pytest`.

## Global Constraints

- **Sem em-dashes (—) nem en-dashes (–)** em qualquer string (manifesto, YAML, código, DOCX gerado).
- **Estilo ATS único**: sem cor, margens 2cm, fonte Calibri 10.5pt corpo, A4, line spacing 1.1. Extraído de `gerar_curriculo_ats.py`.
- **Regras de honestidade** continuam valendo (jOOQ só Live2U, backend IA externo, dívida Apontamento, verbos no passado).
- **Português brasileiro** em todo conteúdo e prints.
- **Manifesto é o contrato**: seleção por nome/índice, nunca texto livre. Falha ruidosamente se chave não existe.
- **Sem invenção**: conteúdo do DOCX vem 100% dos YAMLs. Manifesto só seleciona.

## File Structure

```
curriculo/
├── data/
│   └── perfil.yml                 # MODIFICADO: ganha `perfis:` com chaves
├── gerador/                       # NOVO
│   ├── __init__.py
│   ├── render.py                  # helpers DOCX ATS
│   ├── montar.py                  # lê manifesto+YAML, monta Document
│   ├── validar_docx.py            # assertions ATS sobre Document
│   ├── test_render.py
│   ├── test_montar.py
│   └── test_validar_docx.py
├── manifestos/                    # NOVO
│   └── marlabs_fullstack.json
├── gerar.py                       # NOVO: CLI
└── output/                        # NOVO: DOCX gerados (gitignored)
```

## Tasks

### Task 1: `perfil.yml` com perfis alternativos

Adiciona chave `perfis:` com duas entradas: `generico` (texto atual) e `fullstack` (reescrito para Marlabs).

### Task 2: `gerador/render.py` com helpers ATS

Extrai helpers de `gerar_curriculo_ats.py`: `_style`, `_nome`, `_cargo`, `_contato`, `_h2`, `_paragrafo`, `_bullet`, `_linha_data`. Sem cor, margens 2cm, fonte 10.5pt. + `test_render.py`.

### Task 3: `gerador/montar.py`

Função `montar(manifesto_path)` → `Document`. Carrega YAMLs via `data.validate.carregar_tudo`, carrega manifesto JSON, seleciona itens por nome/índice, chama render em ordem canônica. + `test_montar.py` com manifesto sintético mínimo.

### Task 4: `gerador/validar_docx.py`

Assertions ATS sobre `Document`: sem tabelas, sem em-dash, seções obrigatórias, verbos de ação em bullets de experiência, contato presente, keywords ATS. + `test_validar_docx.py`.

### Task 5: `manifestos/marlabs_fullstack.json`

Manifesto da Marlabs com seleção definida (6 cases, 9 buckets, 7 cursos, idiomas, sem IA).

### Task 6: `gerar.py` CLI

Lê manifesto, chama `montar.montar()`, chama `validar_docx.validar()`, salva em `output/<nome>.docx`.

### Task 7: Roda e valida Marlabs

Executa o CLI, gera DOCX, valida, confirma 2 páginas e conteúdo esperado.

## Critérios de sucesso

1. `python3 gerar.py manifestos/marlabs_fullstack.json` produz `output/marlabs_fullstack.docx` sem erro.
2. `gerador/validar_docx.py` aprova o DOCX.
3. `python3 -m pytest gerador/` reporta todos testes passando.
4. `python3 data/validate.py` ainda passa.
5. DOCX Marlabs tem 2-3 páginas, 6 cases, 3 transversais (2 iusecase + 1 itexto), 9 buckets, 7 cursos, idiomas, sem IA. (Original dizia 2 páginas/2 transversais; ajustado após implementação para refletir o volume real do conteúdo selecionado.)
6. Conteúdo fiel aos YAMLs.

## Fora de escopo

- Migração dos 3 scripts antigos.
- Geração de PDF.
- Estilos coloridos.
- Perfis extras (backend/frontend/ia).
- Schema JSON formal para manifestos.
- Agente LLM que gera manifesto da vaga.

---

_Detalhamento step-by-step das tarefas na implementação SDD. Cada task produz commits isolados e passa por revisão de subagente._
