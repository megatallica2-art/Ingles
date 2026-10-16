# curriculum_data.py
# Plan de estudios estructurado por niveles y subniveles del Marco Común Europeo (CEFR)
import os
import hashlib
import requests

def get_audio_for_text(text: str) -> str:
    """Retorna la ruta al archivo MP3 de audio en data/audio/<hash>.mp3. Si no existe, lo descarga y almacena en caché."""
    os.makedirs(os.path.join("data", "audio"), exist_ok=True)
    fn = hashlib.md5(text.encode("utf-8")).hexdigest() + ".mp3"
    path = os.path.join("data", "audio", fn)
    if not os.path.exists(path):
        try:
            url = "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=" + requests.utils.quote(text)
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=8)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    f.write(r.content)
        except Exception:
            pass
    return path if os.path.exists(path) else ""

def build_interactive_example_html(example: dict) -> str:
    """Construye una tarjeta HTML elegante con tooltips interactivos para cada palabra y fonemas en español."""
    en_words = example.get("words", [])
    if not en_words:
        words_html = f"<span class='hover-word'>{example['en']}</span>"
    else:
        spans = []
        for w_item in en_words:
            w = w_item.get("w", "")
            t = w_item.get("t", "")
            spans.append(f"<span class='hover-word'>{w}<span class='tip'>{t}</span></span>")
        words_html = " ".join(spans)

    es_text = example.get("es", "")
    phonetic_es = example.get("phonetic_es", "")

    html = f"""
    <div class="example-box">
        <div class="example-en">
            <span style="font-size:1.1rem; margin-right:5px;">🇬🇧</span> {words_html}
        </div>
        <div class="example-es">
            🇪🇸 <em>{es_text}</em>
        </div>
        <div class="example-phonetics">
            🗣️ <b>Pronunciación en español:</b> <span class="phonetic-badge">/ {phonetic_es} /</span>
        </div>
    </div>
    """
    return html

CURRICULUM = {
    "A1_A2": {
        "title": "Nivel A1 ➔ A2: Cimientos, Supervivencia & Rutinas",
        "description": "Aprende a presentarte, hablar de tu día a día, viajar y perder el miedo a comunicarte.",
        "badge_color": "#10b981",
        "lessons": [
            {
                "id": "A1.1",
                "title": "El Verbo To Be y Presentaciones Personales",
                "sublevel": "A1.1 - Cimientos",
                "objective": "Aprender a presentarte, decir de dónde eres, tu edad y cómo te sientes.",
                "explanation_es": """
El verbo **To Be** significa *ser* o *estar*. Es la columna vertebral del inglés.
A diferencia del español, en inglés **siempre** necesitamos poner el sujeto antes del verbo (I, you, he, she, it, we, they).

* **I am** (I'm) ➔ Yo soy / estoy
* **You are** (You're) ➔ Tú eres / estás
* **He / She / It is** (He's / She's / It's) ➔ Él / Ella / Eso es o está
* **We / They are** (We're / They're) ➔ Nosotros / Ellos son o están

⚠️ **Diferencia clave con el español:**
En español decimos *'Yo tengo 25 años'*, pero en inglés se dice *'I am 25 years old'* (como si dijeras 'yo soy 25 años viejo').
                """,
                "formula": "Sujeto + am / is / are + complemento",
                "examples": [
                    {
                        "en": "Hello! I am Tania, and I'm very excited to learn English.",
                        "es": "¡Hola! Soy Tania y estoy muy emocionada de aprender inglés.",
                        "phonetic_es": "Jelóu! Ai am Tania, end aim veri eksáited tu lern ínglish.",
                        "words": [
                            {"w": "Hello!", "t": "¡Hola!"},
                            {"w": "I", "t": "Yo"},
                            {"w": "am", "t": "soy / estoy"},
                            {"w": "Tania,", "t": "Tania,"},
                            {"w": "and", "t": "y"},
                            {"w": "I'm", "t": "yo estoy"},
                            {"w": "very", "t": "muy"},
                            {"w": "excited", "t": "emocionada / entusiasmada"},
                            {"w": "to", "t": "de / por"},
                            {"w": "learn", "t": "aprender"},
                            {"w": "English.", "t": "inglés."}
                        ]
                    },
                    {
                        "en": "Anderson is a physicist from Colombia.",
                        "es": "Anderson es físico de Colombia.",
                        "phonetic_es": "Ánderson is e físisist from Kolómbia.",
                        "words": [
                            {"w": "Anderson", "t": "Anderson"},
                            {"w": "is", "t": "es / está"},
                            {"w": "a", "t": "un"},
                            {"w": "physicist", "t": "físico (científico)"},
                            {"w": "from", "t": "de / proveniente de"},
                            {"w": "Colombia.", "t": "Colombia."}
                        ]
                    },
                    {
                        "en": "They are in the library studying right now.",
                        "es": "Ellos están en la biblioteca estudiando ahora mismo.",
                        "phonetic_es": "Dei ar in de láibrari stádi-ing ráit náu.",
                        "words": [
                            {"w": "They", "t": "Ellos"},
                            {"w": "are", "t": "están"},
                            {"w": "in", "t": "en"},
                            {"w": "the", "t": "la"},
                            {"w": "library", "t": "biblioteca"},
                            {"w": "studying", "t": "estudiando"},
                            {"w": "right", "t": "justo / ahora"},
                            {"w": "now.", "t": "mismo."}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "I have 24 years old. / Is very hot today.",
                    "right": "I am 24 years old. / It is very hot today.",
                    "why": "La edad se dice con 'to be' y nunca puedes omitir el sujeto 'It'."
                },
                "quiz": {
                    "question": "¿Cuál es la forma correcta de decir 'Él tiene hambre y tiene 28 años'?",
                    "options": [
                        "He has hungry and has 28 years.",
                        "He is hungry and is 28 years old.",
                        "He is hunger and have 28 years old."
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Correcto! Tanto los estados físicos ('is hungry') como la edad ('is 28 years old') se expresan con el verbo To Be."
                },
                "practice_challenge": "Escribe una breve presentación de 3 oraciones diciendo tu nombre, a qué te dedicas y cómo te sientes hoy."
            },
            {
                "id": "A1.2",
                "title": "Presente Simple: Hábitos y la Regla de Oro (-s / -es)",
                "sublevel": "A1.2 - Rutinas",
                "objective": "Describir tus hábitos diarios y rutinas.",
                "explanation_es": """
Usamos el **Present Simple** para cosas que hacemos siempre, hábitos o verdades generales (no para lo que estás haciendo en este instante).

**La Regla de Oro:**
Cuando hablas de **He, She, It** (tercera persona), al verbo se le agrega **-s** o **-es**:
* *I drink coffee* ➔ *She drink**s** coffee*
* *I watch movies* ➔ *He watch**es** movies*
* *I study English* ➔ *She stud**ies** English*

Para negar o preguntar usamos los auxiliares **Do / Does**:
* *I do not (don't) work on Sundays.*
* *She does not (doesn't) eat meat.* (¡Ojo! El verbo vuelve a su forma base: no lleva -s cuando ya está 'does').
                """,
                "formula": "Afirmativo: Sujeto + Verbo(-s/-es) | Negativo: Sujeto + don't / doesn't + Verbo",
                "examples": [
                    {
                        "en": "I wake up at 7:00 AM every morning.",
                        "es": "Me despierto a las 7:00 AM todas las mañanas.",
                        "phonetic_es": "Ai uéik ap at séven ei-em évri mórning.",
                        "words": [
                            {"w": "I", "t": "Yo"},
                            {"w": "wake", "t": "despierto"},
                            {"w": "up", "t": "arriba (wake up = despertarse)"},
                            {"w": "at", "t": "a las"},
                            {"w": "7:00 AM", "t": "siete de la mañana"},
                            {"w": "every", "t": "cada / todas las"},
                            {"w": "morning.", "t": "mañana(s)."}
                        ]
                    },
                    {
                        "en": "Tania drinks green tea while studying.",
                        "es": "Tania toma té verde mientras estudia.",
                        "phonetic_es": "Tania drinks grin ti uáil stádi-ing.",
                        "words": [
                            {"w": "Tania", "t": "Tania"},
                            {"w": "drinks", "t": "toma / bebe"},
                            {"w": "green", "t": "verde"},
                            {"w": "tea", "t": "té"},
                            {"w": "while", "t": "mientras"},
                            {"w": "studying.", "t": "estudia."}
                        ]
                    },
                    {
                        "en": "He doesn't like waking up early on weekends.",
                        "es": "A él no le gusta despertarse temprano los fines de semana.",
                        "phonetic_es": "Ji dásent láik uéiking ap érli on uíkends.",
                        "words": [
                            {"w": "He", "t": "A él / Él"},
                            {"w": "doesn't", "t": "no (auxiliar)"},
                            {"w": "like", "t": "gusta"},
                            {"w": "waking", "t": "despertarse"},
                            {"w": "up", "t": "(waking up = levantarse)"},
                            {"w": "early", "t": "temprano"},
                            {"w": "on", "t": "los"},
                            {"w": "weekends.", "t": "fines de semana."}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "She doesn't likes coffee.",
                    "right": "She doesn't like coffee.",
                    "why": "Cuando usas 'doesn't', el auxiliar ya absorbe la -s, así que el verbo principal queda limpio."
                },
                "quiz": {
                    "question": "Completa la frase: 'My best friend ___ English every single day.'",
                    "options": ["study", "studies", "studys"],
                    "answer_idx": 1,
                    "feedback": "¡Exacto! Los verbos que terminan en consonante + 'y' cambian a '-ies' en tercera persona: 'studies'."
                },
                "practice_challenge": "Describe 3 cosas que haces en un día normal desde que te levantas hasta que te vas a dormir."
            },
            {
                "id": "A1.3",
                "title": "Preguntas Clave con Wh- (What, Where, When, Why, How)",
                "sublevel": "A1.3 - Preguntas",
                "objective": "Aprender a pedir información y hacer preguntas fluidas en conversación.",
                "explanation_es": """
Para iniciar cualquier conversación en un viaje o con amigos necesitas las **Wh- Questions**:
* **What:** ¿Qué? o ¿Cuál? (*What do you do?* - ¿A qué te dedicas?)
* **Where:** ¿Dónde? (*Where do you live?* - ¿Dónde vives?)
* **When:** ¿Cuándo? (*When do you practice?* - ¿Cuándo practicas?)
* **Why:** ¿Por qué? (*Why do you learn English?* ➔ Se responde con **Because**: *Because I want to travel.*)
* **Who:** ¿Quién? (*Who is your partner?* - ¿Quién es tu pareja?)
* **How:** ¿Cómo? (*How are you?* / *How much is it?* - ¿Cuánto cuesta?)

**Estructura universal:**
`Wh- Word + Do/Does/Am/Is/Are + Sujeto + Verbo + ?`
                """,
                "formula": "Wh- + Auxiliar (do/does/is/are) + Sujeto + Verbo?",
                "examples": [
                    {
                        "en": "Where do you want to travel next year?",
                        "es": "¿A dónde quieres viajar el próximo año?",
                        "phonetic_es": "Uér du iu uónt tu trável nekst íir?",
                        "words": [
                            {"w": "Where", "t": "¿Dónde? / ¿A dónde?"},
                            {"w": "do", "t": "(auxiliar de pregunta)"},
                            {"w": "you", "t": "tú"},
                            {"w": "want", "t": "quieres"},
                            {"w": "to", "t": "(hacia / a)"},
                            {"w": "travel", "t": "viajar"},
                            {"w": "next", "t": "próximo / siguiente"},
                            {"w": "year?", "t": "año?"}
                        ]
                    },
                    {
                        "en": "Why are you studying English tonight?",
                        "es": "¿Por qué estás estudiando inglés esta noche?",
                        "phonetic_es": "Uái ar iu stádi-ing ínglish tunáit?",
                        "words": [
                            {"w": "Why", "t": "¿Por qué?"},
                            {"w": "are", "t": "estás"},
                            {"w": "you", "t": "tú"},
                            {"w": "studying", "t": "estudiando"},
                            {"w": "English", "t": "inglés"},
                            {"w": "tonight?", "t": "esta noche?"}
                        ]
                    },
                    {
                        "en": "How do you say this in English?",
                        "es": "¿Cómo se dice esto en inglés?",
                        "phonetic_es": "Jáu du iu séi dis in ínglish?",
                        "words": [
                            {"w": "How", "t": "¿Cómo?"},
                            {"w": "do", "t": "(auxiliar de pregunta)"},
                            {"w": "you", "t": "tú / se"},
                            {"w": "say", "t": "dices / dice"},
                            {"w": "this", "t": "esto"},
                            {"w": "in", "t": "en"},
                            {"w": "English?", "t": "inglés?"}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "Where you live? / Why you are sad?",
                    "right": "Where do you live? / Why are you sad?",
                    "why": "En inglés no basta con entonar como pregunta; es obligatorio poner el auxiliar antes del sujeto."
                },
                "quiz": {
                    "question": "¿Cuál es la forma correcta de preguntar '¿A qué hora empieza tu clase?'?",
                    "options": [
                        "What time your class starts?",
                        "What time does your class start?",
                        "What time do your class starts?"
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Muy bien! 'Your class' es 'it', por lo que lleva el auxiliar 'does' y el verbo 'start' en infinitivo."
                },
                "practice_challenge": "Imagina que conoces a alguien en un café en Londres. Escribe 3 preguntas que le harías para conocerlo."
            },
            {
                "id": "A2.1",
                "title": "Pasado Simple: Verbos Regulares e Irregulares",
                "sublevel": "A2.1 - El Pasado",
                "objective": "Contar cosas que ya ocurrieron ayer, el fin de semana pasado o hace un año.",
                "explanation_es": """
El **Past Simple** se usa para acciones que empezaron y terminaron en el pasado en un momento definido (*yesterday, last week, in 2024*).

1. **Verbos Regulares:** Solo les agregas **-ed**:
   * *watch* ➔ *watched*
   * *play* ➔ *played*
   * *visit* ➔ *visited*

2. **Verbos Irregulares (Los 6 más importantes para memorizar):**
   * *go* ➔ **went** (ir)
   * *see* ➔ **saw** (ver)
   * *have* ➔ **had** (tener)
   * *eat* ➔ **ate** (comer)
   * *buy* ➔ **bought** (comprar)
   * *make* ➔ **made** (hacer)

3. **Negación y Preguntas con DID:**
   * *I didn't go to work yesterday.* (El verbo vuelve a 'go' porque ya está 'didn't').
   * *Did you watch the movie?*
                """,
                "formula": "Afirmativo: Sujeto + Verbo en Pasado | Negativo: Sujeto + didn't + Verbo base",
                "examples": [
                    {
                        "en": "Yesterday, we went to a cozy coffee shop and ate delicious pizza.",
                        "es": "Ayer fuimos a un café acogedor y comimos pizza deliciosa.",
                        "phonetic_es": "Iésterdei, ui uént tu e kóusi kófi shop end éit delíshos pítsa.",
                        "words": [
                            {"w": "Yesterday,", "t": "Ayer,"},
                            {"w": "we", "t": "nosotros"},
                            {"w": "went", "t": "fuimos (pasado de go)"},
                            {"w": "to", "t": "a"},
                            {"w": "a", "t": "un"},
                            {"w": "cozy", "t": "acogedor / cálido"},
                            {"w": "coffee", "t": "café"},
                            {"w": "shop", "t": "tienda (cafetería)"},
                            {"w": "and", "t": "y"},
                            {"w": "ate", "t": "comimos (pasado de eat)"},
                            {"w": "delicious", "t": "deliciosa"},
                            {"w": "pizza.", "t": "pizza."}
                        ]
                    },
                    {
                        "en": "She didn't sleep well last night.",
                        "es": "Ella no durmió bien anoche.",
                        "phonetic_es": "Shi dídent slip uél last náit.",
                        "words": [
                            {"w": "She", "t": "Ella"},
                            {"w": "didn't", "t": "no (pasado)"},
                            {"w": "sleep", "t": "durmió"},
                            {"w": "well", "t": "bien"},
                            {"w": "last", "t": "la pasada"},
                            {"w": "night.", "t": "noche (anoche)."}
                        ]
                    },
                    {
                        "en": "Did you study with the app yesterday?",
                        "es": "¿Estudiaste con la app ayer?",
                        "phonetic_es": "Did iu stádi uid de ap iésterdei?",
                        "words": [
                            {"w": "Did", "t": "¿(auxiliar pasado)?"},
                            {"w": "you", "t": "tú"},
                            {"w": "study", "t": "estudiaste"},
                            {"w": "with", "t": "con"},
                            {"w": "the", "t": "la"},
                            {"w": "app", "t": "aplicación"},
                            {"w": "yesterday?", "t": "ayer?"}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "Yesterday I didn't went to the gym.",
                    "right": "Yesterday I didn't go to the gym.",
                    "why": "El auxiliar 'didn't' ya indica pasado; el verbo que le sigue debe estar en infinitivo (go)."
                },
                "quiz": {
                    "question": "¿Cómo se dice 'El fin de semana pasado compré un libro y vi una serie'?",
                    "options": [
                        "Last weekend I buyed a book and saw a series.",
                        "Last weekend I bought a book and saw a series.",
                        "Last weekend I bought a book and seed a series."
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Excelente! 'Buy' es irregular ('bought') y 'see' también ('saw')."
                },
                "practice_challenge": "Escribe un párrafo de 3 a 4 oraciones contando qué hiciste el sábado o domingo pasado."
            },
            {
                "id": "A2.2",
                "title": "El Futuro: 'Going to' (Planes) vs 'Will' (Espontáneo)",
                "sublevel": "A2.2 - El Futuro",
                "objective": "Hablar de tus planes futuros, viajes y decisiones.",
                "explanation_es": """
Hay dos formas principales de hablar del futuro en inglés:

1. **Be Going To (Planes decididos con anticipación):**
   Úsalo cuando ya lo planeaste o compraste los boletos.
   * *I am going to travel to Spain in December.* (Ya tengo el plan).
   * *We are going to watch a movie tonight.*

2. **Will (Decisiones espontáneas en el momento o promesas):**
   Úsalo cuando decides algo justo en el instante en que hablas.
   * *Wait, I will open the door for you!* (Lo decidiste en el segundo).
   * *I will always love you.* (Promesa).
                """,
                "formula": "Going to: Sujeto + am/is/are + going to + verbo | Will: Sujeto + will + verbo",
                "examples": [
                    {
                        "en": "Tania and Anderson are going to travel abroad next year.",
                        "es": "Tania y Anderson van a viajar al extranjero el próximo año.",
                        "phonetic_es": "Tania end Ánderson ar góing tu trável ebród nekst íir.",
                        "words": [
                            {"w": "Tania", "t": "Tania"},
                            {"w": "and", "t": "y"},
                            {"w": "Anderson", "t": "Anderson"},
                            {"w": "are", "t": "están"},
                            {"w": "going", "t": "yendo"},
                            {"w": "to", "t": "a (are going to = van a)"},
                            {"w": "travel", "t": "viajar"},
                            {"w": "abroad", "t": "al extranjero"},
                            {"w": "next", "t": "próximo"},
                            {"w": "year.", "t": "año."}
                        ]
                    },
                    {
                        "en": "Don't worry, I will help you with your English practice!",
                        "es": "¡No te preocupes, yo te ayudaré con tu práctica de inglés!",
                        "phonetic_es": "Dóunt uórri, ai uil jelp iu uid ior ínglish práktis!",
                        "words": [
                            {"w": "Don't", "t": "No"},
                            {"w": "worry,", "t": "te preocupes,"},
                            {"w": "I", "t": "yo"},
                            {"w": "will", "t": "(futuro: -ré)"},
                            {"w": "help", "t": "ayudaré"},
                            {"w": "you", "t": "a ti"},
                            {"w": "with", "t": "con"},
                            {"w": "your", "t": "tu"},
                            {"w": "English", "t": "inglés"},
                            {"w": "practice!", "t": "práctica!"}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "I will travel tomorrow because I bought the ticket last month.",
                    "right": "I am going to travel tomorrow because I bought the ticket last month.",
                    "why": "Si ya compraste el boleto con anticipación, es un plan cerrado, se usa 'going to'."
                },
                "quiz": {
                    "question": "El mozo te pregunta qué deseas ordenar. Dices: '___ the pasta, please.'",
                    "options": [
                        "I am going to have",
                        "I will have",
                        "I have"
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Correcto! En restaurantes se usa 'I will have' (o 'I'll have') porque es la fórmula estándar de decisión de pedido."
                },
                "practice_challenge": "Cuéntame 2 cosas que vas a hacer este fin de semana ('I am going to...') y una promesa ('I will...')."
            }
        ]
    },
    "A2_B1": {
        "title": "Nivel A2 ➔ B1: Fluidez Intermedia, Experiencias & Opiniones",
        "description": "El salto más importante: pasa de decir frases sueltas a conectar ideas, contar historias y dar tu punto de vista.",
        "badge_color": "#3b82f6",
        "lessons": [
            {
                "id": "B1.1",
                "title": "Presente Perfecto: Experiencias de Vida (Have / Has + Participio)",
                "sublevel": "B1.1 - Experiencias",
                "objective": "Hablar de cosas que has hecho o no has hecho en tu vida, sin importar la fecha exacta.",
                "explanation_es": """
El **Present Perfect** es el tiempo verbal estrella para conectar el pasado con el presente.
Lo usamos para hablar de **experiencias de vida** cuando el momento exacto no importa, o para acciones que empezaron antes y siguen vivas.

**Estructura:**
`Sujeto + have / has + Verbo en Participio (3ra columna)`

* Palabras clave:
  * **Ever:** ¿Alguna vez...? (*Have you ever visited London?*)
  * **Never:** Nunca (*I have never eaten sushi.*)
  * **Already:** Ya (*I have already finished my homework.*)
  * **Yet:** Aún / Todavía (en preguntas y negativas: *I haven't called him yet.*)
                """,
                "formula": "Sujeto + have/has + participio pasado",
                "examples": [
                    {
                        "en": "Have you ever traveled to another country?",
                        "es": "¿Alguna vez has viajado a otro país?",
                        "phonetic_es": "Jav iu éver tráveld tu anóder kántri?",
                        "words": [
                            {"w": "Have", "t": "Has"},
                            {"w": "you", "t": "tú"},
                            {"w": "ever", "t": "alguna vez"},
                            {"w": "traveled", "t": "viajado"},
                            {"w": "to", "t": "a"},
                            {"w": "another", "t": "otro"},
                            {"w": "country?", "t": "país?"}
                        ]
                    },
                    {
                        "en": "I have studied English for three months now.",
                        "es": "He estudiado inglés durante tres meses hasta ahora.",
                        "phonetic_es": "Ai jav stádid ínglish for zri monts náu.",
                        "words": [
                            {"w": "I", "t": "Yo"},
                            {"w": "have", "t": "he"},
                            {"w": "studied", "t": "estudiado"},
                            {"w": "English", "t": "inglés"},
                            {"w": "for", "t": "por / durante"},
                            {"w": "three", "t": "tres"},
                            {"w": "months", "t": "meses"},
                            {"w": "now.", "t": "ahora."}
                        ]
                    },
                    {
                        "en": "She hasn't seen that movie yet.",
                        "es": "Ella todavía no ha visto esa película.",
                        "phonetic_es": "Shi jásent sin dat múvi iét.",
                        "words": [
                            {"w": "She", "t": "Ella"},
                            {"w": "hasn't", "t": "no ha"},
                            {"w": "seen", "t": "visto"},
                            {"w": "that", "t": "esa"},
                            {"w": "movie", "t": "película"},
                            {"w": "yet.", "t": "todavía / aún."}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "Did you ever went to New York?",
                    "right": "Have you ever been to New York?",
                    "why": "Para preguntar si alguna vez en tu vida has visitado un lugar, se usa 'Have you ever been to...'."
                },
                "quiz": {
                    "question": "¿Cómo se dice 'Nunca he probado comida tailandesa'?",
                    "options": [
                        "I never tried Thai food in my life.",
                        "I have never tried Thai food.",
                        "I haven't never tried Thai food."
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Exacto! En inglés no se usa doble negación ('haven't never' es incorrecto); se dice 'I have never tried'."
                },
                "practice_challenge": "Escribe 2 cosas que NUNCA has hecho en tu vida ('I have never...') y 1 que YA hiciste ('I have already...')."
            },
            {
                "id": "B1.2",
                "title": "Presente Perfecto vs Pasado Simple (El Gran Dilema)",
                "sublevel": "B1.2 - Precisión",
                "objective": "Saber exactamente cuándo usar Pasado Simple y cuándo Presente Perfecto.",
                "explanation_es": """
Esta es la diferencia que separa a los estudiantes principiantes de los intermedios:

* **Usa Pasado Simple:** Cuando dices **CUÁNDO** ocurrió la acción de forma explícita (ayer, en 2021, el martes pasado, hace 2 horas).
  * *I visited Paris **in 2019**.* (Tiempo cerrado)
* **Usa Presente Perfecto:** Cuando la experiencia cuenta para tu presente y **NO** dices cuándo ocurrió.
  * *I have visited Paris twice.* (En toda mi vida hasta hoy)

💡 **Regla nemotécnica:** Si ves *yesterday, ago, last week, in 2020* ➔ **100% Pasado Simple**.
                """,
                "formula": "Tiempo específico ➔ Past Simple | Tiempo abierto/experiencia ➔ Present Perfect",
                "examples": [
                    {
                        "en": "I lost my keys! I can't enter my home right now.",
                        "es": "¡He perdido mis llaves! No puedo entrar a casa ahora mismo.",
                        "phonetic_es": "Ai lost mai kis! Ai kent énter mai jóum ráit náu.",
                        "words": [
                            {"w": "I", "t": "Yo"},
                            {"w": "lost", "t": "perdí / he perdido"},
                            {"w": "my", "t": "mis"},
                            {"w": "keys!", "t": "llaves!"},
                            {"w": "I", "t": "Yo"},
                            {"w": "can't", "t": "no puedo"},
                            {"w": "enter", "t": "entrar a"},
                            {"w": "my", "t": "mi"},
                            {"w": "home", "t": "casa / hogar"},
                            {"w": "right", "t": "ahora"},
                            {"w": "now.", "t": "mismo."}
                        ]
                    },
                    {
                        "en": "I lost my keys yesterday, but my brother found them.",
                        "es": "Perdí mis llaves ayer, pero mi hermano las encontró.",
                        "phonetic_es": "Ai lost mai kis iésterdei, bat mai bróder fáund dem.",
                        "words": [
                            {"w": "I", "t": "Yo"},
                            {"w": "lost", "t": "perdí"},
                            {"w": "my", "t": "mis"},
                            {"w": "keys", "t": "llaves"},
                            {"w": "yesterday,", "t": "ayer,"},
                            {"w": "but", "t": "pero"},
                            {"w": "my", "t": "mi"},
                            {"w": "brother", "t": "hermano"},
                            {"w": "found", "t": "encontró"},
                            {"w": "them.", "t": "las / a ellas."}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "I have seen him yesterday.",
                    "right": "I saw him yesterday.",
                    "why": "Nunca mezcles 'have + participio' con palabras de tiempo cerrado como 'yesterday'."
                },
                "quiz": {
                    "question": "Elige la opción correcta: 'Two years ago, we ___ to Canada, but we ___ back since then.'",
                    "options": [
                        "have traveled / didn't go",
                        "traveled / haven't gone",
                        "traveled / didn't go"
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Brillante! 'Two years ago' pide Pasado Simple ('traveled'), y 'since then' conecta con el presente ('haven't gone')."
                },
                "practice_challenge": "Cuenta una experiencia genial que tuviste usando Presente Perfecto, y luego da 2 detalles de cuándo fue usando Pasado Simple."
            },
            {
                "id": "B1.3",
                "title": "Condicionales: Tipo 1 (Real) y Tipo 2 (Hipotético / Sueños)",
                "sublevel": "B1.3 - Hipótesis",
                "objective": "Expresar causa y efecto, planes condicionados y sueños imaginarios.",
                "explanation_es": """
1. **Primer Condicional (Situaciones reales y probables):**
   *Estructura:* `If + Presente, Will + Verbo`
   * *If it rains tomorrow, we will stay at home.* (Si llueve mañana, nos quedaremos en casa).
   * *If you practice every day, you will speak English fluently.*

2. **Segundo Condicional (Situaciones imaginarias o irreales):**
   *Estructura:* `If + Pasado, Would + Verbo`
   * *If I had a million dollars, I would buy a house on the beach.* (No tengo un millón, pero si lo tuviera...)
   * *If I were you, I would take that opportunity.* (Nótese que formalmente se dice 'If I were', no 'was').
                """,
                "formula": "Tipo 1: If + present, will + base | Tipo 2: If + past, would + base",
                "examples": [
                    {
                        "en": "If we leave early, we will avoid traffic.",
                        "es": "Si salimos temprano, evitaremos el tráfico.",
                        "phonetic_es": "If ui liv érli, ui uil evóid tráfik.",
                        "words": [
                            {"w": "If", "t": "Si (condición)"},
                            {"w": "we", "t": "nosotros"},
                            {"w": "leave", "t": "salimos / partimos"},
                            {"w": "early,", "t": "temprano,"},
                            {"w": "we", "t": "nosotros"},
                            {"w": "will", "t": "(futuro: -emos)"},
                            {"w": "avoid", "t": "evitaremos"},
                            {"w": "traffic.", "t": "tráfico."}
                        ]
                    },
                    {
                        "en": "If I won the lottery, I would travel around the world with Tania.",
                        "es": "Si ganara la lotería, viajaría por el mundo con Tania.",
                        "phonetic_es": "If ai uón de lóteri, ai uúd trável eráund de uórld uid Tania.",
                        "words": [
                            {"w": "If", "t": "Si"},
                            {"w": "I", "t": "yo"},
                            {"w": "won", "t": "ganara (pasado de win)"},
                            {"w": "the", "t": "la"},
                            {"w": "lottery,", "t": "lotería,"},
                            {"w": "I", "t": "yo"},
                            {"w": "would", "t": "(terminación -ía)"},
                            {"w": "travel", "t": "viajaría"},
                            {"w": "around", "t": "alrededor de"},
                            {"w": "the", "t": "el"},
                            {"w": "world", "t": "mundo"},
                            {"w": "with", "t": "con"},
                            {"w": "Tania.", "t": "Tania."}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "If I will study, I will pass the exam.",
                    "right": "If I study, I will pass the exam.",
                    "why": "En la parte que lleva el 'If', nunca se pone 'will'."
                },
                "quiz": {
                    "question": "¿Cómo se dice correctamente: 'Si tuviera más tiempo libre, aprendería a tocar guitarra'?",
                    "options": [
                        "If I have more free time, I would learn guitar.",
                        "If I had more free time, I would learn to play the guitar.",
                        "If I would have more free time, I will learn guitar."
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Excelente! Es una situación imaginaria (Segundo condicional): 'If I had ..., I would learn...'."
                },
                "practice_challenge": "Completa esta frase con tu propia imaginación: 'If I could have any superpower in the world, I would...'"
            }
        ]
    },
    "B1_B2": {
        "title": "Nivel B1 ➔ B2: Inglés Profesional, Trabajo & Negociación",
        "description": "Adquiere el vocabulario formal, la voz pasiva y la solidez argumentativa necesaria para trabajar o estudiar en el extranjero.",
        "badge_color": "#8b5cf6",
        "lessons": [
            {
                "id": "B2.1",
                "title": "La Voz Pasiva en el Entorno Laboral y Científico",
                "sublevel": "B2.1 - Formalidad",
                "objective": "Describir procesos, noticias y resultados donde el foco está en la acción y no en quién la hizo.",
                "explanation_es": """
En inglés profesional y científico, la **Voz Pasiva** es fundamental porque transmite objetividad y elegancia.

* **Activa:** *The team completed the project on time.* (El equipo completó el proyecto a tiempo).
* **Pasiva:** *The project was completed on time.* (El proyecto fue completado a tiempo).

**Estructura:**
`Objeto + Verbo To Be (en el tiempo adecuado) + Participio Pasado`

* Presente: *English **is spoken** worldwide.*
* Pasado: *The discovery **was published** yesterday.*
* Presente Perfecto: *A new solution **has been found**.*
                """,
                "formula": "Sujeto receptor + to be + participio pasado (+ by agente)",
                "examples": [
                    {
                        "en": "The experimental protocol was modified to reduce measurement errors.",
                        "es": "El protocolo experimental fue modificado para reducir errores de medición.",
                        "phonetic_es": "De eksperiméntal prótokol uós módifaid tu rediús mésherment érrors.",
                        "words": [
                            {"w": "The", "t": "El"},
                            {"w": "experimental", "t": "experimental"},
                            {"w": "protocol", "t": "protocolo"},
                            {"w": "was", "t": "fue"},
                            {"w": "modified", "t": "modificado"},
                            {"w": "to", "t": "para"},
                            {"w": "reduce", "t": "reducir"},
                            {"w": "measurement", "t": "de medición"},
                            {"w": "errors.", "t": "errores."}
                        ]
                    },
                    {
                        "en": "Our new website has been launched successfully.",
                        "es": "Nuestro nuevo sitio web ha sido lanzado exitosamente.",
                        "phonetic_es": "Áur niu uébsait jas bin lóncht saksésfuli.",
                        "words": [
                            {"w": "Our", "t": "Nuestro"},
                            {"w": "new", "t": "nuevo"},
                            {"w": "website", "t": "sitio web"},
                            {"w": "has", "t": "ha"},
                            {"w": "been", "t": "sido"},
                            {"w": "launched", "t": "lanzado"},
                            {"w": "successfully.", "t": "exitosamente."}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "The emails was sent this morning.",
                    "right": "The emails were sent this morning.",
                    "why": "Recuerda concordar el verbo 'to be' con el número de elementos (emails = plural ➔ were)."
                },
                "quiz": {
                    "question": "Transforma a pasiva: 'They discovered a new particle in 2024.'",
                    "options": [
                        "A new particle has discovered in 2024.",
                        "A new particle was discovered in 2024.",
                        "A new particle were discovered in 2024."
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Muy bien! Singular en pasado: 'was discovered'."
                },
                "practice_challenge": "Describe un logro en tu trabajo o estudio usando la voz pasiva (ej. 'A new project was developed...')."
            },
            {
                "id": "B2.2",
                "title": "Tercer Condicional: Arrepentimientos y Lecciones Pasadas",
                "sublevel": "B2.2 - Argumentación",
                "objective": "Hablar de cosas que pudieron haber pasado en el pasado pero no sucedieron.",
                "explanation_es": """
El **Third Conditional** analiza hipótesis imposibles porque el pasado ya no se puede cambiar:
`If + Past Perfect (had + participio), would have + participio`

* *If I had studied more, I would have passed the test.* (No estudié suficiente y no aprobé, pero si lo hubiera hecho...)
* *If we had left earlier, we wouldn't have missed the flight.*
                """,
                "formula": "If + had + participio, would have + participio",
                "examples": [
                    {
                        "en": "If I had known about this application earlier, I would have practiced much more.",
                        "es": "Si hubiera sabido de esta aplicación antes, habría practicado mucho más.",
                        "phonetic_es": "If ai jad nóun ebáut dis aplikéishon érli-er, ai uúd jav práktist mach mor.",
                        "words": [
                            {"w": "If", "t": "Si"},
                            {"w": "I", "t": "yo"},
                            {"w": "had", "t": "hubiera"},
                            {"w": "known", "t": "sabido"},
                            {"w": "about", "t": "sobre / de"},
                            {"w": "this", "t": "esta"},
                            {"w": "application", "t": "aplicación"},
                            {"w": "earlier,", "t": "antes / más temprano,"},
                            {"w": "I", "t": "yo"},
                            {"w": "would", "t": "habría"},
                            {"w": "have", "t": "habría"},
                            {"w": "practiced", "t": "practicado"},
                            {"w": "much", "t": "mucho"},
                            {"w": "more.", "t": "más."}
                        ]
                    },
                    {
                        "en": "She wouldn't have gotten lost if she had checked Google Maps.",
                        "es": "Ella no se habría perdido si hubiera mirado Google Maps.",
                        "phonetic_es": "Shi uúdent jav góten lost if shi jad chekt Gúgel Maps.",
                        "words": [
                            {"w": "She", "t": "Ella"},
                            {"w": "wouldn't", "t": "no habría"},
                            {"w": "have", "t": "(have gotten lost = perdido)"},
                            {"w": "gotten", "t": "llegado a estar"},
                            {"w": "lost", "t": "perdida"},
                            {"w": "if", "t": "si"},
                            {"w": "she", "t": "ella"},
                            {"w": "had", "t": "hubiera"},
                            {"w": "checked", "t": "revisado / verificado"},
                            {"w": "Google", "t": "Google"},
                            {"w": "Maps.", "t": "Maps."}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "If I would have known, I would have told you.",
                    "right": "If I had known, I would have told you.",
                    "why": "Nunca uses 'would have' en la cláusula del 'If'."
                },
                "quiz": {
                    "question": "Completa: 'If Anderson ___ that paper earlier, his experiment ___ faster.'",
                    "options": [
                        "had read / would have finished",
                        "readed / would finish",
                        "would have read / had finished"
                    ],
                    "answer_idx": 0,
                    "feedback": "¡Exacto! 'If had read ..., would have finished'."
                },
                "practice_challenge": "Escribe una oración sobre alguna decisión pasada usando 'If I had..., I would have...'."
            }
        ]
    },
    "B2_C1": {
        "title": "Nivel B2 ➔ C1: Dominio Académico, IELTS 8.0+ & Publicaciones STEM",
        "description": "Estructuras complejas, inversión sintáctica, atenuación científica (hedging) y ensayos de alto impacto.",
        "badge_color": "#ec4899",
        "lessons": [
            {
                "id": "C1.1",
                "title": "Inversión Sintáctica para Énfasis Académico",
                "sublevel": "C1.1 - Estilo Avanzado",
                "objective": "Escribir oraciones sofisticadas donde el orden de palabras se invierte para generar impacto retórico.",
                "explanation_es": """
Los examinadores del IELTS y revisores de papers aman la **Inversión Sintáctica**. Ocurre cuando inicias una oración con un adverbio negativo o restrictivo. En ese momento, **el auxiliar pasa antes del sujeto**, como si fuera una pregunta, pero con tono de afirmación formal.

* **Normal:** *The experiment not only confirmed the hypothesis, but it also revealed new phenomena.*
* **C1 Inversión:** **Not only did the experiment confirm** *the hypothesis, but it also revealed new phenomena.*

**Estructuras típicas:**
* **Not only did/does... but also...** (No solo... sino también...)
* **Rarely have I seen...** (Raras veces he visto...)
* **Under no circumstances should...** (Bajo ninguna circunstancia se debe...)
* **Hardly had we begun when...** (Apenas habíamos comenzado cuando...)
                """,
                "formula": "Adverbio negativo + Auxiliar + Sujeto + Verbo principal + Resto",
                "examples": [
                    {
                        "en": "Not only does quantum entanglement challenge classical physics, but it also enables quantum cryptography.",
                        "es": "El entrelazamiento cuántico no solo desafía la física clásica, sino que también posibilita la criptografía cuántica.",
                        "phonetic_es": "Not óunli das kuántom entánguelment chálench klásikal físiks, bat it ólsou enéibels kuántom kriptógrafi.",
                        "words": [
                            {"w": "Not", "t": "No"},
                            {"w": "only", "t": "solamente"},
                            {"w": "does", "t": "(auxiliar de inversión)"},
                            {"w": "quantum", "t": "cuántico"},
                            {"w": "entanglement", "t": "entrelazamiento"},
                            {"w": "challenge", "t": "desafía"},
                            {"w": "classical", "t": "clásica"},
                            {"w": "physics,", "t": "física,"},
                            {"w": "but", "t": "pero / sino que"},
                            {"w": "it", "t": "ello / esto"},
                            {"w": "also", "t": "también"},
                            {"w": "enables", "t": "habilita / posibilita"},
                            {"w": "quantum", "t": "cuántica"},
                            {"w": "cryptography.", "t": "criptografía."}
                        ]
                    },
                    {
                        "en": "Seldom have researchers observed such anomalous behavior in superconducting materials.",
                        "es": "Raras veces los investigadores han observado un comportamiento tan anómalo en materiales superconductores.",
                        "phonetic_es": "Séldom jav risérchers obsérvd sach anómalos bijéivior in súperkondákting matírials.",
                        "words": [
                            {"w": "Seldom", "t": "Raras veces / Pocas veces"},
                            {"w": "have", "t": "han (inversión)"},
                            {"w": "researchers", "t": "investigadores"},
                            {"w": "observed", "t": "observado"},
                            {"w": "such", "t": "tal / tan"},
                            {"w": "anomalous", "t": "anómalo / inusual"},
                            {"w": "behavior", "t": "comportamiento"},
                            {"w": "in", "t": "en"},
                            {"w": "superconducting", "t": "superconductores"},
                            {"w": "materials.", "t": "materiales."}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "Not only the experiment confirmed, but also...",
                    "right": "Not only did the experiment confirm, but also...",
                    "why": "Al iniciar con 'Not only', la inversión con el auxiliar 'did' es gramaticalmente obligatoria en registro formal."
                },
                "quiz": {
                    "question": "¿Cuál de las siguientes oraciones utiliza correctamente la inversión sintáctica?",
                    "options": [
                        "Under no circumstances you should share your confidential password.",
                        "Under no circumstances should you share your confidential password.",
                        "Under no circumstances you must share your confidential password."
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Impecable! 'Under no circumstances should you...' coloca el modal 'should' antes del sujeto 'you'."
                },
                "practice_challenge": "Reescribe esta frase usando inversión con 'Not only did': 'The research solved the equation and it provided empirical verification.'"
            },
            {
                "id": "C1.2",
                "title": "Atenuación Científica (Hedging) y Discurso Académico",
                "sublevel": "C1.2 - Rigor Científico",
                "objective": "Expresar conclusiones sin sonar arrogante ni dogmático, utilizando lenguaje probabilístico formal.",
                "explanation_es": """
En las publicaciones científicas y en el IELTS Task 2, hacer afirmaciones absolutas como *'This proves that X is true'* suele ser penalizado porque la ciencia trabaja con modelos probabilísticos.

El **Hedging** consiste en suavizar las afirmaciones con elegancia:
* En vez de *'This proves'*, usa: **'The empirical findings appear to substantiate...'** o **'These results strongly suggest that...'**
* En vez de *'It is impossible'*, usa: **'It appears improbable that...'**
* En vez de *'Always'*, usa: **'Tends to occur predominantly under conditions of...'**
                """,
                "formula": "Sujeto + appears to / tends to / suggests that + verbo",
                "examples": [
                    {
                        "en": "The preliminary data appear to indicate a non-negligible correlation between temperature and dissipation rates.",
                        "es": "Los datos preliminares parecen indicar una correlación no despreciable entre la temperatura y las tasas de disipación.",
                        "phonetic_es": "De prilíminari déita apíir tu índikeit e non-néglidjibel korreléishon bituín témprecher end disipéishon réits.",
                        "words": [
                            {"w": "The", "t": "Los"},
                            {"w": "preliminary", "t": "preliminares"},
                            {"w": "data", "t": "datos"},
                            {"w": "appear", "t": "parecen"},
                            {"w": "to", "t": "a"},
                            {"w": "indicate", "t": "indicar"},
                            {"w": "a", "t": "una"},
                            {"w": "non-negligible", "t": "no despreciable (significativa)"},
                            {"w": "correlation", "t": "correlación"},
                            {"w": "between", "t": "entre"},
                            {"w": "temperature", "t": "temperatura"},
                            {"w": "and", "t": "y"},
                            {"w": "dissipation", "t": "disipación"},
                            {"w": "rates.", "t": "tasas / ritmos."}
                        ]
                    },
                    {
                        "en": "It is widely acknowledged that peer review, whilst imperfect, remains indispensable.",
                        "es": "Es ampliamente reconocido que la revisión por pares, si bien imperfecta, sigue siendo indispensable.",
                        "phonetic_es": "It is uáidli aknóledcht dat píir reviu, uáilst impérfekt, riméins indispénsabel.",
                        "words": [
                            {"w": "It", "t": "(Sujeto formal)"},
                            {"w": "is", "t": "es"},
                            {"w": "widely", "t": "ampliamente"},
                            {"w": "acknowledged", "t": "reconocido / aceptado"},
                            {"w": "that", "t": "que"},
                            {"w": "peer", "t": "pares (iguales)"},
                            {"w": "review,", "t": "revisión,"},
                            {"w": "whilst", "t": "si bien / mientras que"},
                            {"w": "imperfect,", "t": "imperfecta,"},
                            {"w": "remains", "t": "sigue siendo / permanece"},
                            {"w": "indispensable.", "t": "indispensable."}
                        ]
                    }
                ],
                "common_mistake": {
                    "wrong": "This experiment proves 100% that Einstein was right.",
                    "right": "These experimental findings provide robust empirical support for Einstein's general theory of relativity.",
                    "why": "El registro académico C1 evita afirmaciones dogmáticas simplistas."
                },
                "quiz": {
                    "question": "¿Cuál frase demuestra el mejor nivel de 'hedging' académico?",
                    "options": [
                        "This definitively proves the hypothesis without any doubt.",
                        "The evidence suggests that the observed phenomenon may be attributed to thermal fluctuations.",
                        "Obviously, this is the only correct explanation."
                    ],
                    "answer_idx": 1,
                    "feedback": "¡Excelente! 'The evidence suggests that ... may be attributed to...' es el estándar de oro en artículos de investigación."
                },
                "practice_challenge": "Toma una opinión científica o técnica personal y redáctala en 2 oraciones usando atenuación académica formal."
            }
        ]
    }
}
