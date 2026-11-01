#!/usr/bin/env python3
"""Bouwt per boek en per taal een volwaardige boekpagina: flaptekst, productgegevens,
koopknoppen en een leesfragment (proloog + hoofdstuk 1)."""
import json, os, re, unicodedata, html as H
from fragment import fragment

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = 'https://lowlandspress.com/'
TALEN = ['nl', 'en', 'de', 'es']
LOCALE = {'nl': 'nl_NL', 'en': 'en_US', 'de': 'de_DE', 'es': 'es_ES'}
MAP = {'nl': 'boek/', 'en': 'en/book/', 'de': 'de/buch/', 'es': 'es/libro/'}
MARKT = {'nl': 'amazon.nl', 'en': 'amazon.com', 'de': 'amazon.de', 'es': 'amazon.es'}
DEEL6_MOCKUP = {
    'nl': 'mockups/nl-bekend-gezicht-smartdoorbell-mockup-v1.png',
    'en': 'mockups/en-familiar-face-smartdoorbell-mockup-v1.png',
    'de': 'mockups/de-bekanntes-gesicht-smartdoorbell-mockup-v1.png',
    'es': 'mockups/es-rostro-conocido-smartdoorbell-mockup-v1.png',
}
# Deel 7 is nog niet goedgekeurd voor publicatie: geen pagina, geen fragment.
TOT = 6

W = {
 'nl': dict(terug='Alle boeken', reeks='Thorne-thrillers', deel='Deel %d', lees='Lees het begin',
            gegevens='Productgegevens', kopen='Waar te koop', ebook='E-book', paperback='Paperback',
            hardcover='Hardcover', bij='Bekijk op %s', andere='Andere winkels', gplay='Google Play',
            uitgever='Uitgever', taal='Taal', talen={'nl':'Nederlands','en':'Engels','de':'Duits','es':'Spaans'},
            paginas="Pagina's", woorden='Woorden', isbn='ISBN', asin='ASIN', prijs='Prijs',
            verschenen='Verschenen', fragmentnoot='Het begin van het boek, zoals het in de winkel '
            'ook in te kijken is. Verder lezen kan bij de winkels hierboven.',
            binnenkort='Binnenkort verkrijgbaar'),
 'en': dict(terug='All books', reeks='Thorne thrillers', deel='Book %d', lees='Read the opening',
            gegevens='Product details', kopen='Where to buy', ebook='Ebook', paperback='Paperback',
            hardcover='Hardcover', bij='View on %s', andere='Other stores', gplay='Google Play',
            uitgever='Publisher', taal='Language', talen={'nl':'Dutch','en':'English','de':'German','es':'Spanish'},
            paginas='Pages', woorden='Words', isbn='ISBN', asin='ASIN', prijs='Price',
            verschenen='Published', fragmentnoot='The opening of the book, the same pages a store '
            'lets you look inside. Read on at any of the stores above.',
            binnenkort='Coming soon'),
 'de': dict(terug='Alle Bücher', reeks='Thorne-Thriller', deel='Band %d', lees='Der Anfang',
            gegevens='Produktdetails', kopen='Wo erhältlich', ebook='E-Book', paperback='Taschenbuch',
            hardcover='Hardcover', bij='Bei %s ansehen', andere='Weitere Shops', gplay='Google Play',
            uitgever='Verlag', taal='Sprache', talen={'nl':'Niederländisch','en':'Englisch','de':'Deutsch','es':'Spanisch'},
            paginas='Seiten', woorden='Wörter', isbn='ISBN', asin='ASIN', prijs='Preis',
            verschenen='Erschienen', fragmentnoot='Der Anfang des Buches, dieselben Seiten, die ein '
            'Shop zum Hineinlesen zeigt. Weiterlesen bei den Händlern oben.',
            binnenkort='Demnächst erhältlich'),
 'es': dict(terug='Todos los libros', reeks='Thrillers de Thorne', deel='Libro %d', lees='Lee el principio',
            gegevens='Datos del producto', kopen='Dónde comprarlo', ebook='Ebook', paperback='Tapa blanda',
            hardcover='Tapa dura', bij='Ver en %s', andere='Otras tiendas', gplay='Google Play',
            uitgever='Editorial', taal='Idioma', talen={'nl':'Neerlandés','en':'Inglés','de':'Alemán','es':'Español'},
            paginas='Páginas', woorden='Palabras', isbn='ISBN', asin='ASIN', prijs='Precio',
            verschenen='Publicado', fragmentnoot='El principio del libro, las mismas páginas que una '
            'tienda deja hojear. Sigue leyendo en cualquiera de las tiendas de arriba.',
            binnenkort='Próximamente'),
}


def e(s):
    return H.escape(str(s), quote=True)


def slug(titel):
    t = unicodedata.normalize('NFKD', titel).encode('ascii', 'ignore').decode()
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower())).strip('-')


D = json.load(open(os.path.join(HIER, '_boekdata.json'), encoding='utf-8'))
T = json.load(open(os.path.join(HIER, '_teksten.json'), encoding='utf-8'))
BOEK = {b['n']: b for b in D['boeken']}
TEKST = {b['n']: b for b in T['boeken']}
SLUGS = {(b['n'], t): slug(b['ed'][t]['titel'])
         for b in D['boeken'] if b['n'] <= TOT for t in TALEN if (b['ed'].get(t) or {}).get('titel')}
PIJL = ('<svg class="pijl" viewBox="0 0 10 10" aria-hidden="true" focusable="false">'
        '<path d="M2.6 7.4 7.4 2.6M3.8 2.6h3.6v3.6" fill="none" stroke="currentColor" '
        'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def gegevenslijst(n, taal):
    w, ed = W[taal], BOEK[n]['ed'][taal]
    rijen = [(w['uitgever'], ed.get('uitgever') or 'Lowlands Press'),
             (w['taal'], w['talen'][taal])]
    if ed.get('verschenen'):
        rijen.append((w['verschenen'], ed['verschenen']))
    if ed.get('paginas_paperback'):
        rijen.append(('%s (%s)' % (w['paginas'], w['paperback']), ed['paginas_paperback']))
    if ed.get('paginas_hardcover'):
        rijen.append(('%s (%s)' % (w['paginas'], w['hardcover']), ed['paginas_hardcover']))
    if ed.get('woorden'):
        rijen.append((w['woorden'], format(ed['woorden'], ',d').replace(',', '.')))
    for sleutel, label in (('asin_ebook', w['ebook']), ('asin_paperback', w['paperback']),
                           ('asin_hardcover', w['hardcover'])):
        if ed.get(sleutel):
            rijen.append(('%s (%s)' % (w['asin'], label), ed[sleutel]))
    for sleutel, label in (('isbn_paperback', w['paperback']), ('isbn_hardcover', w['hardcover'])):
        if ed.get(sleutel):
            rijen.append(('%s (%s)' % (w['isbn'], label), ed[sleutel]))
    return ('<dl class="gegevens">%s</dl>'
            % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(k), e(v)) for k, v in rijen))


def koopblok(n, taal):
    w, ed = W[taal], BOEK[n]['ed'][taal]
    links = (TEKST[n]['ed'][taal]['links'] if n in TEKST else {}) or {}
    uit = []
    def knop(adres, label, prijs, hoofd=False):
        p = ' <span class="prijs">%s</span>' % e('€ ' + prijs) if prijs else ''
        return ('<a class="%s" href="%s" target="_blank" rel="noreferrer">%s%s%s</a>'
                % ('koop hoofd' if hoofd else 'koop', adres, e(label), p, PIJL))
    markt = 'https://www.' + MARKT[taal]
    if ed.get('asin_ebook'):
        uit.append(knop('%s/dp/%s' % (markt, ed['asin_ebook']), w['ebook'], ed.get('prijs_ebook'), True))
    if ed.get('asin_paperback'):
        uit.append(knop('%s/dp/%s' % (markt, ed['asin_paperback']), w['paperback'], ed.get('prijs_paperback')))
    if ed.get('asin_hardcover'):
        uit.append(knop('%s/dp/%s' % (markt, ed['asin_hardcover']), w['hardcover'], ed.get('prijs_hardcover')))
    if links.get('googleplay'):
        uit.append(knop(links['googleplay'], w['gplay'], None))
    if links.get('overig'):
        uit.append(knop(links['overig'], w['andere'], None))
    if not uit:
        return '<p class="status-regel">%s</p>' % e(w['binnenkort'])
    return '<div class="koopblok">%s</div>' % ''.join(uit)


def fragmentblok(n, taal):
    delen = fragment(n, taal)
    if not delen:
        return ''
    w = W[taal]
    stuk = []
    for kop, alineas in delen:
        stuk.append('<h3>%s</h3>%s' % (e(kop), ''.join(alineas)))
    return ('<section class="fragment" aria-labelledby="fragment-%d"><h2 id="fragment-%d">%s</h2>'
            '<p class="fragmentnoot">%s</p><div class="fragmenttekst">%s</div></section>'
            % (n, n, e(w['lees']), e(w['fragmentnoot']), ''.join(stuk)))


def schema(n, taal, url):
    ed = BOEK[n]['ed'][taal]
    s = {"@context": "https://schema.org", "@type": "Book", "name": ed['titel'],
         "url": url, "inLanguage": LOCALE[taal].replace('_', '-'),
         "author": {"@type": "Person", "name": "C.M.R. Thorne"},
         "publisher": {"@type": "Organization", "name": "Lowlands Press"},
         "isPartOf": {"@type": "BookSeries", "name": "Thorne Thrillers"},
         "position": n}
    if ed.get('flaptekst'):
        s["description"] = ' '.join(ed['flaptekst'])[:1200]
    uitvoeringen = []
    for soort, asin, isbn, paginas, prijs in (
            ("EBook", ed.get('asin_ebook'), None, None, ed.get('prijs_ebook')),
            ("Paperback", ed.get('asin_paperback'), ed.get('isbn_paperback'),
             ed.get('paginas_paperback'), ed.get('prijs_paperback')),
            ("Hardcover", ed.get('asin_hardcover'), ed.get('isbn_hardcover'),
             ed.get('paginas_hardcover'), ed.get('prijs_hardcover'))):
        if not asin:
            continue
        v = {"@type": "Book", "bookFormat": "https://schema.org/" + soort,
             "isbn": isbn, "numberOfPages": paginas,
             "url": "https://www.%s/dp/%s" % (MARKT[taal], asin)}
        if prijs:
            v["offers"] = {"@type": "Offer", "price": prijs.replace(',', '.'),
                           "priceCurrency": "EUR", "availability": "https://schema.org/InStock"}
        uitvoeringen.append({k: x for k, x in v.items() if x is not None})
    if uitvoeringen:
        s["workExample"] = uitvoeringen
    return '<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False)


def bouw(n, taal):
    w = W[taal]
    ed = BOEK[n]['ed'][taal]
    tek = (TEKST[n]['ed'][taal] if n in TEKST else {})
    titel = ed['titel']
    s = SLUGS[(n, taal)]
    url = BASIS + MAP[taal] + s + '.html'
    voor = '../' * (MAP[taal].count('/'))
    omslag = voor + 'covers/%s-%d.jpg' % (taal, n)
    mock = (TEKST[n].get('mockup') if n in TEKST else None)
    if n == 6:
        omslag = voor + DEEL6_MOCKUP[taal]
    elif taal == 'nl' and mock:
        omslag = voor + mock
    pitch = tek.get('pitch') or ''
    oms = (' '.join(ed['flaptekst'])[:300] if ed.get('flaptekst') else pitch)
    social_image = (BASIS + DEEL6_MOCKUP[taal]
                    if n == 6 else BASIS + 'img/deelkaart.png')

    alt = ''.join('<link rel="alternate" hreflang="%s" href="%s%s%s.html"/>'
                  % (t, BASIS, MAP[t], SLUGS[(n, t)]) for t in TALEN if (n, t) in SLUGS)
    alt += '<link rel="alternate" hreflang="x-default" href="%s%s%s.html"/>' % (BASIS, MAP['nl'], SLUGS[(n, 'nl')])

    flap = ''.join('<p>%s</p>' % e(a) for a in (ed.get('flaptekst') or [])) or '<p>%s</p>' % e(pitch)

    doc = f'''<!DOCTYPE html><html lang="{taal}"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="stylesheet" href="{voor}css/site.css"/><link rel="stylesheet" href="{voor}css/aanpassingen.css?v=9"/>
<title>{e(titel)} | C.M.R. Thorne | Lowlands Press</title>
<meta name="description" content="{e(oms[:250])}"/>
<meta name="robots" content="index, follow"/>
<meta property="og:title" content="{e(titel)} | C.M.R. Thorne"/>
<meta property="og:description" content="{e(oms[:250])}"/>
<meta property="og:url" content="{url}"/><meta property="og:type" content="book"/>
<meta property="og:site_name" content="Lowlands Press"/><meta property="og:locale" content="{LOCALE[taal]}"/>
<meta property="og:image" content="{social_image}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:image" content="{social_image}"/>
{alt}<link rel="canonical" href="{url}"/>
{schema(n, taal, url)}</head>
<body><main>
<header class="masthead"><a class="brand" href="{voor}index.html" aria-label="Lowlands Press">
<img src="{voor}img/lowlands-press.png" alt="Lowlands Press"/><span><strong>LOWLANDS</strong><small>PRESS</small></span></a>
<nav class="languages" aria-label="{e(w['terug'])}"><a class="terug" href="{voor}index.html">{e(w['terug'])}</a></nav></header>

<section class="boekkop">
  <div class="boekkop-beeld"><img src="{omslag}" alt="{e(titel)}, C.M.R. Thorne" loading="eager"/></div>
  <div class="boekkop-tekst">
    <div class="eyebrow">{e(w['reeks'])} &middot; {e(w['deel'] % n)}</div>
    <h1>{e(titel)}</h1>
    {'<p class="ondertitel">' + e(ed['ondertitel']) + '</p>' if ed.get('ondertitel') else ''}
    <p class="pitch">{e(pitch)}</p>
    <h2 class="kopje">{e(w['kopen'])}</h2>
    {koopblok(n, taal)}
  </div>
</section>

<section class="tekstpagina boekflap">{flap}</section>

<section class="tekstpagina"><h2>{e(w['gegevens'])}</h2>{gegevenslijst(n, taal)}</section>

{fragmentblok(n, taal)}

<footer><nav class="voetlinks" aria-label="{e(w['terug'])}"><a href="{voor}index.html">{e(w['terug'])}</a></nav>
<p>&copy; 2026 C.M.R. Thorne &middot; Lowlands Press</p></footer>
</main></body></html>'''
    pad = os.path.join(HIER, MAP[taal], s + '.html')
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    open(pad, 'w', encoding='utf-8').write(doc)
    return os.path.relpath(pad, HIER)


if __name__ == '__main__':
    gemaakt = []
    for n in sorted(BOEK):
        if n > TOT:
            continue
        for taal in TALEN:
            if (n, taal) in SLUGS:
                gemaakt.append(bouw(n, taal))
    # pad per boek en taal wegschrijven, zodat bouw-talen.py ernaar kan linken
    kaart = {'%d-%s' % (n, t): MAP[t] + SLUGS[(n, t)] + '.html' for (n, t) in SLUGS}
    json.dump(kaart, open(os.path.join(HIER, '_slugs.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('%d boekpagina\'s gebouwd' % len(gemaakt))
    for p in gemaakt:
        print(' ', p)
