# 🧠 VidLayer - AI Session Resume Prompt

Geef deze complete prompt als allereerste bericht in een nieuwe AI-sessie om direct alle context, code-architectuur en de roadmap in te laden.

---

**Sessie-overdracht Instructie voor de AI-assistent:**

Hallo AI. Laad de volgende context en projectstatus in. Wij gaan vanaf dit punt direct verder met de ontwikkeling.

### 1. Project & Architect Context
* **Projectnaam:** VidLayer (The Stripe for Social Video Data)
* **Architect:** GtHbbrr (One-Man-IT-Giant filosofie: stateless, serverless, 0-euro compute marge)
* **Doelgroep:** B2B, softwareontwikkelaars, marketingplatforms, data-analisten
* **Gezuiverde Visie:** Een developer-first data-infrastructuur API die rommelige video-transcripts en geneste commentaar-bomen opschoont en omzet in universele, gestructureerde JSON-matrices. Het is een symbiotisch concullega-muisje voor de AI-giganten: we leveren de schone grondstof en jagen juist betaald verkeer naar hun systemen via caching en failovers.

### 2. Technische Stack & Live Componenten
* **Infrastructuur:** Cloudflare Workers (Backend API), Cloudflare Pages (Frontend), Cloudflare D1 (SQL Database), Cloudflare Vectorize (RAG-vector database), Cloudflare AI Gateway (Caching & Analytics).
* **AI-Modellen:** Multi-model failover en load-balancing over Google Gemini Flash API-keys.
* **Data-Ingestie:** Geteste extractielogica gebaseerd op yt-dlp. De data-extractie wordt client-side (browser/bookmarklet) uitgevoerd om de CORS-muur te slopen en IP-blokkeringen door Google centraal te elimineren.

### 3. Huidige Mappenstructuur in de Repo
* 📁 \`src/\` - Bevat \`extractor.py\` (Het Python-script met geavanceerde regex-filters dat de YouTube-ruis en karaoke-tags weghaalt, sprekerswissels herkent en tijdscodes berekent).
* 📁 \`data/\` - Bevat de testbestanden van The Electric Valentines (\`.info.json\`, \`.vtt\` en de opgeschoonde resultaat-txt).
* 📁 \`elevator_pitches/\` - Bevat \`pitches.md\` (Zowel de technische- als de eenvoudige B1-pitch).
* 📁 \`project_ai_prompts/\` - Bevat deze \`CONTEXT_PROMPT.md\`.

### 4. Wat we VANDAAG succesvol hebben afgerond
1. De complete B2B-platformstudie en de gezuiverde platformpropositie zijn gedefinieerd.
2. De extractielogica is lokaal gevalideerd met de data van de 'Electric Valentines' video.
3. Het Python-script is succesvol herstructureerd en schrijft de schone resultaten automatisch weg naar de \`data/\`-map.
4. De complete GitHub repository \`GtHbbrr/VidLayer\` is geinitieerd en alle bestanden zijn gefatsoeneerd en live gepusht.

### 5. Startopdracht voor SPRINT 1 (De AI mag nu antwoorden)
Wij gaan nu de eerste echte code-sprint starten voor het Cloudflare platform. Schrijf en configureer de \`wrangler.toml\` voor de nieuwe Cloudflare Worker backend en zet de basis-architectuur op voor de serverless API-endpoints die de JSON-payload gaan verwerken.
