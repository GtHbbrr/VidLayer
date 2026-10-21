\# 🚀 VidSlayers - Bookmarklet Architectuur Blauwdruk



Dit document beschrijft de technische architectuur en logistiek van de client-side data-ingestie via de VidSlayers JavaScript Bookmarklet. Dit component is fundamenteel voor de \*\*0-euro compute marge\*\* van het platform.



\---



\## 🗺️ De Datatunnel-Architectuur



Wanneer een ontwikkelaar of eindgebruiker de bookmarklet activeert op een YouTube-videopagina, wordt de volgende datastroom in gang gezet:



\[ Gebruiker klikt op Bookmarklet op youtube.com... ]

│

▼ (Lijm-code laadt de zware engine in)

\[ VidSlayers Remote Injector Script ]

│

┌────────────────┴────────────────┐

▼ (Extractie via yt-dlp patronen)  ▼ (Metadata \& Structuur)

\[ Timedtext XML/JSON Fetch ]       \[ Youtubei API (/v1/next) Fetch ]

│                                 │

└────────────────┬────────────────┘

▼

\[ Client-Side Text Cleansing ]

(Wist karaoke-tags, herhalingen \& bouwt commentaar-boom)

│

▼ (Vederlichte JSON POST-request)

\[ Cloudflare Worker Backend API Gateway ]



\---



\## 🏗️ De 3 Componenten van de Ingestie-Motor



\### 1. De Browser-Lijm (De Statische Bookmarklet)

Dit is de minimale JavaScript-code die de gebruiker in de favorietenbalk van de browser sleept. Dit component is bewust statisch en vederlicht. Het doel is enkel het valideren van de URL, het grijpen van de actieve `video\_id`, en het dynamisch inladen van de eigenlijke extractie-engine.



```javascript

javascript:(function(){

&#x20; if(!window.location.hostname.includes('youtube.com')){

&#x20;   alert('VidSlayers: Open eerst een YouTube video!'); return;

&#x20; }

&#x20; const vId = new URLSearchParams(window.location.search).get('v');

&#x20; if(!vId){ alert('VidSlayers: Geen video-ID gevonden.'); return; }

&#x20; 

&#x20; /\* Dynamische bootstrap: laad de meest up-to-date extractie-engine \*/

&#x20; const script = document.createElement('script');

&#x20; script.src = 'https://vidslayers.com' + Date.now();

&#x20; script.id = 'vidslayers-engine';

&#x20; script.setAttribute('data-video-id', vId);

&#x20; document.body.appendChild(script);

})();

```



\### 2. De Remote Ingestie-Engine (`latest.js`)

Dit script draait in de context van de openstaande YouTube-tab van de eindgebruiker. Het script leunt op de beproefde methodiek van `yt-dlp` om netwerkbeperkingen en IP-blokkades van Google te omzeilen:



\*   \*\*De Subtitle Tunnel (yt-dlp methode):\*\* Het script scant het in-memory `ytInitialPlayerResponse` object op de pagina. Hieruit extraheert het de officiële, geautoriseerde en gethrottled-vrije `timedtext` URL van Google. Het script voert direct een client-side `fetch()` uit naar deze XML/JSON-stream om het ruwe transcript binnen te halen.

\*   \*\*De Comment-Boom Scraper (Youtubei methode):\*\* In plaats van een externe server te belasten, bootst het script de interne YouTube-interactie na. Het doet geautomatiseerde POST-requests naar `https://youtube.com` met gebruikmaking van de actieve API-key, de client-context en de `continuation` tokens die al in de browser van de gebruiker aanwezig zijn.



\### 3. Client-Side Text Cleansing \& Compressie

Voordat de data naar de backend wordt verzonden, voert de browser van de gebruiker de CPU-intensieve tekstverwerking uit (gebaseerd op de logica uit het originele `extractor.py` Python-script):



\*   \*\*Schoonmaak:\*\* Alle HTML/wiskundige karaoke-tags (`<c t="..." />`) en individuele tijdstempels per woord worden via reguliere expressies (regex) verwijderd.

\*   \*\*Ontdubbeling:\*\* Automatisch gegenereerde overlappende YouTube-zinnen worden in-memory samengevoegd tot vloeiende, unieke tekstblokken.

\*   \*\*Boomstructuur:\*\* Comments en replies worden wiskundig genormaliseerd naar een platte, hiërarchische boomstructuur op basis van hun `parent`-ID.



\---



\## 💸 Validatie binnen de "0-Euro Compute" Filosofie



De keuze voor deze specifieke client-side architectuur sluit naadloos aan op de commerciële en technische doelstellingen van VidSlayers:



1\.  \*\*0% Server Rekenkracht:\*\* De zware reguliere expressies en het itereren over duizenden reacties gebeurt op de processor van de eindgebruiker. Jouw Cloudflare Worker hoeft enkel een schone, reeds gestructureerde JSON-payload te ontvangen.

2\.  \*\*Immuun voor IP-Blokkades:\*\* Omdat alle netwerkaanroepen naar de Google-servers rechtstreeks via het eigen, legitieme IP-adres van de actieve gebruiker lopen, lift VidSlayers gratis en onbeperkt mee op een vertrouwd netwerkverkeer-profiel. Captcha's en server-IP-bans zijn hiermee geëlimineerd.

3\.  \*\*Onmiddellijke Updates (YouTube-Change-Proof):\*\* Mocht YouTube wijzigingen doorvoeren in haar interne API-structuur, dan hoeft de eindgebruiker de bookmarklet niet aan te passen. Door de code in `latest.js` centraal op Cloudflare Pages te updaten, lift de gehele infrastructuur direct mee op de nieuwste `yt-dlp` herstelpatronen.

