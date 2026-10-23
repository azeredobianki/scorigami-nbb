"""Embute site/games.json no HTML da prévia. Uso: python3 -I scripts/bundle_preview.py site/app.src.html site/games.json saida.html"""
import sys
from pathlib import Path
src, data, out = sys.argv[1:4]
html = Path(src).read_text(encoding="utf-8").replace("/*__DATA__*/null", Path(data).read_text(encoding="utf-8"))
Path(out).write_text(html, encoding="utf-8")
print(out, len(html), "bytes")
