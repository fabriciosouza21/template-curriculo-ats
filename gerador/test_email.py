"""Testes do gerador de email de candidatura (gerador/email.py).

Dados de teste são fictícios, conforme a regra do repositório de não
usar PII real em exemplos e testes.
"""
import pytest
import yaml

from gerador.email import (
    MAX_PALAVRAS,
    carregar_vaga,
    montar_email,
    validar_vaga,
)

PERFIL = {
    "pessoa": {
        "nome": "Candidato Nome Completo",
        "contato": {
            "telefone": "(00) 00000-0000",
            "email": "candidato.exemplo@dominio.com",
            "localizacao": "Cidade, UF",
            "linkedin": "linkedin.com/in/seu-perfil",
            "github": "github.com/seu-usuario",
        },
    }
}

EXPERIENCIAS = [
    {"empresa": "itexto Consultoria", "cases": [{"produto": "Weex"}]},
    {"empresa": "iUsecase", "cases": [{"produto": "Consol"}]},
]


def _vaga_base():
    return {
        "vaga": {
            "empresa": "Empresa X",
            "cargo": "Desenvolvedor Pleno",
            "para": "rh@empresax.com",
        },
        "abertura": {
            "quem_sou": "Sou desenvolvedor com cinco anos de experiência em Java e Angular.",
            "pilha": ["Java 17", "Spring Boot", "Angular 15", "PostgreSQL"],
        },
        "cases": [
            {"produto": "Weex", "frase": "Na itexto construí a plataforma que processou milhões de ações"},
        ],
        "extras": "Na rotina tenho testes com JUnit e code review.",
        "gaps": {
            "itens": ["Kubernetes", "Terraform"],
            "contrapontos": ["Minha base é Docker com CI/CD em GitLab"],
            "extras": ["Não usei Jira, mas mantenho rotina ágil em ClickUp"],
        },
        "remoto_desde": 2021,
    }


class TestMontarEmail:
    def test_email_completo_tem_todos_os_blocos(self):
        email = montar_email(_vaga_base(), PERFIL)
        assert email.startswith("Para: rh@empresax.com")
        assert "Assunto: Candidatura: Desenvolvedor Pleno - Candidato Nome Completo" in email
        assert "Prezados," in email  # saudação default
        assert "Sou desenvolvedor com cinco anos" in email
        assert "A pilha da vaga é a que opero no dia a dia: Java 17, Spring Boot, Angular 15 e PostgreSQL." in email
        assert "Na itexto construí a plataforma que processou milhões de ações." in email
        assert "Na rotina tenho testes com JUnit e code review." in email
        assert "Para ser transparente: não tenho experiência com Kubernetes e Terraform." in email
        assert "Minha base é Docker com CI/CD em GitLab." in email
        assert "Não usei Jira, mas mantenho rotina ágil em ClickUp." in email
        assert "Atuo remoto desde 2021. Currículo em anexo e disponho-me a uma conversa." in email
        assert "Atenciosamente," in email
        assert "Candidato Nome Completo" in email
        assert "(00) 00000-0000 | candidato.exemplo@dominio.com" in email
        assert "linkedin.com/in/seu-perfil" in email

    def test_saudacao_customizada_substitui_default(self):
        vaga = _vaga_base()
        vaga["vaga"]["saudacao"] = "Prezada Ana,"
        assert "Prezada Ana," in montar_email(vaga, PERFIL)
        assert "Prezados," not in montar_email(vaga, PERFIL)

    def test_sem_gaps_nao_gera_paragrafo_de_transparencia(self):
        vaga = _vaga_base()
        del vaga["gaps"]
        corpo = montar_email(vaga, PERFIL)
        assert "Para ser transparente" not in corpo

    def test_anexo_menciona_empresa_e_cargo(self):
        email = montar_email(_vaga_base(), PERFIL)
        assert "Anexo: currículo PDF (Empresa X, Desenvolvedor Pleno)" in email


class TestValidarVaga:
    def test_vaga_valida_passa(self):
        validar_vaga(_vaga_base(), EXPERIENCIAS)

    def test_produto_inexistente_erro_com_validos(self):
        vaga = _vaga_base()
        vaga["cases"][0]["produto"] = "Foo"
        with pytest.raises(ValueError, match="Foo.*Weex, Consol"):
            validar_vaga(vaga, EXPERIENCIAS)

    def test_em_dash_no_yaml_erro(self):
        vaga = _vaga_base()
        vaga["abertura"]["quem_sou"] = "Sou desenvolvedor — com experiência"
        with pytest.raises(ValueError, match="em-dash"):
            validar_vaga(vaga, EXPERIENCIAS)

    def test_corpo_acima_do_limite_erro(self):
        vaga = _vaga_base()
        palavras = " ".join(["palavra"] * (MAX_PALAVRAS + 10))
        vaga["abertura"]["quem_sou"] = palavras
        with pytest.raises(ValueError, match=str(MAX_PALAVRAS)):
            validar_vaga(vaga, EXPERIENCIAS)

    def test_campo_obrigatorio_ausente_erro(self):
        vaga = _vaga_base()
        del vaga["vaga"]["para"]
        with pytest.raises(ValueError, match="vaga.para"):
            validar_vaga(vaga, EXPERIENCIAS)

    def test_sem_cases_erro(self):
        vaga = _vaga_base()
        vaga["cases"] = []
        with pytest.raises(ValueError, match="cases"):
            validar_vaga(vaga, EXPERIENCIAS)

    def test_email_invalido_erro(self):
        vaga = _vaga_base()
        vaga["vaga"]["para"] = "sem-arroba"
        with pytest.raises(ValueError, match="e-mail"):
            validar_vaga(vaga, EXPERIENCIAS)

    def test_remoto_desde_obrigatorio(self):
        vaga = _vaga_base()
        del vaga["remoto_desde"]
        with pytest.raises(ValueError, match="remoto_desde"):
            validar_vaga(vaga, EXPERIENCIAS)

    def test_frase_de_case_minuscula_erro(self):
        vaga = _vaga_base()
        vaga["cases"][0]["frase"] = "na itexto construí a plataforma"
        with pytest.raises(ValueError, match="cases\\[0\\].frase"):
            validar_vaga(vaga, EXPERIENCIAS)

    def test_extras_minusculo_erro(self):
        vaga = _vaga_base()
        vaga["extras"] = "na rotina tenho testes com JUnit"
        with pytest.raises(ValueError, match="extras"):
            validar_vaga(vaga, EXPERIENCIAS)


class TestCarregarVaga:
    def test_carrega_yaml_de_disco(self, tmp_path):
        arquivo = tmp_path / "vaga.yml"
        with open(arquivo, "w") as f:
            yaml.safe_dump(_vaga_base(), f)
        assert carregar_vaga(arquivo) == _vaga_base()
