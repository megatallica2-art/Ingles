# curriculum_data.py
# Plan de estudios estructurado por niveles y subniveles del Marco Común Europeo (CEFR)

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
                    {"en": "Hello! I am Tania, and I'm very excited to learn English.", "es": "¡Hola! Soy Tania y estoy muy emocionada de aprender inglés."},
                    {"en": "Anderson is a physicist from Colombia.", "es": "Anderson es físico de Colombia."},
                    {"en": "They are in the library studying right now.", "es": "Ellos están en la biblioteca estudiando ahora mismo."}
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
                    {"en": "I wake up at 7:00 AM every morning.", "es": "Me despierto a las 7:00 AM todas las mañanas."},
                    {"en": "Tania drinks green tea while studying.", "es": "Tania toma té verde mientras estudia."},
                    {"en": "He doesn't like waking up early on weekends.", "es": "A él no le gusta despertarse temprano los fines de semana."}
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
                    {"en": "Where do you want to travel next year?", "es": "¿A dónde quieres viajar el próximo año?"},
                    {"en": "Why are you studying English tonight?", "es": "¿Por qué estás estudiando inglés esta noche?"},
                    {"en": "How do you say this in English?", "es": "¿Cómo se dice esto en inglés?"}
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
                    {"en": "Yesterday, we went to a cozy coffee shop and ate delicious pizza.", "es": "Ayer fuimos a un café acogedor y comimos pizza deliciosa."},
                    {"en": "She didn't sleep well last night.", "es": "Ella no durmió bien anoche."},
                    {"en": "Did you study with the app yesterday?", "es": "¿Estudiaste con la app ayer?"}
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
                    {"en": "Tania and Anderson are going to travel abroad next year.", "es": "Tania y Anderson van a viajar al extranjero el próximo año."},
                    {"en": "Don't worry, I will help you with your English practice!", "es": "¡No te preocupes, yo te ayudaré con tu práctica de inglés!"}
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
                    {"en": "Have you ever traveled to another country?", "es": "¿Alguna vez has viajado a otro país?"},
                    {"en": "I have studied English for three months now.", "es": "He estudiado inglés durante tres meses hasta ahora."},
                    {"en": "She hasn't seen that movie yet.", "es": "Ella todavía no ha visto esa película."}
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
                    {"en": "I lost my keys! I can't enter my home right now.", "es": "¡He perdido mis llaves! No puedo entrar a casa ahora mismo."},
                    {"en": "I lost my keys yesterday, but my brother found them.", "es": "Perdí mis llaves ayer, pero mi hermano las encontró."}
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
                    {"en": "If we leave early, we will avoid traffic.", "es": "Si salimos temprano, evitaremos el tráfico."},
                    {"en": "If I won the lottery, I would travel around the world with Tania.", "es": "Si ganara la lotería, viajaría por el mundo con Tania."}
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
                    {"en": "The experimental protocol was modified to reduce measurement errors.", "es": "El protocolo experimental fue modificado para reducir errores de medición."},
                    {"en": "Our new website has been launched successfully.", "es": "Nuestro nuevo sitio web ha sido lanzado exitosamente."}
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
                    {"en": "If I had known about this application earlier, I would have practiced much more.", "es": "Si hubiera sabido de esta aplicación antes, habría practicado mucho más."},
                    {"en": "She wouldn't have gotten lost if she had checked Google Maps.", "es": "Ella no se habría perdido si hubiera mirado Google Maps."}
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
                    {"en": "Not only does quantum entanglement challenge classical physics, but it also enables quantum cryptography.", "es": "El entrelazamiento cuántico no solo desafía la física clásica, sino que también posibilita la criptografía cuántica."},
                    {"en": "Seldom have researchers observed such anomalous behavior in superconducting materials.", "es": "Raras veces los investigadores han observado un comportamiento tan anómalo en materiales superconductores."}
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
                    {"en": "The preliminary data appear to indicate a non-negligible correlation between temperature and dissipation rates.", "es": "Los datos preliminares parecen indicar una correlación no despreciable entre la temperatura y las tasas de disipación."},
                    {"en": "It is widely acknowledged that peer review, whilst imperfect, remains indispensable.", "es": "Es ampliamente reconocido que la revisión por pares, si bien imperfecta, sigue siendo indispensable."}
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
