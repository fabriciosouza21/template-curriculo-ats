# Email padrão de candidatura

Emails de candidatura são gerados a partir de um YAML por vaga:

```bash
python3 gerar_email.py emails/actdigital.yml   # gera cartas/actdigital_email.md
```

A estrutura fixa (frases de abertura, parágrafo de transparência,
fechamento, assinatura) mora em `gerador/email.py`. O YAML da vaga carrega
só o que muda por candidatura. Testes em `gerador/test_email.py`.

## Estrutura do YAML da vaga

```yaml
vaga:
  empresa: Act Digital
  cargo: Desenvolvedor(a) Pleno Remoto
  para: ana.araujo@actdigital.com
  saudacao: Prezada Ana,        # opcional, default "Prezados,"

abertura:
  quem_sou: >                    # quem sou, com números do YAML canônico
    Sou Desenvolvedor Full Stack Pleno com ...
  pilha:                         # itens entram em série com vírgulas e "e"
    - Java EE
    - Spring Boot

cases:                           # produto valida existência em data/experiencias/
  - produto: Weex                # frase é sentença completa, maiúscula inicial
    frase: >
      Na itexto construí a Weex, plataforma de gamificação que ...

extras: >                        # opcional: requisitos e diferenciais da rotina
  Na rotina tenho testes com JUnit e Testcontainers, ...

gaps:                            # opcional: sem a seção, não há parágrafo
  itens: [Spring Batch, DB2]     # entram na frase "não tenho experiência com ..."
  contrapontos:                  # base equivalente real das experiências
    - >
      Minha base é PostgreSQL e MySQL em SQL ANSI
  extras:                        # tratamento especial, ex.: Jira vs ClickUp
    - >
      Não usei Jira, mas mantenho rotina ágil completa em ClickUp

remoto_desde: 2021
```

## Regras (validadas pelo gerador)

- Corpo até 200 palavras. Acima disso falha com a contagem.
- Gap com contraponto real quando existe, vindo das experiências ou dos
  cursos em data/ (ex.: Jira tem ClickUp/Redmine; Spring Batch tem
  mensageria assíncrona; SQL Server tem formação IGTI). Gap sem
  contraponto é declarado seco, sem frase de efeito.
- Sem em-dash nem en-dash (U+2013 e U+2014) no YAML da vaga.
- Todo case referencia um `produto` existente em `data/experiencias/`.
- Sentenças (frases de case, extras, contrapontos) começam com
  maiúscula, porque viram parágrafos completos.
- Números sempre conferidos com `data/*.yml`, nunca de memória.
- Não afirmar ferramenta sem base no YAML ou cursos (ex.: Bitbucket,
  Jira, SVN, SQL Server, DB2 só entram como gap ou contraponto).
- Se citar IA, o backend é sempre "externo" e o trabalho foi integração
  e orquestração.

## Checklist antes de enviar

- [ ] `python3 gerar_email.py emails/<vaga>.yml` passou
- [ ] Assunto com o cargo exato do anúncio (gerado de `vaga.cargo`)
- [ ] Currículo PDF da vaga anexado (gerado via `gerar.py` com manifesto
      correspondente)
- [ ] Gaps do anúncio todos endereçados (cobertos, com contraponto ou
      declarados)
