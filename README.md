# 🇬🇧 English Together: Anderson & Tania

Aplicación web interactiva y personalizada para que Anderson y Tania aprendan inglés juntos, se motiven mutuamente y midan su progreso en tiempo real con Inteligencia Artificial (**Gemini**).

---

## 🌟 Características Principales

### 1. Dos Rutas de Aprendizaje Personalizadas
* **🔬 Modo Anderson (Física & Academia STEM - Ruta C1):**
  * Meta: 700 horas de práctica deliberada.
  * Estándar riguroso de examinador **IELTS Academic** (evalúa Task Response, Cohesión, Vocabulario Académico y Gramática avanzada).
  * Foco en papers, conferencias, escritura científica y simulacros de examen.
* **✨ Modo Tania (Inglés General, Práctico & Conversacional):**
  * Meta: 200 horas (personalizable).
  * Enfoque en la vida real: viajes, restaurantes, series, trabajo, anécdotas y conversación fluida.
  * Tutora IA empática que explica errores en español sencillo, sugiere cómo diría las cosas un hablante nativo y propone mini-retos motivadores.

### 2. 🔐 Sistema de Usuarios, Jerarquía & Recuperación de Cuentas
* **👑 Administrador (Anderson):** Acceso total al panel de administración, control de configuraciones del sistema, restablecimiento de contraseñas de invitados y gestión de cuentas.
* **💖 Co-administradora (Tania):** Acceso al espacio de estudio, resumen de pareja, personalización de metas y gustos propios.
* **🌟 Invitados / Amigos:** Pueden crear su propia cuenta desde la pantalla principal, elegir su enfoque (Negocios, Viajes, Conversación), registrar sus horas y personalizar sus gustos.
* **🆘 Recuperación de Usuario y Contraseña:** En caso de olvido, cualquier persona puede recuperar su nombre de usuario o restablecer su contraseña respondiendo su **Pregunta Secreta de Seguridad** o usando su **PIN de 4 dígitos**.

### 3. 🎓 Academia de Clases por Niveles (CEFR A1 ➔ C1)
* **A1 ➔ A2 (Cimientos & Rutinas):** Verbo To Be, Presente Simple, Regla de Oro (-s/-es), preguntas con Wh-, Pasado Simple, Futuro con Going to vs Will.
* **A2 ➔ B1 (Experiencias & Fluidez):** Presente Perfecto, Presente Perfecto vs Pasado Simple, Condicionales 1 y 2.
* **B1 ➔ B2 (Profesional & Formal):** Voz Pasiva, Tercer Condicional, modales de deducción, colocaciones profesionales.
* **B2 ➔ C1 (Académico STEM & IELTS 8+):** Inversión sintáctica retórica, atenuación científica (*hedging*), vocabulario AWL.
* Cada clase incluye **teoría en español**, **fórmulas**, **ejemplos bilingües**, **alertas de errores típicos**, **mini-quiz interactivo** y **reto de práctica evaluado por Gemini IA**.

### 4. 💑 Resumen de Pareja (Dashboard Privado)
* Exclusivo para Anderson y Tania: horas acumuladas en equipo, rachas y comparativas.

### 5. ⏱️ Centro de Estudio & Cronómetro
* Cronómetro interactivo por bloques y registro manual rápido.

### 6. 🤖 Evaluador Gemini IA Personalizado
* Generador dinámico de temas según los gustos e intereses de cada usuario (Cine, Tecnología, Viajes, etc.).
* Correcciones instantáneas y explicaciones amigables.

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

## 🌐 Cómo Publicarla en Internet GRATIS para que Tania la Use en su Celular

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
6. ¡Listo! Te dará un enlace web (ejemplo: `https://ingles-pareja.streamlit.app`) que le puedes enviar por WhatsApp a Tania para que lo abra desde su celular.
