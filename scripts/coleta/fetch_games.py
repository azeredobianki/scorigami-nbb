import json, sys, os, ssl, urllib.request, concurrent.futures as cf, time, re
sys.path.insert(0, os.path.dirname(__file__))
from quarters import quarters
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
games = json.load(open(sys.argv[1])); outp = sys.argv[2]
done = {}
if os.path.exists(outp):
    for l in open(outp): d = json.loads(l); done[d['id']] = d
todo = [g for g in games if g['link'] and g['id'] not in done]
print(len(todo), 'to fetch', flush=True)
def get(g):
    for a in range(4):
        try:
            req = urllib.request.Request(g['link'], headers={'User-Agent': 'Mozilla/5.0'})
            h = urllib.request.urlopen(req, context=ctx, timeout=60).read().decode('utf-8', 'replace')
            q = quarters(h)
            sc = re.search(r'matchData = \{.*?\};', h, re.S)
            return dict(id=g['id'], q=q, status=200)
        except Exception as e:
            err = str(e); time.sleep(2 * 2 ** a)
    return dict(id=g['id'], q=None, status=err)
with open(outp, 'a') as fo, cf.ThreadPoolExecutor(12) as ex:
    for i, r in enumerate(ex.map(get, todo)):
        fo.write(json.dumps(r, ensure_ascii=False) + '\n'); fo.flush()
        if i % 250 == 0: print(i, flush=True)
