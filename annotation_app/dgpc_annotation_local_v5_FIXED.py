"""
dgpc_annotation_local_v5_FIXED.py
==================================
Version corrigée de l'app d'annotation - Gère mieux les erreurs d'import
"""

import streamlit as st
import os
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from glob import glob
import time

# Configuration initiale
st.set_page_config(
    page_title="DGPC Annotation Hub", 
    layout="wide", 
    page_icon="🛡️"
)

# CSS simple
st.markdown("""
<style>
body {
    background-color: #1a1c1e;
    color: #e1e4e8;
}
.stApp {
    background-color: #1a1c1e;
}
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────

st.title("🛡️ DGPC Annotation Hub")
st.markdown("#### Outil de transcription et annotation des appels d'urgence")

# ────────────────────────────────────────────────────────────
# INITIALIZE SESSION STATE
if "current_call" not in st.session_state:
    st.session_state.current_call = 0
if "dataset" not in st.session_state:
    st.session_state.dataset = None
if "audio_files" not in st.session_state:
    st.session_state.audio_files = []

# ────────────────────────────────────────────────────────────
# SIDEBAR CONFIGURATION
st.sidebar.markdown("### ⚙️ Configuration")

# Chemin dataset
project_dir = Path(__file__).parent.parent
dataset_dir = project_dir / "dataset"
audio_dir = project_dir / "audio_processed"

st.sidebar.markdown("**📁 Chemins:**")
st.sidebar.caption(f"Dataset: `{dataset_dir}`")
st.sidebar.caption(f"Audio: `{audio_dir}`")

# Charger dataset
dataset_files = sorted(glob(str(dataset_dir / "*.csv")))
selected_dataset = st.sidebar.selectbox(
    "📊 Sélectionner dataset",
    dataset_files,
    format_func=lambda x: os.path.basename(x)
)

st.sidebar.markdown("---")

# ────────────────────────────────────────────────────────────
# LOAD DATA
try:
    df = pd.read_csv(selected_dataset, encoding='utf-8')
    st.session_state.dataset = df
    
    st.sidebar.success(f"✅ Dataset chargé: {len(df)} appels")
    
except Exception as e:
    st.error(f"❌ Erreur chargement dataset: {e}")
    st.stop()

# ────────────────────────────────────────────────────────────
# MAIN INTERFACE
if st.session_state.dataset is not None:
    df = st.session_state.dataset
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.current_call = st.slider(
            "Choisir appel",
            0, len(df)-1,
            st.session_state.current_call
        )
    with col2:
        st.markdown(f"**Appel: {st.session_state.current_call + 1}/{len(df)}**")
    with col3:
        if st.button("🔄 Rafraîchir"):
            st.rerun()
    
    st.markdown("---")
    
    # Display current call
    call_idx = st.session_state.current_call
    call_row = df.iloc[call_idx]
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📝 Transcription", "🎧 Audio", "📊 Métadonnées"])
    
    with tab1:
        st.markdown("### Transcription")
        text_val = call_row.get("Transcription", "") if hasattr(call_row, 'get') else call_row.get("Transcription") if "Transcription" in call_row.index else ""
        st.text_area(
            "Texte transcrit:",
            value=str(text_val) if text_val else "",
            height=200,
            disabled=True,
            label_visibility="collapsed"
        )
    
    with tab2:
        st.markdown("### Audio")
        audio_file = call_row.get("File") if "File" in call_row.index else ""
        audio_path = audio_dir / str(audio_file) if audio_file else None
        
        if audio_path and audio_path.exists():
            st.audio(str(audio_path))
        elif audio_file:
            st.warning(f"⚠️ Audio non trouvé: {audio_file}")
        else:
            st.info("ℹ️ Pas de fichier audio associé")
    
    with tab3:
        st.markdown("### Informations")
        cols_to_show = ["ID", "incident_type", "urgency_human", "daira", "commune", "location_description"]
        for col in cols_to_show:
            if col in call_row.index:
                val = call_row[col]
                st.write(f"**{col}:** `{val if val else '—'}`")
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📊 Statistiques Dataset")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total appels", len(df))
    with col2:
        if "_annotation_status" in df.columns:
            annotated = len(df[df["_annotation_status"].fillna("") == "annotated"])
            st.metric("Annotés", annotated)
        else:
            st.metric("Annotés", 0)
    with col3:
        if "_annotation_status" in df.columns:
            pending = len(df[df["_annotation_status"].fillna("") == "pending"])
            st.metric("En attente", pending)
        else:
            st.metric("En attente", len(df))
    with col4:
        if "_annotation_status" in df.columns:
            annotated = len(df[df["_annotation_status"].fillna("") == "annotated"])
            st.metric("Couverture", f"{int(annotated/len(df)*100) if len(df) > 0 else 0}%")
        else:
            st.metric("Couverture", "0%")

st.markdown("---")
st.caption("🛡️ DGPC Annotation Hub | Protection Civile Béjaïa | v5.0")
