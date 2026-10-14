# 🇬🇧 English Together: Anderson & Su Novia

Aplicación web interactiva y personalizada para que tú y tu novia aprendan inglés juntos, se motiven mutuamente y midan su progreso en tiempo real con Inteligencia Artificial (**Gemini**).

---

## 🌟 Características Principales

### 1. Dos Rutas de Aprendizaje Personalizadas
* **🔬 Modo Anderson (Física & Academia STEM - Ruta C1):**
  * Meta: 700 horas de práctica deliberada.
  * Estándar riguroso de examinador **IELTS Academic** (evalúa Task Response, Cohesión, Vocabulario Académico y Gramática avanzada).
  * Foco en papers, conferencias, escritura científica y simulacros de examen.
* **✨ Modo Novia (Inglés General, Práctico & Conversacional):**
  * Meta: 200 horas (personalizable).
  * Enfoque en la vida real: viajes, restaurantes, series, trabajo, anécdotas y conversación fluida.
  * Tutora IA empática que explica errores en español sencillo, sugiere cómo diría las cosas un hablante nativo y propone mini-retos motivadores.

### 2. 💑 Resumen de Pareja (Dashboard)
* Horas acumuladas en equipo.
* Racha de días seguidos de estudio (streaks 🔥).
* Gráfica comparativa de los últimos 7 días.
* Seguimiento de fases de aprendizaje para cada uno.

### 3. ⏱️ Centro de Estudio & Cronómetro
* Cronómetro interactivo por bloques (Pomodoro 20, 25, 45 min).
* Registro manual rápido de minutos para estudios en el celular (podcasts, YouTube, Duolingo, lectura).

### 4. 🤖 Evaluador Inteligente Gemini
* Corrige textos de Writing o transcripciones de Speaking al instante.
* Detecta errores gramaticales con explicaciones amigables.
* Reescribe tu texto completo en una versión limpia y elegante.

---

## 🚀 Cómo Iniciar la App en tu Computador

Solo tienes que hacer doble clic en el archivo:
```bash
iniciar_app.bat
```
O desde la terminal:
```bash
.\venv\Scripts\activate
streamlit run app.py
```
Se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## 🌐 Cómo Publicarla en Internet GRATIS para que tu Novia la Use en su Celular

1. **Sube este proyecto a tu GitHub** (repositorio privado o público).
2. Entra a **[share.streamlit.io](https://share.streamlit.io/)** e inicia sesión con GitHub.
3. Haz clic en **"New app"**:
   * Repositorio: tu repositorio de GitHub
   * Main file path: `app.py`
4. En **Advanced settings ➔ Secrets**, pega tu clave:
   ```toml
   GEMINI_API_KEY = "tu_clave_aquí"
   ```
5. Haz clic en **Deploy**.
6. ¡Listo! Te dará un enlace web (ejemplo: `https://ingles-pareja.streamlit.app`) que le puedes enviar por WhatsApp a tu novia para que lo abra desde su celular.
