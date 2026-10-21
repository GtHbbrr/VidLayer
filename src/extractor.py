import json
import os
import glob
import re

# Schakel over naar de actieve map van het script
map_pad = os.path.dirname(os.path.abspath(__file__))
os.chdir(map_pad)

# Zoek naar de bestanden
info_bestanden = glob.glob("../data/*.info.json")
vtt_bestanden = glob.glob("../data/*.vtt")


if not info_bestanden:
    print("Fout: Geen .info.json gevonden!")
    exit()

# Laad de basisvideo-data
with open(info_bestanden[0], 'r', encoding='utf-8') as f:
    video_data = json.load(f)

# === DEEL 1: BESTANDSNAAM GENEREREN (TITEL + TIMESTAMP SANITIZER) ===
titel = video_data.get('title', 'Onbekende_Titel')
upload_datum = video_data.get('upload_date', 'Onbekende_Datum') # Formaat: YYYYMMDD

# Maak de titel veilig voor Windows-bestandsnamen (verwijder verboden tekens)
veilige_titel = re.sub(r'[\\/*?:"<>|]', '_', titel)
veilige_titel = " ".join(veilige_titel.split()) # Voorkom dubbele spaties

# Dynamische bestandsnaam: bijv. "20251209 - Tesla FSD 14.2.1 vs Comma.ai...txt"
nieuwe_bestandsnaam = f"{upload_datum} - {veilige_titel}.txt"

# === DEEL 2: ONDERTITELS PARSEN MET TIMESTAMPS ===
opgebouwde_dialoog = []

if vtt_bestanden:
    print(f"Ondertitelbestand gevonden: {vtt_bestanden[0]}. Timestamps worden berekend...")
    with open(vtt_bestanden[0], 'r', encoding='utf-8') as f:
        vtt_lines = f.readlines()
    
    huidige_spreker = 1 # 1 = Jerry, 2 = Allison
    huidige_tijdcode = "[00:00]"
    lopende_zin_blok = []
    
    for line in vtt_lines:
        line = line.strip()
        
        if not line or 'WEBVTT' in line or 'Kind:' in line or 'Language:' in line or line.startswith('NOTE'):
            continue
            
        time_match = re.match(r'(\d\d):(\d\d):(\d\d)\.\d\d\d -->', line)
        if time_match:
            uren = time_match.group(1)
            minuten = time_match.group(2)
            seconden = time_match.group(3)
            
            if uren != "00":
                huidige_tijdcode = f"[{uren}:{minuten}:{seconden}]"
            else:
                huidige_tijdcode = f"[{minuten}:{seconden}]"
            continue
            
        is_wissel = '>>' in line or '&gt;&gt;' in line
        
        line = re.sub(r'</?c[^>]*>', '', line)
        line = re.sub(r'<\d\d:\d\d:\d\d\.\d\d\d>', '', line)
        line = line.replace('&gt;&gt;', '').replace('>>', '').replace('&gt;', '').replace('>', '')
        line = " ".join(line.split()).strip()
        
        if not line:
            continue
            
        if is_wissel and lopende_zin_blok:
            schone_tekst_blok = " ".join(lopende_zin_blok)
            schone_tekst_blok = re.sub(r'\b(\w+)( \1)+\b', r'\1', schone_tekst_blok)
            
            naam = "JERRY" if huidige_spreker == 1 else "ALLISON / SPREKER 2"
            opgebouwde_dialoog.append(f"{huidige_tijdcode} {naam}:\n    {schone_tekst_blok}\n")
            
            lopende_zin_blok = [line]
            huidige_spreker = 2 if huidige_spreker == 1 else 1
        else:
            if not lopende_zin_blok or line != lopende_zin_blok[-1]:
                lopende_zin_blok.append(line)
                
    if lopende_zin_blok:
        naam = "JERRY" if huidige_spreker == 1 else "ALLISON / SPREKER 2"
        opgebouwde_dialoog.append(f"{huidige_tijdcode} {naam}:\n    {' '.join(lopende_zin_blok)}\n")
        
    lopende_tekst = "\n".join(opgebouwde_dialoog)
else:
    lopende_tekst = "[Geen .vtt-ondertitelbestand gevonden in deze map.]"

# === DEEL 3: COMMENTS FORMATTEREN ALS TEKST ===
opgebouwde_comments = []
print("Comments worden verwerkt...")

for item in video_data.get('comments', []):
    is_reply = 'parent' in item and item['parent'] != 'root'
    gebruiker = item.get('author', 'Anoniem')
    likes = item.get('like_count', 0)
    datum = item.get('_time_text', 'Onbekend')
    reactie = item.get('text', '').strip()
    
    if is_reply:
        opgebouwde_comments.append(f"    └── ANTWOORD van {gebruiker} ({datum}) | {likes} Likes:\n        \"{reactie}\"\n")
    else:
        opgebouwde_comments.append(f"💬 HOOFDCOMMENT van {gebruiker} ({datum}) | {likes} Likes:\n    \"{reactie}\"\n")

comments_tekst = "\n".join(opgebouwde_comments)

# === DEEL 4: ALLES IN HET DYNAMISCHE BESTAND SCHRIJVEN ===
with open(f"../data/{nieuwe_bestandsnaam}", 'w', encoding='utf-8') as t_file:
    t_file.write(f"COMPLEET DOSSIER VOOR: {titel}\n")
    t_file.write(f"UPLOAD DATUM: {upload_datum}\n")
    t_file.write("="*80 + "\n\n")
    
    t_file.write("--- VIDEO BESCHRIJVING & CHAPTERS ---\n")
    t_file.write(video_data.get('description', 'Geen beschrijving') + "\n\n")
    t_file.write("="*80 + "\n\n")
    
    t_file.write("--- TRANSCRIPT MET SCHONE TIJDCODES ---\n")
    t_file.write(lopende_tekst + "\n")
    t_file.write("="*80 + "\n\n")
    
    t_file.write("--- GEËXPORTEERDE YOUTUBE DISCUSSIES & COMMENTS ---\n\n")
    t_file.write(comments_tekst)

print(f"Succes! Alles is samengevoegd in: '{nieuwe_bestandsnaam}'")
