"""
Serveur de vérification de transcription — MODE COLLABORATIF.
Lance: python verification_tool/server.py
Ouvre: http://localhost:5000

Fonctionnement collaboratif :
  - Lit automatiquement TOUS les CSV d'annotations disponibles (500annotations + annotation_app)
  - Cherche les audios dans mehrere dossiers
  - Après un `git pull`, appelle /api/reload pour recharger sans redémarrer
"""
import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, send_file

BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent

# ── Sources CSV : tous les fichiers CSV d'annotations à fusionner ──────────
# Ajoute ici tout nouveau CSV si besoin
CSV_SOURCES = [
    PROJECT_DIR / "dataset" / "500annotations_local.csv",           # annotations originales (1-505)
    PROJECT_DIR / "annotation_app" / "dataset" / "annotations_local.csv",  # nouvelles annotations (506+)
]

# ── Dossiers audio : cherche dans tous ces dossiers ────────────────────────
AUDIO_DIRS = [
    BASE_DIR / "audio",                                        # audios vérification (1-505)
    PROJECT_DIR / "annotation_app" / "audio_processed",        # audios traités annotation_app
    PROJECT_DIR / "annotation_app" / "audio_raw",              # audios bruts annotation_app
]

PROGRESS_FILE = BASE_DIR / "verification_progress.json"

app = Flask(__name__, static_folder=str(BASE_DIR))

# ── Ontology (aligned with dgpc_annotation_local.py / enums.py) ──────────
INCIDENT_TYPE_OPTIONS = {
    "❓ Inconnu": "unknown",
    "🚗 Accident véhiculaire": "accident_vehicular",
    "🚶 Accident piéton": "accident_pedestrian",
    "🔥 Incendie bâtiment": "fire_building",
    "🌲 Feu de forêt": "fire_forest",
    "🚗🔥 Véhicule en feu": "fire_vehicle",
    "🏥 Urgence médicale": "medical_emergency",
    "🌊 Noyade": "drowning",
    "👊 Agression / Violence": "assault_violence",
    "🔓 Vol / Cambriolage": "theft_robbery",
    "🌍 Catastrophe naturelle": "natural_disaster",
    "☣️ Matières dangereuses": "hazmat",
    "🔍 Personne disparue": "lost_person",
    "🏚️ Effondrement": "structural_collapse",
    "📝 Autre": "other",
}
SEVERITY_OPTIONS = {
    "❓ Inconnu": "unknown",
    "✅ Aucune": "none",
    "🟡 Légère": "minor",
    "🟠 Grave": "severe",
    "⚫ Décès": "fatal",
}
URGENCY_OPTIONS = {
    "❓ Inconnu": "unknown",
    "🟢 Faible": "low",
    "🟡 Moyen": "medium",
    "🟠 Élevé": "high",
    "🔴 Critique": "critical",
}
INTENT_OPTIONS = {
    "📞 Signalement d'incident": "report_incident",
    "❓ Demande d'aide": "request_help",
    "🔄 Mise à jour": "update_info",
    "🚫 Faux appel / Blague": "false_alarm",
    "❌ Autre (erreur n°, test)": "other",
}
TRISTATE_OPTIONS = {"❓ Inconnu": "unknown", "✅ Oui": "yes", "❌ Non": "no"}
DAIRAS_BEJAIA = [
    'Inconnu', 'Adekar', 'Akbou', 'Amizour', 'Aokas', 'Barbacha',
    'Béjaïa', 'Beni Maouche', 'Chemini', 'Darguina', 'El Kseur',
    'Ighil Ali', 'Kherrata', 'Ouzellaguen', 'Seddouk', 'Sidi-Aïch',
    'Souk El-Ténine', 'Tazmalt', 'Tichy', 'Timezrit'
]

# ── Data Store ──────────────────────────────────────────────────────────
calls_data = []      # list of dicts from CSV
progress = {}        # {call_id: {status, corrected_transcription, timestamp}}


def natural_sort_key(name):
    """Sort 'Appelle 2.wav' before 'Appelle 10.wav'."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]


def find_audio(filename):
    """Cherche un fichier audio dans tous les dossiers audio."""
    for audio_dir in AUDIO_DIRS:
        candidate = audio_dir / filename
        if candidate.exists():
            return candidate
    return None


def load_csv():
    """Charge et fusionne tous les CSV sources disponibles."""
    global calls_data
    merged = {}  # clé = nom de fichier audio, valeur = row dict (dédoublonnage)
    loaded_sources = []

    for csv_path in CSV_SOURCES:
        if not csv_path.exists():
            print(f"[SKIP] CSV introuvable : {csv_path}")
            continue
        try:
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            for row in rows:
                file_key = row.get("File", "").strip()
                if file_key and file_key not in merged:
                    merged[file_key] = row
                # Si déjà présent, le CSV plus récent (ordre dans CSV_SOURCES) a priorité
                # → on ne re-écrase pas (premier chargé = priorité)
            loaded_sources.append(str(csv_path.name))
            print(f"[OK] Chargé {len(rows)} entrées depuis {csv_path.name}")
        except Exception as e:
            print(f"[ERREUR] Impossible de lire {csv_path}: {e}")

    calls_data = list(merged.values())
    calls_data.sort(key=lambda r: natural_sort_key(r.get("File", "")))
    for i, row in enumerate(calls_data):
        row["_index"] = i

    print(f"\n[OK] Total fusionne : {len(calls_data)} appels depuis {loaded_sources}\n")


def load_progress():
    global progress
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            progress = json.load(f)
        print(f"Loaded progress: {len(progress)} entries")


def save_progress():
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


# ── API Routes ──────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_file(str(BASE_DIR / "index.html"))


@app.route("/api/reload", methods=["POST"])
def api_reload():
    """Recharge tous les CSV et la progression sans redémarrer le serveur.
    Utile après un `git pull` pour voir les nouvelles annotations de ta binôme.
    """
    load_csv()
    load_progress()
    return jsonify({
        "ok": True,
        "total": len(calls_data),
        "message": f"{len(calls_data)} appels chargés après rechargement."
    })


@app.route("/api/sources")
def api_sources():
    """Retourne les fichiers CSV sources chargés et leur statut."""
    sources = []
    for csv_path in CSV_SOURCES:
        sources.append({
            "path": str(csv_path),
            "name": csv_path.name,
            "exists": csv_path.exists(),
            "size": csv_path.stat().st_size if csv_path.exists() else 0,
        })
    audio_info = []
    for d in AUDIO_DIRS:
        audio_info.append({
            "path": str(d),
            "exists": d.exists(),
            "files": len(list(d.glob("*.*"))) if d.exists() else 0,
        })
    return jsonify({"csv_sources": sources, "audio_dirs": audio_info})


@app.route("/api/calls")
def api_calls():
    """Return summary list of all calls with status info."""
    result = []
    for row in calls_data:
        filename = row.get("File", "").strip()
        # Use filename as unique ID (the ID column is often truncated/duplicate)
        call_id = filename
        audio_path = find_audio(filename)
        p = progress.get(call_id, {})
        result.append({
            "id": call_id,
            "index": row["_index"],
            "file": filename,
            "incident_type": row.get("incident_type", ""),
            "summary": row.get("summary", "")[:100],
            "status": p.get("status", "pending"),
            "audio_exists": audio_path is not None,
        })
    return jsonify(result)


@app.route("/api/call/<path:call_id>")
def api_call_detail(call_id):
    """Return full detail of one call. call_id = filename (unique key)."""
    # call_id is the filename used as unique key
    row = next((r for r in calls_data if r.get("File", "").strip() == call_id), None)
    if not row:
        return jsonify({"error": "not found"}), 404
    filename = row.get("File", "").strip()
    p = progress.get(call_id, {})
    audio_path = find_audio(filename)
    return jsonify({
        "id": call_id,
        "index": row["_index"],
        "file": filename,
        "transcription": row.get("Transcription", ""),
        "corrected_transcription": p.get("corrected_transcription", ""),
        "incident_type": row.get("incident_type", ""),
        "injury_severity": row.get("injury_severity", ""),
        "victims_count": row.get("victims_count", ""),
        "fire_present": row.get("fire_present", ""),
        "trapped_persons": row.get("trapped_persons", ""),
        "weapons_involved": row.get("weapons_involved", ""),
        "hazmat_involved": row.get("hazmat_involved", ""),
        "intent": row.get("intent", ""),
        "urgency_human": row.get("urgency_human", ""),
        "daira": row.get("daira", ""),
        "commune": row.get("commune", ""),
        "lieu": row.get("lieu", ""),
        "location_description": row.get("location_description", ""),
        "summary": row.get("summary", ""),
        "notes_cot": row.get("notes_cot", ""),
        "status": p.get("status", "pending"),
        "audio_exists": audio_path is not None,
        "audio_source": str(audio_path) if audio_path else None,
    })


@app.route("/api/ontology")
def api_ontology():
    """Return the ontology options for the UI dropdowns."""
    return jsonify({
        "incident_type": INCIDENT_TYPE_OPTIONS,
        "severity": SEVERITY_OPTIONS,
        "urgency": URGENCY_OPTIONS,
        "intent": INTENT_OPTIONS,
        "tristate": TRISTATE_OPTIONS,
        "dairas": DAIRAS_BEJAIA,
    })


@app.route("/api/call/<path:call_id>/action", methods=["POST"])
def api_call_action(call_id):
    """Update call status: verified / corrected / skipped. call_id = filename."""
    data = request.json
    action = data.get("action")  # verified, corrected, skipped
    corrected = data.get("corrected_transcription", "")
    metadata = data.get("metadata", {})

    if action not in ("verified", "corrected", "skipped"):
        return jsonify({"error": "invalid action"}), 400

    progress[call_id] = {
        "status": action,
        "corrected_transcription": corrected if action == "corrected" else "",
        "metadata": metadata,
        "timestamp": datetime.now().isoformat(),
    }
    save_progress()
    return jsonify({"ok": True, "status": action})


@app.route("/api/stats")
def api_stats():
    """Return verification statistics."""
    total = len(calls_data)
    statuses = {"verified": 0, "corrected": 0, "skipped": 0, "pending": 0}
    audio_available = sum(1 for r in calls_data if find_audio(r.get("File", "")) is not None)

    for row in calls_data:
        # Use filename as unique key
        cid = row.get("File", "").strip()
        s = progress.get(cid, {}).get("status", "pending")
        statuses[s] = statuses.get(s, 0) + 1

    return jsonify({
        "total": total,
        "audio_available": audio_available,
        **statuses,
    })


@app.route("/api/export", methods=["GET"])
def api_export():
    """Export corrected dataset as CSV with metadata overrides applied."""
    import io
    output = io.StringIO()
    fieldnames = list(calls_data[0].keys()) if calls_data else []
    fieldnames = [f for f in fieldnames if not f.startswith("_")]
    fieldnames.append("verification_status")
    fieldnames.append("corrected_transcription")

    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in calls_data:
        cid = row.get("ID", "")
        p = progress.get(cid, {})
        out = {k: v for k, v in row.items() if not k.startswith("_")}
        # Apply metadata overrides from verification
        meta = p.get("metadata", {})
        for mk, mv in meta.items():
            if mk in out:
                out[mk] = mv
        out["verification_status"] = p.get("status", "pending")
        out["corrected_transcription"] = p.get("corrected_transcription", "")
        writer.writerow(out)

    from flask import Response
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=500annotations_verified.csv"}
    )


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    """Cherche et sert l'audio depuis n'importe quel dossier audio disponible."""
    audio_path = find_audio(filename)
    if audio_path is None:
        return jsonify({"error": f"Audio '{filename}' introuvable dans tous les dossiers."}), 404
    return send_from_directory(str(audio_path.parent), audio_path.name)


# ── Startup ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Crée le dossier audio principal si besoin
    AUDIO_DIRS[0].mkdir(exist_ok=True)
    load_csv()
    load_progress()
    print("\n" + "="*60)
    print("  [DGPC] Verification Tool -- MODE COLLABORATIF")
    print("="*60)
    print("\n  [CSV] Sources CSV :")
    for csv_path in CSV_SOURCES:
        status = "[OK]" if csv_path.exists() else "[ABSENT]"
        print(f"    {status}  {csv_path}")
    print("\n  [AUDIO] Dossiers audio :")
    for d in AUDIO_DIRS:
        status = "[OK]" if d.exists() else "[ABSENT]"
        print(f"    {status}  {d}")
    print("\n  [WEB] Ouvre: http://localhost:5000")
    print("\n  [INFO] Apres un git pull, POST sur /api/reload pour recharger les CSV")
    print("     sans redemarrer le serveur.")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
