#!/usr/bin/env python3
"""Montagem e validação de email de candidatura a partir de emails/*.yml.

O YAML da vaga carrega o que muda por candidatura (casos, gaps com
contraponto, pilha de encaixe). Este módulo dona a estrutura fixa do
template em cartas/EMAIL_PADRAO.md: frases de abertura, parágrafo de
transparência, fechamento e assinatura (do perfil real).

Uso via CLI: python3 gerar_email.py emails/actdigital.yml
"""
import json
import re
import yaml

# Régua do template: corpo curto, até 200 palavras (saudação incluída).
MAX_PALAVRAS = 200


def carregar_vaga(path) -> dict:
    """Carrega o YAML da vaga de email."""
    with open(path) as f:
        return yaml.safe_load(f)


def _serie(itens: list) -> str:
    """Junta itens em série com vírgulas e 'e' antes do último."""
    if len(itens) == 1:
        return itens[0]
    return ", ".join(itens[:-1]) + " e " + itens[-1]


def _com_ponto(frase: str) -> str:
    """Garante ponto final em sentença que ainda não tem pontuação."""
    frase = frase.strip()
    if not frase:
        return frase
    if frase[-1] in ".!?":
        return frase
    return frase + "."


def _checar_maiuscula(campo: str, texto: str) -> None:
    """Sentenças viram parágrafos completos: devem começar maiúsculas."""
    if texto and not texto.strip()[0].isupper():
        raise ValueError(f"{campo} deve começar com letra maiúscula")


def _validar_campos(vaga: dict) -> None:
    """Confere campos obrigatórios do YAML da vaga."""
    secao = vaga.get("vaga")
    if not isinstance(secao, dict):
        raise ValueError("seção 'vaga' ausente ou mal formada no YAML da vaga")
    for campo in ("empresa", "cargo", "para"):
        if not secao.get(campo):
            raise ValueError(f"campo obrigatório 'vaga.{campo}' ausente ou vazio")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", secao["para"]):
        raise ValueError(f"vaga.para não parece um e-mail válido: {secao['para']!r}")

    abertura = vaga.get("abertura")
    if not isinstance(abertura, dict):
        raise ValueError("seção 'abertura' ausente ou mal formada no YAML da vaga")
    for campo in ("quem_sou", "pilha"):
        if not abertura.get(campo):
            raise ValueError(f"campo obrigatório 'abertura.{campo}' ausente ou vazio")
    if not isinstance(abertura["pilha"], list):
        raise ValueError("abertura.pilha deve ser uma lista de itens")

    cases = vaga.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("seção 'cases' ausente ou vazia: informe ao menos um case")
    for i, case in enumerate(vaga["cases"]):
        for campo in ("produto", "frase"):
            if not case.get(campo):
                raise ValueError(f"case sem campo obrigatório '{campo}'")
        _checar_maiuscula(f"cases[{i}].frase", case["frase"])
    _checar_maiuscula("extras", vaga.get("extras") or "")

    gaps = vaga.get("gaps") or {}
    for i, c in enumerate(gaps.get("contrapontos") or []):
        _checar_maiuscula(f"gaps.contrapontos[{i}]", c)
    for i, e in enumerate(gaps.get("extras") or []):
        _checar_maiuscula(f"gaps.extras[{i}]", e)

    if not vaga.get("remoto_desde"):
        raise ValueError("campo obrigatório 'remoto_desde' ausente")


def _validar_sem_em_dash(vaga: dict) -> None:
    """Nenhuma string do YAML da vaga pode ter em-dash ou en-dash."""
    blob = json.dumps(vaga, ensure_ascii=False)
    if "—" in blob or "–" in blob:
        raise ValueError(
            "em-dash (U+2014) ou en-dash (U+2013) encontrado no YAML da "
            "vaga. Use ponto, vírgula ou hífen simples."
        )


def montar_corpo(vaga: dict) -> str:
    """Monta o corpo do email: saudação + parágrafos, sem assinatura."""
    saudacao = vaga["vaga"].get("saudacao") or "Prezados,"
    paragrafos = []

    abertura = vaga["abertura"]
    paragrafos.append(
        f"{abertura['quem_sou'].strip()} "
        f"A pilha da vaga é a que opero no dia a dia: {_serie(abertura['pilha'])}."
    )

    frases = [_com_ponto(c["frase"]) for c in vaga["cases"]]
    if vaga.get("extras"):
        frases.append(_com_ponto(vaga["extras"]))
    paragrafos.append(" ".join(frases))

    gaps = vaga.get("gaps")
    if gaps and gaps.get("itens"):
        sentencas = [
            f"Para ser transparente: não tenho experiência com {_serie(gaps['itens'])}."
        ]
        for c in gaps.get("contrapontos") or []:
            sentencas.append(_com_ponto(c))
        for e in gaps.get("extras") or []:
            sentencas.append(_com_ponto(e))
        paragrafos.append(" ".join(sentencas))

    paragrafos.append(
        f"Atuo remoto desde {vaga['remoto_desde']}. "
        "Currículo em anexo e disponho-me a uma conversa."
    )
    return saudacao + "\n\n" + "\n\n".join(paragrafos)


def _validar_limite_palavras(vaga: dict) -> None:
    n = len(montar_corpo(vaga).split())
    if n > MAX_PALAVRAS:
        raise ValueError(
            f"corpo do email tem {n} palavras, acima do limite de "
            f"{MAX_PALAVRAS}. Enxugue frases ou cases."
        )


def validar_vaga(vaga: dict, experiencias: list) -> None:
    """Valida estrutura, referências de case e regras de estilo."""
    _validar_campos(vaga)
    _validar_sem_em_dash(vaga)
    _validar_limite_palavras(vaga)

    validos = [
        case["produto"] for exp in experiencias for case in exp["cases"]
    ]
    for case in vaga["cases"]:
        if case["produto"] not in validos:
            raise ValueError(
                f"case com produto '{case['produto']}' não existe em "
                f"data/experiencias/. Válidos: {', '.join(validos)}"
            )


def montar_email(vaga: dict, perfil: dict) -> str:
    """Monta o email completo: cabeçalho + corpo + assinatura do perfil."""
    pessoa = perfil["pessoa"]
    contato = pessoa["contato"]
    info = vaga["vaga"]

    cabecalho = "\n".join([
        f"Para: {info['para']}",
        f"Assunto: Candidatura: {info['cargo']} - {pessoa['nome']}",
        f"Anexo: currículo PDF ({info['empresa']}, {info['cargo']})",
    ])
    assinatura = "\n".join([
        "Atenciosamente,",
        pessoa["nome"],
        f"{contato['telefone']} | {contato['email']}",
        contato["localizacao"],
        f"{contato['linkedin']} | {contato['github']}",
    ])
    return f"{cabecalho}\n\n{montar_corpo(vaga)}\n\n{assinatura}\n"
