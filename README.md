# Scorigami NBB

Todos os placares finais do NBB (Novo Basquete Brasil) desde 2008-09, no estilo do
[NBA Scorigami](https://www.scorigaminba.com/). Uma scorigami é um placar final que nunca tinha acontecido.

## Estrutura

| Pasta | O que tem |
|---|---|
| `site/` | Site estático. Só `index.html`, `app.js` e `games.json` são publicados. `app.src.html` é o código-fonte. |
| `scripts/coleta/` | Coleta na LNB, placar por quarto (prorrogação), segunda fonte (BetExplorer) e conferência. |
| `scripts/build_data.py` | Gera `site/games.json` a partir dos CSVs brutos. |
| `scripts/build_site.py` | Gera `site/index.html` e `site/app.js` a partir de `site/app.src.html`. |
| `dados/brutos/` | Dados brutos da LNB e do BetExplorer (não vão para o site). |
| `dados/conferencia/` | Relatório de conferência por temporada. |
| `fontes-de-dados.md` | Fontes, IDs de temporada e decisões de coleta. |

## Atualizar

```sh
python3 -I scripts/build_data.py dados/brutos/lnb site/games.json
python3 -I scripts/build_site.py site/app.src.html site
```

Ver o site localmente: `cd site && python3 -m http.server`, depois abrir http://localhost:8000.

## Publicação

O site fica na Cloudflare, em [scorigaminbb.azeredo.app](https://scorigaminbb.azeredo.app), e é publicado a cada push na `main`.

## Regras

- Vale o placar final, com prorrogação. A prorrogação é conhecida a partir de 2012-13.
- Vitórias por W.O. (20 × 0) ficam de fora.
- Nomes de patrocínio são unidos na franquia (mapa em `scripts/build_data.py`).
