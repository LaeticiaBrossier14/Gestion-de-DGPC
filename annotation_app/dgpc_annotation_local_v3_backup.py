import streamlit as st
import os
import json
import pandas as pd
import google.generativeai as genai
from datetime import datetime
from glob import glob
from pydub import AudioSegment
import time

# --- TENTATIVE IMPORT GEOPY ---
try:
    from geopy.geocoders import Nominatim
    GEOPY_AVAILABLE = True
    geolocator = Nominatim(user_agent='dgpc_precision_v3')
except ImportError:
    GEOPY_AVAILABLE = False
    geolocator = None

# --- CONFIGURATION INITIALE ---
st.set_page_config(
    page_title="DGPC Precision Hub", 
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
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

for d in [DATA_DIR, AUDIO_RAW_DIR, AUDIO_PROC_DIR]: os.makedirs(d, exist_ok=True)

DAIRAS_BEJAIA = [
    'NON_COMMUNIQUE', 'Béjaïa', 'Akbou', 'Amizour', 'Aokas', 'Barbacha',
    'Chemini', 'Darguina', 'El Kseur', 'Ighil Ali', 'Kherrata',
    'Ouzellaguen', 'Seddouk', 'Sidi Aïch', 'Souk El Ténine', 
    'Tazmalt', 'Tichy', 'Timezrit'
]

# --- AI CORE (RESTORED GOLDEN PROMPT) ---
SYSTEM_PROMPT = """Tu es un expert linguiste du dialecte Béjaoui (Taqbaylit n Bgayet), un mélange fluide de Kabyle, Français et Arabe Algérien.

RÈGLES DE TRANSCRIPTION (GOLD STANDARD) :
1. Code-Switching "Bejaia Style" :
   - Garde les mots français intégrés tels quels, souvent avec l'article "l'" collé (ex: "lvirement", "limpossible", "laccident", "lgroupe").
   - Ne traduis PAS "l'maire" en "amdir" ou "l'statut" en "addad". Écris ce qui est dit.
2. Arabizi & Chiffres :
   - Accepte et utilise les chiffres pour les sons arabes : 3 (ع), 7 (ح), 9 (ق), 5 (خ).
   - Exemples : "l3chiya" (soir), "l7uma" (quartier), "za3ma".
3. Particules & Connecteurs :
   - "bessah" (mais), "wesh" (alors/quoi), "da" (ici), "aka" (comme ça), "wallah".
4. Verbes & Grammaire :
   - Verbes français conjugués en Kabyle/Arabe : "ti parti" (tu es parti), "nraja" (on attend), "at-tahdred" (tu parleras).

CONTEXTE URGENCE :
- "l7riq" (feu), "l'accident", "teqleb" (renversé), "yejreh" (blessé).
- Lieux : Tichy, Aokas, Sidi Aïch (orthographe standard).

TA MISSION :
- Transcris exactement ce mélange. Si l'appelant dit "Ma3labalnache kifach sra l'accident", écris exactement ça.
- Extrais les entités (Lieu, Type) en normalisant l'orthographe des villes seulement.
"""

EXTRACTION_PROMPT = """Analyse cet appel d'urgence :

Reponds UNIQUEMENT en JSON avec ce schéma exact :
{
  "transcription": "transcription verbatim complète en langue mixte originale",
  "lieu": "lieu (Village/Quartier) corrigé orthographiquement OU 'NON_COMMUNIQUE'",
  "commune": "commune si identifiée OU 'NON_COMMUNIQUE'",
  "daira": "daïra OU 'NON_COMMUNIQUE'",
  "nature": "nature de l'incident (langue originale) OU 'NON_COMMUNIQUE'",
  "victimes": "nombre de victimes OU 'NON_COMMUNIQUE'",
  "etat": "état médical des victimes (langue originale) OU 'NON_COMMUNIQUE'",
  "urgence": "critique|urgent|normal|NON_COMMUNIQUE",
  "gps": "coordonnées GPS si mentionnées OU 'NON_COMMUNIQUE'",
  "notes": "infos supplémentaires"
}"""

# --- UTILS ---
def load_data(p):
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f: return json.load(f)
    return {} if "config" in p else []

def save_all(data_list):
    with open(ANNOTATIONS_FILE, 'w', encoding='utf-8') as f: json.dump(data_list, f, ensure_ascii=False, indent=2)
    rows = []
    for a in data_list:
        row = {'ID': a.get('id_audio'), 'File': a.get('audio_file'), 'Date': a.get('date_appel'), 'Time': a.get('heure_appel')}
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
config = load_data(CONFIG_FILE)
annotations = load_data(ANNOTATIONS_FILE)
ann_map = { a.get('audio_file'): a for a in annotations }
done_files = set(ann_map.keys())

raw_files = sorted(glob(f"{AUDIO_RAW_DIR}/*.*"))
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'key' not in st.session_state: st.session_state.key = config.get('key', '')

# --- SIDEBAR (Minimalist) ---
st.sidebar.markdown('<p style="font-weight:700; color:#2188ff; font-size:0.9rem; margin-bottom:0px;">DGPC CONNECT</p>', unsafe_allow_html=True)
st.session_state.key = st.sidebar.text_input("API KEY", value=st.session_state.key, type="password", label_visibility="collapsed")
if st.session_state.key != config.get('key'):
    with open(CONFIG_FILE, 'w') as f: json.dump({'key': st.session_state.key}, f)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
def fmt_f(p):
    f = os.path.basename(p)
    icon = "✅ [CORRIGÉ]" if f in done_files else "📝 [À TRAITER]"
    return f"{icon} {f}"
sel = st.sidebar.selectbox("Queue", raw_files, index=st.session_state.idx, format_func=fmt_f, label_visibility="collapsed")
cur_idx = raw_files.index(sel)
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
    st.session_state.f_date = entry.get('date_appel', datetime.now().strftime('%Y-%m-%d'))
    st.session_state.f_time = entry.get('heure_appel', datetime.now().strftime('%H:%M'))
    st.session_state.f_text = entry.get('transcription', "")
    e = entry.get('extraction', {})
    for k in ['daira','commune','lieu','nature','victimes','etat','urgence','gps']:
        st.session_state[f"v_{k}"] = e.get(k, "NON_COMMUNIQUE")
    st.session_state.f_notes = entry.get('notes', "")

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
            with st.spinner("Analyse par Gemini 3.1 Pro Preview..."):
                try:
                    genai.configure(api_key=st.session_state.key)
                    # Force JSON output mode
                    model = genai.GenerativeModel(
                        'gemini-3.1-pro-preview',
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
                        st.session_state.f_text = data.get('transcription', "")
                        for k in ['daira','commune','lieu','nature','victimes','etat','urgence','gps']:
                            st.session_state[f"v_{k}"] = data.get(k, "NON_COMMUNIQUE")
                        st.session_state.f_notes = data.get("notes", "")
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

# 3. ATTRIBUTE GRID (Bottom Section)
st.markdown('<span class="section-label">02 // PARAMÈTRES ET ATTRIBUTS SYSTÈME</span>', unsafe_allow_html=True)
grid_r1_c1, grid_r1_c2, grid_r1_c3, grid_r1_c4 = st.columns(4)
st.session_state.v_daira = grid_r1_c1.selectbox("Daïra", DAIRAS_BEJAIA, index=DAIRAS_BEJAIA.index(st.session_state.v_daira) if st.session_state.v_daira in DAIRAS_BEJAIA else 0)
st.session_state.v_commune = grid_r1_c2.text_input("Commune", value=st.session_state.v_commune)
st.session_state.v_lieu = grid_r1_c3.text_input("Village / Localité", value=st.session_state.v_lieu)
st.session_state.v_nature = grid_r1_c4.text_input("Nature du sinistre", value=st.session_state.v_nature)

grid_r2_c1, grid_r2_c2, grid_r2_c3, grid_r2_c4 = st.columns(4)
st.session_state.v_victimes = grid_r2_c1.text_input("Nombre Victimes", value=st.session_state.v_victimes)
st.session_state.v_etat = grid_r2_c2.text_input("État de santé", value=st.session_state.v_etat)
urg_opts = ["normal", "urgent", "critique", "NON_COMMUNIQUE"]
st.session_state.v_urgence = grid_r2_c3.selectbox("Priorité", urg_opts, index=urg_opts.index(st.session_state.v_urgence) if st.session_state.v_urgence in urg_opts else 0)
st.session_state.v_gps = grid_r2_c4.text_input("Coordonnées GPS", value=st.session_state.v_gps)

grid_r3_c1, grid_r3_c2, grid_r3_c3 = st.columns([1,1,2])
st.session_state.f_date = grid_r3_c1.date_input("Date", value=datetime.strptime(st.session_state.f_date, '%Y-%m-%d')).strftime('%Y-%m-%d')
st.session_state.f_time = grid_r3_c2.text_input("Heure", value=st.session_state.f_time)
st.session_state.f_notes = grid_r3_c3.text_input("Observations", value=st.session_state.f_notes)

# 4. GLOBAL ACTIONS
st.markdown("---")
foot_c1, foot_c2, foot_c3, foot_c4 = st.columns([2, 1, 1, 1])

with foot_c1:
    st.markdown('<div class="btn-save">', unsafe_allow_html=True)
    if st.button("APPROUVER ET ENREGISTRER LE DOSSIER", use_container_width=True):
        entry = {
            "id_audio": st.session_state.f_id,
            "audio_file": cur_f,
            "date_appel": st.session_state.f_date,
            "heure_appel": st.session_state.f_time,
            "timestamp": datetime.now().isoformat(),
            "transcription": st.session_state.f_text,
            "extraction": { k: st.session_state[f"v_{k}"] for k in ['daira','commune','lieu','nature','victimes','etat','urgence','gps'] },
            "notes": st.session_state.f_notes
        }
        for i, a in enumerate(annotations):
            if a.get('audio_file') == cur_f: annotations[i] = entry; break
        else: annotations.append(entry)
        save_all(annotations)
        st.session_state.idx = (st.session_state.idx + 1) % len(raw_files); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with foot_c2:
    st.markdown('<div class="btn-skip">', unsafe_allow_html=True)
    if st.button("PASSER", use_container_width=True): st.session_state.idx = (st.session_state.idx + 1) % len(raw_files); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with foot_c3:
    if st.button("SYNCHRO CSV", use_container_width=True): save_all(annotations); st.toast("CSV sync.")

with foot_c4:
    if GEOPY_AVAILABLE and st.session_state.v_gps != "NON_COMMUNIQUE":
        if st.button("GEOLOC", use_container_width=True):
            try:
                l = geolocator.reverse(st.session_state.v_gps, language='fr')
                if l: st.session_state.v_lieu = l.address; st.rerun()
            except: pass

st.sidebar.markdown(f'<div style="font-size:0.6rem; color:var(--slate-muted); position:fixed; bottom:10px;">PRO V3.0 // DGPC HUB</div>', unsafe_allow_html=True)
