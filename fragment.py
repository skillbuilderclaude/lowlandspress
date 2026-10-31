#!/usr/bin/env python3
"""Haalt het leesfragment (proloog + eerste hoofdstuk) uit een manuscriptmap."""
import os, re, glob, html as H

WORTEL = os.path.expanduser('~/Boeken')
MAPPEN = {1: 'het-huis-weet-het', 2: 'de-vrijgave', 3: 'polsslag', 4: 'boek4-dna',
          5: 'boek5-ev', 6: 'boek6-deurbel', 7: 'boek7'}
PROLOOG = re.compile(r'(proloog|prologue|prolog|prólogo|prologo)', re.I)
DEEL = re.compile(r'deel|part|teil|parte', re.I)
KOP = {'nl': ('Proloog', 'Hoofdstuk 1'), 'en': ('Prologue', 'Chapter 1'),
       'de': ('Prolog', 'Kapitel 1'), 'es': ('Prólogo', 'Capítulo 1')}


def _naar_html(tekst):
    """Markdown-alinea's naar <p>. Cursief, en afgebakende blokken (logregels, transcripties)
    als <pre>, want die staan in het manuscript tussen backticks en moeten hun regelafbreking
    houden."""
    tekst = re.sub(r'^#.*$', '', tekst, flags=re.M)              # kop eraf
    uit = []
    # eerst de blokken tussen ``` eruit lichten, de rest gewoon als alinea's
    stukken = re.split(r'```', tekst)
    for i, stuk in enumerate(stukken):
        if i % 2 == 1:                                            # oneven = binnen de backticks
            regels = [r.rstrip() for r in stuk.strip('\n').split('\n')]
            if any(r.strip() for r in regels):
                uit.append('<pre class="log">%s</pre>'
                           % H.escape('\n'.join(regels).strip()))
            continue
        for a in re.split(r'\n\s*\n', stuk):
            a = a.strip()
            if not a:
                continue
            a = H.escape(' '.join(a.split()))
            a = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', a)
            uit.append('<p>%s</p>' % a)
    return uit


def fragment(n, taal):
    """(lijst van (kop, [alinea-html])) voor proloog en hoofdstuk 1, of een lege lijst."""
    map_ = os.path.join(WORTEL, MAPPEN[n], 'manuscript-%s' % taal)
    if not os.path.isdir(map_):
        return []
    bestanden = sorted(glob.glob(os.path.join(map_, '*.md')))
    if not bestanden:
        return []
    proloog = next((b for b in bestanden if PROLOOG.search(os.path.basename(b))), None)
    rest = [b for b in bestanden
            if b != proloog and not DEEL.search(os.path.basename(b))
            and not PROLOOG.search(os.path.basename(b))]
    eerste = rest[0] if rest else None
    delen = []
    for pad, kop in ((proloog, KOP[taal][0]), (eerste, KOP[taal][1])):
        if not pad:
            continue
        ruw = open(pad, encoding='utf-8').read()
        alineas = _naar_html(ruw)
        if alineas:
            delen.append((kop, alineas))
    return delen


if __name__ == '__main__':
    for n in sorted(MAPPEN):
        for t in ('nl', 'en', 'de', 'es'):
            d = fragment(n, t)
            print('boek %d %s: %s' % (n, t, ' + '.join('%s (%d alinea\'s)' % (k, len(a)) for k, a in d) or 'geen'))
