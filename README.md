# Busca Revista UNEMAT — painel público de publicação científica

Plataforma: https://ernandes-sobreira.github.io/busca-revista/plataforma.html

## Catálogos institucionais integrados (10/11/2026)

| Editora | Registros na base | Elegibilidade do título para APC |
|---|---:|---|
| Springer | 1.770 | Lista oficial Springer; confirmação do artigo e autor necessária |
| Wiley | 1.292 | Planilha oficial CAPES 2026 (periódicos híbridos) |
| Elsevier | 1.693 | Contrato CAPES 57/2025: **1.619 Read & Publish**, **74 apenas leitura** |
| ACM | 73 | Contrato CAPES 56/2025, títulos para publicação |
| Royal Society Publishing | 10 | Página oficial Royal Society CAPES |
| **Total de linhas** | **4.838** | **4.764 títulos potencialmente com APC coberta**, condicionado à elegibilidade |

**ACS:** participação institucional da UNEMAT verificada, porém a lista nominal ainda não foi incorporada. A ACS informa que os periódicos da editora são contemplados no acordo CAPES, ressalvadas condições específicas; consultar https://acsopenscience.org/customers/capes/ e https://pubs.acs.org/journal/ . **IEEE:** UNEMAT não localizada na lista institucional divulgada e, portanto, não certificada como elegível.

## Proveniência
- Springer: `data/springer.json`, extraído da planilha Springer Nature referente ao acordo CAPES.
- Wiley: `data/wiley.json`, planilha oficial [Wiley CAPES 2026](https://authors.wiley.com/asset/2026-Peri%C3%B3dicos-elegiveis-CAPES-Wiley.xlsx) com 1.292 registros distintos válidos.
- Elsevier: `data/elsevier.json`, extraído do [Contrato 57/2025](https://www.gov.br/capes/pt-br/centrais-de-conteudo/documentos/contratos-capes/04122025_Contrato_572025_SEI_2729395.pdf/@@display-file/file) e validado contra o total do contrato.
- ACM: `data/acm.json`, extraído do [Contrato 56/2025](https://www.gov.br/capes/pt-br/centrais-de-conteudo/documentos/contratos-capes/04122025_SEI_2729393_Contrato_56.pdf/@@display-file/file).
- Royal Society: `data/royal-society.json`, [página do acordo](https://royalsociety.org/journals/capes/).

## Interpretação dos indicadores
Fator de impacto (`jif_editora`) preenchido somente quando informado pela planilha Wiley. **O ano do JIF não está identificado nessa fonte**: não usar em análises formais antes da conferência no Journal Citation Reports. Quartis SJR e JIF não são inventados.

## Apoio UNEMAT
Foi relatado teto de R$ 5.000 por docente efetivo, **mas a norma atual com esse valor e a disponibilidade orçamentária não foram comprovadas**. A Resolução 011/2013–CONSUNI é histórica e remete o valor a outra norma; consulte a PRPPG antes de assumir elegibilidade financeira.

## Atualização e controle
- `.github/workflows/atualizar-catalogo.yml`: importações automatizadas de Springer, Wiley, Elsevier e ACM com travas de contagem e proveniência.
- `.github/workflows/testar-plataforma.yml`: verificação de sintaxe JavaScript e auditoria de arquivos.
- `scripts/validar_painel.py`: verifica títulos, fontes, quantitativos, cobertura Elsevier e componentes essenciais.
- Interface em `plataforma.html` com filtro de revistas contempladas para UNEMAT e de cobertura a confirmar, busca de ISSN, área, exportação e checklist editorial.

**Importante:** estar listado em um acordo não é o mesmo que a CAPES aprovar uma APC específica. Verifique instituição, categoria do artigo, autor correspondente, ORCID e modalidade de acesso aberto. Pagamento direto à editora; não há reembolso.
