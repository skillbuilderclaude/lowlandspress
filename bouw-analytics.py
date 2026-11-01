#!/usr/bin/env python3
"""Zet de bezoekersteller op elke pagina, of haalt hem er weer af.

Zolang `endpoint` in _analytics.json leeg is staat er geen enkel script op de site; dat is de
toestand waarin de privacyverklaring klopt zoals hij nu geschreven is. Zodra er een adres in
staat, komt op elke pagina een klein script dat één telverzoek doet. Geen cookies, geen
profiel, geen derde partij die meer ziet dan de pagina en de verwijzer.
"""
import glob, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
MERK = '<!-- teller -->'
CFG = json.load(open(os.path.join(HIER, '_analytics.json'), encoding='utf-8'))


def blok(endpoint):
    return (MERK +
            '<script data-goatcounter="%s" async '
            'src="//gc.zgo.at/count.js"></script>' % endpoint + MERK)


def paginas():
    uit = []
    for patroon in ('*.html', '*/*.html', '*/*/*.html'):
        uit += glob.glob(os.path.join(HIER, patroon))
    return sorted(p for p in uit if not os.path.basename(p).startswith('_'))


def zet(endpoint):
    aan = bool(endpoint)
    n = 0
    for pad in paginas():
        h = open(pad, encoding='utf-8').read()
        schoon = re.sub(re.escape(MERK) + '.*?' + re.escape(MERK), '', h, flags=re.S)
        nieuw = schoon.replace('</body>', blok(endpoint) + '</body>') if aan else schoon
        if nieuw != h:
            open(pad, 'w', encoding='utf-8').write(nieuw)
            n += 1
    return n, len(paginas())


if __name__ == '__main__':
    e = CFG.get('endpoint') or ''
    n, totaal = zet(e)
    print('teller %s; %d van %d pagina\'s aangepast'
          % ('AAN op ' + e if e else 'UIT (geen enkel script op de site)', n, totaal))
