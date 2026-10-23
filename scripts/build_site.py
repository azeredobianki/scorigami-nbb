"""Gera o site estático a partir de site/app.src.html.

Uso: python3 -I scripts/build_site.py site/app.src.html site
Escreve site/index.html e site/app.js. O app.js lê o site/games.json, que vem de build_data.py.
"""
import re
import sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
html = src.read_text(encoding="utf-8")
m = re.search(r"<script>\n(.*)</script>\s*$", html, re.S)
js = m.group(1).replace("const DATA = /*__DATA__*/null;", "const DATA = window.__DATA;")
head, body = html[:m.start()].split("</style>", 1)
loader = """<script>
fetch("games.json").then(r => r.json()).then(d => {
  window.__DATA = d;
  const s = document.createElement("script"); s.src = "app.js"; document.body.appendChild(s);
});
</script>"""
page = ("<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        + head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
        + "body{margin:0}img{max-width:100%}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}\n</style>\n</head>\n<body>"
        + body + loader + "\n</body>\n</html>\n")
(out / "index.html").write_text(page, encoding="utf-8")
(out / "app.js").write_text(js, encoding="utf-8")
print("index.html e app.js ->", out)
