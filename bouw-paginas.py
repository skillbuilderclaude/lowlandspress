#!/usr/bin/env python3
"""Bouwt de zakelijke pagina's (over, contact, privacy, voorwaarden) in vier talen."""
import json, os, html as H

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = 'https://lowlandspress.com/'
LOCALE = {'nl': 'nl_NL', 'en': 'en_US', 'de': 'de_DE', 'es': 'es_ES'}

# per taal: map, bestandsnamen, labels
MAP = {'nl': '', 'en': 'en/', 'de': 'de/', 'es': 'es/'}
NAMEN = {
 'nl': ('over.html', 'contact.html', 'privacy.html', 'voorwaarden.html'),
 'en': ('about.html', 'contact.html', 'privacy.html', 'terms.html'),
 'de': ('ueber.html', 'kontakt.html', 'datenschutz.html', 'nutzungsbedingungen.html'),
 'es': ('sobre.html', 'contacto.html', 'privacidad.html', 'condiciones.html'),
}
LABELS = {
 'nl': ('Over Lowlands Press', 'Contact', 'Privacy', 'Voorwaarden'),
 'en': ('About Lowlands Press', 'Contact', 'Privacy', 'Terms'),
 'de': ('Über Lowlands Press', 'Kontakt', 'Datenschutz', 'Nutzungsbedingungen'),
 'es': ('Sobre Lowlands Press', 'Contacto', 'Privacidad', 'Condiciones'),
}
TERUG = {'nl': 'Boeken', 'en': 'Books', 'de': 'Bücher', 'es': 'Libros'}
VOETREGEL = {
 'nl': 'Lowlands Press · KvK 52231895 · Klundert, Nederland',
 'en': 'Lowlands Press · Chamber of Commerce 52231895 · Klundert, the Netherlands',
 'de': 'Lowlands Press · Handelsregister (KvK) 52231895 · Klundert, Niederlande',
 'es': 'Lowlands Press · Registro Mercantil (KvK) 52231895 · Klundert, Países Bajos',
}
ORG = {"@context": "https://schema.org", "@type": "Organization",
       "@id": BASIS + "#uitgeverij", "name": "Lowlands Press", "url": BASIS,
       "email": "info@lowlandspress.com",
       "address": {"@type": "PostalAddress", "addressLocality": "Klundert", "addressCountry": "NL"},
       "identifier": {"@type": "PropertyValue", "name": "KvK", "value": "52231895"}}

def e(s):
    return H.escape(s, quote=True)

def schrijf(taal, index, titel, oms, eyebrow, kop, body, schema=None):
    voor = '../' if taal != 'nl' else ''
    bestand = NAMEN[taal][index]
    pad = os.path.join(HIER, MAP[taal], bestand)
    os.makedirs(os.path.dirname(pad) or '.', exist_ok=True)
    mast = ('<header class="masthead"><a class="brand" href="index.html" aria-label="Lowlands Press">'
            '<img src="%simg/lowlands-press.png" alt="Lowlands Press"/><span><strong>LOWLANDS</strong>'
            '<small>PRESS</small></span></a><nav class="languages" aria-label="%s">'
            '<a class="terug" href="index.html">%s</a></nav></header>'
            % (voor, e(TERUG[taal]), e(TERUG[taal])))
    links = ''.join('<a href="%s">%s</a>' % (NAMEN[taal][i], e(LABELS[taal][i])) for i in range(4))
    voet = ('<footer><nav class="voetlinks" aria-label="%s">%s</nav>'
            '<p>© 2026 Lowlands Press</p><p class="voet-kvk">%s</p></footer>'
            % (e(LABELS[taal][0]), links, e(VOETREGEL[taal])))
    ld = ('<script type="application/ld+json">%s</script>' % json.dumps(schema, ensure_ascii=False)) if schema else ''
    url = BASIS + MAP[taal] + bestand
    alt = ''.join('<link rel="alternate" hreflang="%s" href="%s%s%s"/>'
                  % (t, BASIS, MAP[t], NAMEN[t][index]) for t in ('nl', 'en', 'de', 'es'))
    alt += '<link rel="alternate" hreflang="x-default" href="%s%s"/>' % (BASIS, NAMEN['nl'][index])
    doc = f'''<!DOCTYPE html><html lang="{taal}"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="stylesheet" href="{voor}css/site.css"/><link rel="stylesheet" href="{voor}css/aanpassingen.css?v=9"/>
<title>{e(titel)}</title>
<meta name="description" content="{e(oms)}"/>
<meta name="robots" content="index, follow"/>
<meta property="og:title" content="{e(titel)}"/>
<meta property="og:description" content="{e(oms)}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:site_name" content="Lowlands Press"/>
<meta property="og:type" content="website"/><meta property="og:locale" content="{LOCALE[taal]}"/>
<meta property="og:image" content="https://lowlandspress.com/img/deelkaart.png"/>
<meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="Lowlands Press"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:image" content="https://lowlandspress.com/img/deelkaart.png"/>
{alt}<link rel="canonical" href="{url}"/>{ld}</head>
<body><main>{mast}
<section class="intro" id="top"><div class="eyebrow">{eyebrow}</div><h1>{kop}</h1></section>
<section class="tekstpagina">{body}</section>
{voet}</main></body></html>'''
    open(pad, 'w', encoding='utf-8').write(doc)
    return pad

T = {}

T['nl'] = {
 'over': ('Over Lowlands Press',
  'Lowlands Press is een onafhankelijke uitgeverij in het zuidwesten van Nederland, met boeken in het Nederlands, Engels, Duits en Spaans.',
  'DE UITGEVERIJ', 'Het gewone leven, net iets <em>te</em> dichtbij bekeken.', '''
<p class="lead">Lowlands Press is een kleine, onafhankelijke uitgeverij in het zuidwesten van
Nederland. De boeken verschijnen in het Nederlands, Engels, Duits en Spaans. Roman of
non-fictie, ze beginnen allemaal op dezelfde plek: een huis, een dorp, een gewone dinsdag, en
iemand die daar net iets langer naar blijft kijken dan de bedoeling was.</p>
<h2>Wat wij uitgeven</h2>
<p>De uitgeverij is opgezet om meerdere auteurs in meerdere genres te kunnen voeren. De eerste
reeks op de lijst zijn de Thorne-thrillers van C.M.R. Thorne: op zichzelf staande zaken rond
rechercheur Saskia Bruins, waarin telkens een apparaat heeft meegekeken. Daarnaast verschijnt
er non-fictie onder eigen naam.</p>
<h2>Hoe wij werken</h2>
<p>Elke titel verschijnt in vier talen, en elke taaleditie wordt afzonderlijk geredigeerd
voordat hij uitkomt. Het uitgangspunt is dat een Duitse of Spaanse lezer een boek in handen
krijgt dat in zijn eigen taal geschreven lijkt, niet een vertaling die zich als origineel
voordoet. Een editie gaat pas in de verkoop als die controle is afgerond.</p>
<h2>Waar de boeken te koop zijn</h2>
<p>Lowlands Press verkoopt niet rechtstreeks. De boeken zijn verkrijgbaar als e-book en in druk
via Amazon, Google Play Boeken, Kobo, bol.com, Apple Books en de overige winkels die via
Draft2Digital worden beleverd. Welke uitvoering beschikbaar is, verschilt per taal en per land.
Op de <a href="index.html">boekenpagina</a> staat per deel waar die editie te vinden is.</p>
<h2>De uitgeverij</h2>
<p>Lowlands Press is ingeschreven bij de Kamer van Koophandel onder nummer 52231895 en is
gevestigd in Klundert. De volledige gegevens staan op de <a href="contact.html">contactpagina</a>.</p>
'''),
 'contact': ('Contact en colofon | Lowlands Press',
  'Contactgegevens van Lowlands Press: e-mail, KvK-nummer 52231895 en vestigingsplaats Klundert.',
  'CONTACT', 'Een bericht aan de uitgeverij.', '''
<p class="lead">Vragen over een boek, een vertaling, een recensie-exemplaar of een
samenwerking kunnen per e-mail. Lowlands Press is een kleine uitgeverij, dus een antwoord kan
een paar dagen duren.</p>
<h2>E-mail</h2>
<p><a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a></p>
<h2>Recensenten en boekbloggers</h2>
<p>Recensie-exemplaren zijn als e-book beschikbaar in het Nederlands, Engels, Duits en Spaans.
Vermeld in je bericht om welk deel en welke taal het gaat en waar de recensie verschijnt.</p>
<h2>Rechten en vertalingen</h2>
<p>De vertaalrechten en audiorechten worden door de uitgeverij zelf beheerd. Voorstellen kunnen
naar hetzelfde adres.</p>
<h2>Colofon</h2>
<dl class="gegevens">
<div><dt>Handelsnaam</dt><dd>Lowlands Press</dd></div>
<div><dt>KvK-nummer</dt><dd>52231895</dd></div>
<div><dt>Vestigingsplaats</dt><dd>Klundert, Nederland</dd></div>
<div><dt>E-mail</dt><dd><a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a></dd></div>
<div><dt>Btw</dt><dd>Boeken worden verkocht door de winkels, niet door de uitgeverij. De
winkel waar u koopt, verzorgt de factuur en de btw.</dd></div>
</dl>
<p class="klein">Omdat deze website zelf niets verkoopt en alleen doorverwijst naar winkels,
staat hier een vestigingsplaats en geen bezoekadres.</p>
'''),
 'privacy': ('Privacyverklaring | Lowlands Press',
  'Deze site verzamelt geen persoonsgegevens, gebruikt geen cookies en laadt geen trackers van derden.',
  'PRIVACY', 'Wat deze site van u bewaart.', '''
<p class="lead">Deze website gebruikt geen cookies, slaat niets op in uw browser en laat geen
enkele advertentie- of volgdienst toe. Wel tellen wij hoe vaak een pagina wordt bekeken, op een
server die wij zelf beheren. Hieronder staat precies wat daarbij wordt bewaard.</p>

<h2>De bezoekersteller</h2>
<p>Bij het openen van een pagina gaat er één verzoek naar onze eigen teller. Daarbij leggen wij
vast: welke pagina, in welke taal, op welk tijdstip, en van welke site u kwam (de verwijzer),
plus een eventueel merkteken in de link waarmee wij zien of u via bijvoorbeeld Instagram
binnenkwam.</p>
<p><strong>Uw IP-adres wordt niet opgeslagen.</strong> Om te kunnen tellen hoeveel verschillende
mensen langskwamen in plaats van alleen hoeveel klikken er waren, berekenen wij uit uw IP-adres
en uw browser een onleesbare code, met een geheim getal dat elke dag wisselt. Daardoor is die
code niet terug te rekenen naar u, en herkent hij u morgen niet meer. Er wordt niets gedeeld met
derden, er is geen profiel en er is geen advertentienetwerk bij betrokken.</p>
<p>De teller draait op een eigen server in Nederland, in beheer van de uitgeverij. Er komt geen
analysedienst of advertentienetwerk aan te pas. Wilt u niet geteld worden, dan volstaat een
blokkeerder of JavaScript uitzetten; de site werkt gewoon door.</p>
<h2>Wat er wel wordt vastgelegd</h2>
<p>De site wordt gehost op GitHub Pages. Zoals elke webserver legt die host technische gegevens
vast van elk bezoek, waaronder uw IP-adres, het tijdstip, de opgevraagde pagina en uw browser.
Die gegevens worden door de host gebruikt om de site uit te leveren en misbruik tegen te gaan.
Lowlands Press heeft er geen toegang toe en gebruikt ze niet.</p>
<h2>Lettertypen en afbeeldingen</h2>
<p>De lettertypen en afbeeldingen worden vanaf deze site zelf geladen, niet vanaf Google Fonts
of een ander extern netwerk. Buiten de teller hierboven gaat er bij het openen van een pagina
dus geen enkel verzoek naar een andere partij.</p>
<h2>Links naar winkels</h2>
<p>De knoppen bij elk boek verwijzen naar Amazon, Google Play Boeken, Kobo, bol.com en andere
winkels. Zodra u op zo'n knop klikt, verlaat u deze site en gelden de privacyvoorwaarden van
die winkel. Lowlands Press ontvangt van die winkels geen gegevens over u, en er worden geen
affiliate- of volgparameters aan de links toegevoegd.</p>
<h2>E-mail</h2>
<p>Stuurt u ons een bericht, dan bewaren wij dat bericht en uw e-mailadres zolang dat nodig is
om uw vraag af te handelen, en daarna voor de administratie zolang de wet dat vereist. Wij
gebruiken uw adres niet voor een nieuwsbrief en geven het niet door.</p>
<h2>Uw rechten</h2>
<p>U kunt vragen welke gegevens wij van u hebben, ze laten corrigeren of laten verwijderen.
Een verzoek kan naar <a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a>.
Komt u er met ons niet uit, dan kunt u een klacht indienen bij de Autoriteit
Persoonsgegevens.</p>
<h2>Verwerkingsverantwoordelijke</h2>
<p>Lowlands Press, KvK 52231895, Klundert, Nederland.</p>
<p class="klein">Versie 1 november 2026.</p>
'''),
 'voorwaarden': ('Voorwaarden | Lowlands Press',
  'Gebruiksvoorwaarden van lowlandspress.com, auteursrecht, voorbehoud tekst- en datamining en aansprakelijkheid.',
  'VOORWAARDEN', 'Spelregels voor deze site.', '''
<p class="lead">Deze voorwaarden gelden voor het gebruik van lowlandspress.com. De site is een
etalage: er wordt hier niets verkocht en niets geleverd. Koopt u een boek, dan sluit u die
overeenkomst met de winkel waar u koopt, en gelden de voorwaarden van die winkel.</p>
<h2>1. Over de uitgeverij</h2>
<p>Lowlands Press, ingeschreven bij de Kamer van Koophandel onder nummer 52231895, gevestigd te
Klundert, bereikbaar via info@lowlandspress.com.</p>
<h2>2. Auteursrecht</h2>
<p>De teksten, titels, omslagen en afbeeldingen op deze site zijn auteursrechtelijk beschermd.
Overnemen voor een recensie, een nieuwsbericht of een boekbespreking mag, met bronvermelding en
in de omvang die daarvoor nodig is. Overnemen voor andere doeleinden mag alleen met
voorafgaande schriftelijke toestemming.</p>
<h2>3. Tekst- en datamining</h2>
<p>Voor het gebruik van de boeken van Lowlands Press, in welke vorm dan ook, voor het trainen
van taalmodellen of andere systemen voor kunstmatige intelligentie wordt voorbehoud gemaakt in
de zin van artikel 15o van de Auteurswet en artikel 4 lid 3 van richtlijn (EU) 2019/790. De
inhoud van deze website mag wel worden gelezen en geciteerd door zoekmachines en assistenten
die lezers naar de boeken verwijzen.</p>
<h2>4. Juistheid van de gegevens</h2>
<p>Prijzen, verschijningsdata en beschikbaarheid worden bepaald door de winkels en kunnen per
land en per taal verschillen. Wij doen ons best de verwijzingen op deze site kloppend te
houden, maar aan de informatie hier kunnen geen rechten worden ontleend. Wat op de pagina van
de winkel staat, is leidend.</p>
<h2>5. Links naar derden</h2>
<p>Deze site verwijst naar externe winkels. Lowlands Press heeft geen zeggenschap over die
sites en is niet verantwoordelijk voor hun inhoud, hun voorwaarden of hun beschikbaarheid.</p>
<h2>6. Aansprakelijkheid</h2>
<p>Lowlands Press is niet aansprakelijk voor schade die voortvloeit uit het gebruik van deze
website of uit het tijdelijk niet beschikbaar zijn ervan, behalve bij opzet of bewuste
roekeloosheid.</p>
<h2>7. Klachten over een boek</h2>
<p>Een beschadigd exemplaar, een verkeerde levering of een terugbetaling regelt u met de winkel
waar u het boek hebt gekocht. Gaat het om de inhoud, bijvoorbeeld een fout in de tekst of een
ontbrekend hoofdstuk, dan horen wij dat graag rechtstreeks.</p>
<h2>8. Toepasselijk recht</h2>
<p>Op deze voorwaarden is Nederlands recht van toepassing.</p>
<h2>9. Wijzigingen</h2>
<p>Deze voorwaarden kunnen worden aangepast. De versie die op het moment van uw bezoek op deze
pagina staat, is de geldende.</p>
<p class="klein">Versie 1 november 2026.</p>
'''),
}

T['en'] = {
 'over': ('About Lowlands Press',
  'An independent publisher in the south-west of the Netherlands, with books in Dutch, English, German and Spanish.',
  'THE PUBLISHER', 'Ordinary life, looked at a little <em>too</em> closely.', '''
<p class="lead">Lowlands Press is a small, independent publishing house in the south-west of the
Netherlands. Its books come out in Dutch, English, German and Spanish. Novel or non-fiction,
they all start in the same place: a house, a village, an ordinary Tuesday, and someone who goes
on looking a little longer than anyone intended.</p>
<h2>What we publish</h2>
<p>The house was set up to carry several authors across several genres. First on the list are
the Thorne thrillers by C.M.R. Thorne: standalone cases around detective Saskia Bruins, in each
of which a device was watching. Non-fiction appears alongside them.</p>
<h2>How we work</h2>
<p>Every title appears in four languages, and each language edition is edited separately before
it goes on sale. The standard is that a German or Spanish reader should be holding a book that
reads as though it was written in that language, not a translation passing itself off as one.
An edition goes on sale only once that check is finished.</p>
<h2>Where to buy the books</h2>
<p>Lowlands Press does not sell directly. The books are available as ebooks and in print through
Amazon, Google Play Books, Kobo, bol.com, Apple Books and the other stores supplied through
Draft2Digital. Which format is available differs per language and per country. The
<a href="index.html">books page</a> lists, for each title, where that edition can be found.</p>
<h2>The company</h2>
<p>Lowlands Press is registered with the Dutch Chamber of Commerce under number 52231895 and is
based in Klundert. Full details are on the <a href="contact.html">contact page</a>.</p>
'''),
 'contact': ('Contact | Lowlands Press',
  'Contact details for Lowlands Press: email, Chamber of Commerce number 52231895 and place of business Klundert.',
  'CONTACT', 'A message to the publisher.', '''
<p class="lead">Questions about a book, a translation, a review copy or a collaboration are
welcome by email. Lowlands Press is a small house, so a reply can take a few days.</p>
<h2>Email</h2>
<p><a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a></p>
<h2>Reviewers and book bloggers</h2>
<p>Review copies are available as ebooks in Dutch, English, German and Spanish. Please say which
book and which language you need, and where the review will appear.</p>
<h2>Rights and translations</h2>
<p>Translation and audio rights are handled by the publisher directly. Proposals can go to the
same address.</p>
<h2>Company details</h2>
<dl class="gegevens">
<div><dt>Trading name</dt><dd>Lowlands Press</dd></div>
<div><dt>Chamber of Commerce</dt><dd>52231895 (KvK, the Netherlands)</dd></div>
<div><dt>Place of business</dt><dd>Klundert, the Netherlands</dd></div>
<div><dt>Email</dt><dd><a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a></dd></div>
<div><dt>VAT</dt><dd>Books are sold by the stores, not by the publisher. The store you buy from
issues the invoice and handles the VAT.</dd></div>
</dl>
<p class="klein">Because this website sells nothing itself and only links on to stores, it lists
a place of business rather than a street address.</p>
'''),
 'privacy': ('Privacy | Lowlands Press',
  'This site collects no personal data, uses no cookies and loads no third-party trackers.',
  'PRIVACY', 'What this site keeps about you.', '''
<p class="lead">This website uses no cookies, stores nothing in your browser and allows no
advertising or tracking service of any kind. We do count how often a page is read, on a server
we run ourselves. What that records is set out below.</p>

<h2>The visitor counter</h2>
<p>Opening a page sends one request to our own counter. It records which page, in which
language, at what time, and which site you came from (the referrer), plus any tag in the link
that tells us whether you arrived from, say, Instagram.</p>
<p><strong>Your IP address is not stored.</strong> To count how many different people came
rather than merely how many clicks there were, we derive an unreadable code from your IP address
and your browser, using a secret number that changes every day. That code cannot be turned back
into you, and tomorrow it no longer recognises you. Nothing is shared with anyone, there is no
profile, and no advertising network is involved.</p>
<p>The counter runs on our own server in the Netherlands, operated by the publisher. No
analytics service and no advertising network is involved. If you would rather not be counted, a
blocker or turning off JavaScript stops it; the site works as normal either way.</p>
<h2>What is recorded</h2>
<p>The site is hosted on GitHub Pages. Like any web server, that host records technical details
of each visit, including your IP address, the time, the page requested and your browser. The
host uses those records to deliver the site and to prevent abuse. Lowlands Press has no access
to them and does not use them.</p>
<h2>Fonts and images</h2>
<p>Fonts and images are served from this site itself, not from Google Fonts or any other
external network. Apart from the counter above, opening a page therefore sends no request to
anyone else.</p>
<h2>Links to stores</h2>
<p>The buttons on each book lead to Amazon, Google Play Books, Kobo, bol.com and other stores.
The moment you click one, you leave this site and that store's privacy terms apply. Lowlands
Press receives no data about you from those stores, and no affiliate or tracking parameters are
added to the links.</p>
<h2>Email</h2>
<p>If you write to us, we keep your message and your email address for as long as it takes to
deal with your question, and after that for our records for as long as the law requires. We do
not use your address for a newsletter and we do not pass it on.</p>
<h2>Your rights</h2>
<p>You may ask what data we hold about you, have it corrected, or have it deleted. Write to
<a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a>. If we cannot resolve
it between us, you may complain to the Dutch Data Protection Authority (Autoriteit
Persoonsgegevens).</p>
<h2>Controller</h2>
<p>Lowlands Press, Chamber of Commerce 52231895, Klundert, the Netherlands.</p>
<p class="klein">Version 1 November 2026.</p>
'''),
 'voorwaarden': ('Terms | Lowlands Press',
  'Terms of use for lowlandspress.com: copyright, text and data mining reservation and liability.',
  'TERMS', 'Ground rules for this site.', '''
<p class="lead">These terms govern the use of lowlandspress.com. The site is a shop window:
nothing is sold or delivered here. When you buy a book, that contract is with the store you buy
from, under that store's terms.</p>
<h2>1. The publisher</h2>
<p>Lowlands Press, registered with the Dutch Chamber of Commerce under number 52231895, based in
Klundert, reachable at info@lowlandspress.com.</p>
<h2>2. Copyright</h2>
<p>The texts, titles, covers and images on this site are protected by copyright. Quoting them
for a review, a news item or a book discussion is fine, with attribution and in the extent that
purpose requires. Any other use needs written permission in advance.</p>
<h2>3. Text and data mining</h2>
<p>Use of the books published by Lowlands Press, in any form, for training language models or
other artificial intelligence systems is expressly reserved under Article 15o of the Dutch
Copyright Act and Article 4(3) of EU Directive 2019/790. The content of this website may be read
and quoted by search engines and assistants that direct readers to the books.</p>
<h2>4. Accuracy</h2>
<p>Prices, publication dates and availability are set by the stores and differ per country and
per language. We do our best to keep the references here correct, but no rights can be derived
from the information on this site. What the store's own page says prevails.</p>
<h2>5. Third-party links</h2>
<p>This site links to external stores. Lowlands Press has no control over those sites and is not
responsible for their content, their terms or their availability.</p>
<h2>6. Liability</h2>
<p>Lowlands Press is not liable for damage arising from the use of this website or from its
temporary unavailability, except in cases of intent or conscious recklessness.</p>
<h2>7. Complaints about a book</h2>
<p>A damaged copy, a wrong delivery or a refund is a matter for the store you bought it from. If
it concerns the content, for instance an error in the text or a missing chapter, we would like
to hear about it directly.</p>
<h2>8. Governing law</h2>
<p>Dutch law applies to these terms.</p>
<h2>9. Changes</h2>
<p>These terms may be amended. The version shown on this page at the time of your visit is the
one that applies.</p>
<p class="klein">Version 1 November 2026.</p>
'''),
}

T['de'] = {
 'over': ('Über Lowlands Press',
  'Ein unabhängiger Verlag im Südwesten der Niederlande, mit Büchern auf Niederländisch, Englisch, Deutsch und Spanisch.',
  'DER VERLAG', 'Das gewöhnliche Leben, eine Spur <em>zu</em> genau betrachtet.', '''
<p class="lead">Lowlands Press ist ein kleiner, unabhängiger Verlag im Südwesten der
Niederlande. Die Bücher erscheinen auf Niederländisch, Englisch, Deutsch und Spanisch. Ob Roman
oder Sachbuch, sie fangen alle an derselben Stelle an: ein Haus, ein Dorf, ein ganz gewöhnlicher
Dienstag, und jemand, der ein wenig länger hinsieht, als vorgesehen war.</p>
<h2>Was wir verlegen</h2>
<p>Der Verlag ist so angelegt, dass er mehrere Autoren in mehreren Genres führen kann. Als
Erstes stehen die Thorne-Thriller von C.M.R. Thorne auf dem Programm: in sich abgeschlossene
Fälle um die Ermittlerin Saskia Bruins, bei denen jedes Mal ein Gerät mitgesehen hat. Daneben
erscheint Sachbuchliteratur.</p>
<h2>Wie wir arbeiten</h2>
<p>Jeder Titel erscheint in vier Sprachen, und jede Sprachausgabe wird einzeln lektoriert, bevor
sie in den Handel geht. Der Maßstab: Wer die deutsche Ausgabe liest, soll ein Buch in der Hand
halten, das auf Deutsch geschrieben wirkt, und keine Übersetzung, die sich als Original ausgibt.
Eine Ausgabe geht erst in den Verkauf, wenn diese Prüfung abgeschlossen ist.</p>
<h2>Wo es die Bücher gibt</h2>
<p>Lowlands Press verkauft nicht selbst. Die Bücher gibt es als E-Book und gedruckt bei Amazon,
Google Play Bücher, Kobo, Thalia, Apple Books und den weiteren Shops, die über Draft2Digital
beliefert werden. Welche Ausgabe lieferbar ist, hängt von Sprache und Land ab. Auf der
<a href="index.html">Bücherseite</a> steht bei jedem Band, wo die jeweilige Ausgabe zu finden
ist.</p>
<h2>Der Verlag</h2>
<p>Lowlands Press ist bei der niederländischen Handelskammer unter der Nummer 52231895
eingetragen und hat seinen Sitz in Klundert. Die vollständigen Angaben stehen auf der
<a href="kontakt.html">Kontaktseite</a>.</p>
'''),
 'contact': ('Kontakt und Impressum | Lowlands Press',
  'Kontaktdaten von Lowlands Press: E-Mail, Handelsregisternummer 52231895 und Sitz Klundert.',
  'KONTAKT', 'Eine Nachricht an den Verlag.', '''
<p class="lead">Fragen zu einem Buch, einer Übersetzung, einem Rezensionsexemplar oder einer
Zusammenarbeit gehen am besten per E-Mail ein. Lowlands Press ist ein kleiner Verlag, eine
Antwort kann also ein paar Tage dauern.</p>
<h2>E-Mail</h2>
<p><a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a></p>
<h2>Rezensenten und Buchblogger</h2>
<p>Rezensionsexemplare gibt es als E-Book auf Niederländisch, Englisch, Deutsch und Spanisch.
Bitte nennen Sie Band und Sprache und sagen Sie dazu, wo die Rezension erscheint.</p>
<h2>Rechte und Übersetzungen</h2>
<p>Übersetzungs- und Audiorechte liegen beim Verlag selbst. Anfragen gehen an dieselbe Adresse.</p>
<h2>Impressum</h2>
<dl class="gegevens">
<div><dt>Handelsname</dt><dd>Lowlands Press</dd></div>
<div><dt>Handelsregister</dt><dd>52231895 (KvK, Niederlande)</dd></div>
<div><dt>Sitz</dt><dd>Klundert, Niederlande</dd></div>
<div><dt>E-Mail</dt><dd><a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a></dd></div>
<div><dt>Umsatzsteuer</dt><dd>Die Bücher verkaufen die Shops, nicht der Verlag. Rechnung und
Umsatzsteuer übernimmt der Shop, bei dem Sie kaufen.</dd></div>
</dl>
<p class="klein">Da diese Website selbst nichts verkauft und nur auf Shops weiterleitet, steht
hier ein Sitz und keine Hausanschrift.</p>
'''),
 'privacy': ('Datenschutz | Lowlands Press',
  'Diese Website erhebt keine personenbezogenen Daten, setzt keine Cookies und lädt keine Tracker Dritter.',
  'DATENSCHUTZ', 'Was diese Seite über Sie behält.', '''
<p class="lead">Diese Website setzt keine Cookies, speichert nichts in Ihrem Browser und lässt
keinerlei Werbe- oder Trackingdienst zu. Wir zählen allerdings, wie oft eine Seite gelesen wird,
auf einem Server, den wir selbst betreiben. Was dabei festgehalten wird, steht unten.</p>

<h2>Der Besucherzähler</h2>
<p>Beim Öffnen einer Seite geht eine Anfrage an unseren eigenen Zähler. Festgehalten werden:
welche Seite, in welcher Sprache, zu welcher Zeit und von welcher Seite Sie kamen (der
Referrer), dazu eine etwaige Markierung im Link, an der wir sehen, ob Sie etwa über Instagram
gekommen sind.</p>
<p><strong>Ihre IP-Adresse wird nicht gespeichert.</strong> Um zählen zu können, wie viele
verschiedene Menschen da waren und nicht bloß wie viele Klicks, berechnen wir aus Ihrer
IP-Adresse und Ihrem Browser einen unlesbaren Code, mit einer geheimen Zahl, die täglich
wechselt. Dieser Code lässt sich nicht zu Ihnen zurückrechnen und erkennt Sie morgen nicht mehr.
Nichts davon wird weitergegeben, es gibt kein Profil und kein Werbenetzwerk ist beteiligt.</p>
<p>Der Zähler läuft auf einem eigenen Server in den Niederlanden, betrieben vom Verlag. Ein
Analysedienst oder Werbenetzwerk ist nicht beteiligt. Wer nicht gezählt werden möchte: mit einem
Blocker oder abgeschaltetem JavaScript unterbleibt die Zählung, die Seite funktioniert
trotzdem.</p>
<h2>Was festgehalten wird</h2>
<p>Die Seite liegt bei GitHub Pages. Wie jeder Webserver hält dieser Anbieter technische Daten
jedes Aufrufs fest, darunter Ihre IP-Adresse, den Zeitpunkt, die aufgerufene Seite und Ihren
Browser. Der Anbieter nutzt diese Daten, um die Seite auszuliefern und Missbrauch zu verhindern.
Lowlands Press hat darauf keinen Zugriff und verwendet sie nicht.</p>
<h2>Schriften und Bilder</h2>
<p>Schriften und Bilder werden von dieser Seite selbst geladen, nicht von Google Fonts oder
einem anderen externen Netz. Außer dem Zähler oben geht beim Öffnen einer Seite deshalb keine
Anfrage an Dritte.</p>
<h2>Links zu Shops</h2>
<p>Die Schaltflächen bei jedem Buch führen zu Amazon, Google Play Bücher, Kobo, Thalia und
weiteren Shops. Sobald Sie darauf klicken, verlassen Sie diese Seite, und es gelten die
Datenschutzbestimmungen des jeweiligen Shops. Lowlands Press erhält von diesen Shops keine
Daten über Sie, und den Links werden keine Affiliate- oder Tracking-Parameter angehängt.</p>
<h2>E-Mail</h2>
<p>Wenn Sie uns schreiben, bewahren wir Ihre Nachricht und Ihre E-Mail-Adresse so lange auf, wie
es zur Bearbeitung Ihrer Frage nötig ist, und danach für die Buchhaltung so lange, wie das
Gesetz es verlangt. Wir nutzen Ihre Adresse nicht für einen Newsletter und geben sie nicht
weiter.</p>
<h2>Ihre Rechte</h2>
<p>Sie können Auskunft über die zu Ihnen gespeicherten Daten verlangen, sie berichtigen oder
löschen lassen. Schreiben Sie an
<a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a>. Kommen wir nicht zusammen,
können Sie sich bei der niederländischen Datenschutzbehörde (Autoriteit Persoonsgegevens)
beschweren; als Betroffener in Deutschland steht Ihnen auch Ihre örtliche Aufsichtsbehörde
offen.</p>
<h2>Verantwortlicher</h2>
<p>Lowlands Press, Handelsregister (KvK) 52231895, Klundert, Niederlande.</p>
<p class="klein">Stand 1. November 2026.</p>
'''),
 'voorwaarden': ('Nutzungsbedingungen | Lowlands Press',
  'Nutzungsbedingungen für lowlandspress.com: Urheberrecht, Vorbehalt für Text- und Data-Mining und Haftung.',
  'NUTZUNGSBEDINGUNGEN', 'Spielregeln für diese Seite.', '''
<p class="lead">Diese Bedingungen gelten für die Nutzung von lowlandspress.com. Die Seite ist
ein Schaufenster: Hier wird nichts verkauft und nichts geliefert. Kaufen Sie ein Buch, kommt
der Vertrag mit dem Shop zustande, bei dem Sie kaufen, und es gelten dessen Bedingungen.</p>
<h2>1. Der Verlag</h2>
<p>Lowlands Press, eingetragen bei der niederländischen Handelskammer unter der Nummer
52231895, mit Sitz in Klundert, erreichbar unter info@lowlandspress.com.</p>
<h2>2. Urheberrecht</h2>
<p>Die Texte, Titel, Umschläge und Bilder auf dieser Seite sind urheberrechtlich geschützt.
Zitieren für eine Rezension, eine Meldung oder eine Buchbesprechung ist zulässig, mit
Quellenangabe und in dem dafür nötigen Umfang. Jede andere Verwendung bedarf der vorherigen
schriftlichen Zustimmung.</p>
<h2>3. Text- und Data-Mining</h2>
<p>Die Nutzung der Bücher von Lowlands Press, in welcher Form auch immer, zum Training von
Sprachmodellen oder anderen Systemen künstlicher Intelligenz wird hiermit ausdrücklich
vorbehalten, im Sinne von Artikel 15o des niederländischen Urheberrechtsgesetzes und Artikel 4
Absatz 3 der Richtlinie (EU) 2019/790. Der Inhalt dieser Website darf von Suchmaschinen und
Assistenten, die Leser zu den Büchern führen, gelesen und zitiert werden.</p>
<h2>4. Richtigkeit der Angaben</h2>
<p>Preise, Erscheinungstermine und Lieferbarkeit legen die Shops fest; sie unterscheiden sich je
nach Land und Sprache. Wir halten die Verweise hier nach bestem Wissen aktuell, ein Anspruch
lässt sich daraus aber nicht ableiten. Maßgeblich ist, was auf der Seite des Shops steht.</p>
<h2>5. Links zu Dritten</h2>
<p>Diese Seite verweist auf externe Shops. Lowlands Press hat auf diese Seiten keinen Einfluss
und ist für deren Inhalte, Bedingungen und Erreichbarkeit nicht verantwortlich.</p>
<h2>6. Haftung</h2>
<p>Lowlands Press haftet nicht für Schäden aus der Nutzung dieser Website oder aus ihrer
vorübergehenden Nichterreichbarkeit, außer bei Vorsatz oder bewusster Fahrlässigkeit.</p>
<h2>7. Reklamationen zu einem Buch</h2>
<p>Ein beschädigtes Exemplar, eine falsche Lieferung oder eine Rückerstattung regeln Sie mit dem
Shop, bei dem Sie gekauft haben. Geht es um den Inhalt, etwa einen Fehler im Text oder ein
fehlendes Kapitel, hören wir gern direkt davon.</p>
<h2>8. Anwendbares Recht</h2>
<p>Auf diese Bedingungen ist niederländisches Recht anwendbar.</p>
<h2>9. Änderungen</h2>
<p>Diese Bedingungen können angepasst werden. Es gilt die Fassung, die zum Zeitpunkt Ihres
Besuchs auf dieser Seite steht.</p>
<p class="klein">Stand 1. November 2026.</p>
'''),
}

T['es'] = {
 'over': ('Sobre Lowlands Press',
  'Editorial independiente del suroeste de los Países Bajos, con libros en neerlandés, inglés, alemán y español.',
  'LA EDITORIAL', 'La vida corriente, mirada un poco <em>demasiado</em> de cerca.', '''
<p class="lead">Lowlands Press es una editorial pequeña e independiente del suroeste de los
Países Bajos. Sus libros salen en neerlandés, inglés, alemán y español. Novela o ensayo, todos
empiezan en el mismo sitio: una casa, un pueblo, un martes cualquiera y alguien que se queda
mirando un rato más de la cuenta.</p>
<h2>Qué publicamos</h2>
<p>La editorial nació para poder llevar a varios autores y varios géneros. Lo primero del
catálogo son los thrillers de Thorne, de C.M.R. Thorne: casos independientes en torno a la
inspectora Saskia Bruins, en los que siempre hay un aparato que estaba mirando. Junto a ellos
se publica ensayo.</p>
<h2>Cómo trabajamos</h2>
<p>Cada título sale en cuatro idiomas y cada edición se corrige por separado antes de ponerse a
la venta. El criterio es que quien lee la edición española tenga entre manos un libro que
parezca escrito en español, no una traducción que se hace pasar por original. Una edición no
sale a la venta hasta que esa revisión está cerrada.</p>
<h2>Dónde se compran los libros</h2>
<p>Lowlands Press no vende directamente. Los libros están disponibles en digital y en papel a
través de Amazon, Google Play Libros, Kobo, Apple Books y las demás tiendas que se abastecen
mediante Draft2Digital. Qué formato hay disponible cambia según el idioma y el país. En la
<a href="index.html">página de libros</a> figura, para cada título, dónde encontrar esa
edición.</p>
<h2>La empresa</h2>
<p>Lowlands Press está inscrita en la Cámara de Comercio neerlandesa con el número 52231895 y
tiene su sede en Klundert. Los datos completos están en la
<a href="contacto.html">página de contacto</a>.</p>
'''),
 'contact': ('Contacto | Lowlands Press',
  'Datos de contacto de Lowlands Press: correo, número 52231895 de la Cámara de Comercio y sede en Klundert.',
  'CONTACTO', 'Un mensaje a la editorial.', '''
<p class="lead">Las preguntas sobre un libro, una traducción, un ejemplar de reseña o una
colaboración se atienden por correo. Lowlands Press es una editorial pequeña, así que la
respuesta puede tardar unos días.</p>
<h2>Correo</h2>
<p><a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a></p>
<h2>Reseñistas y blogueros</h2>
<p>Hay ejemplares de reseña en digital en neerlandés, inglés, alemán y español. Indica de qué
título y qué idioma se trata y dónde se publicará la reseña.</p>
<h2>Derechos y traducciones</h2>
<p>Los derechos de traducción y de audio los gestiona la propia editorial. Las propuestas van a
la misma dirección.</p>
<h2>Datos de la empresa</h2>
<dl class="gegevens">
<div><dt>Nombre comercial</dt><dd>Lowlands Press</dd></div>
<div><dt>Registro Mercantil</dt><dd>52231895 (KvK, Países Bajos)</dd></div>
<div><dt>Sede</dt><dd>Klundert, Países Bajos</dd></div>
<div><dt>Correo</dt><dd><a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a></dd></div>
<div><dt>IVA</dt><dd>Los libros los venden las tiendas, no la editorial. La factura y el IVA
corren a cargo de la tienda donde compras.</dd></div>
</dl>
<p class="klein">Como esta web no vende nada por sí misma y solo remite a tiendas, aquí figura
una sede y no una dirección de visita.</p>
'''),
 'privacy': ('Privacidad | Lowlands Press',
  'Esta web no recoge datos personales, no usa cookies y no carga rastreadores de terceros.',
  'PRIVACIDAD', 'Qué guarda esta web sobre ti.', '''
<p class="lead">Esta web no usa cookies, no guarda nada en tu navegador y no admite ningún
servicio de publicidad ni de rastreo. Sí contamos cuántas veces se lee una página, en un
servidor que gestionamos nosotros. Abajo está exactamente lo que se registra.</p>

<h2>El contador de visitas</h2>
<p>Al abrir una página se envía una petición a nuestro propio contador. Se registra qué página,
en qué idioma, a qué hora y desde qué sitio llegaste (el referente), más cualquier marca en el
enlace que nos indique si vienes, por ejemplo, de Instagram.</p>
<p><strong>Tu dirección IP no se guarda.</strong> Para poder contar cuántas personas distintas
pasaron y no solo cuántos clics hubo, calculamos a partir de tu IP y tu navegador un código
ilegible, con un número secreto que cambia cada día. Ese código no puede deshacerse hasta
llegar a ti, y mañana ya no te reconoce. No se comparte con nadie, no hay perfil y no
interviene ninguna red publicitaria.</p>
<p>El contador funciona en un servidor propio en los Países Bajos, gestionado por la
editorial. No interviene ningún servicio de analítica ni red publicitaria. Si prefieres no ser
contado, basta con un bloqueador o desactivar JavaScript; la web sigue funcionando igual.</p>
<h2>Qué sí queda registrado</h2>
<p>La web está alojada en GitHub Pages. Como cualquier servidor, ese proveedor registra datos
técnicos de cada visita: tu dirección IP, la hora, la página solicitada y tu navegador. Los usa
para servir la web y para evitar abusos. Lowlands Press no tiene acceso a ellos ni los
utiliza.</p>
<h2>Tipografías e imágenes</h2>
<p>Las tipografías y las imágenes se cargan desde esta misma web, no desde Google Fonts ni
ninguna otra red externa. Salvo el contador de arriba, abrir una página no envía ninguna
petición a nadie más.</p>
<h2>Enlaces a tiendas</h2>
<p>Los botones de cada libro llevan a Amazon, Google Play Libros, Kobo, Apple Books y otras
tiendas. En cuanto pulsas uno, sales de esta web y se aplican las condiciones de privacidad de
esa tienda. Lowlands Press no recibe datos tuyos de esas tiendas, y a los enlaces no se les
añade ningún parámetro de afiliación o de seguimiento.</p>
<h2>Correo</h2>
<p>Si nos escribes, conservamos tu mensaje y tu dirección el tiempo necesario para atender tu
consulta y, después, para la contabilidad durante el plazo que marque la ley. No usamos tu
dirección para ningún boletín y no la cedemos.</p>
<h2>Tus derechos</h2>
<p>Puedes pedir qué datos tenemos sobre ti, corregirlos o suprimirlos. Escribe a
<a href="mailto:info@lowlandspress.com">info@lowlandspress.com</a>. Si no llegamos a un
acuerdo, puedes reclamar ante la autoridad neerlandesa de protección de datos (Autoriteit
Persoonsgegevens) o ante la autoridad de tu país.</p>
<h2>Responsable del tratamiento</h2>
<p>Lowlands Press, Registro Mercantil (KvK) 52231895, Klundert, Países Bajos.</p>
<p class="klein">Versión del 1 de noviembre de 2026.</p>
'''),
 'voorwaarden': ('Condiciones | Lowlands Press',
  'Condiciones de uso de lowlandspress.com: derechos de autor, reserva de minería de textos y datos y responsabilidad.',
  'CONDICIONES', 'Reglas de esta web.', '''
<p class="lead">Estas condiciones rigen el uso de lowlandspress.com. La web es un escaparate:
aquí no se vende ni se entrega nada. Cuando compras un libro, el contrato es con la tienda
donde compras y se aplican sus condiciones.</p>
<h2>1. La editorial</h2>
<p>Lowlands Press, inscrita en la Cámara de Comercio neerlandesa con el número 52231895, con
sede en Klundert, disponible en info@lowlandspress.com.</p>
<h2>2. Derechos de autor</h2>
<p>Los textos, títulos, cubiertas e imágenes de esta web están protegidos por derechos de
autor. Citarlos para una reseña, una noticia o un comentario de libros es legítimo, con mención
de la fuente y en la medida necesaria. Cualquier otro uso requiere autorización previa por
escrito.</p>
<h2>3. Minería de textos y datos</h2>
<p>Queda expresamente reservado el uso de los libros de Lowlands Press, en cualquier forma,
para entrenar modelos de lenguaje u otros sistemas de inteligencia artificial, conforme al
artículo 15o de la Ley de Derechos de Autor neerlandesa y al artículo 4.3 de la Directiva (UE)
2019/790. El contenido de esta web sí puede ser leído y citado por buscadores y asistentes que
dirijan lectores a los libros.</p>
<h2>4. Exactitud de los datos</h2>
<p>Los precios, las fechas de publicación y la disponibilidad los fijan las tiendas y varían
según el país y el idioma. Procuramos mantener correctas las referencias de esta web, pero de
la información aquí recogida no se derivan derechos. Prevalece lo que figure en la página de la
tienda.</p>
<h2>5. Enlaces a terceros</h2>
<p>Esta web enlaza a tiendas externas. Lowlands Press no controla esos sitios y no responde de
su contenido, sus condiciones ni su disponibilidad.</p>
<h2>6. Responsabilidad</h2>
<p>Lowlands Press no responde de los daños derivados del uso de esta web ni de su indisponibilidad
temporal, salvo en caso de dolo o imprudencia consciente.</p>
<h2>7. Reclamaciones sobre un libro</h2>
<p>Un ejemplar dañado, una entrega equivocada o una devolución se resuelven con la tienda donde
compraste. Si se trata del contenido, por ejemplo una errata o un capítulo que falta, preferimos
saberlo directamente.</p>
<h2>8. Legislación aplicable</h2>
<p>A estas condiciones se les aplica el derecho neerlandés.</p>
<h2>9. Modificaciones</h2>
<p>Estas condiciones pueden modificarse. Rige la versión que figure en esta página en el
momento de tu visita.</p>
<p class="klein">Versión del 1 de noviembre de 2026.</p>
'''),
}

SLEUTELS = ('over', 'contact', 'privacy', 'voorwaarden')
if __name__ == '__main__':
    for taal in ('nl', 'en', 'de', 'es'):
        for i, s in enumerate(SLEUTELS):
            titel, oms, eyebrow, kop, body = T[taal][s]
            schema = ORG if s == 'over' else (
                {"@context": "https://schema.org", "@type": "ContactPage", "name": titel,
                 "url": BASIS + MAP[taal] + NAMEN[taal][i], "about": ORG} if s == 'contact' else None)
            p = schrijf(taal, i, titel, oms, eyebrow, kop, body, schema)
            print(os.path.relpath(p, HIER))
