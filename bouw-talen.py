#!/usr/bin/env python3
"""Bouwt de Engelse, Duitse en Spaanse versie van de voorpagina uit index.html (NL)
en _teksten.json. De Nederlandse pagina is de bron; die wordt alleen voorzien van
hreflang-verwijzingen."""
import json, os, re, html as H

HIER = os.path.dirname(os.path.abspath(__file__))
TALEN = ['nl', 'en', 'de', 'es']
LOCALE = {'nl': 'nl_NL', 'en': 'en_US', 'de': 'de_DE', 'es': 'es_ES'}
HREF = {'nl': 'nl', 'en': 'en', 'de': 'de', 'es': 'es'}
BASIS = 'https://lowlandspress.com/'

D = json.load(open(os.path.join(HIER, '_teksten.json'), encoding='utf-8'))
_sp = os.path.join(HIER, '_slugs.json')
SLUGS = json.load(open(_sp, encoding='utf-8')) if os.path.exists(_sp) else {}
UI = D['ui']
BOEKEN = sorted(D['boeken'], key=lambda b: b['n'])
# deel 6 en 7 staan niet in _teksten.json; ze komen uit EXTRA hieronder
BOEKEN = BOEKEN + [{'n': 6}, {'n': 7}]

# ---- deel 6 en 7: aangekondigd, staan niet in _teksten.json ----
EXTRA = {
 6: {'omslag': 'covers/nl-bekend-gezicht.jpg', 'status': 'binnenkort',
     'nl': ('Bekend Gezicht', 'De deurbel van de buurvrouw zet een naam onder de man op de stoep. Alleen is hij het niet.',
            'Het manuscript is af in het Nederlands, Engels, Duits en Spaans. De editie wacht op de laatste stap bij de winkels.'),
     'en': ('Familiar Face', "The neighbour's doorbell puts a name to the man on the step. It isn't him.",
            'The paperback is out. The ebook follows shortly.'),
     'de': ('Bekanntes Gesicht', 'Die Türklingel der Nachbarin setzt einen Namen unter den Mann auf der Treppe. Nur ist er es nicht.',
            'Das Taschenbuch ist erschienen. Das E-Book folgt in Kürze.'),
     'es': ('Rostro conocido', 'El timbre de la vecina pone un nombre al hombre que está en la puerta. Pero no es él.',
            'El manuscrito está terminado en neerlandés, inglés, alemán y español. La edición espera el último paso en las tiendas.'),
     'links': {'en': {'paperback': 'https://www.amazon.com/dp/B0HPVT557H'},
               'de': {'paperback': 'https://www.amazon.de/dp/B0HPVCV7B7'}}},
 7: {'omslag': None, 'status': 'voorbereiding',
     'nl': ('Poorttijd', 'Een schoolpasje registreerde wie er die middag naar binnen ging. Haar eigen scan staat op het verkeerde uur.',
            'Deel zeven wordt geschreven. Verschijningsdatum nog niet bekend.'),
     'en': ('Poorttijd', 'A school pass logged who went in that afternoon. Her own scan is at the wrong hour.',
            'Book seven is being written. Working title, Dutch. No publication date yet.'),
     'de': ('Poorttijd', 'Ein Schulausweis hat festgehalten, wer an jenem Nachmittag hineinging. Ihr eigener Scan steht auf der falschen Uhrzeit.',
            'Band sieben entsteht gerade. Niederländischer Arbeitstitel. Ein Erscheinungstermin steht noch nicht fest.'),
     'es': ('Poorttijd', 'Una tarjeta escolar registró quién entró aquella tarde. Su propio escaneo marca una hora que no encaja.',
            'El séptimo libro se está escribiendo. Título provisional en neerlandés. Todavía sin fecha de publicación.')},
}
LABEL = {
 'binnenkort':   {'nl': 'Binnenkort',      'en': 'Coming soon',  'de': 'Demnächst',  'es': 'Próximamente'},
 'voorbereiding':{'nl': 'In voorbereiding','en': 'In progress',  'de': 'In Arbeit',  'es': 'En preparación'},
}
OMSLAG_VOLGT = {'nl': 'OMSLAG<br/>VOLGT', 'en': 'COVER<br/>TO COME',
                'de': 'COVER<br/>FOLGT', 'es': 'PORTADA<br/>PENDIENTE'}
# teller in de kop: zeven delen, vijf te koop
KOP = {
 'en': ('Seven villages where a device was watching.', 'Seven cases. One recurring detective.',
        'The first five books are published in Dutch, English, German and Spanish. Which editions are on sale, ebook or print, differs per store and per language.'),
 'de': ('Sieben Dörfer, in denen ein Gerät mitgesehen hat.', 'Sieben Fälle. Eine Ermittlerin, die wiederkommt.',
        'Die ersten fünf Bände erscheinen auf Niederländisch, Englisch, Deutsch und Spanisch. Welche Ausgaben lieferbar sind, E-Book oder Print, hängt von Shop und Sprache ab.'),
 'es': ('Siete pueblos donde un aparato estaba mirando.', 'Siete casos. Una investigadora que siempre vuelve.',
        'Los cinco primeros libros se publican en neerlandés, inglés, alemán y español. Qué ediciones hay a la venta, digital o en papel, depende de la tienda y del idioma.'),
}
META = {
 'en': ('Lowlands Press', 'Lowlands Press is an independent publisher in the south-west of the Netherlands. Books in Dutch, English, German and Spanish, starting with the Thorne thrillers by C.M.R. Thorne.'),
 'de': ('Lowlands Press', 'Lowlands Press ist ein unabhängiger Verlag im Südwesten der Niederlande. Bücher auf Niederländisch, Englisch, Deutsch und Spanisch, beginnend mit den Thorne-Thrillern von C.M.R. Thorne.'),
 'es': ('Lowlands Press', 'Lowlands Press es una editorial independiente del suroeste de los Países Bajos. Libros en neerlandés, inglés, alemán y español, empezando por los thrillers de Thorne de C.M.R. Thorne.'),
}
PAGINAS = {'nl': ('over.html', 'contact.html', 'privacy.html', 'voorwaarden.html'),
           'en': ('about.html', 'contact.html', 'privacy.html', 'terms.html'),
           'de': ('ueber.html', 'kontakt.html', 'datenschutz.html', 'nutzungsbedingungen.html'),
           'es': ('sobre.html', 'contacto.html', 'privacidad.html', 'condiciones.html')}
MEER = {'nl': 'Over dit boek en een leesfragment',
        'en': 'About this book and an excerpt',
        'de': 'Über dieses Buch und eine Leseprobe',
        'es': 'Sobre este libro y un fragmento'}
VOETREGEL = {
 'nl': 'Lowlands Press · KvK 52231895 · Klundert, Nederland',
 'en': 'Lowlands Press · Chamber of Commerce 52231895 · Klundert, the Netherlands',
 'de': 'Lowlands Press · Handelsregister (KvK) 52231895 · Klundert, Niederlande',
 'es': 'Lowlands Press · Registro Mercantil (KvK) 52231895 · Klundert, Países Bajos',
}
PAGINA_LABEL = {
 'nl': ('Over Lowlands Press','Contact','Privacy','Voorwaarden'),
 'en': ('About Lowlands Press','Contact','Privacy','Terms'),
 'de': ('Über Lowlands Press','Kontakt','Datenschutz','Nutzungsbedingungen'),
 'es': ('Sobre Lowlands Press','Contacto','Privacidad','Condiciones'),
}

def e(s):
    return H.escape(s, quote=True)

RECENSIE = {
 'nl': ('EEN PAAR REGELS', 'Een boek uit?',
        'Winkels laten vooral zien wat gelezen en besproken wordt, en zonder dat blijft een '
        'onbekende auteur onzichtbaar. Een paar eerlijke regels zijn genoeg. Schrijf ze waar u '
        'het boek kocht; voor Amazon staan de directe links hieronder.',
        'Schrijf een recensie:'),
 'en': ('A FEW LINES', 'Finished a book?',
        'Stores show what is being read and talked about, and an unknown author depends on that '
        'more than on anything else. A few honest lines are enough. Leave them wherever you '
        'bought the book; the direct links for Amazon are below.',
        'Write a review:'),
 'de': ('EIN PAAR ZEILEN', 'Ein Buch ausgelesen?',
        'Die Händler zeigen vor allem, was gelesen und besprochen wird, und wer noch keinen Namen '
        'hat, kann sich auf wenig anderes verlassen. Ein paar ehrliche Zeilen reichen. Schreiben '
        'Sie sie dort, wo Sie das Buch gekauft haben; für Amazon stehen die Links unten.',
        'Rezension schreiben:'),
 'es': ('UNAS LÍNEAS', '¿Has terminado un libro?',
        'Las tiendas enseñan sobre todo lo que se lee y se comenta, y quien todavía no tiene '
        'nombre depende de eso más que de nada. Bastan unas líneas sinceras. Déjalas donde '
        'compraste el libro; abajo están los enlaces directos de Amazon.',
        'Escribe una reseña:'),
}


def recensieblok(taal):
    """Sectie met het recensieverzoek plus een directe recensielink per editie."""
    eyebrow, kop, tekst, label = RECENSIE[taal]
    links = []
    for b in BOEKEN:
        if b['n'] in EXTRA:
            continue
        ed = b['ed'][taal]
        adres = (ed.get('links') or {}).get('amazon')
        if not adres:
            continue
        markt = adres.split('/dp/')[0]
        asin = adres.rsplit('/', 1)[-1]
        links.append('<a href="%s/review/create-review?asin=%s" target="_blank" rel="noreferrer">'
                     '%s<svg class="pijl" viewBox="0 0 10 10" aria-hidden="true" focusable="false"><path d="M2.6 7.4 7.4 2.6M3.8 2.6h3.6v3.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg></a>' % (markt, asin, e(ed['titel'])))
    if not links:
        return ''
    return ('<section class="recensie" aria-labelledby="recensie-titel">'
            '<div class="eyebrow">%s</div><h2 id="recensie-titel">%s</h2><p>%s</p>'
            '<p class="recensie-label">%s</p><div class="recensie-links">%s</div></section>'
            % (e(eyebrow), e(kop), e(tekst), e(label), ''.join(links)))


def kaart(taal, boek, voor):
    """Eén dossierkaart. `voor` is '' voor de hoofdmap, '../' voor een taalmap."""
    ui = UI[taal]
    n = boek['n']
    nr = '%02d' % n
    if n in EXTRA:
        x = EXTRA[n]
        titel, pitch, status = x[taal]
        if x['omslag']:
            beeld = ('<img src="%scovers/%s-%d.jpg" alt="%s, C.M.R. Thorne" class="cover" width="625" height="1000" loading="lazy"/>'
                     % (voor, taal, n, e(titel)))
        else:
            beeld = ('<div class="cover-volgt" aria-label="%s"><span>%s</span></div>'
                     % (e(LABEL[x['status']][taal]), OMSLAG_VOLGT[taal]))
        vl = (x.get('links') or {}).get(taal) or {}
        if vl.get('paperback'):
            knop = ('<a class="primary" href="%s" target="_blank" rel="noreferrer">%s<svg class="pijl" viewBox="0 0 10 10" aria-hidden="true" focusable="false"><path d="M2.6 7.4 7.4 2.6M3.8 2.6h3.6v3.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
                    '<div class="format-group" aria-label="%s"><a href="%s" target="_blank" rel="noreferrer">%s</a></div>'
                    % (vl['paperback'], e(ui['bekijkOpAmazon']), e(ui['paperback']),
                       vl['paperback'], e(ui['paperback'])))
            merk = '<span class="availability"><i></i>%s</span>' % e(ui['nuVerkrijgbaar'])
        else:
            knop = ''
            merk = '<span class="availability upcoming"><i></i>%s</span>' % e(LABEL[x['status']][taal])
        meer = SLUGS.get('%d-%s' % (n, taal))
        if meer:
            knop += '<a class="meer" href="%s%s">%s</a>' % (voor, meer, e(MEER[taal]))
        return ('<article class="book"><div class="cover-wrap"><span class="case-number">%s %s</span>%s</div>'
                '<div class="book-copy">%s<h2>%s</h2><p>%s</p>%s<p class="status-regel">%s</p></div></article>'
                % (e(ui['dossier']), nr, beeld, merk, e(titel), e(pitch), knop, e(status)))

    ed = boek['ed'][taal]
    titel, pitch, links = ed['titel'], ed['pitch'], ed['links']
    mock = boek.get('mockup')
    if taal == 'nl' and mock:
        beeld = '<img src="%s%s" alt="%s, C.M.R. Thorne" class="cover mockup"/>' % (voor, mock, e(titel))
    else:
        beeld = ('<img src="%scovers/%s-%d.jpg" alt="%s, C.M.R. Thorne" class="cover" width="625" height="1000" loading="lazy"/>'
                 % (voor, taal, n, e(titel)))

    knoppen = []
    if links.get('amazon'):
        knoppen.append('<a class="primary" href="%s" target="_blank" rel="noreferrer">%s<svg class="pijl" viewBox="0 0 10 10" aria-hidden="true" focusable="false"><path d="M2.6 7.4 7.4 2.6M3.8 2.6h3.6v3.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
                       % (links['amazon'], e(ui['bekijkOpAmazon'])))
        uitvoeringen = ['<a href="%s" target="_blank" rel="noreferrer">%s</a>' % (links['amazon'], e(ui['ebook']))]
        if links.get('paperback'):
            uitvoeringen.append('<a href="%s" target="_blank" rel="noreferrer">%s</a>'
                                % (links['paperback'], e(ui['paperback'])))
        knoppen.append('<div class="format-group" aria-label="%s">%s</div>'
                       % (e(ui['ebook']), ''.join(uitvoeringen)))
    winkels = []
    if links.get('overig'):
        winkels.append('<a href="%s" target="_blank" rel="noreferrer">%s<svg class="pijl" viewBox="0 0 10 10" aria-hidden="true" focusable="false"><path d="M2.6 7.4 7.4 2.6M3.8 2.6h3.6v3.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
                       % (links['overig'], e(ui['andereWinkels'])))
    if links.get('googleplay'):
        winkels.append('<a href="%s" target="_blank" rel="noreferrer">Google Play<svg class="pijl" viewBox="0 0 10 10" aria-hidden="true" focusable="false"><path d="M2.6 7.4 7.4 2.6M3.8 2.6h3.6v3.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
                       % links['googleplay'])
    if winkels:
        knoppen.append('<div class="store-group" aria-label="%s">%s</div>' % (e(ui['andereWinkels']), ''.join(winkels)))

    meer = SLUGS.get('%d-%s' % (n, taal))
    if meer:
        knoppen.append('<a class="meer" href="%s%s">%s%s</a>' % (voor, meer, e(MEER[taal]), ''))
    return ('<article class="book"><div class="cover-wrap"><span class="case-number">%s %s</span>%s</div>'
            '<div class="book-copy"><span class="availability"><i></i>%s</span><h2>%s</h2><p>%s</p>%s</div></article>'
            % (e(ui['dossier']), nr, beeld, e(ui['nuVerkrijgbaar']), e(titel), e(pitch), ''.join(knoppen)))

def hreflangs():
    r = ['<link rel="alternate" hreflang="%s" href="%s"/>'
         % (HREF[t], BASIS if t == 'nl' else BASIS + t + '/') for t in TALEN]
    r.append('<link rel="alternate" hreflang="x-default" href="%s"/>' % BASIS)
    return ''.join(r)

def taalnav(actief, voor):
    stuk = []
    for t in TALEN:
        doel = (voor or './') if t == 'nl' else (voor + t + '/')
        if t == 'nl' and not voor:
            doel = './'
        if t == actief:
            stuk.append('<a class="active" aria-current="page" href="%s">%s</a>' % (doel, t.upper()))
        else:
            stuk.append('<a class="" hreflang="%s" href="%s">%s</a>' % (HREF[t], doel, t.upper()))
    return '<nav class="languages" aria-label="Language">%s</nav>' % ''.join(stuk)

def voet(taal, voor):
    """De zakelijke pagina's staan in dezelfde map als de voorpagina van die taal."""
    paden = PAGINAS[taal]
    labels = PAGINA_LABEL[taal]
    links = ''.join('<a href="%s">%s</a>' % (p, e(l)) for p, l in zip(paden, labels))
    return ('<footer><a href="https://www.instagram.com/cmr.thorne/" target="_blank" rel="noreferrer" '
            'class="instagram"><span aria-hidden="true">\u25ce</span> %s</a>'
            '<nav class="voetlinks" aria-label="%s">%s</nav><p>%s</p>'
            '<p class="voet-kvk">%s</p></footer>'
            % (e(UI[taal]['volgOpInstagram']), e(labels[0]), links, e(UI[taal]['voet']),
               e(VOETREGEL[taal])))


def schema(taal):
    delen = []
    for b in BOEKEN:
        t = EXTRA[b['n']][taal][0] if b['n'] in EXTRA else b['ed'][taal]['titel']
        delen.append({"@type": "Book", "name": t, "position": b['n'],
                      "author": {"@type": "Person", "name": "C.M.R. Thorne"},
                      "inLanguage": LOCALE[taal].replace('_', '-')})
    reeks = {"@context": "https://schema.org", "@type": "BookSeries", "name": "Thorne Thrillers",
             "url": BASIS if taal == 'nl' else BASIS + taal + '/',
             "author": {"@type": "Person", "name": "C.M.R. Thorne"},
             "publisher": {"@type": "Organization", "name": "Lowlands Press"},
             "inLanguage": [LOCALE[t].replace('_', '-') for t in TALEN], "hasPart": delen}
    return '<script type="application/ld+json">%s</script>' % json.dumps(reeks, ensure_ascii=False)

# ---------------------------------------------------------------- bouwen
# Vaste bron. Nooit index.html lezen: dat is de uitvoer, en dan stapelt elke draai zich op.
bron = open(os.path.join(HIER, '_sjabloon.html'), encoding='utf-8').read()

def bouw(taal):
    voor = '' if taal == 'nl' else '../'
    h = bron
    ui = UI[taal]

    # kaarten
    a = h.find('<section class="shelf"')
    b = h.find('<section class="series-note"')
    assert a != -1 and b > a, 'shelf of reeksblok niet gevonden in het sjabloon'
    kaarten = ''.join(kaart(taal, bk, voor) for bk in BOEKEN)
    h = h[:a] + '<section class="shelf" aria-label="%s">%s</section>' % (e(ui['heroSub']), kaarten) + h[b:]

    # hero
    a = h.find('<section class="intro"'); b = h.find('</section>', a) + 10
    herotitel = KOP[taal][0] if taal != 'nl' else 'Zeven dorpen waar een apparaat meekeek.'
    h = h[:a] + ('<section class="intro" id="top"><div class="eyebrow">%s</div><h1>%s</h1><p>%s</p></section>'
                 % (e(ui['heroEyebrow']), e(herotitel), e(ui['heroSub']))) + h[b:]

    # reeksblok
    a = h.find('<section class="series-note"'); b = h.find('</section>', a) + 10
    reekstitel = KOP[taal][1] if taal != 'nl' else 'Zeven zaken. Eén terugkerende rechercheur.'
    talentekst = KOP[taal][2] if taal != 'nl' else ui['talenTekst']
    h = h[:a] + ('<section class="series-note" id="series" aria-labelledby="series-title">'
                 '<div class="eyebrow">%s</div><h2 id="series-title">%s</h2><dl class="series-facts">'
                 '<div><dt>%s</dt><dd>%s</dd></div><div><dt>%s</dt><dd>%s</dd></div>'
                 '<div><dt>%s</dt><dd>%s</dd></div><div><dt>%s</dt><dd>%s</dd></div></dl></section>'
                 % (e(ui['reeksEyebrow']), e(reekstitel),
                    e(ui['leesvolgordeKop']), e(ui['leesvolgordeTekst']),
                    e(ui['talenKop']), e(talentekst),
                    e(ui['auteurKop']), e(ui['auteurTekst']),
                    e(ui['rodeDraadKop']), e(ui['rodeDraadTekst']))) + h[b:]

    # recensieverzoek, achter het reeksblok
    rb = recensieblok(taal)
    if rb:
        merk = '<footer>'
        j = h.rfind(merk)
        h = h[:j] + rb + h[j:]

    # taalnav en voet
    a = h.find('<nav class="languages"'); b = h.find('</nav>', a) + 6
    h = h[:a] + taalnav(taal, voor) + h[b:]
    a = h.rfind('<footer'); b = h.find('</footer>', a) + 9
    h = h[:a] + voet(taal, voor) + h[b:]

    # merkverwijzing in de kop van de pagina
    h = h.replace('<a class="brand" href="#top"', '<a class="brand" href="%s"' % (voor + 'index.html' if voor else '#top'), 1)

    if taal != 'nl':
        titel, oms = META[taal]
        h = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % e(titel), h)
        h = re.sub(r'<meta name="description" content="[^"]*"/>',
                   '<meta name="description" content="%s"/>' % e(oms), h)
        h = re.sub(r'<meta property="og:description" content="[^"]*"/>',
                   '<meta property="og:description" content="%s"/>' % e(oms), h)
        h = h.replace('<meta property="og:locale" content="nl_NL"/>',
                      '<meta property="og:locale" content="%s"/>' % LOCALE[taal])
        h = h.replace('<meta property="og:url" content="https://lowlandspress.com"/>',
                      '<meta property="og:url" content="%s%s/"/>' % (BASIS, taal))
        h = h.replace('<link rel="canonical" href="https://lowlandspress.com/"/>',
                      '<link rel="canonical" href="%s%s/"/>' % (BASIS, taal))
        h = h.replace('<html lang="nl">', '<html lang="%s">' % taal)
        # paden een niveau omhoog
        for pad in ('css/', 'img/', 'covers/', 'mockups/', 'fonts/'):
            h = h.replace('href="%s' % pad, 'href="../%s' % pad)
            h = h.replace('src="%s' % pad, 'src="../%s' % pad)
            h = h.replace('url(%s' % pad, 'url(../%s' % pad)

    # schema vervangen (de BookSeries, niet het organisatieblok)
    a = h.find('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BookSeries"')
    if a == -1:
        a = h.rfind('<script type="application/ld+json">')
    b = h.find('</script>', a) + 9
    h = h[:a] + schema(taal) + h[b:]

    # hreflang
    h = h.replace('<link rel="canonical"', hreflangs() + '<link rel="canonical"', 1)
    return h

for taal in TALEN:
    doel = os.path.join(HIER, 'index.html') if taal == 'nl' else os.path.join(HIER, taal, 'index.html')
    os.makedirs(os.path.dirname(doel), exist_ok=True)
    open(doel, 'w', encoding='utf-8').write(bouw(taal))
    print('%s -> %s' % (taal, os.path.relpath(doel, HIER)))
