# Busca Revista UNEMAT — Plataforma de apoio à publicação científica

**Página principal:** `plataforma.html` (redirecionamento automático de `index.html`).

## Ativar o site
GitHub → Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save.

Endereço esperado depois da publicação: https://ernandes-sobreira.github.io/busca-revista/

## Situação dos dados — 10/11/2026
- O catálogo inicial possui **12 títulos de exemplo**, incluindo dois periódicos UNEMAT explicitamente sem APC conforme suas páginas.
- O **catálogo completo de cada editora ainda não foi importado para o repositório**. A aba «Importar catálogos» permite ao navegador ler listas XLSX/CSV oficiais, mas os dados ficam locais até serem exportados e publicados no GitHub.
- Os totais divulgados pela CAPES (Springer 1.738, Elsevier 1.619, ACM 73, IEEE 217 conforme comunicado de 2024) não são métricas de registros carregados nem garantia de APC para a UNEMAT.
- A **UNEMAT está na lista de instituições Springer**. Na página oficial da Springer Nature, asterisco identifica as instituições que participam apenas do acordo Springer e **não do Nature**; a universidade aparece com asterisco.
- O apoio institucional de **R$ 5.000 por docente efetivo** foi informado pelo usuário, mas a norma vigente, o orçamento, a disponibilidade e as regras do benefício **ainda não foram confirmados por documento oficial**. O simulador é hipotético.

## Fontes oficiais
- [CAPES — orientação APC, 06/11/2026](https://www.gov.br/capes/pt-br/assuntos/noticias/saiba-como-publicar-artigos-em-acesso-aberto)
- [CAPES — instruções completas e Portarias](https://www.gov.br/capes/pt-br/acesso-a-informacao/acoes-e-programas/carta-de-servicos-ao-usuario/obter-acesso-ao-portal-de-periodicos-da-capes)
- [Springer Nature — acordo CAPES, listas XLSX e instituições](https://www.springernature.com/br/open-science/oa-agreements/brazil/capes)
- [Elsevier — catálogo elegível por título e assunto](https://agreements.journals.elsevier.com/capes)
- [Revistas da UNEMAT](https://periodicos.unemat.br/index/pt_BR)

## Critérios
Aderência temática, ética editorial, indexação e condições de APC vêm antes do uso isolado de JIF ou quartil. Qualis histórico não é critério exclusivo para selecionar revista.

## Limitações técnicas
Planilhas XLSX exigem a biblioteca SheetJS via CDN; importação e buscas locais não criam banco central institucional. Uma implantação de produção precisa de base versionada com atualização das listas por editora, auditoria de elegibilidade institucional e de cada periódico, versionamento das normas UNEMAT e eventualmente atualização licenciada de indicadores JCR/Scopus.
