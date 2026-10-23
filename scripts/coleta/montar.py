"""Junta a tabela da LNB com os placares por quarto e grava os CSVs brutos por temporada/fase."""
import json, csv, sys, os
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from ot_minutos import ot_from_minutes
from bx_ot import bx_ot
tab, qfile, outdir = sys.argv[1:4]
# Fontes extras de prorrogação: box score da LNB (minutos) e página da partida no BetExplorer.
BOX = {}
if len(sys.argv) > 4 and os.path.exists(sys.argv[4]):
    for l in open(sys.argv[4]): d = json.loads(l); BOX[d['id']] = d
BXM = {}
if len(sys.argv) > 5 and os.path.exists(sys.argv[5]):
    for l in open(sys.argv[5]): d = json.loads(l); BXM[d['id']] = d
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
    q = [t for t in d['q'] if (t[1], t[2]) != ('0', '0')]  # período 0-0 é dado vazio, não período jogado
    if len(q) < 4 or any(t[1] == '' or t[2] == '' for t in q):
        return '', '', 'sem_quartos'
    qs = ' '.join(f'{t[1]}-{t[2]}' for t in q)
    if (sum(int(t[1]) for t in q), sum(int(t[2]) for t in q)) != (int(x['hs']), int(x['as_'])):
        return '', qs, 'soma_diferente'
    return str(len(q) - 4), qs, 'ok'
def prorrogacao(x):
    """(número de prorrogações ou '', quartos, status dos quartos, fonte)."""
    n, qs, st = ot_info(x)
    if st == 'ok': return n, qs, st, 'quartos LNB'
    hs, as_ = int(x['hs']), int(x['as_'])
    b = BOX.get(x['id'])
    if b and b['status'] == 200:
        k, _ = ot_from_minutes(b['tm'], hs, as_)
        if k is not None: return str(k), qs, st, 'minutos LNB'
    m = BXM.get(x['id'])
    if m and m['status'] == 200:
        k = bx_ot(m, hs, as_)
        if k is not None: return ('1+' if k else '0'), qs, st, 'BetExplorer'
    return '', qs, st, ''
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
                    'prorrogacoes', 'quartos', 'status_quartos', 'fonte_prorrogacao', 'id_lnb', 'link'])
        for x in rows:
            n, qs, st, fonte = prorrogacao(x)
            w.writerow([x['date'], x['home'], x['hs'], x['as_'], x['away'], x['round'], x['stage'], x['time'],
                        n, qs, st, fonte, x['id'], x['link']])
    print(s, p, len(rows))
