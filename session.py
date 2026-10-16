import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Asegurar codificación UTF-8 en consola de Windows
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

load_dotenv()

TRACKER_FILE = os.path.join("logs", "time_tracker.json")
TARGET_HOURS = float(os.getenv("TARGET_HOURS", 700.0))

# Fases del Plan Maestro
PHASES = [
    {
        "phase": 1,
        "name": "Fase 1: Cimientos y Fluidez Base (A2 ➔ B1)",
        "min_h": 0.0,
        "max_h": 180.0,
        "focus": "English Grammar in Use, Shadowing, BBC 6-Minute, Anki base"
    },
    {
        "phase": 2,
        "name": "Fase 2: Transición STEM & Vocabulario (B1 ➔ B2)",
        "min_h": 180.0,
        "max_h": 400.0,
        "focus": "Academic Word List (570), Physics World, Gráficos IELTS Task 1, método PEEL"
    },
    {
        "phase": 3,
        "name": "Fase 3: Consolidación C1 (B2 ➔ C1)",
        "min_h": 400.0,
        "max_h": 650.0,
        "focus": "Papers arXiv, conferencias Perimeter/MIT, inversión sintáctica, ensayos complejos"
    },
    {
        "phase": 4,
        "name": "Fase 4: Técnica de Examen & Simulacros Oficiales",
        "min_h": 650.0,
        "max_h": 750.0,
        "focus": "Cambridge IELTS 15-19, tiempos estrictos, simulacros semanales"
    }
]

def load_tracker_data() -> dict:
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(TRACKER_FILE):
        initial = {
            "target_hours": TARGET_HOURS,
            "total_minutes": 0.0,
            "total_hours": 0.0,
            "sessions": []
        }
        save_tracker_data(initial)
        return initial
        
    try:
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Asegurar consistencia
            total_min = sum(s.get("minutes", 0) for s in data.get("sessions", []))
            data["total_minutes"] = total_min
            data["total_hours"] = round(total_min / 60.0, 2)
            data["target_hours"] = TARGET_HOURS
            return data
    except (json.JSONDecodeError, OSError):
        return {
            "target_hours": TARGET_HOURS,
            "total_minutes": 0.0,
            "total_hours": 0.0,
            "sessions": []
        }

def save_tracker_data(data: dict):
    os.makedirs("logs", exist_ok=True)
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_current_phase(total_hours: float) -> dict:
    for p in PHASES:
        if p["min_h"] <= total_hours < p["max_h"]:
            return p
    return PHASES[-1]

def render_progress_bar(current: float, total: float, width: int = 30) -> str:
    ratio = min(max(current / total, 0.0), 1.0)
    filled = int(width * ratio)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    pct = ratio * 100.0
    return f"[{bar}] {current:.1f} / {total:.0f} h ({pct:.1f}%)"

def print_header(data: dict):
    total_h = data.get("total_hours", 0.0)
    phase = get_current_phase(total_h)
    
    print("\n" + "=" * 65)
    print("🚀  ENGLISH C1 ACCELERATOR • CENTRO DE CONTROL DIARIO")
    print("=" * 65)
    print(f"🎯 Meta General:        {TARGET_HOURS:.0f} Horas de Práctica Deliberada")
    print(f"📊 Progreso Total:       {render_progress_bar(total_h, TARGET_HOURS)}")
    print(f"📍 Fase Actual:          {phase['name']}")
    print(f"💡 Foco Pedagógico:      {phase['focus']}")
    
    sessions = data.get("sessions", [])
    if sessions:
        last = sessions[-1]
        print(f"🕒 Última Sesión:       {last.get('timestamp', '')[:10]} | {last.get('minutes', 0)} min ({last.get('category', 'general')})")
    print("=" * 65)

def run_timer(minutes: int, block_name: str) -> int:
    """Ejecuta un cronómetro en consola. Permite cancelar con Ctrl+C y registrar minutos reales."""
    total_sec = int(minutes * 60)
    print(f"\n⏳ Iniciando bloque: {block_name} ({minutes} minutos)")
    print("   [Presiona Ctrl+C en cualquier momento para terminar antes y guardar]")
    
    start_time = time.time()
    try:
        for remaining in range(total_sec, 0, -1):
            mins, secs = divmod(remaining, 60)
            elapsed_m, elapsed_s = divmod(int(time.time() - start_time), 60)
            print(f"\r⏱️  Restante: {mins:02d}:{secs:02d} | Transcurrido: {elapsed_m:02d}:{elapsed_s:02d} ", end="", flush=True)
            time.sleep(1)
        print("\n\n🔔 ¡TIEMPO COMPLETADO! Excelente trabajo.")
        return minutes
    except KeyboardInterrupt:
        elapsed_seconds = time.time() - start_time
        elapsed_minutes = round(elapsed_seconds / 60.0, 1)
        print(f"\n\n⏸️  Bloque detenido. Tiempo transcurrido: {elapsed_minutes} minutos.")
        confirm = input(f"¿Deseas registrar estos {elapsed_minutes} min en tu progreso? [S/n]: ").strip().lower()
        if confirm in ("", "s", "si", "y", "yes"):
            return int(round(elapsed_minutes))
        return 0

def log_session(minutes: int, category: str, description: str, notes: str = ""):
    if minutes <= 0:
        return
    data = load_tracker_data()
    try:
        from users_manager import get_user_now
        now_iso = get_user_now().isoformat()
    except Exception:
        now_iso = datetime.now().isoformat()
    entry = {
        "timestamp": now_iso,
        "minutes": minutes,
        "category": category,
        "description": description,
        "notes": notes
    }
    data["sessions"].append(entry)
    data["total_minutes"] = sum(s.get("minutes", 0) for s in data["sessions"])
    data["total_hours"] = round(data["total_minutes"] / 60.0, 2)
    save_tracker_data(data)
    print(f"✅ ¡Registrados exitosamente {minutes} minutos en tu historial!")
    
    # Sincronización automática con Google Sheets
    try:
        from scripts.sheets_sync import sync_study_session
        ok = sync_study_session(entry["timestamp"][:16].replace("T", " "), minutes, data["total_hours"], category, description, notes)
        if ok:
            print("📊 Sincronizado automáticamente con tu Google Sheet.")
    except Exception:
        pass

def launch_evaluator():
    print("\n" + "-" * 50)
    print("🤖 Abriendo Evaluador IELTS / C1 (Gemini)...")
    print("-" * 50)
    try:
        from evaluator import evaluate_submission, print_report, get_input_text
        task_type = input("Tipo de ejercicio ([w]riting / [s]peaking): ").strip().lower()
        t_type = "writing" if task_type.startswith("w") else "speaking"
        
        user_text = get_input_text()
        if user_text:
            print("\nEvaluando con Gemini...")
            res = evaluate_submission(t_type, user_text)
            print_report(res)
        else:
            print("Entrada vacía. Operación cancelada.")
    except Exception as e:
        print(f"❌ Error al ejecutar el evaluador: {e}")

def manual_log_menu():
    print("\n📝 REGISTRO MANUAL DE ESTUDIO")
    print("Ingresa los minutos estudiados fuera del cronómetro (ej. Anki en móvil, lectura física):")
    try:
        mins_str = input("Minutos: ").strip()
        mins = int(mins_str)
        if mins <= 0:
            print("Cantidad no válida.")
            return
    except ValueError:
        print("Debes ingresar un número entero.")
        return
        
    print("\nCategoría:")
    print("1. Input & SRS (Anki / Podcast / Lectura)")
    print("2. Output & Producción (Writing / Speaking)")
    print("3. Gramática & Técnica (Murphy / Cambridge)")
    cat_opt = input("Selecciona [1/2/3]: ").strip()
    
    cat_map = {
        "1": "Input & SRS",
        "2": "Output & Producción",
        "3": "Gramática & Técnica"
    }
    category = cat_map.get(cat_opt, "General")
    description = input("Descripción breve (ej. 20 min Anki + Nature Physics): ").strip()
    log_session(mins, category, description)

def view_statistics(data: dict):
    sessions = data.get("sessions", [])
    total_h = data.get("total_hours", 0.0)
    
    print("\n" + "=" * 65)
    print("📈  ESTADÍSTICAS DETALLADAS DE APRENDIZAJE")
    print("=" * 65)
    print(f"Total de Sesiones:      {len(sessions)}")
    print(f"Horas Acumuladas:       {total_h:.2f} h / {TARGET_HOURS:.0f} h")
    print(f"Horas Restantes:        {max(0.0, TARGET_HOURS - total_h):.2f} h")
    
    # Desglose por categoría
    cats = {}
    for s in sessions:
        c = s.get("category", "General")
        cats[c] = cats.get(c, 0) + s.get("minutes", 0)
        
    if cats:
        print("\n📊 Desglose por Categoría:")
        for cat, mins in cats.items():
            print(f"  • {cat:<24}: {mins/60.0:6.1f} h ({mins} min)")
            
    print("\n🕒 Últimas 5 Sesiones:")
    for s in sessions[-5:]:
        ts = s.get("timestamp", "")[:16].replace("T", " ")
        print(f"  [{ts}] {s.get('minutes', 0):3d} min | {s.get('category', ''):<20} | {s.get('description', '')}")
    print("=" * 65)

def run_daily_routine():
    print("\n" + "=" * 65)
    print("🔥 INICIANDO RUTINA DIARIA COMPLETA (2.5 HORAS)")
    print("=" * 65)
    print("La rutina recomendada se divide en 3 bloques deliberados:")
    print("  1. Bloque 1 (45 min): Input & SRS (20 min Anki + 25 min Lectura/Podcast)")
    print("  2. Bloque 2 (60 min): Output & Producción (Redacción / Speaking + Evaluador)")
    print("  3. Bloque 3 (45 min): Gramática o Técnica de Examen")
    print("=" * 65)
    
    # Bloque 1
    input("\nPresiona Enter para comenzar el BLOQUE 1 (Input & SRS - 45 min)...")
    m1 = run_timer(45, "Bloque 1: Input & SRS (Anki + Lectura/Podcast)")
    log_session(m1, "Input & SRS", "Rutina diaria Bloque 1")
    
    # Bloque 2
    input("\nPresiona Enter para comenzar el BLOQUE 2 (Output & Producción - 60 min)...")
    m2 = run_timer(60, "Bloque 2: Output & Producción")
    log_session(m2, "Output & Producción", "Rutina diaria Bloque 2")
    
    opt_eval = input("\n¿Deseas evaluar tu producción de hoy con Gemini ahora mismo? [S/n]: ").strip().lower()
    if opt_eval in ("", "s", "si", "y", "yes"):
        launch_evaluator()
        
    # Bloque 3
    input("\nPresiona Enter para comenzar el BLOQUE 3 (Gramática / Técnica - 45 min)...")
    m3 = run_timer(45, "Bloque 3: Gramática / Técnica")
    log_session(m3, "Gramática & Técnica", "Rutina diaria Bloque 3")
    
    total_day = m1 + m2 + m3
    print(f"\n🎉 ¡Felicidades! Has completado {total_day/60.0:.1f} horas de estudio hoy.")

def run_single_block():
    print("\n⚡ INICIAR BLOQUE INDIVIDUAL")
    print("1. Bloque Input & SRS (45 min)")
    print("2. Bloque Output & Producción (60 min)")
    print("3. Bloque Gramática / Técnica (45 min)")
    print("4. Bloque personalizado (Tú defines los minutos)")
    print("0. Volver")
    
    opt = input("Selecciona [0-4]: ").strip()
    if opt == "1":
        m = run_timer(45, "Input & SRS (Anki / Lectura)")
        log_session(m, "Input & SRS", "Sesión de Input")
    elif opt == "2":
        m = run_timer(60, "Output & Producción")
        log_session(m, "Output & Producción", "Sesión de Output")
        eval_now = input("¿Evaluar texto/audio ahora con Gemini? [S/n]: ").strip().lower()
        if eval_now in ("", "s", "si", "y", "yes"):
            launch_evaluator()
    elif opt == "3":
        m = run_timer(45, "Gramática / Técnica")
        log_session(m, "Gramática & Técnica", "Sesión de Gramática")
    elif opt == "4":
        try:
            custom_m = int(input("¿Cuántos minutos deseas cronometrar?: ").strip())
            desc = input("Nombre de la tarea (ej. Shadowing podcast): ").strip()
            m = run_timer(custom_m, desc or "Sesión personalizada")
            log_session(m, "General", desc or "Personalizada")
        except ValueError:
            print("Número no válido.")

def launch_anki_generator():
    print("\n" + "-" * 50)
    print("📇 GENERADOR DE FLASHCARDS C1 / STEM PARA ANKI")
    print("-" * 50)
    print("Ingresa una palabra, términos separados por comas, o un párrafo de física:")
    terms = input("Término(s) a procesar: ").strip()
    if terms:
        try:
            from scripts.anki_generator import generate_flashcards
            generate_flashcards(terms)
        except Exception as e:
            print(f"❌ Error al generar flashcards: {e}")
    else:
        print("Operación cancelada.")

def main():
    while True:
        data = load_tracker_data()
        print_header(data)
        
        print("\nMENÚ PRINCIPAL:")
        print(" [1] 🚀 Iniciar Rutina Diaria Completa (2.5 h - 3 Bloques)")
        print(" [2] ⚡ Iniciar un Bloque Específico (con temporizador)")
        print(" [3] 📝 Registrar tiempo de estudio manualmente (sin cronómetro)")
        print(" [4] 🤖 Abrir Evaluador IELTS / C1 (Gemini)")
        print(" [5] 📇 Generar Tarjetas para Anki (Gemini + AnkiConnect)")
        print(" [6] 📊 Ver estadísticas y desglose por categorías")
        print(" [0] 🚪 Salir")
        
        choice = input("\nElige una opción [0-6]: ").strip()
        
        if choice == "1":
            run_daily_routine()
        elif choice == "2":
            run_single_block()
        elif choice == "3":
            manual_log_menu()
        elif choice == "4":
            launch_evaluator()
        elif choice == "5":
            launch_anki_generator()
        elif choice == "6":
            view_statistics(data)
        elif choice == "0":
            print("\n¡Nos vemos en la siguiente sesión de estudio! Sigue sumando hacia el C1. 👋\n")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
