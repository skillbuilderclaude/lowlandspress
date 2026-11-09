#!/usr/bin/env python3
"""Loopt elke pagina van lowlandspress.com na op dingen die een lezer zouden opvallen.

Draait standaard op de gebouwde bestanden in deze map; met --live haalt hij dezelfde
pagina's van het web, zodat je ziet wat er echt gepubliceerd staat.

    python3 controleer-paginas.py
    python3 controleer-paginas.py --live
"""
import html
import os
import re
import sys
import urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = 'https://lowlandspress.com/'

# Woorden die alleen in het Nederlands zo voorkomen. Bewust kort gehouden: 'ein', 'niet'
# en 'is' lijken te veel op Duits of Engels om iets te bewijzen.
NL_VERKLIKKERS = [
    'voordeur', 'deurbel', 'gezicht herkend', 'beweging', 'bekijken', 'corrigeren',
    'opname loopt', 'ingedrukt', 'overeenkomst', 'duimpjes', 'leden)', 'gedeeld in',
    'vriend ', 'zoekt', 'niet ingedrukt',
]
TAAL_VAN_PAD = [('en/', 'en'), ('de/', 'de'), ('es/', 'es')]


def taal(pad):
    for voor, t in TAAL_VAN_PAD:
        if pad.startswith(voor):
            return t
    return 'nl'


def paginas():
    bron = open(os.path.join(HIER, 'sitemap.xml'), encoding='utf-8').read()
    for url in re.findall(r'<loc>(.*?)</loc>', bron):
        pad = url[len(BASIS):]
        yield url, pad or 'index.html'


def haal(url, pad, live):
    if live:
        req = urllib.request.Request(url, headers={'User-Agent': 'lowlandspress-controle'})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode('utf-8', 'replace')
    lokaal = os.path.join(HIER, pad if pad.endswith('.html') else pad + 'index.html')
    return open(lokaal, encoding='utf-8').read()


def tekst_van(h):
    kaal = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', ' ', kaal))


def controleer(h, pad):
    t = taal(pad)
    uit = []

    logs = [html.unescape(x) for x in re.findall(r'<pre class="log">(.*?)</pre>', h, re.S)]
    for log in logs:
        if t != 'nl':
            gevonden = [w for w in NL_VERKLIKKERS if w in log.lower()]
            if gevonden:
                uit.append('logblok staat in het Nederlands op een %s-pagina (%s)'
                           % (t.upper(), ', '.join(gevonden[:3])))

    titels = re.findall(r'<title>(.*?)</title>', h, re.S)
    if len(titels) != 1:
        uit.append('%d <title>-elementen' % len(titels))
    elif not titels[0].strip():
        uit.append('lege <title>')

    taalattr = re.search(r'<html[^>]*\blang="([^"]+)"', h)
    if not taalattr:
        uit.append('geen lang-attribuut op <html>')
    elif taalattr.group(1)[:2] != t:
        uit.append('lang="%s" terwijl de pagina %s is' % (taalattr.group(1), t))

    if not re.search(r'<meta name="description" content="[^"]{20,}"', h):
        uit.append('geen bruikbare meta-omschrijving')

    kaarten = len(re.findall(r'<article class="boek', h))
    if pad.endswith('index.html') or pad in ('index.html',):
        if kaarten and kaarten > 10:
            uit.append('%d boekkaarten op de plank (generator heeft gestapeld)' % kaarten)

    tekst = tekst_van(h)
    # Op hele woorden en hoofdlettergevoelig: 'todo' zit in het Spaans in elke tweede zin
    # en 'nan' in Duitse woorden, dus zonder die twee eisen is het alleen maar vals alarm.
    for marker in ('TODO', 'PLACEHOLDER', 'undefined', 'NaN', 'FIXME', 'XXX'):
        if re.search(r'\b%s\b' % re.escape(marker), tekst):
            uit.append('verdachte tekst in de pagina: %r' % marker)
    for marker in ('lorem ipsum', '{{', 'None', 'null,'):
        if marker in tekst:
            uit.append('verdachte tekst in de pagina: %r' % marker)

    return uit, len(logs)


def main():
    live = '--live' in sys.argv
    print('bron:', 'het live web' if live else 'de gebouwde bestanden')
    totaal = fout = 0
    for url, pad in paginas():
        totaal += 1
        try:
            h = haal(url, pad, live)
        except Exception as e:
            print('  !! %-46s niet op te halen: %s' % (pad, e))
            fout += 1
            continue
        meldingen, aantal_logs = controleer(h, pad)
        if meldingen:
            fout += 1
            print('  !! %-46s %s' % (pad, '; '.join(meldingen)))
    print('%d pagina\'s nagelopen, %d met een melding' % (totaal, fout))


if __name__ == '__main__':
    main()
