import re, sys, json, html
from pathlib import Path
def txt(s): return html.unescape(re.sub(r'<[^>]+>', ' ', s)).split() and ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).split()) or ''
out=[]
for f in sorted(Path(sys.argv[1]).glob('*_[12].html')):
    season, ph = f.stem.split('_')
    h=f.read_text(encoding='utf-8', errors='replace')
    h=re.sub(r'<!--.*?-->', '', h, flags=re.S)
    rows=re.split(r'<tr\b', h)
    for r in rows:
        m=re.search(r'data-real-id="(\d+)"', r)
        if not m: continue
        rid=m.group(1)
        d=re.search(r'data-label="DATA">\s*<span[^>]*>([^<]*)</span>\s*<span[^>]*>([^<]*)</span>', r)
        home=re.search(r'home_team_value[^>]*>\s*<span class="team-shortname">([^<]*)<', r)
        away=re.search(r'visitor_team_value[^>]*>\s*<span class="team-shortname">([^<]*)<', r)
        sc=re.search(r'score_value show-for-medium">(.*?)</td>', r, re.S)
        scs=sc.group(1) if sc else ''
        hs=re.search(r'<span class="home">\s*(\d*)\s*</span>', scs); as_=re.search(r'<span class="away">\s*(\d*)\s*</span>', scs)
        link=re.search(r'href="([^"]+)"', scs)
        rnd=re.search(r'data-label="RODADA">(.*?)</td>', r, re.S)
        stg=re.search(r'class="stage_value hide_value" data-label="FASE">(.*?)</td>', r, re.S)
        champ=re.search(r'data-label="CAMPEONATO">(.*?)</td>', r, re.S)
        out.append(dict(id=rid, season=season, phase='reg' if ph=='1' else 'po',
            date=d.group(1).strip() if d else '', time=d.group(2).strip() if d else '',
            home=html.unescape(home.group(1).strip()) if home else '', away=html.unescape(away.group(1).strip()) if away else '',
            hs=hs.group(1) if hs else '', as_=as_.group(1) if as_ else '', link=link.group(1) if link else '',
            round=txt(rnd.group(1)) if rnd else '', stage=txt(stg.group(1)) if stg else '', champ=txt(champ.group(1)) if champ else '',
            score_text=txt(scs)))
json.dump(out, open(sys.argv[2],'w',encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(out))
