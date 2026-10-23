"""Liga cada jogo da LNB ao jogo do BetExplorer (mesmo mando por franquia, data a até 2 dias, mesmo placar)."""
import csv, glob, json, sys, os, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
from franquias import LNB, BETEXPLORER
def load(csvdir, bxfile):
    bx = json.load(open(bxfile, encoding='utf-8')); out = {}
    for f in sorted(glob.glob(f'{csvdir}/*.csv')):
        s = os.path.basename(f)[:7]; y0 = int(s[:4]); B = []
        for r in bx.get(f'nbb-{y0}-{y0+1}') or []:
            if not r['score'] or '.' not in r['date'] or len(r['date'].strip('.').split('.')) != 3: continue
            d, m, y = r['date'].strip('.').split('.')
            B.append((BETEXPLORER.get(r['home']), BETEXPLORER.get(r['away']), r['score'], dt.date(int(y), int(m), int(d)), r['url']))
        for r in csv.DictReader(open(f, encoding='utf-8')):
            d, m, y = r['data'].split('/'); date = dt.date(int(y), int(m), int(d))
            h, a = LNB.get(r['mandante']), LNB.get(r['visitante']); sc = f"{r['pts_mandante']}:{r['pts_visitante']}"
            c = [b for b in B if b[0] == h and b[1] == a and b[2] == sc and abs((b[3] - date).days) <= 2]
            if len(c) == 1: out[r['id_lnb']] = c[0][4]
    return out
if __name__ == '__main__':
    m = load(sys.argv[1], sys.argv[2]); json.dump(m, open(sys.argv[3], 'w')); print(len(m))
