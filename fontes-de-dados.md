# Scorigami NBB: levantamento de fontes

## Fonte principal: LNB (lnb.com.br)

- Tabela de jogos por temporada e fase numa única página:
  `https://lnb.com.br/nbb/tabela-de-jogos/?season[]=<id>&phase[]=<1|2>` (1 = fase de classificação, 2 = playoffs).
- IDs de temporada conhecidos (do pacote `nbb-api`): 2008-09=1, 2009-10=2, 2010-11=3, 2011-12=4, 2012-13=8,
  2013-14=15, 2014-15=20, 2015-16=27, 2016-17=34, 2017-18=41, 2018-19=47, 2019-20=54, 2020-21=59, 2021-22=63,
  2022-23=71, 2023-24=80. Os IDs de 2024-25, 2025-26 e 2026-27 saem do próprio seletor da página na coleta.
- Cada linha traz data, hora, mandante, placar, visitante, rodada, fase/etapa e link do relatório
  (`/noticias/...`) ou da partida (`/partidas/...`).
- Prorrogação não aparece na tabela. Plano: ler a página de cada partida (placar por quarto) e marcar
  prorrogação quando houver período extra.
- Cuidados: os nomes dos times mudam com patrocínio (BRB/Brasília, CAIXA/Brasília Basquete...), então há um
  mapa de franquias em `scripts/build_data.py`. O `nbb-api` corta o placar com `str[:2]`, o que quebra
  placares de 100+; o nosso coletor não vai repetir isso.

## Segunda fonte (conferência)

Candidatas, a confirmar quando a rede liberar: páginas de temporada da Wikipédia em inglês (playoffs
completos), RealGM e Proballers (temporada regular). O relatório de conferência por temporada vai comparar
contagem de jogos e placar jogo a jogo, e listar cada diferença.

## Coleta completa (23/10/2026)

- 5.202 jogos com placar, de 2008-09 a 2026-27 (até a 2ª rodada de 2026-27), temporada regular e playoffs.
  2019-20 não teve playoffs (pandemia). IDs de temporada novos: 2024-25=88, 2025-26=97, 2026-27=106.
- Brutos: `dados/brutos/lnb/<temporada>_<reg|po>.csv` (com etapa, hora, número de prorrogações, placar por
  quarto, id e link da LNB), `dados/brutos/lnb/tabela_completa.json` (inclui jogos ainda sem placar),
  `dados/brutos/lnb/quartos.jsonl` (quartos lidos de cada partida), `dados/brutos/betexplorer/resultados.json`.
- Segunda fonte: BetExplorer (RealGM e Proballers bloqueiam com 403; a API da Wikipédia limita, mas as páginas
  das temporadas em português serviram de terceira fonte nas divergências).
- Relatório: `dados/conferencia/relatorio-por-temporada.md`.
- Prorrogação: conhecida em 5.105 jogos (275 com prorrogação), por três fontes em ordem: quartos da LNB,
  minutos do box score da LNB (200 por time + 25 por prorrogação) e página da partida no BetExplorer. Ficam 97
  sem informação (`ot` = null), quase todos de 2008-09 e 2010-11. Coluna `fonte_prorrogacao` nos CSVs.
- Scripts em `scripts/coleta/`: `parse_tabela.py` (tabela da LNB), `fetch_games.py` + `quarters.py` (quartos),
  `betexplorer.py`, `fetch_box.py` + `minutos.py` + `ot_minutos.py` (minutos), `bx_match.py` +
  `fetch_bx_match.py` + `bx_ot.py` (partidas do BetExplorer), `montar.py` (gera os CSVs; uso: `montar.py
  tabela_completa.json quartos.jsonl saida/ box_minutos.jsonl partidas.jsonl`), `conferir.py` + `franquias.py` (relatório). O
  `scripts/build_data.py` agora lê os CSVs com cabeçalho e preenche `ot`.
- A pasta `dados/brutos/amostra-lnb/` é a amostra antiga e pode ser apagada.
