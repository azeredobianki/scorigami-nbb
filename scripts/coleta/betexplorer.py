import re, json, sys, ssl, urllib.request, time, html, os
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
def get(u):
    for a in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), context=ctx, timeout=60).read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(3 * 2 ** a)
        except Exception:
            time.sleep(3 * 2 ** a)
    return None
def parse(h, stage):
    i = h.find('table-main'); j = h.find('</table>', i)
    t = h[i:j]; rows = []; label = ''
    for tr in re.findall(r'<tr>(.*?)</tr>', t, re.S):
        th = re.search(r'<th class="h-text-left"[^>]*>([^<]*)<', tr)
        if th: label = html.unescape(th.group(1)).strip(); continue
        m = re.search(r'class="in-match"><span>(?:<strong>)?([^<]*)(?:</strong>)?</span> - <span>(?:<strong>)?([^<]*)(?:</strong>)?</span></a></td><td class="h-text-center">(?:<a[^>]*>)?([^<]*)<', tr)
        d = re.search(r'h-text-no-wrap">([^<]*)<', tr)
        if m: rows.append(dict(stage=stage, label=label, home=html.unescape(m.group(1)), away=html.unescape(m.group(2)), score=m.group(3).strip(), date=d.group(1) if d else ''))
    return rows
out = {}
for y in range(2008, 2027):
    slug = f'nbb-{y}-{y+1}'
    base = f'https://www.betexplorer.com/basketball/brazil/{slug}/results/'
    h = get(base)
    if h is None and y == 2026:
        base = 'https://www.betexplorer.com/basketball/brazil/nbb/results/'; h = get(base)
    if h is None: print(slug, 'none'); out[slug] = None; continue
    stages = dict((s, html.unescape(n).strip()) for s, n in re.findall(r'\?stage=([A-Za-z0-9]+)"[^>]*>([^<]*)<', h))
    rows = []
    if not stages: rows = parse(h, '')
    for s, n in stages.items():
        hs = get(base + '?stage=' + s); time.sleep(1.5)
        rows += parse(hs or '', n)
    out[slug] = rows
    print(slug, stages, len(rows), flush=True); time.sleep(1.5)
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=0)
