\# 🛡️ VidSlayers - API Gateway Beveiligingsarchitectuur



Dit document beschrijft de cryptografische en stateless verdedigingslinie van de VidSlayers API-gateway (Cloudflare Workers). Omdat het platform gebruikmaakt van een client-side Bookmarklet die data vanaf de browser van de eindgebruiker naar een publiek endpoint stuurt, is deze beveiliging cruciaal om misbruik, token-verspilling en ongewenste API-kosten te voorkomen — zonder de \*\*0-euro compute marge\*\* te belasten.



De architectuur is direct afgeleid van en geüpgraded op basis van het beproefde en robuuste framework uit de `openheatpumps-logs-analyzer` backend.



\---



\## 🗺️ De 3-Traps Stateless Verdedigingslinie



\[ Inkomend Request vanaf de Browser / Script ]

│

▼

┌───────────────────────────┐

│  Linie 1: Origin Pinning  │ ──► \[Fout 403] Niet van youtube.com

└───────────────────────────┘

│ Legitiem

▼

┌───────────────────────────┐

│ Linie 2: Time-Window Check│ ──► \[Fout 401] Request ouder dan 60s (Anti-Replay)

└───────────────────────────┘

│ Legitiem

▼

┌───────────────────────────┐

│   Linie 3: HMAC-SHA256    │ ──► \[Fout 401] Handtekening corrupt of nagemaakt

└───────────────────────────┘

│ Legitiem

▼

\[ Veilig naar de Gemini-Cycler Motor \& RAG ]





\---



\## 🏗️ Functionele Beschrijving van de Beveiligingslinies



\### 1. Linie 1: CORS \& Origin Pinning (Het Eerste Filter)

De Cloudflare Worker controleert dwingend de metadata van het HTTP-verzoek. Hoewel de Bookmarklet overal kan worden geactiveerd, accepteert de API-gateway \*uitsluitend\* verkeer waarbij de browser verklaart dat het verzoek is geïnitieerd vanaf het officiële domein van YouTube.



\*   \*\*Implementatie:\*\* De `Access-Control-Allow-Origin` header in de CORS-configuratie staat niet op de lakse wild-card `\*`, maar is keihard vastgezet op `https://youtube.com`. Verzoeken vanuit scripts buiten de browser (zoals Postman of geautomatiseerde curl-spammers) die geen geldige origin meesturen, worden direct geweigerd.



\### 2. Linie 2: Stateless Time-Window Validation (Anti-Replay)

Om te voorkomen dat een kwaadwillende een legitieme netwerkaanvraag (inclusief geldige handtekening) onderschept en deze duizenden keren achter elkaar herhaalt om jouw Gemini-quota leeg te trekken (een \*Replay Attack\*), gebruikt de Worker een tijd-slot-controle.



\*   \*\*Implementatie:\*\* De Bookmarklet voegt in de header een actuele UNIX-timestamp in seconden toe (`X-VidSlayers-Timestamp`). De Cloudflare Worker trekt deze af van zijn eigen actuele servertijd. Is het verschil groter dan \*\*60 seconden\*\*? Dan wordt het verzoek onmiddellijk vernietigd. De geldigheid van een onderschept pakketje is hierdoor gereduceerd tot één minuut.



\### 3. Linie 3: Cryptografische Payload Signing (HMAC-SHA256)

Dit is de belangrijkste linie die garandeert dat de payload \*echt\* door jouw legitieme `latest.js` extractie-engine in de browser is gegenereerd en schoongemaakt.



\*   \*\*Implementatie:\*\* 

&#x20;   1. De Cloudflare Worker en de remote `latest.js` engine delen een geheime sleutel (een \*Shared Secret\* verwerkt in de omgevingsvariabelen).

&#x20;   2. Voordat de data de browser verlaat, berekent de `Web Crypto API` een unieke SHA256-hash over de cruciale payload-data (bijv. `videoId` + `timestamp`).

&#x20;   3. Deze hash wordt meegestuurd in de `X-VidSlayers-Signature` header.

&#x20;   4. De Cloudflare Worker voert in-memory exact dezelfde wiskundige berekening uit. Als de handtekeningen niet matchen, is de data gemanipuleerd en blokkeert de poort direct.



\---



\## 💻 De Backend "Crash-Pijp" Integratie



Geïnspireerd op de foutloze runtime van de Quatt-analyzer, is de gehele beveiligingscontrole ingemetseld in een allesomvattende `try/catch`-architectuur. Mocht een aanvaller corrupte JSON-bestanden sturen met de intentie de server te laten crashen, dan vangt de "Crash-pijp" dit op zonder cpu- overhead te genereren:



```typescript

try {

&#x20; // Voer Linie 1, 2 en 3 cryptografisch uit...

} catch (error) {

&#x20; // De Universele Crash-Pijp achtervang

&#x20; return new Response(JSON.stringify({ 

&#x20;   status: "error", 

&#x20;   model: "Crash-pijp", 

&#x20;   diagnose: `🚨 SYSTEMISCHE CRASH: ${error.message}` 

&#x20; }), { status: 500, headers: corsHeaders });

}

```



\---



\## 💸 Voordelen voor het Businessmodel



1\.  \*\*Volledig Stateless (0-Euro Rekenkracht):\*\* De Worker hoeft geen database of Cloudflare KV-store te raadplegen om de authenticiteit te controleren. De cryptografische verificatie gebeurt direct in het tijdelijke geheugen, wat zorgt voor een latency van slechts enkele milliseconden en nul verbruikskosten.

2\.  \*\*Naadloze Enterprise Upgrade:\*\* Zodra een agency of productie-klant live gaat en via Stripe betaalt, switcht de Worker voor die specifieke route naar een database-check op de unieke `X-VidSlayers-Api-Key`. Het gratis sandboxverkeer blijft ondertussen veilig en kosteloos draaien op de HMAC-motor.

