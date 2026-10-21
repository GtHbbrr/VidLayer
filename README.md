# VidSlayer 🚀

Eenvoudige data-infrastructuur voor online video. Welkom bij de code-blauwdruk van VidSlayer! Dit platform helpt softwarebouwers, marketingbedrijven en data-analisten om waardevolle informatie te halen uit online video's en de duizenden reacties daaronder. 

Dit is een onafhankelijke, developer-first data-infrastructuur die de ruwe multimedia-chaos van YouTube volledig omzet naar loepzuivere, gestructureerde en direct bruikbare JSON-bestanden.

---

## 🛠️ Hoe werkt het platform (v1.0 Architectuur)

VidSlayer werkt volledig *serverless* en *stateless* binnen het Cloudflare-ecosysteem om maximale snelheid, uptime en kostenefficiëntie te garanderen:

1. **De Data-Ingestie & Schone Extractie (`frontend/` & `extractor/`):** De gebruiker of een externe applicatie stuurt een YouTube-URL in via onze API of de laagdrempelige URL-hack. De code haalt de data client-side binnen via het IP-adres van de eindgebruiker (waarmee CORS-beperkingen en serverblokkades door Google direct worden omzeild). De extractie-motor filtert alle computercodes (`<c>`), timestamps per woord en YouTube-herhalingen volledig weg.
2. **De Serverless Backend Motor (`backend/` - Cloudflare Workers):** Een slanke, snelle Worker fungeert als de API-gateway. De Worker verwerkt de opgeschoonde tekstpakketjes en stuurt deze door naar de kunstmatige intelligentie.
3. **De Enterprise Multi-Model Failover (De Cycler):** Om de app in de testfase volledig kosteloos te houden, balanceert een slimme *model cycler* de requests over 5 gratis Google AI Studio (Gemini Flash) slots. Dit garandeert een gratis capaciteit tot 75 requests per minuut. Zodra een applicatie in productie gaat en over de gratis limiet schiet, schakelt het systeem via de **Cloudflare AI Gateway** automatisch over naar de officiële, betaalde pay-as-you-go API-pijpen van Google.
4. **Het Slimme RAG-Geheugen (Cloudflare Vectorize):** Het platform beschikt over een digitale context-bibliotheek (een vector-database) aangedreven door het `@cf/baai/bge-base-en-v1.5` embedding-model. Voordat data wordt verwerkt, kan de API vlijmscherp live documentatie of klantspecifieke productsheets raadplegen voor extra context-verrijking.

---

## 📊 De 3 Universele Gestructureerde Datalagen (JSON API)

VidSlayer doet geen aannames over de specifieke use-case (het is geen gadget, maar infrastructuur) en levert via één POST-request drie objectieve, universele datalagen terug in een strakke JSON-matrix:

*   **Laag 1: Gesynchroniseerd Gespreksverslag:** Een volledig schoongemaakt, leesbaar transcript waarin de tekst automatisch is opgeknipt per sprekerswissel en is voorzien van heldere tijdstempels (bijv. `[01:21] JERRY:`).
*   **Laag 2: Genormaliseerde Comment-boomstructuur:** Een wiskundig geordende mappenstructuur van alle reacties onder de video, waarbij de hiërarchische samenhang van hoofdreacties en geneste antwoorden (`└── replies`) volledig intact blijft.
*   **Laag 3: Objectieve NLP-Entiteiten- en Keyword-Matrix:** Een AI-verrijkte laag die automatisch alle thema's, personen, merken en specifieke gebruikersintenties (zoals onbeantwoorde vragen en vergelijkingen) classificeert en sorteert met een relevantie-score.

---

## 🗺️ De Agile Backlog & User Stories (Sprint 1 t/m v1.0)

### 🏃 Story 1: De Snelle Ingang (De URL-hack & Bookmarklet)
*   **Als** softwareontwikkelaar of actieve gebruiker,
*   **wil ik** met minimale handelingen een video kunnen indienen via de URL-balk of een favorietenknop,
*   **zodat ik** direct binnen één seconde de data-extractie kan starten.
*   *Acceptatiecriteria:* De frontend accepteert URL-invoer, herkent video-IDs via een wildcard-domeinhack (bijv. `aiyoutube.com/watch?...`), en bevat een werkende Javascript Bookmarklet-knop voor de favorietenbalk.

### 🏃 Story 2: De Slanke Ingestie-motor (Text Cleansing)
*   **Als** API-backend,
*   **wil ik** ondertitels en geneste comments ontdoen van alle karaoke-tags en herhalende overlappingen,
*   **zodat** we netwerkverkeer minimaliseren en het AI-model zuivere data voeren zonder token-verspilling.
*   *Acceptatiecriteria:* Verwijdering van alle HTML-tags en tijdcodes per woord; automatische ontdubbeling van overlappende YouTube-zinnen; behoud van de boomstructuur van replies.

### 🏃 Story 3: De Enterprise Load Balancer (Failover & Uptime)
*   **Als** platform-architect,
*   **wil ik** dat de API-aanroepen automatisch balanceren over meerdere AI-slots en bij haperingen direct overschakelen naar een achtervang,
*   **zodat** het platform een maximale uptime en extreem lage latency kan garanderen.
*   *Acceptatiecriteria:* Automatische sequentiële rotatie over de slots in de sandbox-omgeving; directe opvang (failover) van HTTP 429 of 503 fouten binnen dezelfde runtime; foutloze gateway-routering.

### 🏃 Story 4: De Geautomatiseerde Facturatie (Stripe Metered Billing)
*   **Als** platform-eigenaar,
*   **wil ik** dat het verbruik van productie-klanten automatisch per request wordt bijgehouden en afgerekend,
*   **zodat** het platform direct vanaf de lancering commercieel levensvatbaar is.
*   *Acceptatiecriteria:* Integratie van **Stripe Billing**; de Cloudflare Worker stuurt aan het einde van de dag geautomatiseerd de verbruikscijfers door; productie-verkeer wordt direct losgekoppeld van de gratis test-tiers.

---

## 💸 Het Symbiotische Business- & Monetizationmodel

VidSlayer is ontworpen als een **concullega-muisje** voor de grote AI-spelers. We concurreren niet met de grote LLM-aanbieders, maar we zijn een partner die juist hoogwaardig, gezuiverd dataverkeer en extra omzet naar hun netwerken jaagt. Dankzij de ingebouwde caching via Cloudflare AI Gateway belasten we hun servers nooit met onnodige dubbele aanroepen.

*   **De Gratis Sandbox:** Ontwikkelaars kunnen de API volledig gratis testen in een gelimiteerde proefomgeving (aangedreven door onze gratis failover-cycler).
*   **Pay-as-you-go SaaS:** Zodra de applicaties van onze klanten live gaan, betalen ze automatisch een vast, laag bedrag per verwerkte video-minuut via Stripe, of ze vullen *hun eigen enterprise API-key* in waarbij VidSlayer puur als de gestructureerde data-infrastructuurtunnel fungeert.

---
*Dit project is gebouwd met de robuuste, serverless filosofie van een eenmans-it-gigant. AI-responses op data-analyses kunnen fouten bevatten. Controleer de onbewerkte databestanden bij twijfel.*
