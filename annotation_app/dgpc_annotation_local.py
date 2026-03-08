import streamlit as st
import os
import sys
import json
import pandas as pd
import google.generativeai as genai
from datetime import datetime
from glob import glob
from pydub import AudioSegment
import time

# Add project root to path for augmentation imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from augmentation.engine.corrector import KabyleCorrector

# Initialize corrector once
_corrector = KabyleCorrector()

# --- .env support (clé API sécurisée) ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optionnel — fallback sidebar

# --- CONFIGURATION INITIALE ---
st.set_page_config(
    page_title="DGPC Annotation Hub v4", 
    layout="wide", 
    page_icon="🛡️"
)

# --- WORKSTATION SLATE DESIGN (High Density) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500;600;700&display=swap');
    
    :root {
        --slate-bg: #1a1c1e;
        --slate-card: #24272a;
        --slate-input: #0d0e10;
        --slate-border: #3f444c;
        --slate-text: #e1e4e8;
        --slate-muted: #959da5;
        --accent-blue: #2188ff;
        --accent-green: #28a745;
        --accent-red: #ea4a5a;
    }

    /* Zero-Scroll Optimization */
    .stApp {
        background-color: var(--slate-bg);
        color: var(--slate-text);
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 98% !important;
    }

    /* Compact Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #121416;
        border-right: 1px solid var(--slate-border);
        width: 250px !important;
    }

    /* Master Layout Sections */
    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--slate-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
        display: block;
    }

    /* Transcription Area (Full Width) */
    .stTextArea textarea {
        background-color: var(--slate-input) !important;
        border: 1px solid var(--slate-border) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
    }

    /* Attributes Grid (Compact) */
    .stTextInput input, .stSelectbox [data-baseweb="select"], .stDateInput input {
        background-color: var(--slate-input) !important;
        border: 1px solid var(--slate-border) !important;
        color: var(--slate-text) !important;
        font-size: 0.85rem !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
    }
    
    .stTextInput label, .stSelectbox label, .stDateInput label {
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        color: var(--slate-muted) !important;
        margin-bottom: 2px !important;
    }

    /* Unified Actions Bar */
    .stButton>button {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        padding: 0.4rem 1rem !important;
        border-radius: 4px !important;
        transition: all 0.1s ease !important;
    }
    .btn-ai button {
        background-color: #31363f !important;
        color: #61afef !important;
        border: 1px solid #4b5263 !important;
        width: 100% !important;
    }
    .btn-save button {
        background-color: var(--accent-green) !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
    }
    .btn-skip button {
        background-color: #31363f !important;
        color: var(--slate-muted) !important;
        border: 1px solid var(--slate-border) !important;
        width: 100% !important;
    }

    /* Status Header */
    .status-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 800;
        padding: 1px 8px;
        border-radius: 2px;
        border: 1px solid currentColor;
    }
    .status-done { color: #50fa7b; }
    .status-todo { color: #ff5555; }

    /* Space Reducer */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- PATHS & DATA ---
DATA_DIR = "dataset"
AUDIO_RAW_DIR = "audio_raw"
AUDIO_PROC_DIR = "audio_processed"
ANNOTATIONS_FILE = os.path.join(DATA_DIR, "annotations_local.json")
ANNOTATIONS_CSV = os.path.join(DATA_DIR, "annotations_local.csv")

for d in [DATA_DIR, AUDIO_RAW_DIR, AUDIO_PROC_DIR]:
    os.makedirs(d, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ONTOLOGIE — Alignée avec ml_pipeline/dataset/enums.py (SINGLE SOURCE OF TRUTH)
# ═══════════════════════════════════════════════════════════════════════════════

DAIRAS_BEJAIA = [
    'Inconnu', 'Adekar', 'Akbou', 'Amizour', 'Aokas', 'Barbacha',
    'Béjaïa', 'Beni Maouche', 'Chemini', 'Darguina', 'El Kseur',
    'Ighil Ali', 'Kherrata', 'Ouzellaguen', 'Seddouk', 'Sidi-Aïch',
    'Souk El-Ténine', 'Tazmalt', 'Tichy', 'Timezrit'
]

# Labels FR (UI) → valeurs EN (machine) — alignés avec enums.py IncidentType
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
INCIDENT_LABELS = list(INCIDENT_TYPE_OPTIONS.keys())
INCIDENT_VALUES = list(INCIDENT_TYPE_OPTIONS.values())

# Urgence humaine (calibration) — alignée avec enums.py UrgencyLevel
URGENCY_OPTIONS = {
    "❓ Inconnu": "unknown",
    "🟢 Faible": "low",
    "🟡 Moyen": "medium",
    "🟠 Élevé": "high",
    "🔴 Critique": "critical",
}
URGENCY_LABELS = list(URGENCY_OPTIONS.keys())
URGENCY_VALUES = list(URGENCY_OPTIONS.values())

# Gravité blessures — alignée avec enums.py InjurySeverity
SEVERITY_OPTIONS = {
    "❓ Inconnu": "unknown",
    "✅ Aucune": "none",
    "🟡 Légère": "minor",
    "🟠 Grave": "severe",
    "⚫ Décès": "fatal",
}
SEVERITY_LABELS = list(SEVERITY_OPTIONS.keys())
SEVERITY_VALUES = list(SEVERITY_OPTIONS.values())

# TriState — aligné avec enums.py TriState
TRISTATE_OPTIONS = {"❓ Inconnu": "unknown", "✅ Oui": "yes", "❌ Non": "no"}
TRISTATE_LABELS = list(TRISTATE_OPTIONS.keys())
TRISTATE_VALUES = list(TRISTATE_OPTIONS.values())

# Intent — aligné avec enums.py Intent
INTENT_OPTIONS = {
    "📞 Signalement d'incident": "report_incident",
    "❓ Demande d'aide": "request_help",
    "🔄 Mise à jour": "update_info",
    "🚫 Faux appel / Blague": "false_alarm",
    "❌ Autre (erreur n°, test)": "other",
}
INTENT_LABELS = list(INTENT_OPTIONS.keys())
INTENT_VALUES = list(INTENT_OPTIONS.values())

# Champs d'extraction — clés machine utilisées dans le JSON/CSV
EXTRACTION_KEYS = [
    'incident_type', 'injury_severity', 'victims_count',
    'fire_present', 'trapped_persons', 'weapons_involved', 'hazmat_involved',
    'intent', 'urgency_human',
    'daira', 'commune', 'lieu', 'location_description',
    'summary', 'notes_cot',
]

# --- AI CORE (ENRICHED PROMPT — derived from PROFIL_LINGUISTIQUE_BEJAIA.md + 100 corpus analysis) ---
SYSTEM_PROMPT = """Tu es un expert linguiste du dialecte Béjaoui (Taqbaylit n Bgayet), un mélange fluide de Kabyle, Français et Arabe Algérien.

RÈGLES DE TRANSCRIPTION (GOLD STANDARD) :

1. ROMANISATION ARABIZI (OBLIGATOIRE) :
   Utilise UNIQUEMENT le système arabizi, JAMAIS les caractères linguistiques académiques.
   | Son    | Écris  | JAMAIS  | Exemples corpus             |
   | ع ayn  | 3      | ɛ       | an3am, ma3lich, l3chiya      |
   | ح ha   | 7      | ħ       | l7uma, sa7a, 7imaya          |
   | ق qaf  | 9      | q       | 9abel                        |
   | غ ghayn| gh     | ɣ       | ghli, eghli, gher            |
   | θ tha  | th     | θ       | thella, thmesth, thyugh      |
   | ش shin | ch     | ʃ       | chwiya, che3l, dachu         |
   → Les emphatics ẓ ḍ ṭ ṣ → z d t s (sans diacritiques)

2. CODE-SWITCHING "Bejaia Style" :
   - Garde les mots français intégrés avec l'article "l'" collé : l'ambulance, l'accident, l'bloc, l'camion, l'tension, l'oxygène.
   - NE TRADUIS JAMAIS ces termes en kabyle. Écris ce qui est DIT.
   - Termes médicaux FR maintenus : crise, tension, saturation, inconscient, blessé, cancéreuse, diabétique.

3. NÉGATION (CIRCUMFIXE OBLIGATOIRE) :
   - Forme verbale : ur {verbe} ara  (ex: "ur yezmir ara" = il ne peut pas)
   - Variante Béjaïa : ul {verbe} ula
   - Nominal : ulach / wlach (il n'y a pas)
   - Identité : machi + NOM (jamais verbe). Ex: "machi d argaz" (ce n'est pas un homme)
   - Refus : khati / xati (non)

4. PARTICULES & MARQUEURS (fréquence corpus sur 100 appels) :
   - Affirmation : an3am (36), ih (96), iyeh, d'accord (97)
   - Déictiques : dayi (25), dagi (21), dinna (9), tura (23)
   - Interrogatifs : anda/anida (où), amek (comment), dachu/achu (quoi), anwa (lequel)
   - Connecteurs : bessah (mais), wesh, wallah
   - Quantificateurs : chwiya (28), yiwen/yiweth (un/une)
   - Politesse : ma3lich (13), la3nayek, agma, khouya, a sidi

5. VERBES D'URGENCE (conjugaison corpus) :
   - ghli (tomber/s'évanouir) : i-ghli, t-ghli, ye-ghli
   - che3l (brûler) : tche3l, ich3el, cha3let
   - doukh (étourdi) : i-doukh
   - yugh (faire mal) : thyugh, i-yugh
   - nuffes (respirer) : t-nuffes, ur t-nuffes ara
   - Verbes hybrides FR+KAB : it-respirerara, at-transporter-en, t-deplacer-ed

6. FORMAT DE DIALOGUE :
   - 65% flux continu (sans marqueur), 31% tirets (—), 3% étiquettes Operator:/Caller:
   - Utilise le format qui correspond le MIEUX à l'audio.

7. SALUTATIONS & CLÔTURE :
   - Ouverture : Allo (59%), Salam alaykoum (39%), Azul (3%)
   - Clôture : saha/sahit (universel), d'accord, ya3tik sa7a

CONTEXTE URGENCE BÉJAÏA :
- Termes feu : thmesth/tmess (feu), che3l (brûler), ddaxan (fumée), n-nar
- Termes médicaux : sbitar (hôpital), crise n'wul (cardiaque), l'malade
- Communes fréquentes : Béjaïa (48), El Kseur (7), Seddouk (5), Sidi Aïch (5)
- Structure localisation : [commune] + [quartier/cité] + [repère] + [détail]

TA MISSION :
- Transcris EXACTEMENT ce mélange linguistique tel que prononcé.
- Si l'appelant dit "Ma3labalnache kifach sra l'accident", écris exactement ça.
- Extrais les entités (Lieu, Type) en normalisant l'orthographe des communes seulement.
"""

EXTRACTION_PROMPT = """Analyse cet appel d'urgence et extrais les informations.

Réponds UNIQUEMENT en JSON avec ce schéma exact :
{
  "transcription": "transcription verbatim complète en langue mixte originale",
  "incident_type": "unknown|accident_vehicular|accident_pedestrian|fire_building|fire_forest|fire_vehicle|medical_emergency|drowning|assault_violence|theft_robbery|natural_disaster|hazmat|lost_person|structural_collapse|other",
  "injury_severity": "unknown|none|minor|severe|fatal",
  "victims_count": null ou nombre entier,
  "fire_present": "unknown|yes|no",
  "trapped_persons": "unknown|yes|no",
  "weapons_involved": "unknown|yes|no",
  "hazmat_involved": "unknown|yes|no",
  "intent": "report_incident|request_help|update_info|false_alarm|other",
  "urgency_human": "unknown|low|medium|high|critical",
  "daira": "daïra si identifiée OU 'Inconnu'",
  "commune": "commune si identifiée OU 'Inconnu'",
  "lieu": "village/quartier/lieu-dit OU 'Inconnu'",
  "location_description": "description itinéraire/repères verbatim (arrêt de bus, porte verte, arbre...) OU 'Inconnu'",
  "summary": "résumé court de l'appel en français (1-2 phrases)",
  "notes_cot": "raisonnement: quels mots/indices → quelles décisions (ex: times=feu, wexxam=maison → fire_building)"
}

RÈGLES :
- Si information non mentionnée → "unknown" (pas "NON_COMMUNIQUE")
- incident_type DOIT être une des 15 valeurs exactes ci-dessus
- fire_present/trapped_persons/weapons_involved/hazmat_involved = TriState (unknown/yes/no)
- victims_count = nombre entier ou null si pas mentionné
- location_description = les repères de navigation donnés par l'appelant (verbatim, très important)
- notes_cot = explique TON raisonnement mot par mot
- Si l'appel n'est pas une urgence (faux appel, erreur, question) → intent="false_alarm" ou "other", incident_type="unknown"
"""

# --- UTILS ---
def load_data(p):
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f: return json.load(f)
    return {} if "config" in p else []

def save_all(data_list):
    with open(ANNOTATIONS_FILE, 'w', encoding='utf-8') as f: json.dump(data_list, f, ensure_ascii=False, indent=2)
    rows = []
    for a in data_list:
        row = {
            'ID': a.get('id_audio'),
            'File': a.get('audio_file'),
            'Transcription': a.get('transcription', ''),
        }
        row.update(a.get('extraction', {}))
        rows.append(row)
    pd.DataFrame(rows).to_csv(ANNOTATIONS_CSV, index=False, encoding='utf-8-sig')

def process_audio(p):
    out = os.path.join(AUDIO_PROC_DIR, os.path.basename(p).split('.')[0] + ".wav")
    if not os.path.exists(out):
        try: AudioSegment.from_file(p).set_frame_rate(16000).set_channels(1).export(out, format="wav")
        except: return None
    return out

# --- APP STATE ---
annotations = load_data(ANNOTATIONS_FILE)
ann_map = { a.get('audio_file'): a for a in annotations }
done_files = set(ann_map.keys())

raw_files = sorted(glob(f"{AUDIO_RAW_DIR}/*.*"))

if not raw_files:
    st.error(f"Aucun fichier audio trouvé dans `{AUDIO_RAW_DIR}`. Ajoutez des fichiers .wav/.ogg/.mp3.")
    st.stop()

# Auto-resume : démarre au premier fichier non annoté
if 'idx' not in st.session_state:
    resume_idx = 0
    for i, rf in enumerate(raw_files):
        if os.path.basename(rf) not in done_files:
            resume_idx = i
            break
    st.session_state.idx = resume_idx

# Clamp index to valid range (safety)
st.session_state.idx = min(st.session_state.idx, len(raw_files) - 1)

# --- SIDEBAR (Minimalist) ---
st.sidebar.markdown('<p style="font-weight:700; color:#2188ff; font-size:0.9rem; margin-bottom:0px;">DGPC CONNECT</p>', unsafe_allow_html=True)

# Clé API : .env d'abord, fallback sidebar
env_key = os.environ.get('GEMINI_API_KEY', '')
if 'key' not in st.session_state:
    st.session_state.key = env_key

if env_key:
    st.sidebar.success("🔑 Clé API chargée depuis .env", icon="✅")
else:
    st.session_state.key = st.sidebar.text_input("API KEY", value=st.session_state.key, type="password", label_visibility="collapsed")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
def fmt_f(p):
    f = os.path.basename(p)
    icon = "✅ [CORRIGÉ]" if f in done_files else "📝 [À TRAITER]"
    return f"{icon} {f}"
sel = st.sidebar.selectbox("Queue", raw_files, index=st.session_state.idx, format_func=fmt_f, label_visibility="collapsed")
cur_idx = raw_files.index(sel) if sel in raw_files else st.session_state.idx
if cur_idx != st.session_state.idx: 
    st.session_state.idx = cur_idx
    st.rerun()

# --- PRECISION HUB LAYOUT ---
cur_path = raw_files[st.session_state.idx]
cur_f = os.path.basename(cur_path)
is_done = cur_f in done_files

# Sync State
if 'last_f' not in st.session_state or st.session_state.last_f != cur_f:
    st.session_state.last_f = cur_f
    entry = ann_map.get(cur_f, {})
    st.session_state.f_id = entry.get('id_audio', f"CALL_{datetime.now().strftime('%m%d')}_{cur_f[:4]}")
    st.session_state.f_text = entry.get('transcription', "")
    e = entry.get('extraction', {})
    # Champs enum
    st.session_state.v_incident_type = e.get('incident_type', 'unknown')
    st.session_state.v_injury_severity = e.get('injury_severity', 'unknown')
    st.session_state.v_urgency_human = e.get('urgency_human', 'unknown')
    st.session_state.v_intent = e.get('intent', 'report_incident')
    # TriState
    st.session_state.v_fire_present = e.get('fire_present', 'unknown')
    st.session_state.v_trapped_persons = e.get('trapped_persons', 'unknown')
    st.session_state.v_weapons_involved = e.get('weapons_involved', 'unknown')
    st.session_state.v_hazmat_involved = e.get('hazmat_involved', 'unknown')
    # Numérique
    st.session_state.v_victims_count = e.get('victims_count', None)
    # Localisation
    st.session_state.v_daira = e.get('daira', 'Inconnu')
    st.session_state.v_commune = e.get('commune', 'Inconnu')
    st.session_state.v_lieu = e.get('lieu', 'Inconnu')
    st.session_state.v_location_description = e.get('location_description', 'Inconnu')
    # Texte libre
    st.session_state.v_summary = e.get('summary', '')
    st.session_state.v_notes_cot = e.get('notes_cot', '')

# 1. TOP HEADER & AUDIO (Full Width)
header_status = f'<span class="status-badge status-done"> ARCHIVÉ </span>' if is_done else f'<span class="status-badge status-todo"> À TRAITER </span>'
st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">'
            f'<div style="font-weight:700; font-size:0.95rem;">DOSSIER: {cur_f}</div>'
            f'<div>{header_status} &nbsp; <span style="font-family:JetBrains Mono; font-size:0.7rem;">ID: {st.session_state.f_id}</span></div>'
            f'</div>', unsafe_allow_html=True)

wav = process_audio(cur_path)
audio_container = st.empty()
with audio_container:
    if wav:
        with open(wav, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')

# 2. IA ACTION & TRANSCRIPTION (Middle Section)
st.markdown('<span class="section-label">01 // CONTRÔLE IA & TRANSCRIPTION VERBATIM</span>', unsafe_allow_html=True)
act_col1, act_col2 = st.columns([1, 4])
with act_col1:
    st.markdown('<div class="btn-ai">', unsafe_allow_html=True)
    if st.button("DÉMARRER ANALYSE IA", use_container_width=True):
        if st.session_state.key and wav:
            with st.spinner("Analyse par Gemini 3.0..."):
                try:
                    genai.configure(api_key=st.session_state.key)
                    # Force JSON output mode
                    model = genai.GenerativeModel(
                        'gemini-3-flash-preview', 
                        system_instruction=SYSTEM_PROMPT,
                        generation_config={"response_mime_type": "application/json"}
                    )
                    
                    gf = genai.upload_file(wav)
                    while gf.state.name == "PROCESSING": 
                        time.sleep(1)
                        gf = genai.get_file(gf.name)
                    
                    res = model.generate_content([gf, EXTRACTION_PROMPT])
                    
                    if not res.text:
                        st.error("L'IA a retourné une réponse vide. Réessayez.")
                    else:
                        data = json.loads(res.text)
                        raw_text = data.get('transcription', "")
                        # Run corrector on Gemini output
                        correction_result = _corrector.correct(
                            raw_text,
                            data.get('incident_type', '')
                        )
                        st.session_state.f_text = correction_result.corrected_text
                        st.session_state.f_raw_text = raw_text
                        st.session_state.f_corrections = [
                            {"icon": c.icon, "rule": c.rule, "tier": c.tier,
                             "original": c.original, "replacement": c.replacement,
                             "explanation": c.explanation}
                            for c in correction_result.corrections
                        ]
                        # Enums
                        st.session_state.v_incident_type = data.get('incident_type', 'unknown')
                        st.session_state.v_injury_severity = data.get('injury_severity', 'unknown')
                        st.session_state.v_urgency_human = data.get('urgency_human', 'unknown')
                        st.session_state.v_intent = data.get('intent', 'report_incident')
                        # TriState
                        st.session_state.v_fire_present = data.get('fire_present', 'unknown')
                        st.session_state.v_trapped_persons = data.get('trapped_persons', 'unknown')
                        st.session_state.v_weapons_involved = data.get('weapons_involved', 'unknown')
                        st.session_state.v_hazmat_involved = data.get('hazmat_involved', 'unknown')
                        # Numérique
                        vc = data.get('victims_count', None)
                        st.session_state.v_victims_count = int(vc) if vc is not None else None
                        # Localisation
                        st.session_state.v_daira = data.get('daira', 'Inconnu')
                        st.session_state.v_commune = data.get('commune', 'Inconnu')
                        st.session_state.v_lieu = data.get('lieu', 'Inconnu')
                        st.session_state.v_location_description = data.get('location_description', 'Inconnu')
                        # Texte libre
                        st.session_state.v_summary = data.get('summary', '')
                        st.session_state.v_notes_cot = data.get('notes_cot', '')
                        st.rerun()
                except json.JSONDecodeError as je:
                    st.error(f"Erreur de formatage JSON : {je}. Contenu reçu : {res.text[:100]}...")
                except Exception as e:
                    # Streamlit utilise des exceptions pour le contrôle de flux (Rerun), on doit les laisser passer
                    if "RerunData" in str(e) or "StopException" in str(e):
                        raise e
                    st.error(f"Échec de l'analyse : {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

with act_col2:
    st.session_state.f_text = st.text_area("Transcription", value=st.session_state.f_text, height=140, label_visibility="collapsed")

# --- CORRECTION PANEL ---
if hasattr(st.session_state, 'f_corrections') and st.session_state.f_corrections:
    corrections = st.session_state.f_corrections
    n_auto = sum(1 for c in corrections if c['tier'] == 1)
    n_suggest = sum(1 for c in corrections if c['tier'] == 2)
    with st.expander(f"🔧 CORRECTIONS KABYLE ({n_auto} auto-fix, {n_suggest} suggestions)", expanded=True):
        if n_auto > 0:
            st.markdown("**Auto-corrections appliquées :**")
            for c in corrections:
                if c['tier'] == 1:
                    st.markdown(f"✅ **{c['rule']}**: `{c['original']}` → `{c['replacement']}` — {c['explanation']}")
        if n_suggest > 0:
            st.markdown("**Suggestions à vérifier :**")
            for c in corrections:
                if c['tier'] == 2:
                    st.markdown(f"💡 **{c['rule']}**: `{c['original']}` — {c['explanation']}")
        if hasattr(st.session_state, 'f_raw_text') and st.session_state.f_raw_text:
            with st.expander("📝 Texte original (avant corrections)"):
                st.text(st.session_state.f_raw_text)

# 3. ATTRIBUTE GRID (Bottom Section)
st.markdown('<span class="section-label">02 // PARAMÈTRES ET ATTRIBUTS SYSTÈME</span>', unsafe_allow_html=True)

# --- Row 1 : Type d'incident + Intent + Urgence humaine + Gravité ---
grid_r1_c1, grid_r1_c2, grid_r1_c3, grid_r1_c4 = st.columns(4)

_inc_val = st.session_state.v_incident_type
_inc_idx = INCIDENT_VALUES.index(_inc_val) if _inc_val in INCIDENT_VALUES else 0
sel_inc = grid_r1_c1.selectbox("Type d'incident", INCIDENT_LABELS, index=_inc_idx)
st.session_state.v_incident_type = INCIDENT_TYPE_OPTIONS[sel_inc]

_int_val = st.session_state.v_intent
_int_idx = INTENT_VALUES.index(_int_val) if _int_val in INTENT_VALUES else 0
sel_int = grid_r1_c2.selectbox("Intention appel", INTENT_LABELS, index=_int_idx)
st.session_state.v_intent = INTENT_OPTIONS[sel_int]

_urg_val = st.session_state.v_urgency_human
_urg_idx = URGENCY_VALUES.index(_urg_val) if _urg_val in URGENCY_VALUES else 0
sel_urg = grid_r1_c3.selectbox("Urgence (humain)", URGENCY_LABELS, index=_urg_idx)
st.session_state.v_urgency_human = URGENCY_OPTIONS[sel_urg]

_sev_val = st.session_state.v_injury_severity
_sev_idx = SEVERITY_VALUES.index(_sev_val) if _sev_val in SEVERITY_VALUES else 0
sel_sev = grid_r1_c4.selectbox("Gravité blessures", SEVERITY_LABELS, index=_sev_idx)
st.session_state.v_injury_severity = SEVERITY_OPTIONS[sel_sev]

# --- Row 2 : TriState flags + Victimes ---
grid_r2_c1, grid_r2_c2, grid_r2_c3, grid_r2_c4, grid_r2_c5 = st.columns(5)

_fire_val = st.session_state.v_fire_present
_fire_idx = TRISTATE_VALUES.index(_fire_val) if _fire_val in TRISTATE_VALUES else 0
sel_fire = grid_r2_c1.selectbox("🔥 Feu ?", TRISTATE_LABELS, index=_fire_idx)
st.session_state.v_fire_present = TRISTATE_OPTIONS[sel_fire]

_trap_val = st.session_state.v_trapped_persons
_trap_idx = TRISTATE_VALUES.index(_trap_val) if _trap_val in TRISTATE_VALUES else 0
sel_trap = grid_r2_c2.selectbox("🚧 Coincés ?", TRISTATE_LABELS, index=_trap_idx)
st.session_state.v_trapped_persons = TRISTATE_OPTIONS[sel_trap]

_weap_val = st.session_state.v_weapons_involved
_weap_idx = TRISTATE_VALUES.index(_weap_val) if _weap_val in TRISTATE_VALUES else 0
sel_weap = grid_r2_c3.selectbox("🔫 Armes ?", TRISTATE_LABELS, index=_weap_idx)
st.session_state.v_weapons_involved = TRISTATE_OPTIONS[sel_weap]

_haz_val = st.session_state.v_hazmat_involved
_haz_idx = TRISTATE_VALUES.index(_haz_val) if _haz_val in TRISTATE_VALUES else 0
sel_haz = grid_r2_c4.selectbox("☣️ HAZMAT ?", TRISTATE_LABELS, index=_haz_idx)
st.session_state.v_hazmat_involved = TRISTATE_OPTIONS[sel_haz]

vc_val = st.session_state.v_victims_count
grid_r2_c5.number_input("Nb victimes", min_value=0, value=int(vc_val) if vc_val is not None else 0, step=1, key="w_victims_count")
st.session_state.v_victims_count = st.session_state.w_victims_count if st.session_state.w_victims_count > 0 else None

# --- Row 3 : Localisation ---
grid_r3_c1, grid_r3_c2, grid_r3_c3 = st.columns(3)

_da_val = st.session_state.v_daira
_da_idx = DAIRAS_BEJAIA.index(_da_val) if _da_val in DAIRAS_BEJAIA else 0
st.session_state.v_daira = grid_r3_c1.selectbox("Daïra", DAIRAS_BEJAIA, index=_da_idx)

st.session_state.v_commune = grid_r3_c2.text_input("Commune", value=st.session_state.v_commune)
st.session_state.v_lieu = grid_r3_c3.text_input("Village / Localité", value=st.session_state.v_lieu)

# --- Row 4 : Location description (repères) ---
st.session_state.v_location_description = st.text_area(
    "📍 Repères / Description itinéraire (verbatim de l'appelant)",
    value=st.session_state.v_location_description, height=60
)

# --- Row 5 : Summary + Notes CoT ---
grid_r5_c1, grid_r5_c2 = st.columns(2)
st.session_state.v_summary = grid_r5_c1.text_area("📝 Résumé (français)", value=st.session_state.v_summary, height=60)
st.session_state.v_notes_cot = grid_r5_c2.text_area("🧠 Raisonnement (Chain-of-Thought)", value=st.session_state.v_notes_cot, height=60)

# 4. GLOBAL ACTIONS
st.markdown("---")
foot_c1, foot_c2, foot_c3, foot_c4 = st.columns([2, 1, 1, 1])

with foot_c1:
    st.markdown('<div class="btn-save">', unsafe_allow_html=True)
    if st.button("APPROUVER ET ENREGISTRER LE DOSSIER", use_container_width=True):
        # Validation: transcription obligatoire
        if not st.session_state.f_text or st.session_state.f_text.strip() == "":
            st.error("❌ ERREUR: La transcription est obligatoire. Veuillez compléter le champ 'Transcription' avant d'enregistrer.")
        else:
            entry = {
                "id_audio": st.session_state.f_id,
                "audio_file": cur_f,
                "timestamp": datetime.now().isoformat(),
                "transcription": st.session_state.f_text,
                "extraction": {
                    "incident_type": st.session_state.v_incident_type,
                    "injury_severity": st.session_state.v_injury_severity,
                    "victims_count": st.session_state.v_victims_count,
                    "fire_present": st.session_state.v_fire_present,
                    "trapped_persons": st.session_state.v_trapped_persons,
                    "weapons_involved": st.session_state.v_weapons_involved,
                    "hazmat_involved": st.session_state.v_hazmat_involved,
                    "intent": st.session_state.v_intent,
                    "urgency_human": st.session_state.v_urgency_human,
                    "daira": st.session_state.v_daira,
                    "commune": st.session_state.v_commune,
                    "lieu": st.session_state.v_lieu,
                    "location_description": st.session_state.v_location_description,
                    "summary": st.session_state.v_summary,
                    "notes_cot": st.session_state.v_notes_cot,
                },
            }
            for i, a in enumerate(annotations):
                if a.get('audio_file') == cur_f: annotations[i] = entry; break
            else: annotations.append(entry)
            save_all(annotations)
            st.success(f"✅ Dossier {cur_f} enregistré avec succès!")
            st.session_state.idx = (st.session_state.idx + 1) % len(raw_files); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with foot_c2:
    st.markdown('<div class="btn-skip">', unsafe_allow_html=True)
    if st.button("PASSER", use_container_width=True): st.session_state.idx = (st.session_state.idx + 1) % len(raw_files); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with foot_c3:
    if st.button("SYNCHRO CSV", use_container_width=True): save_all(annotations); st.toast("CSV sync.")

with foot_c4:
    total = len(raw_files)
    done = len(done_files)
    st.markdown(f'<div style="text-align:center; padding-top:0.3rem;">'
                f'<span style="font-family:JetBrains Mono; font-size:0.75rem; color:var(--accent-green);">{done}/{total}</span>'
                f'<br><span style="font-size:0.6rem; color:var(--slate-muted);">annotés</span></div>',
                unsafe_allow_html=True)

st.sidebar.markdown(f'<div style="font-size:0.6rem; color:var(--slate-muted); position:fixed; bottom:10px;">V4.0 // DGPC Annotation Hub</div>', unsafe_allow_html=True)
