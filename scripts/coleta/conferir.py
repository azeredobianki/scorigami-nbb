"""Confere os jogos da LNB (CSVs brutos) com o BetExplorer e escreve o relatório por temporada."""
import csv, json, sys, os, datetime as dt, collections
sys.path.insert(0, os.path.dirname(__file__))
from franquias import LNB, BETEXPLORER
from pathlib import Path
csvdir, bxfile, report, today = sys.argv[1], sys.argv[2], sys.argv[3], dt.date.fromisoformat(sys.argv[4])
bx = json.load(open(bxfile, encoding='utf-8'))
import re, html as H
WIKI = {}
wdir = sys.argv[5] if len(sys.argv) > 5 else None
if wdir:
    for f in Path(wdir).glob('*.html'):
        y = f.stem.split('_')[1]  # pt_2011-12 ou po_2012
        season = y if '-' in y else f'{int(y)-1}-{y[2:]}'
        WIKI[season] = WIKI.get(season, '') + ' ' + re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', f.read_text(encoding='utf-8'))))
def wiki(season, lh, la, bh, ba):
    t = WIKI.get(season)
    if not t: return 'Wikipédia: sem página da temporada'
    f = lambda x, y: bool(re.search(rf'(?<!\d){x} ?[-–] ?{y}(?!\d)', t))
    a, b = f(lh, la), f(bh, ba)
    if a and not b: return 'Wikipédia confirma a LNB'
    if b and not a: return 'Wikipédia confirma o BetExplorer'
    if a and b: return 'Wikipédia traz os dois placares'
    return 'Wikipédia não traz nenhum dos dois'
def bdate(s, season_end):
    if s == 'Today': return today
    if s == 'Yesterday': return today - dt.timedelta(1)
    p = s.strip('.').split('.')
    if len(p) == 2: return dt.date(today.year, int(p[1]), int(p[0]))
    return dt.date(int(p[2]), int(p[1]), int(p[0]))
lines = ['# Conferência LNB x BetExplorer', '',
         f'Gerado em {today.isoformat()}. Fonte principal: tabela de jogos da LNB (lnb.com.br). Segunda fonte: '
         'resultados do BetExplorer (betexplorer.com), temporada regular ("Main") e playoffs ("Play Offs").', '',
         'Critério: mesmo mandante, mesmo visitante (pela franquia) e datas a até 2 dias de distância '
         '(o BetExplorer usa horário europeu, então jogos à noite caem no dia seguinte).', '']
summary = []; details = []; unknown = set(); diffs_all = []
seasons = sorted({p.stem.split('_')[0] for p in Path(csvdir).glob('*.csv')})
for s in seasons:
    L = []
    for ph in ('reg', 'po'):
        f = Path(csvdir) / f'{s}_{ph}.csv'
        if not f.exists(): continue
        for r in csv.DictReader(open(f, encoding='utf-8')):
            d, m, y = r['data'].split('/')
            h, a = LNB.get(r['mandante']), LNB.get(r['visitante'])
            if h is None: unknown.add(('LNB', r['mandante']))
            if a is None: unknown.add(('LNB', r['visitante']))
            L.append(dict(ph=ph, date=dt.date(int(y), int(m), int(d)), h=h or r['mandante'], a=a or r['visitante'],
                          hs=int(r['pts_mandante']), as_=int(r['pts_visitante']), raw=r))
    y0 = int(s[:4]); slug = f'nbb-{y0}-{y0+1}'
    B = []
    for r in bx.get(slug) or []:
        if not r['score']: continue
        h, a = BETEXPLORER.get(r['home']), BETEXPLORER.get(r['away'])
        if h is None: unknown.add(('BX', r['home']))
        if a is None: unknown.add(('BX', r['away']))
        hs, as_ = map(int, r['score'].split(':'))
        B.append(dict(ph='po' if r['stage'] == 'Play Offs' else 'reg', date=bdate(r['date'], y0 + 1), h=h or r['home'],
                      a=a or r['away'], hs=hs, as_=as_, label=r['label']))
    usedB = set(); res = collections.Counter(); notes = []
    pairs = collections.defaultdict(list)
    for j, b in enumerate(B): pairs[(b['h'], b['a'])].append(j)
    def find(l, swap=False):
        key = (l['a'], l['h']) if swap else (l['h'], l['a'])
        best = None
        for j in pairs.get(key, []):
            if j in usedB: continue
            dd = abs((B[j]['date'] - l['date']).days)
            if dd <= 2 and (best is None or dd < best[0]): best = (dd, j)
        return best[1] if best else None
    pending = []
    # 1ª passada: mesmo placar
    for i, l in enumerate(L):
        cands = [j for j in pairs.get((l['h'], l['a']), []) if j not in usedB and abs((B[j]['date'] - l['date']).days) <= 2
                 and (B[j]['hs'], B[j]['as_']) == (l['hs'], l['as_'])]
        if cands:
            usedB.add(cands[0]); res['iguais'] += 1
            if B[cands[0]]['ph'] != l['ph']: res['fase diferente'] += 1; notes.append(f"- Fase diferente: {l['date']:%d/%m/%Y} {l['h']} {l['hs']}x{l['as_']} {l['a']} (LNB: {l['ph']}, BetExplorer: {B[cands[0]]['ph']})")
        else: pending.append(l)
    rest = []
    for l in pending:
        j = find(l)
        if j is not None:
            usedB.add(j); res['placar diferente'] += 1; b = B[j]
            notes.append(f"- Placar diferente: {l['date']:%d/%m/%Y} {l['h']} x {l['a']}: LNB {l['hs']}x{l['as_']}, BetExplorer {b['hs']}x{b['as_']} ({b['date']:%d/%m/%Y}). {wiki(s, l['hs'], l['as_'], b['hs'], b['as_'])}")
            diffs_all.append((s, l, b)); continue
        j = find(l, swap=True)
        if j is not None:
            usedB.add(j); b = B[j]
            same = (b['hs'], b['as_']) == (l['as_'], l['hs'])
            res['mando invertido'] += 1
            notes.append(f"- Mando invertido{'' if same else ' e placar diferente'}: LNB {l['date']:%d/%m/%Y} {l['h']} {l['hs']}x{l['as_']} {l['a']}; BetExplorer {b['h']} {b['hs']}x{b['as_']} {b['a']}")
            continue
        cands = [j for j in pairs.get((l['h'], l['a']), []) if j not in usedB and (B[j]['hs'], B[j]['as_']) == (l['hs'], l['as_'])]
        if cands:
            j = min(cands, key=lambda j: abs((B[j]['date'] - l['date']).days)); usedB.add(j); b = B[j]
            res['data diferente'] += 1
            notes.append(f"- Data diferente: {l['h']} {l['hs']}x{l['as_']} {l['a']}: LNB {l['date']:%d/%m/%Y}, BetExplorer {b['date']:%d/%m/%Y}")
            continue
        rest.append(l)
    for l in rest:
        res['só na LNB'] += 1
        notes.append(f"- Só na LNB: {l['date']:%d/%m/%Y} {l['h']} {l['hs']}x{l['as_']} {l['a']} ({l['ph']}, {l['raw']['rodada']})")
    for j, b in enumerate(B):
        if j in usedB: continue
        res['só no BetExplorer'] += 1
        notes.append(f"- Só no BetExplorer: {b['date']:%d/%m/%Y} {b['h']} {b['hs']}x{b['as_']} {b['a']} ({b['ph']}, {b['label']})")
    ot = collections.Counter(l['raw']['status_quartos'] if l['raw']['status_quartos'] != 'ok' else ('prorrogação' if l['raw']['prorrogacoes'] not in ('', '0') else 'sem prorrogação') for l in L)
    summary.append((s, sum(1 for l in L if l['ph'] == 'reg'), sum(1 for l in L if l['ph'] == 'po'), len(B), res, ot))
    details.append((s, notes))
lines += ['## Resumo por temporada', '',
          '| Temporada | LNB regular | LNB playoffs | BetExplorer | Iguais | Data diferente | Placar diferente | Mando invertido | Só LNB | Só BetExplorer | Prorrogações | Sem dado de quartos |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
for s, nr, np_, nb, res, ot in summary:
    lines.append(f"| {s} | {nr} | {np_} | {nb} | {res['iguais']} | {res['data diferente']} | {res['placar diferente']} | {res['mando invertido']} | {res['só na LNB']} | {res['só no BetExplorer']} | {ot['prorrogação']} | {ot['sem_quartos'] + ot['soma_diferente']} |")
tot = collections.Counter()
for *_, res, ot in summary: tot.update(res)
lines += ['', f"Total: {sum(x[1]+x[2] for x in summary)} jogos na LNB, {sum(x[3] for x in summary)} no BetExplorer, {tot['iguais']} iguais, {tot['data diferente']} com data diferente, "
          f"{tot['placar diferente']} com placar diferente, {tot['mando invertido']} com mando invertido, {tot['só na LNB']} só na LNB, {tot['só no BetExplorer']} só no BetExplorer.", '']
if unknown: lines += ['Nomes sem franquia mapeada: ' + ', '.join(f'{a}: {b}' for a, b in sorted(unknown)), '']
lines += ['## Diferenças por temporada', '']
for s, notes in details:
    lines.append(f'### {s}'); lines.append('')
    lines += notes if notes else ['Nenhuma diferença.']
    lines.append('')
Path(report).write_text('\n'.join(lines), encoding='utf-8')
print('\n'.join(lines[:40]))
