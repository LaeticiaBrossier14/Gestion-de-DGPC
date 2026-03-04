"""
Serveur de vérification de transcription.
Lance: python verification_tool/server.py
Ouvre: http://localhost:5000
"""
import csv
import json
import os
import re
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, send_file

BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent
CSV_PATH = PROJECT_DIR / "dataset" / "500annotations_local.csv"
AUDIO_DIR = BASE_DIR / "audio"
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


def load_csv():
    global calls_data
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        calls_data = list(reader)
    # Sort by natural file name order
    calls_data.sort(key=lambda r: natural_sort_key(r.get("File", "")))
    # Assign sequential order index
    for i, row in enumerate(calls_data):
        row["_index"] = i
    print(f"Loaded {len(calls_data)} calls from {CSV_PATH.name}")


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


@app.route("/api/calls")
def api_calls():
    """Return summary list of all calls with status info."""
    result = []
    for row in calls_data:
        call_id = row.get("ID", "")
        filename = row.get("File", "")
        audio_exists = (AUDIO_DIR / filename).exists()
        p = progress.get(call_id, {})
        result.append({
            "id": call_id,
            "index": row["_index"],
            "file": filename,
            "incident_type": row.get("incident_type", ""),
            "summary": row.get("summary", "")[:100],
            "status": p.get("status", "pending"),
            "audio_exists": audio_exists,
        })
    return jsonify(result)


@app.route("/api/call/<call_id>")
def api_call_detail(call_id):
    """Return full detail of one call."""
    row = next((r for r in calls_data if r.get("ID") == call_id), None)
    if not row:
        return jsonify({"error": "not found"}), 404
    p = progress.get(call_id, {})
    filename = row.get("File", "")
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
        "audio_exists": (AUDIO_DIR / filename).exists(),
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


@app.route("/api/call/<call_id>/action", methods=["POST"])
def api_call_action(call_id):
    """Update call status: verified / corrected / skipped. Also saves metadata."""
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
    audio_available = sum(1 for r in calls_data if (AUDIO_DIR / r.get("File", "")).exists())

    for row in calls_data:
        cid = row.get("ID", "")
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
    """Serve audio files from the audio directory."""
    return send_from_directory(str(AUDIO_DIR), filename)


# ── Startup ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    AUDIO_DIR.mkdir(exist_ok=True)
    load_csv()
    load_progress()
    print(f"\n  Audio directory: {AUDIO_DIR}")
    print(f"  Put your WAV files in: {AUDIO_DIR}")
    print(f"\n  Open: http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
