import os
import sys
import json
import warnings
from datetime import datetime
from dotenv import load_dotenv

# Evitar advertencias ruidosas en consola
warnings.filterwarnings("ignore", category=FutureWarning)

# Asegurar codificación UTF-8 en la consola de Windows para soporte de emojis y caracteres especiales
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import google.generativeai as genai

# Cargar variables de entorno desde .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "tu_clave_api_aqui":
    print("❌ Error: Falta configurar GEMINI_API_KEY en el archivo .env")
    print("👉 Abre el archivo .env y reemplaza 'tu_clave_api_aqui' por tu clave obtenida en Google AI Studio.")
    sys.exit(1)

# Configuración del modelo Gemini
genai.configure(api_key=api_key)
model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
model = genai.GenerativeModel(model_name)

SYSTEM_PROMPT = """
Eres un examinador senior oficial de IELTS Academic y evaluador de admisiones para posgrados en física en Europa.
Tu estándar de evaluación es riguroso (escala 0.0 a 9.0 con precisión decimal).

Evalúa el texto del estudiante según los 4 criterios oficiales:
1. Task Achievement / Task Response (TR)
2. Coherence and Cohesion (CC)
3. Lexical Resource (LR) - penaliza la falta de vocabulario académico/científico preciso.
4. Grammatical Range and Accuracy (GRA) - evalúa estructuras complejas (inversión, pasivas, condicionales).

Debes devolver ÚNICAMENTE un JSON válido con esta estructura exacta:
{
  "task_response": 0.0,
  "coherence_cohesion": 0.0,
  "lexical_resource": 0.0,
  "grammatical_accuracy": 0.0,
  "overall_band": 0.0,
  "accuracy_percentage": 0.0,
  "cefr_level": "A2|B1|B2|C1",
  "critical_grammar_errors": [
    {"error": "texto erróneo", "fix": "corrección", "rule": "explicación"}
  ],
  "academic_vocab_used": ["palabra 1", "palabra 2"],
  "weak_phrases_to_upgrade": [
    {"original": "frase básica", "c1_alternative": "alternativa académica formal"}
  ],
  "c1_rewrite": "Reescritura completa del texto adaptada a nivel C1 formal para física",
  "next_action_item": "El aspecto prioritario que debe trabajar en la siguiente sesión"
}
"""

def clean_json_text(text: str) -> str:
    """Elimina delimitadores markdown si el modelo los incluye."""
    clean = text.strip()
    if clean.startswith("```json"):
        clean = clean[7:]
    elif clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    return clean.strip()

def evaluate_submission(submission_type: str, text: str):
    prompt = f"{SYSTEM_PROMPT}\n\nTipo de tarea: {submission_type.upper()}\nTexto del estudiante:\n\"\"\"\n{text}\n\"\"\""
    
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    raw_text = clean_json_text(response.text)
    result = json.loads(raw_text)
    
    try:
        from users_manager import get_user_now
        now_iso = get_user_now().isoformat()
    except Exception:
        now_iso = datetime.now().isoformat()

    # Registro local persistente en logs/study_log.json
    log_entry = {
        "timestamp": now_iso,
        "type": submission_type,
        "input_text": text,
        "metrics": result
    }
    
    log_path = os.path.join("logs", "study_log.json")
    os.makedirs("logs", exist_ok=True)
    history = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    
    history.append(log_entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
        
    # Sincronización automática con Google Sheets
    try:
        from scripts.sheets_sync import sync_evaluation_result
        sync_evaluation_result(log_entry["timestamp"][:16].replace("T", " "), submission_type, result)
    except Exception:
        pass

    return result

def print_report(res: dict):
    print("\n" + "="*50)
    print(f"📊 REPORTE DE EVALUACIÓN OFICIAL (Nivel detectado: {res.get('cefr_level', 'N/A')})")
    print("="*50)
    print(f"Banda Global Estimada: {res.get('overall_band', 0.0)} / 9.0")
    acc = res.get('accuracy_percentage', 0.0)
    try:
        print(f"Precisión General:     {float(acc):.1f}%")
    except (ValueError, TypeError):
        print(f"Precisión General:     {acc}")
    print("-" * 50)
    print(f"• Task Response:       {res.get('task_response', 0.0)}")
    print(f"• Coherence/Cohesion:  {res.get('coherence_cohesion', 0.0)}")
    print(f"• Lexical Resource:    {res.get('lexical_resource', 0.0)}")
    print(f"• Grammatical Range:   {res.get('grammatical_accuracy', 0.0)}")
    print("-" * 50)
    
    if res.get("critical_grammar_errors"):
        print("\n❌ ERRORES GRAMATICALES CRÍTICOS:")
        for err in res["critical_grammar_errors"]:
            print(f"  • '{err.get('error', '')}' ➔ '{err.get('fix', '')}' ({err.get('rule', '')})")
            
    if res.get("academic_vocab_used"):
        print("\n📚 VOCABULARIO ACADÉMICO DETECTADO:")
        print("  " + ", ".join(res["academic_vocab_used"]))

    if res.get("weak_phrases_to_upgrade"):
        print("\n💡 MEJORAS DE REGISTRO (A2/B1 ➔ C1):")
        for up in res["weak_phrases_to_upgrade"]:
            print(f"  • '{up.get('original', '')}' ➔ '{up.get('c1_alternative', '')}'")
            
    print("\n📝 REESCRITURA A NIVEL C1:")
    print(res.get("c1_rewrite", "No disponible"))
    print("\n🎯 SIGUIENTE TAREA RECOMENDADA:")
    print(res.get("next_action_item", "Continuar practicando"))
    print("="*50 + "\n")

def get_input_text() -> str:
    print("\nOpciones de entrada:")
    print("1. Pega tu texto (en una o varias líneas). Para finalizar:")
    print("   - En Windows: presiona Enter, luego Ctrl+Z y Enter.")
    print("2. O escribe la ruta de un archivo existente (ej. data/essays/ensayo1.txt) y presiona Enter.\n")
    
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
            
    text = "\n".join(lines).strip()
    
    # Si ingresó una sola línea y corresponde a un archivo existente, leerlo
    if text and "\n" not in text and os.path.isfile(text):
        print(f"📄 Leyendo archivo: {text}")
        with open(text, "r", encoding="utf-8") as f:
            return f.read().strip()
            
    return text

if __name__ == "__main__":
    task_type = input("Tipo de ejercicio ([w]riting / [s]peaking): ").strip().lower()
    t_type = "writing" if task_type.startswith("w") else "speaking"
    
    user_text = get_input_text()
    
    if user_text:
        print(f"\nEvaluando con {model_name} bajo rúbrica IELTS...")
        try:
            eval_result = evaluate_submission(t_type, user_text)
            print_report(eval_result)
        except Exception as e:
            print(f"\n❌ Ocurrió un error durante la evaluación: {e}")
    else:
        print("Entrada vacía. Operación cancelada.")
