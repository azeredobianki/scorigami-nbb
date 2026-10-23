def bx_ot(m, hs, as_):
    """True/False pela página do BetExplorer (parciais por quarto e 'After Extra Time'); None se inconclusivo."""
    if m.get('stage') == 'After Extra Time': return True
    if m.get('stage') == 'Awarded' or not m.get('partial'): return None
    parts = [p.strip().split(':') for p in m['partial'].split(',')]
    try: parts = [(int(a), int(b)) for a, b in parts]
    except ValueError: return None
    if len(parts) == 4 and (sum(p[0] for p in parts), sum(p[1] for p in parts)) == (hs, as_): return False
    if len(parts) > 4 and (sum(p[0] for p in parts), sum(p[1] for p in parts)) == (hs, as_): return True
    return None
