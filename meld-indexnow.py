#!/usr/bin/env python3
"""Meldt alle adressen uit sitemap.xml bij IndexNow (Bing, Yandex, Seznam, Naver).

Google doet niet mee aan IndexNow. Voor Google is Search Console de weg.
"""
import json, os, re, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HIER, '_indexnow.json'), encoding='utf-8'))
SITE = 'lowlandspress.com'

sitemap = open(os.path.join(HIER, 'sitemap.xml'), encoding='utf-8').read()
urls = sorted(set(re.findall(r'<loc>([^<]+)</loc>', sitemap)))

lading = json.dumps({
    'host': SITE,
    'key': CFG['sleutel'],
    'keyLocation': CFG['bestand'],
    'urlList': urls,
}).encode()

verzoek = urllib.request.Request(
    'https://api.indexnow.org/indexnow', data=lading,
    headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(verzoek, timeout=30) as a:
        print('IndexNow: %s voor %d adressen' % (a.status, len(urls)))
except Exception as e:
    print('IndexNow mislukt:', e)
