import json, sys, os, ssl, urllib.request, concurrent.futures as cf, time
sys.path.insert(0, os.path.dirname(__file__))
from minutos import team_minutes
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
games = {g['id']: g for g in json.load(open(sys.argv[1]))}
ids = [l.strip() for l in open(sys.argv[2]) if l.strip()]
outp = sys.argv[3]
done = set()
if os.path.exists(outp):
    done = {json.loads(l)['id'] for l in open(outp)}
todo = [i for i in ids if i not in done]
print(len(todo), 'to fetch', flush=True)
def get(i):
    g = games[i]; err = ''
    for a in range(3):
        try:
            h = urllib.request.urlopen(urllib.request.Request(g['link'], headers={'User-Agent': 'Mozilla/5.0'}), context=ctx, timeout=60).read().decode('utf-8', 'replace')
            return dict(id=i, tm=team_minutes(h), status=200)
        except Exception as e:
            err = str(e); time.sleep(2 * 2 ** a)
    return dict(id=i, tm=None, status=err)
with open(outp, 'a') as fo, cf.ThreadPoolExecutor(12) as ex:
    for k, r in enumerate(ex.map(get, todo)):
        fo.write(json.dumps(r) + '\n'); fo.flush()
        if k % 250 == 0: print(k, flush=True)
