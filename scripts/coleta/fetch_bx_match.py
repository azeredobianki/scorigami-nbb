import json, sys, re, ssl, urllib.request, concurrent.futures as cf, time, os
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
urls = json.load(open(sys.argv[1])); ids = [l.strip() for l in open(sys.argv[2]) if l.strip() in urls]; outp = sys.argv[3]
done = {json.loads(l)['id'] for l in open(outp)} if os.path.exists(outp) else set()
todo = [i for i in ids if i not in done]; print(len(todo), flush=True)
def get(i):
    for a in range(3):
        try:
            h = urllib.request.urlopen(urllib.request.Request(urls[i], headers={'User-Agent': UA}), context=ctx, timeout=60).read().decode('utf-8', 'replace')
            st = re.search(r'id="js-eventstage">([^<]*)<', h); p = re.search(r'id="js-partial">\(([^)]*)\)', h)
            return dict(id=i, stage=st.group(1) if st else None, partial=p.group(1) if p else None, status=200)
        except Exception as e:
            err = str(e); time.sleep(3 * 2 ** a)
    return dict(id=i, stage=None, partial=None, status=err)
with open(outp, 'a') as fo, cf.ThreadPoolExecutor(4) as ex:
    for k, r in enumerate(ex.map(get, todo)):
        fo.write(json.dumps(r) + '\n'); fo.flush()
