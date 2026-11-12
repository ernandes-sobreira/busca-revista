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
| **Total de linhas** | **4.838** | **4.764 linhas com título no acordo de publicação**, condicionado à elegibilidade |

A tela mostra **4.835** periódicos: o contrato Elsevier repete três ISSN (2667-2901, 2666-9919 e 2666-6367) e a interface unifica essas linhas. Os arquivos em `data/` preservam as 4.838 linhas da fonte.

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
A norma vigente é a **Resolução 076/2022-CONSUNI**, que revoga as Resoluções 011/2013 e 012/2013: até R$ 5.000 por pesquisador por ano, para servidores efetivos (docentes e PTES), com até cinco solicitações anuais, comprovação das despesas e limite no orçamento disponível. O critério de periódico cita os quatro estratos superiores do Qualis; confirme com a PRPPG como isso se aplica no ciclo CAPES 2025-2028. Documentos: https://unemat.br/pro-reitoria/prppg/auxilio-financeiro-ao-pesquisador

## Atualização e controle
- `.github/workflows/atualizar-catalogo.yml`: importações automatizadas de Springer, Wiley, Elsevier e ACM com travas de contagem e proveniência.
- `.github/workflows/testar-plataforma.yml`: verificação de sintaxe JavaScript e auditoria de arquivos.
- `scripts/validar_painel.py`: verifica títulos, fontes, quantitativos, cobertura Elsevier e componentes essenciais.
- Interface em `plataforma.html` com filtro de revistas contempladas para UNEMAT e de cobertura a confirmar, busca de ISSN, área, exportação e checklist editorial.

**Importante:** estar listado em um acordo não é o mesmo que a CAPES aprovar uma APC específica. Verifique instituição, categoria do artigo, autor correspondente, ORCID e modalidade de acesso aberto. Pagamento direto à editora; não há reembolso.

## Auditoria de novembro de 2026
Correções aplicadas no branch `auditoria-2026-11` (ponto de reversão: tag `pre-auditoria-2026-11`). Nenhum arquivo de `data/` foi alterado.

Pendências que dependem de conferência externa:
- **PECON:** o exemplo "JIF 2025: 5,0" e "12 de 78" não pôde ser conferido no JCR (acesso por assinatura). Fontes abertas consultadas mostram 3,5 para a edição do JCR publicada em junho de 2025.
- **Springer:** a base tem 1.770 títulos; CAPES e Springer divulgaram 1.738 títulos para publicação em janeiro de 2026. Conferir se a planilha atual inclui títulos só de leitura.
- **Wiley:** a editora divulga 1.296 periódicos; a base tem 1.292. O ISSN `2832480X` (Sociology Lens) vem inválido na planilha; a URL do próprio registro indica 2832-580X.
- **Royal Society:** os 10 títulos estão sem ISSN, o que limita o cruzamento com o OpenAlex ao nome do periódico.
- **Elsevier e IEEE:** a participação da UNEMAT na Elsevier consta do Anexo II do Contrato 57/2025 e não foi reconferida nesta auditoria; na IEEE a UNEMAT não foi localizada.
- **OpenAlex:** desde fevereiro de 2026 a API exige chave para uso regular. Sem chave, a cota diária é pequena e a documentação diverge sobre o valor (US$ 0,01 ou US$ 0,10 por dia; cada busca custa US$ 0,001). Uma chave não pode ficar no HTML público; a solução estável é um intermediário com chave protegida e cache.

