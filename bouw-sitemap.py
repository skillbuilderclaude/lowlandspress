#!/usr/bin/env python3
"""Sitemap met taalalternatieven voor alle pagina's van lowlandspress.com."""
import json, os, datetime

HIER = os.path.dirname(os.path.abspath(__file__))
B = 'https://lowlandspress.com/'
TALEN = ['nl', 'en', 'de', 'es']
MAP = {'nl': '', 'en': 'en/', 'de': 'de/', 'es': 'es/'}
PAGINAS = {
 'nl': ('over.html', 'contact.html', 'privacy.html', 'voorwaarden.html'),
 'en': ('about.html', 'contact.html', 'privacy.html', 'terms.html'),
 'de': ('ueber.html', 'kontakt.html', 'datenschutz.html', 'nutzungsbedingungen.html'),
 'es': ('sobre.html', 'contacto.html', 'privacidad.html', 'condiciones.html'),
}
vandaag = datetime.date.today().isoformat()
slugs = json.load(open(os.path.join(HIER, '_slugs.json'), encoding='utf-8'))

r = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
     'xmlns:xhtml="http://www.w3.org/1999/xhtml">']


def groep(urls, prio, freq):
    alt = ''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (t, u)
                  for t, u in urls.items())
    alt += '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % urls['nl']
    for t, u in urls.items():
        p = prio if t == 'nl' else '%.1f' % (float(prio) - 0.1)
        r.append('  <url><loc>%s</loc>%s<lastmod>%s</lastmod><changefreq>%s</changefreq>'
                 '<priority>%s</priority></url>' % (u, alt, vandaag, freq, p))


groep({t: B + MAP[t] for t in TALEN}, '1.0', 'monthly')

boeken = sorted({int(k.split('-')[0]) for k in slugs})
for n in boeken:
    urls = {t: B + slugs['%d-%s' % (n, t)] for t in TALEN if '%d-%s' % (n, t) in slugs}
    if urls:
        groep(urls, '0.8', 'monthly')

for i in range(4):
    groep({t: B + MAP[t] + PAGINAS[t][i] for t in TALEN}, '0.5' if i < 2 else '0.3', 'yearly')

r.append('</urlset>')
open(os.path.join(HIER, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(r) + '\n')
print('%d urls in de sitemap' % (len(r) - 3))
