def ot_from_minutes(tm, hs, as_, tol=2.0):
    """Número de prorrogações pela soma de minutos de cada time; None se inconclusivo."""
    if not tm: return None, ''
    h = max((t[0] for t in tm if t[2] == hs), default=None)
    a = max((t[0] for t in tm if t[2] == as_), default=None)
    if h is None or a is None: return None, f'{h}/{a}'
    ks = []
    for m in (h, a):
        k = round((m - 200) / 25)
        if k < 0 or abs(m - (200 + 25 * k)) > tol: return None, f'{h}/{a}'
        ks.append(k)
    return (ks[0], f'{h}/{a}') if ks[0] == ks[1] else (None, f'{h}/{a}')
