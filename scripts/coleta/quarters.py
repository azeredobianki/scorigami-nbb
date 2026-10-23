import re, sys, html
def quarters(h):
    i=h.find('score_for_quarter')
    if i<0: return None
    seg=h[i:h.find('detail_game_screen_two', i)]
    out=[]
    for q in re.split(r'<div class="quarter"', seg)[1:]:
        hm=re.search(r'id="home_quarter_\d+">\s*<strong[^>]*>([^<]*)<', q)
        aw=re.search(r'id="away_quarter_\d+">\s*<strong[^>]*>([^<]*)<', q)
        lab=re.search(r'class="quarter_time">([^<]*)<', q)
        out.append(((lab.group(1).strip() if lab else ''), html.unescape(hm.group(1)).strip() if hm else '', html.unescape(aw.group(1)).strip() if aw else ''))
    return out
if __name__=='__main__':
    for f in sys.argv[1:]:
        print(f, quarters(open(f,encoding='utf-8',errors='replace').read()))
