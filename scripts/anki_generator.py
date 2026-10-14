import os
import sys
import json
import warnings
import requests
from dotenv import load_dotenv

# Evitar advertencias ruidosas en consola
warnings.filterwarnings("ignore", category=FutureWarning)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
ANKI_URL = os.getenv("ANKI_CONNECT_URL", "http://127.0.0.1:8765")
DECK_NAME = os.getenv("ANKI_DECK_NAME", "English::Physics_C1")
EXPORT_FILE = os.path.join("data", "vocab", "anki_cards_export.tsv")

import google.generativeai as genai
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
else:
    model = None

ANKI_PROMPT = """
Eres un lexicógrafo y profesor de inglés científico para posgrados de física en Europa.
Dado un término, frase o párrafo, extrae o genera fichas de vocabulario académico C1/STEM.

Para cada término relevante solicitado, debes devolver un JSON con esta estructura exacta:
[
  {
    "term": "palabra o frase",
    "ipa": "/transcripción fonética/",
    "part_of_speech": "noun / verb / adjective",
    "definition": "Definición clara y concisa en inglés académico formal",
    "physics_examples": [
      "Oración de ejemplo 1 contextualizada en física experimental o teórica",
      "Oración de ejemplo 2 contextualizada en análisis de datos o formulación matemática"
    ],
    "collocations": ["colocación 1", "colocación 2", "colocación 3"],
    "spanish_meaning": "Significado en español preciso para el ámbito científico"
  }
]

Devuelve ÚNICAMENTE el array JSON sin texto adicional ni bloques markdown.
"""

def clean_json_response(raw: str) -> str:
    clean = raw.strip()
    if clean.startswith("```json"):
        clean = clean[7:]
    elif clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    return clean.strip()

def check_anki_connected() -> bool:
    try:
        res = requests.post(ANKI_URL, json={"action": "version", "version": 6}, timeout=1.5)
        return res.status_code == 200
    except Exception:
        return False

def add_card_to_anki(front_html: str, back_html: str, tags: list = None) -> bool:
    if not tags:
        tags = ["physics", "academic", "c1"]
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": DECK_NAME,
                "modelName": "Basic",
                "fields": {
                    "Front": front_html,
                    "Back": back_html
                },
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "deck"
                },
                "tags": tags
            }
        }
    }
    try:
        # Asegurar que el mazo exista
        requests.post(ANKI_URL, json={"action": "createDeck", "version": 6, "params": {"deck": DECK_NAME}}, timeout=2)
        res = requests.post(ANKI_URL, json=payload, timeout=2)
        resp_json = res.json()
        return resp_json.get("error") is None
    except Exception:
        return False

def export_card_to_tsv(term: str, front_html: str, back_html: str):
    os.makedirs(os.path.dirname(EXPORT_FILE), exist_ok=True)
    clean_front = front_html.replace("\t", " ").replace("\n", "<br>")
    clean_back = back_html.replace("\t", " ").replace("\n", "<br>")
    with open(EXPORT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{clean_front}\t{clean_back}\tphysics c1\n")

def generate_flashcards(input_text: str):
    if not model:
        print("❌ Error: GEMINI_API_KEY no configurada.")
        return
        
    print(f"\n🧠 Analizando y generando flashcards con Gemini ({model_name})...")
    prompt = f"{ANKI_PROMPT}\n\nEntrada del estudiante:\n\"\"\"\n{input_text}\n\"\"\""
    
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    clean_text = clean_json_response(response.text)
    try:
        cards_data = json.loads(clean_text)
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar respuesta JSON: {e}")
        return

    anki_online = check_anki_connected()
    if anki_online:
        print(f"🔗 Conectado a AnkiConnect en {ANKI_URL}. Mazo: '{DECK_NAME}'.")
    else:
        print(f"ℹ️  Anki no está abierto o AnkiConnect no está activo.")
        print(f"📁 Las tarjetas se guardarán en '{EXPORT_FILE}' listas para importar en Anki.")

    print("\n" + "="*60)
    for card in cards_data:
        term = card.get("term", "")
        ipa = card.get("ipa", "")
        pos = card.get("part_of_speech", "")
        definition = card.get("definition", "")
        examples = card.get("physics_examples", [])
        collocs = card.get("collocations", [])
        meaning = card.get("spanish_meaning", "")
        
        # Diseño HTML elegante para la tarjeta Anki
        front_html = f"<div style='font-size:24px; font-weight:bold; color:#1a73e8;'>{term}</div>"
        if ipa:
            front_html += f"<div style='font-size:14px; color:#5f6368;'>{ipa} &bull; <i>{pos}</i></div>"
            
        back_html = f"<div style='font-size:16px; margin-bottom:8px;'><b>{meaning}</b></div>"
        back_html += f"<div style='font-size:14px; color:#202124; margin-bottom:10px;'>{definition}</div><hr style='border:none; border-top:1px solid #ddd;'>"
        
        if examples:
            back_html += "<div style='font-size:13px; color:#188038; margin-top:6px;'><b>Physics Context:</b><ul>"
            for ex in examples:
                back_html += f"<li>{ex}</li>"
            back_html += "</ul></div>"
            
        if collocs:
            back_html += f"<div style='font-size:12px; color:#5f6368;'><b>Collocations:</b> {', '.join(collocs)}</div>"

        # Mostrar en consola
        print(f"📌 Término: {term} {ipa}")
        print(f"   Significado: {meaning}")
        print(f"   Definición:  {definition}")
        if examples:
            print(f"   Ejemplo STEM: {examples[0]}")
        print("-" * 60)

        # Guardar en Anki y/o en TSV
        added = False
        if anki_online:
            added = add_card_to_anki(front_html, back_html)
            if added:
                print(f"   ✅ Insertada directamente en Anki (Mazo: {DECK_NAME})")
            else:
                print("   ⚠️  No se pudo insertar en AnkiConnect, exportando a TSV...")
                export_card_to_tsv(term, front_html, back_html)
                print(f"   📁 Guardada en {EXPORT_FILE}")
        else:
            export_card_to_tsv(term, front_html, back_html)
            print(f"   📁 Guardada en archivo de importación: {EXPORT_FILE}")

    print("="*60)
    print(f"✨ ¡Proceso completado! Se procesaron {len(cards_data)} tarjeta(s).\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("\n📇 GENERADOR DE FLASHCARDS C1 / STEM PARA ANKI")
        print("Ingresa una palabra, una lista separada por comas, o un párrafo de física:")
        query = input("Texto/Palabra(s): ").strip()
        
    if query:
        generate_flashcards(query)
    else:
        print("No se ingresó ningún término.")
