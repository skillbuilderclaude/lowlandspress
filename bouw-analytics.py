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
    """Twee metingen. Eén telverzoek per paginaweergave, met verwijzer en merkteken uit de link,
    en één bij een klik op een link naar buiten, zodat zichtbaar is hoeveel mensen doorgaan naar
    een winkel. Geen cookie, niets in de browser opgeslagen."""
    js = ("(function(){var E='%s';try{"
          # paginaweergave
          "var q=new URLSearchParams(location.search),u=new URL(E);"
          "u.searchParams.set('u',location.pathname);"
          "if(document.referrer)u.searchParams.set('r',document.referrer);"
          "var s=q.get('utm_source')||q.get('bron');if(s)u.searchParams.set('s',s);"
          "var c=q.get('utm_content')||q.get('utm_campaign');if(c)u.searchParams.set('c',c);"
          "new Image().src=u.toString();"
          # uitgaande kliks
          "document.addEventListener('click',function(e){var a=e.target.closest&&"
          "e.target.closest('a[href^=\"http\"]');if(!a)return;"
          "var h;try{h=new URL(a.href).hostname.replace(/^www\\./,'');}catch(x){return;}"
          "if(!h||h.indexOf('lowlandspress.com')>-1)return;"
          "var v=new URL(E);v.searchParams.set('u',location.pathname);"
          "v.searchParams.set('t','uit');v.searchParams.set('d',h);"
          "if(navigator.sendBeacon){navigator.sendBeacon(v.toString());}"
          "else{new Image().src=v.toString();}},true);"
          "}catch(e){}})();" % endpoint)
    return (MERK + '<script>' + js + '</script>'
            + '<noscript><img src="' + endpoint + '?u=zonder-js" alt="" width="1" height="1"'
              ' style="position:absolute;left:-9999px"/></noscript>' + MERK)


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
