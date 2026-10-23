"""Junta a tabela da LNB com os placares por quarto e grava os CSVs brutos por temporada/fase."""
import json, csv, sys, os
from pathlib import Path
tab, qfile, outdir = sys.argv[1:4]
games = json.load(open(tab, encoding='utf-8'))
# Correções manuais: só quando o placar por quarto da própria LNB e a segunda fonte concordam contra a tabela.
CORRECOES = {
    '2462': ('82', '87'),  # Suzano x Bauru, 21/03/2013: tabela da LNB inverte o placar; quartos e BetExplorer dão 82x87
}
for x in games:
    if x['id'] in CORRECOES:
        x['hs'], x['as_'] = CORRECOES[x['id']]
Q = {}
for l in open(qfile, encoding='utf-8'):
    d = json.loads(l); Q[d['id']] = d
def ot_info(x):
    d = Q.get(x['id'])
    if not d or d['status'] != 200 or not d['q']:
        return '', '', 'sem_quartos'
    q = d['q']
    if len(q) < 4 or any(t[1] == '' or t[2] == '' for t in q):
        return '', '', 'sem_quartos'
    qs = ' '.join(f'{t[1]}-{t[2]}' for t in q)
    if (sum(int(t[1]) for t in q), sum(int(t[2]) for t in q)) != (int(x['hs']), int(x['as_'])):
        return '', qs, 'soma_diferente'
    return str(len(q) - 4), qs, 'ok'
out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
by = {}
for x in games:
    if x['hs'] == '' or x['as_'] == '':
        continue
    by.setdefault((x['season'], x['phase']), []).append(x)
for (s, p), rows in sorted(by.items()):
    with open(out / f'{s}_{p}.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['data', 'mandante', 'pts_mandante', 'pts_visitante', 'visitante', 'rodada', 'etapa', 'hora',
                    'prorrogacoes', 'quartos', 'status_quartos', 'id_lnb', 'link'])
        for x in rows:
            n, qs, st = ot_info(x)
            w.writerow([x['date'], x['home'], x['hs'], x['as_'], x['away'], x['round'], x['stage'], x['time'],
                        n, qs, st, x['id'], x['link']])
    print(s, p, len(rows))
