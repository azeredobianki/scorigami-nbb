# Conferência LNB x BetExplorer

Gerado em 2026-10-23. Fonte principal: tabela de jogos da LNB (lnb.com.br). Segunda fonte: resultados do BetExplorer (betexplorer.com), temporada regular ("Main") e playoffs ("Play Offs").

Critério: mesmo mandante, mesmo visitante (pela franquia) e datas a até 2 dias de distância (o BetExplorer usa horário europeu, então jogos à noite caem no dia seguinte).

## Resumo por temporada

| Temporada | LNB regular | LNB playoffs | BetExplorer | Iguais | Data diferente | Placar diferente | Mando invertido | Só LNB | Só BetExplorer | Prorrogações | Sem dado de quartos |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2008-09 | 210 | 27 | 237 | 237 | 0 | 0 | 0 | 0 | 0 | 0 | 237 |
| 2009-10 | 182 | 39 | 196 | 189 | 2 | 5 | 0 | 25 | 0 | 0 | 221 |
| 2010-11 | 210 | 44 | 254 | 249 | 2 | 3 | 0 | 0 | 0 | 0 | 254 |
| 2011-12 | 210 | 42 | 252 | 240 | 0 | 12 | 0 | 0 | 0 | 0 | 252 |
| 2012-13 | 306 | 44 | 350 | 349 | 0 | 0 | 1 | 0 | 0 | 3 | 255 |
| 2013-14 | 272 | 44 | 316 | 316 | 0 | 0 | 0 | 0 | 0 | 13 | 15 |
| 2014-15 | 239 | 46 | 285 | 285 | 0 | 0 | 0 | 0 | 0 | 11 | 71 |
| 2015-16 | 210 | 45 | 255 | 254 | 0 | 1 | 0 | 0 | 0 | 11 | 57 |
| 2016-17 | 210 | 50 | 260 | 260 | 0 | 0 | 0 | 0 | 0 | 2 | 218 |
| 2017-18 | 210 | 43 | 253 | 253 | 0 | 0 | 0 | 0 | 0 | 12 | 40 |
| 2018-19 | 182 | 36 | 218 | 218 | 0 | 0 | 0 | 0 | 0 | 6 | 53 |
| 2019-20 | 207 | 0 | 207 | 207 | 0 | 0 | 0 | 0 | 0 | 14 | 4 |
| 2020-21 | 240 | 28 | 268 | 268 | 0 | 0 | 0 | 0 | 0 | 14 | 16 |
| 2021-22 | 272 | 34 | 306 | 306 | 0 | 0 | 0 | 0 | 0 | 19 | 9 |
| 2022-23 | 272 | 41 | 313 | 313 | 0 | 0 | 0 | 0 | 0 | 13 | 4 |
| 2023-24 | 342 | 45 | 387 | 387 | 0 | 0 | 0 | 0 | 0 | 22 | 23 |
| 2024-25 | 306 | 59 | 365 | 365 | 0 | 0 | 0 | 0 | 0 | 16 | 24 |
| 2025-26 | 380 | 59 | 439 | 439 | 0 | 0 | 0 | 0 | 0 | 21 | 14 |
| 2026-27 | 16 | 0 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Total: 5202 jogos na LNB, 5177 no BetExplorer, 5151 iguais, 4 com data diferente, 21 com placar diferente, 1 com mando invertido, 25 só na LNB, 0 só no BetExplorer.

## Prorrogações

A tabela da LNB não marca prorrogação. Para cada jogo foi lida a página da partida na LNB e contados os períodos: mais de 4 períodos é prorrogação. O resultado só é aceito quando a soma dos períodos bate com o placar final.

- Jogos com placar por quarto válido: 3435 de 5202. Desses, 177 tiveram prorrogação (o recorde é Cerrado 122x126 Fortaleza, 09/01/2022, com 4 prorrogações).
- De 2008-09 a 2011-12 a LNB não publica placar por quarto (a página só traz o placar final e a súmula é um PDF escaneado), e o BetExplorer também não tem parciais desses anos. Nesses jogos, e nos demais sem dado, o campo `ot` fica `null` (desconhecido).
- Em 2012-13 e 2016-17 a maior parte das páginas não tem quartos preenchidos.
- 30 páginas de partida retornam erro 500 na LNB mesmo após novas tentativas.

Jogos em que a soma dos quartos não bate com o placar final:
- 09/11/2013 Flamengo 84x82 Brasília: quartos 18-12 22-16 19-19 27-35. O BetExplorer confirma o placar da tabela, então a tabela foi mantida e `ot` ficou `null`.
- 04/05/2015 Mogi 91x84 Macaé: quartos 12-10 20-14 26-30 30-20. O BetExplorer confirma o placar da tabela, então a tabela foi mantida e `ot` ficou `null`.

## Correções aplicadas

- 21/03/2013 Suzano x Bauru: a tabela da LNB dá 87x82, mas o placar por quarto da própria LNB (18-20, 25-20, 26-25, 13-22) e o BetExplorer dão 82x87 para o Bauru. Corrigido para 82x87.

Todas as outras divergências ficaram com o placar da LNB. Nas de placar diferente em que a Wikipédia (páginas das temporadas em português) tem o jogo, ela confirma a LNB em todos os casos com resposta única.

## Diferenças por temporada

### 2008-09

Nenhuma diferença.

### 2009-10

- Placar diferente: 29/01/2010 Espírito Santo x Londrina: LNB 77x68, BetExplorer 77x66 (29/01/2010). Wikipédia confirma a LNB
- Data diferente: Assis 83x85 Paulistano: LNB 31/01/2010, BetExplorer 31/12/2009
- Data diferente: São José 79x100 Pinheiros: LNB 10/02/2010, BetExplorer 03/02/2010
- Placar diferente: 04/04/2010 Brasília x Flamengo: LNB 90x83, BetExplorer 88x83 (04/04/2010). Wikipédia confirma a LNB
- Placar diferente: 12/04/2010 São José x Araraquara: LNB 71x67, BetExplorer 88x74 (11/04/2010). Wikipédia não traz nenhum dos dois
- Placar diferente: 12/04/2010 Bauru x Assis: LNB 86x81, BetExplorer 90x68 (11/04/2010). Wikipédia não traz nenhum dos dois
- Placar diferente: 06/06/2010 Brasília x Flamengo: LNB 76x74, BetExplorer 88x84 (06/06/2010). Wikipédia não traz nenhum dos dois
- Só na LNB: 01/11/2009 Pinheiros 92x98 Brasília (reg, 1ª RODADA)
- Só na LNB: 01/11/2009 Franca 74x63 Assis (reg, 1ª RODADA)
- Só na LNB: 01/11/2009 Paulistano 85x88 Minas (reg, 1ª RODADA)
- Só na LNB: 01/11/2009 Flamengo 99x70 Espírito Santo (reg, 1ª RODADA)
- Só na LNB: 01/11/2009 Joinville 108x76 Londrina (reg, 1ª RODADA)
- Só na LNB: 01/11/2009 São José 84x72 Saldanha da Gama (reg, 1ª RODADA)
- Só na LNB: 01/11/2009 Araraquara 76x69 Bauru (reg, 1ª RODADA)
- Só na LNB: 02/11/2009 Paulistano 67x75 Brasília (reg, 2ª RODADA)
- Só na LNB: 06/11/2009 Flamengo 109x72 Saldanha da Gama (reg, 2ª RODADA)
- Só na LNB: 08/11/2009 Franca 88x69 Bauru (reg, 2ª RODADA)
- Só na LNB: 08/11/2009 Pinheiros 78x70 Minas (reg, 2ª RODADA)
- Só na LNB: 08/11/2009 São José 94x70 Espírito Santo (reg, 2ª RODADA)
- Só na LNB: 08/11/2009 Araraquara 64x66 Assis (reg, 2ª RODADA)
- Só na LNB: 15/11/2009 Joinville 72x69 Flamengo (reg, 3ª RODADA)
- Só na LNB: 15/11/2009 Bauru 88x64 Assis (reg, 3ª RODADA)
- Só na LNB: 15/11/2009 Saldanha da Gama 75x76 Pinheiros (reg, 3ª RODADA)
- Só na LNB: 15/11/2009 Londrina 69x67 São José (reg, 3ª RODADA)
- Só na LNB: 15/11/2009 Brasília 88x80 Franca (reg, 3ª RODADA)
- Só na LNB: 15/11/2009 Espírito Santo 54x52 Paulistano (reg, 3ª RODADA)
- Só na LNB: 08/12/2009 Saldanha da Gama 71x91 Assis (reg, 8ª RODADA)
- Só na LNB: 08/12/2009 Espírito Santo 69x67 Bauru (reg, 8ª RODADA)
- Só na LNB: 19/01/2010 Minas 91x85 Araraquara (reg, 3ª RODADA)
- Só na LNB: 31/01/2010 Flamengo 73x81 Brasília (reg, 14ª RODADA)
- Só na LNB: 26/03/2010 Araraquara 94x90 Pinheiros (reg, 25ª RODADA)
- Só na LNB: 22/05/2010 Flamengo 88x84 Brasília (po, 0ª RODADA)

### 2010-11

- Data diferente: Uberlândia 96x64 Assis: LNB 12/12/2010, BetExplorer 19/12/2010
- Data diferente: Brasília 92x85 Bauru: LNB 12/12/2010, BetExplorer 19/12/2010
- Placar diferente: 03/04/2011 Franca x Pinheiros: LNB 92x78, BetExplorer 92x76 (03/04/2011). Wikipédia confirma a LNB
- Placar diferente: 23/04/2011 Uberlândia x Brasília: LNB 96x91, BetExplorer 95x89 (23/04/2011). Wikipédia não traz nenhum dos dois
- Placar diferente: 23/04/2011 Joinville x Pinheiros: LNB 66x72, BetExplorer 65x72 (24/04/2011). Wikipédia não traz nenhum dos dois

### 2011-12

- Placar diferente: 21/11/2011 Flamengo x Pinheiros: LNB 84x89, BetExplorer 84x87 (22/11/2011). Wikipédia confirma a LNB
- Placar diferente: 01/12/2011 Flamengo x Bauru: LNB 81x66, BetExplorer 81x64 (01/12/2011). Wikipédia confirma a LNB
- Placar diferente: 03/12/2011 Tijuca x Bauru: LNB 66x72, BetExplorer 67x72 (03/12/2011). Wikipédia confirma a LNB
- Placar diferente: 15/12/2011 Limeira x Bauru: LNB 69x75, BetExplorer 69x64 (15/12/2011). Wikipédia confirma a LNB
- Placar diferente: 05/01/2012 Tijuca x Uberlândia: LNB 69x103, BetExplorer 71x103 (05/01/2012). Wikipédia confirma a LNB
- Placar diferente: 05/01/2012 Flamengo x Franca: LNB 93x81, BetExplorer 91x81 (05/01/2012). Wikipédia confirma a LNB
- Placar diferente: 14/01/2012 Minas x Liga Sorocabana: LNB 84x77, BetExplorer 84x75 (14/01/2012). Wikipédia confirma a LNB
- Placar diferente: 25/01/2012 Espírito Santo x Liga Sorocabana: LNB 74x76, BetExplorer 75x76 (25/01/2012). Wikipédia confirma a LNB
- Placar diferente: 13/03/2012 Brasília x Espírito Santo: LNB 81x66, BetExplorer 95x88 (14/03/2012). Wikipédia traz os dois placares
- Placar diferente: 29/03/2012 Liga Sorocabana x Brasília: LNB 89x91, BetExplorer 87x88 (30/03/2012). Wikipédia confirma a LNB
- Placar diferente: 06/04/2012 Brasília x Minas: LNB 87x76, BetExplorer 87x57 (06/04/2012). Wikipédia confirma a LNB
- Placar diferente: 07/05/2012 Brasília x Bauru: LNB 90x78, BetExplorer 90x76 (08/05/2012). Wikipédia confirma a LNB

### 2012-13

- Mando invertido: LNB 16/02/2013 Tijuca 63x83 Uberlândia; BetExplorer Uberlândia 83x63 Tijuca

### 2013-14

Nenhuma diferença.

### 2014-15

Nenhuma diferença.

### 2015-16

- Placar diferente: 03/03/2016 Vitória x Bauru: LNB 96x94, BetExplorer 95x94 (04/03/2016). Wikipédia confirma a LNB

### 2016-17

Nenhuma diferença.

### 2017-18

Nenhuma diferença.

### 2018-19

Nenhuma diferença.

### 2019-20

Nenhuma diferença.

### 2020-21

Nenhuma diferença.

### 2021-22

Nenhuma diferença.

### 2022-23

Nenhuma diferença.

### 2023-24

Nenhuma diferença.

### 2024-25

Nenhuma diferença.

### 2025-26

Nenhuma diferença.

### 2026-27

Nenhuma diferença.
