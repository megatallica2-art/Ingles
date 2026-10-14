import os
import sys
import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()
WEBHOOK_URL = os.getenv("GOOGLE_SHEETS_WEBHOOK_URL")

def send_to_google_sheets(payload: dict) -> bool:
    """Envía un registro en formato JSON a la aplicación web de Google Sheets."""
    if not WEBHOOK_URL or "macros/s/" not in WEBHOOK_URL:
        return False
        
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=8)
        if response.status_code == 200:
            res_json = response.json()
            return res_json.get("status") == "success"
        return False
    except Exception as e:
        print(f"⚠️ No se pudo sincronizar con Google Sheets: {e}")
        return False

def sync_study_session(timestamp: str, minutes: int, total_hours: float, category: str, description: str, notes: str = "") -> bool:
    payload = {
        "timestamp": timestamp,
        "type": f"Sesión: {category}",
        "minutes": minutes,
        "total_hours": total_hours,
        "band": "",
        "cefr": "",
        "description": description,
        "notes": notes
    }
    return send_to_google_sheets(payload)

def sync_evaluation_result(timestamp: str, submission_type: str, result: dict, total_hours: float = "") -> bool:
    overall_band = result.get("overall_band", "")
    cefr = result.get("cefr_level", "")
    tr = result.get("task_response", "")
    cc = result.get("coherence_cohesion", "")
    lr = result.get("lexical_resource", "")
    gra = result.get("grammatical_accuracy", "")
    
    desc = f"TR:{tr} | CC:{cc} | LR:{lr} | GRA:{gra}"
    next_item = result.get("next_action_item", "")
    
    payload = {
        "timestamp": timestamp,
        "type": f"Evaluación IELTS ({submission_type.upper()})",
        "minutes": 0,
        "total_hours": total_hours,
        "band": overall_band,
        "cefr": cefr,
        "description": desc,
        "notes": next_item
    }
    return send_to_google_sheets(payload)

if __name__ == "__main__":
    from datetime import datetime
    print("Probando sincronización con Google Sheets...")
    ok = sync_study_session(datetime.now().strftime("%Y-%m-%d %H:%M"), 30, 0.5, "Input & SRS", "Prueba manual directa")
    if ok:
        print("✅ Sincronización exitosa.")
    else:
        print("❌ Error al sincronizar.")
