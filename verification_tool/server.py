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
import unicodedata
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
AUTO_EXPORT_CSV = PROJECT_DIR / "dataset_avec_corrections.csv"

app = Flask(__name__, static_folder=str(BASE_DIR))
app.json.ensure_ascii = False

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
    'Inconnu',
    'Béjaïa',
    'Akbou',
    'Amizour',
    'Adekar',
    'Aokas',
    'Barbacha',
    'Beni Maouche',
    'Chemini',
    'Darguina',
    'El Kseur',
    'Kherrata',
    'Ouzellaguen',
    'Seddouk',
    'Sidi Aïch',
    'Souk El Tenine',
    'Tazmalt',
    'Tichy',
    'Timezrit',
    'Tifra',
]

COMMUNES_BEJAIA = [
    'Béjaïa',
    'Amizour',
    'Ferraoun',
    'Taourirt Ighil',
    'Chellata',
    'Tamokra',
    'Timezrit',
    'Souk El Tenine',
    "M'cisna",
    'Tinabdher',
    'Tichy',
    'Semaoun',
    'Kendira',
    'Tifra',
    'Ighram',
    'Amalou',
    'Ighil Ali',
    'Fenaïa Ilmaten',
    'Toudja',
    'Darguina',
    'Sidi Ayad',
    'Aokas',
    'Beni Djellil',
    'Adekar',
    'Akbou',
    'Seddouk',
    'Tazmalt',
    'Aït R\'zine',
    'Chemini',
    'Souk Oufella',
    'Taskriout',
    'Tibane',
    'Tala Hamza',
    'Barbacha',
    'Beni Ksila',
    'Ouzellaguen',
    'Bouhamza',
    'Beni Mellikeche',
    'Sidi Aïch',
    'El Kseur',
    'Melbou',
    'Akfadou',
    'Leflaye',
    'Kherrata',
    'Draâ El Kaïd',
    'Tamridjet',
    'Aït Smail',
    'Boukhelifa',
    'Tizi N\'Berber',
    'Beni Maouche',
    'Oued Ghir',
    'Boudjellil',
]

# ── Data Store ──────────────────────────────────────────────────────────
calls_data = []      # list of dicts from CSV
progress = {}        # {call_id: {status, corrected_transcription, timestamp}}

MOJIBAKE_MARKERS = ("Ã", "Â", "â", "ð", "�", "├", "┬", "ÔÇ", "┼ô")


def repair_mojibake_text(value):
    """Repair common UTF-8/Windows mojibake without touching normal text."""
    if not isinstance(value, str):
        return value

    text = unicodedata.normalize("NFC", value.replace("﻿", ""))
    if not any(marker in text for marker in MOJIBAKE_MARKERS):
        return text

    repaired = text
    for source_encoding in ("cp1252", "latin-1", "cp850"):
        try:
            candidate = repaired.encode(source_encoding).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if candidate != repaired:
            repaired = unicodedata.normalize("NFC", candidate)

    replacements = {
        "ÔÇö": "—",
        "┼ô": "œ",
        "ÔÇ’": "’",
        "ÔÇœ": "“",
        "ÔÇ": "”",
        "ÔÇª": "…",
    }
    for bad, good in replacements.items():
        repaired = repaired.replace(bad, good)

    return repaired


def sanitize_text_tree(value):
    if isinstance(value, dict):
        return {k: sanitize_text_tree(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_text_tree(v) for v in value]
    if isinstance(value, str):
        return repair_mojibake_text(value)
    return value


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
                rows = [sanitize_text_tree(row) for row in reader]
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
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                raw_progress = json.load(f)
            progress = sanitize_text_tree(raw_progress)
            if progress != raw_progress:
                save_progress()
            print(f"Loaded progress: {len(progress)} entries")
        except Exception as e:
            progress = {}
            print(f"[ERREUR] Impossible de lire {PROGRESS_FILE.name}: {e}")


def save_progress():
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(sanitize_text_tree(progress), f, ensure_ascii=False, indent=2)


def auto_export_csv():
    """Exporte automatiquement toutes les corrections vers dataset_avec_corrections.csv.
    Appelé après chaque action (corrected / verified / skipped).
    """
    if not calls_data:
        return
    try:
        fieldnames = [f for f in calls_data[0].keys() if not f.startswith("_")]
        for extra in ["corrected_transcription", "verification_status", "verification_timestamp"]:
            if extra not in fieldnames:
                fieldnames.append(extra)

        with open(AUTO_EXPORT_CSV, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in calls_data:
                cid = row.get("File", "").strip()
                p = progress.get(cid, {})
                out = {k: v for k, v in row.items() if not k.startswith("_")}
                meta = p.get("metadata", {})
                for mk, mv in meta.items():
                    if mk in out and mv is not None:
                        out[mk] = mv
                out["corrected_transcription"] = p.get("corrected_transcription", "")
                out["verification_status"] = p.get("status", "pending")
                out["verification_timestamp"] = p.get("timestamp", "")
                writer.writerow(out)
        print(f"[AUTO-EXPORT] CSV mis a jour : {AUTO_EXPORT_CSV.name}")
    except Exception as e:
        print(f"[AUTO-EXPORT] Erreur export CSV : {e}")


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
        meta = p.get("metadata", {})
        result.append({
            "id": call_id,
            "index": row["_index"],
            "file": filename,
            "incident_type": meta.get("incident_type", row.get("incident_type", "")),
            "summary": meta.get("summary", row.get("summary", ""))[:100],
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
    meta = p.get("metadata", {})
    audio_path = find_audio(filename)
    return jsonify({
        "id": call_id,
        "index": row["_index"],
        "file": filename,
        "transcription": p.get("original_transcription", row.get("Transcription", "")),
        "corrected_transcription": p.get("corrected_transcription", ""),
        "incident_type": meta.get("incident_type") or row.get("incident_type", ""),
        "injury_severity": meta.get("injury_severity") or row.get("injury_severity", ""),
        # victims_count: priorite au meta JSON enregistre, fallback CSV, defaut 0
        "victims_count": meta.get("victims_count") if meta.get("victims_count") not in (None, "") else (row.get("victims_count") or "0"),
        "fire_present": meta.get("fire_present") or row.get("fire_present", ""),
        "trapped_persons": meta.get("trapped_persons") or row.get("trapped_persons", ""),
        "weapons_involved": meta.get("weapons_involved") or row.get("weapons_involved", ""),
        "hazmat_involved": meta.get("hazmat_involved") or row.get("hazmat_involved", ""),
        "intent": meta.get("intent") or row.get("intent", ""),
        "urgency_human": meta.get("urgency_human") or row.get("urgency_human", ""),
        "daira": meta.get("daira") or row.get("daira", ""),
        "commune": meta.get("commune") or row.get("commune", ""),
        "lieu": meta.get("lieu") or row.get("lieu", ""),
        # location_description/summary/notes_cot: UNIQUEMENT depuis meta JSON si disponible
        # (evite les melanges avec des donnees CSV potentiellement erronees d'un autre appel)
        "location_description": meta.get("location_description", "") if meta else row.get("location_description", ""),
        "summary": meta.get("summary", "") if meta else row.get("summary", ""),
        "notes_cot": meta.get("notes_cot", "") if meta else row.get("notes_cot", ""),
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
        "communes": COMMUNES_BEJAIA,
    })


@app.route("/api/call/<path:call_id>/action", methods=["POST"])
def api_call_action(call_id):
    """Update call status: verified / corrected / skipped. call_id = filename."""
    data = request.json
    action = data.get("action")  # verified, corrected, skipped
    corrected = repair_mojibake_text(data.get("corrected_transcription", ""))
    metadata = sanitize_text_tree(data.get("metadata", {}))

    if action not in ("verified", "corrected", "skipped"):
        return jsonify({"error": "invalid action"}), 400

    # Conserver la corrected_transcription existante si on re-verifie sans la modifier
    existing = progress.get(call_id, {})
    existing_corrected = existing.get("corrected_transcription", "")
    if action == "corrected":
        final_corrected = corrected  # nouvelle version corrigee
    else:
        # verified ou skipped : conserver la corrected_transcription precedente si elle existait
        final_corrected = existing_corrected

    progress[call_id] = {
        "status": action,
        "original_transcription": data.get("original_transcription", existing.get("original_transcription", "")),
        "corrected_transcription": final_corrected,
        "metadata": metadata,
        "timestamp": datetime.now().isoformat(),
    }
    save_progress()
    auto_export_csv()
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
        cid = row.get("File", "").strip()
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
