import re
def team_minutes(h):
    """Soma dos minutos dos jogadores em cada tabela de box score (sem duplicatas de abas)."""
    out = []
    for t in re.findall(r'<table.*?</table>', h, re.S):
        rows = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', r)).strip() for r in re.findall(r'<tr.*?</tr>', t, re.S)]
        if not rows or not rows[0].startswith('Nr. Jogador'): continue
        tot = 0.0; n = 0; equipe = None
        for r in rows[1:]:
            m = re.match(r'#\S* .*? (\d+) (\d+(?:\.\d+)?) (\d+)/', r)
            if r.startswith('Equipe'):
                e = re.match(r'Equipe \d+ [\d.]+ (\d+)/', r); equipe = int(e.group(1)) if e else None; continue
            if m: tot += float(m.group(2)); n += 1
        out.append((round(tot, 1), n, equipe))
    return out
