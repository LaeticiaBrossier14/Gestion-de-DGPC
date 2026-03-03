"""
Analyse linguistique du corpus annoté d'appels d'urgence — Dialecte Béjaïa (Tasahlit/Kabyle)
Extraction de règles pour le guard_kabyle_language de la pipeline de génération.
"""
import os
import sys
import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


def configure_utf8_stdio() -> None:
    """Best-effort UTF-8 stdout/stderr on Windows terminals."""
    current = (getattr(sys.stdout, "encoding", None) or "").lower()
    if "utf" in current:
        return

    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


configure_utf8_stdio()

ROOT = Path(__file__).resolve().parent
DEFAULT_CSV_CANDIDATES = [
    ROOT / "dataset" / "annotations_real_calls.csv",
    ROOT / "dataset" / "annotations_lcocal.csv",
    ROOT / "dataset" / "annotations_clocal.csv",
    ROOT / "dataset" / "annotations_local.csv",
]

parser = argparse.ArgumentParser()
parser.add_argument(
    "--csv_paths",
    nargs="+",
    default=None,
    help="One or more CSV paths to analyze. If omitted, the first existing default corpus is used.",
)
args = parser.parse_args()

if args.csv_paths:
    csv_paths = [Path(p) for p in args.csv_paths if Path(p).exists()]
else:
    csv_paths = []
    for candidate in DEFAULT_CSV_CANDIDATES:
        if candidate.exists():
            csv_paths = [candidate]
            break

if not csv_paths:
    raise FileNotFoundError(
        "No input CSV found. Expected one of: "
        + ", ".join(str(p) for p in DEFAULT_CSV_CANDIDATES)
    )

# ── 1. Load data ──
rows = []
for csv_path in csv_paths:
    with open(csv_path, encoding="utf-8-sig") as f:
        rows.extend(list(csv.DictReader(f)))

transcriptions = [r["Transcription"] for r in rows if r.get("Transcription")]
print(f"{'='*70}")
print(f"CSV INPUTS: {', '.join(str(p) for p in csv_paths)}")
print(f"CORPUS: {len(transcriptions)} transcriptions chargées")
print(f"{'='*70}\n")

# ── 2. Distribution des labels ──
print("═══ DISTRIBUTION DES LABELS ═══\n")
for col in ["incident_type", "injury_severity", "intent", "urgency_human"]:
    counts = Counter(r.get(col, "").strip() for r in rows)
    print(f"--- {col} ---")
    for k, v in counts.most_common():
        print(f"  {k or '(vide)'}: {v}")
    print()

# Distribution géographique
print("--- daira (top 15) ---")
daira_counts = Counter(r.get("daira", "").strip() for r in rows)
for k, v in daira_counts.most_common(15):
    print(f"  {k or '(vide)'}: {v}")
print()

# ── 3. Statistiques textuelles ──
print("═══ STATISTIQUES TEXTUELLES ═══\n")
lengths = [len(t) for t in transcriptions]
word_counts = [len(t.split()) for t in transcriptions]
print(f"Longueur (chars): min={min(lengths)}, max={max(lengths)}, moy={sum(lengths)/len(lengths):.0f}, médiane={sorted(lengths)[len(lengths)//2]}")
print(f"Mots: min={min(word_counts)}, max={max(word_counts)}, moy={sum(word_counts)/len(word_counts):.0f}, médiane={sorted(word_counts)[len(word_counts)//2]}")
print()

# ── 4. Salutations et formules d'ouverture ──
print("═══ SALUTATIONS & OUVERTURE ═══\n")
greeting_patterns = [
    (r'\ballo\b', 'Allo'),
    (r'\bsalam(?:\s+(?:alai?k(?:ou)?m|aley?k(?:ou)?m|3(?:li|ala)k(?:ou)?m))?', 'Salam/Salamou alaykoum'),
    (r'\bazul\b', 'Azul'),
    (r'\bsba7\s*l.khir\b', 'Sba7 lkhir'),
    (r'\bms[ae]l?\s*l?khir\b', 'Msa lkhir'),
    (r"\bl['']?(?:h|7)ima(?:ya|wi|oui|wai|yai)\b", "L'Himaya (Protection Civile)"),
    (r'\bl.pomp(?:iers?|iyer?)\b', 'L\'pompiers'),
    (r'\bprotection\s+civil', 'Protection Civile'),
    (r'\bl.ambulance\b', "L'ambulance"),
    (r'\b(?:les\s+)?pompiers\b', 'Pompiers'),
]
for pat, name in greeting_patterns:
    matches = sum(1 for t in transcriptions if re.search(pat, t, re.I))
    print(f"  {name}: {matches}/{len(transcriptions)} ({100*matches/len(transcriptions):.0f}%)")
print()

# ── 5. Négation kabyle ──
print("═══ NÉGATION KABYLE ═══\n")
neg_patterns = [
    (r'\bur\b.*?\bara\b', 'ur ... ara (négation standard kabyle)'),
    (r'\b(?:u|w)lac(?:h)?(?:it)?(?:hn)?\b', 'ulach/wlach (il n\'y a pas)'),
    (r'\bkhati?\b', 'khati (non)'),
    (r'\bmachi\b', 'machi (ce n\'est pas)'),
    (r'\bla\s+la\b', 'la la (non non — arabe/darija)'),
    (r'\bnon\b', 'non (français)'),
    (r'\bxati\b', 'xati (non — variante)'),
]
for pat, name in neg_patterns:
    matches = []
    for i, t in enumerate(transcriptions):
        found = re.findall(pat, t, re.I)
        if found:
            matches.extend(found)
    print(f"  {name}: {len(matches)} occurrences")
    if matches[:3]:
        for m in matches[:3]:
            print(f"    ex: «{m.strip()[:60]}»")
print()

# ── 6. Affirmation kabyle ──
print("═══ AFFIRMATION KABYLE ═══\n")
affirm_patterns = [
    (r'\ban3am\b', 'an3am (oui)'),
    (r'\b(?:i|a)?yeh\b', 'ih/iyeh (oui)'),
    (r'\bd.accord\b', "d'accord"),
    (r'\bouai?s?\b', 'ouais'),
    (r'\bsa7(?:it|a|ha)\b', 'saha/sahit (merci/au revoir)'),
    (r'\bkhalass?\b', 'khalas (c\'est fait)'),
]
for pat, name in affirm_patterns:
    count = sum(len(re.findall(pat, t, re.I)) for t in transcriptions)
    print(f"  {name}: {count} occurrences")
print()

# ── 7. Verbes et conjugaison kabyle ──
print("═══ VERBES & CONJUGAISON ═══\n")

# Préfixes verbaux kabyle (aoriste, prétérit, participe)
verb_prefixes = [
    (r'\b(?:i|y)-?\w+', 'i-/y- (3ème pers. masc. sing.)'),
    (r'\bt-\w+', 't- (2ème pers. ou 3ème fém.)'),
    (r'\bn-\w+', 'n- (1ère pers. plur.)'),
    (r'\bat-t-\w+', 'at-t- (futur/subjonctif)'),
    (r'\bad-\w+', 'ad- (futur/aoriste)'),
]

# Verbes d'urgence spécifiques
urgency_verbs = [
    (r'\b(?:i|y|t)?-?(?:ghli|eghli|ighli)\b', 'ghli (tomber/s\'évanouir)'),
    (r'\bt?che3l\b', 'che3l (brûler/prendre feu)'),
    (r'\b(?:i|t)?-?(?:doukh|dukh)\b', 'doukh (être étourdi/mal)'),
    (r'\b(?:i|t)?-?(?:yuɣ|yugh|thyugh)\b', 'yugh (faire mal/être malade)'),
    (r'\b(?:i|t)?-?(?:jerr?e7|jra7)\b', 'jerre7 (blesser)'),
    (r'\b(?:i|t)?-?(?:mmouth|meouth|mmuth)\b', 'mmuth (mourir)'),
    (r'\barwa7\b', 'arwa7 (venir — impératif)'),
    (r'\bchey3(?:e[td]|em)\b', 'chey3 (envoyer)'),
    (r'\b(?:i|y|t)?-?(?:tteddu?|teddu?)\b', 'teddu (aller/venir)'),
    (r'\b(?:a|i)t-?taw(?:i|e)(?:t|gh|m)?\b', 'ttawi (emmener/transporter)'),
]

print("Verbes d'urgence fréquents:")
for pat, name in urgency_verbs:
    count = sum(len(re.findall(pat, t, re.I)) for t in transcriptions)
    print(f"  {name}: {count}")
print()

# ── 8. Code-switching (Kabyle ↔ Français ↔ Arabe/Darija) ──
print("═══ CODE-SWITCHING ═══\n")

french_markers = [
    r'\b(?:s\'il vous plaît|monsieur|madame|d\'accord|merci|docteur|bon)\b',
    r'\b(?:bloc|étage|logement|appartement|ambulance|accident|urgence)\b',
    r'\b(?:enceinte|inconscient|blessé|malade|fracture|crise|tension)\b',
    r'\b(?:parce que|actuellement|exactement|normalement)\b',
]
arab_markers = [
    r'\bwa(?:llah|lah)\b',
    r'\binchallah\b',
    r'\bbarak\s*allah\b',
    r'\b(?:ya3tik|ya7fdhek)\b',
    r'\b(?:rahi|rani|rahoum|kayen)\b',
    r'\b(?:hna|hadik|hadak|hadou)\b',
    r'\b(?:kifach|wach|wesh)\b',
]

french_count = 0
arab_count = 0
for t in transcriptions:
    for pat in french_markers:
        french_count += len(re.findall(pat, t, re.I))
    for pat in arab_markers:
        arab_count += len(re.findall(pat, t, re.I))

print(f"  Marqueurs français détectés: {french_count}")
print(f"  Marqueurs arabe/darija détectés: {arab_count}")
print()

# Per-call language mixing analysis
print("Analyse par appel — profil linguistique:")
lang_profiles = {"kabyle_dominant": 0, "mixed_kabyle_french": 0, "darija_dominant": 0, "mixed_all": 0}
for t in transcriptions:
    fr = sum(len(re.findall(p, t, re.I)) for p in french_markers)
    ar = sum(len(re.findall(p, t, re.I)) for p in arab_markers)
    total_words = len(t.split())
    fr_ratio = fr / max(total_words, 1)
    ar_ratio = ar / max(total_words, 1)
    if ar_ratio > 0.15:
        lang_profiles["darija_dominant"] += 1
    elif fr_ratio > 0.1 and ar_ratio > 0.05:
        lang_profiles["mixed_all"] += 1
    elif fr_ratio > 0.05:
        lang_profiles["mixed_kabyle_french"] += 1
    else:
        lang_profiles["kabyle_dominant"] += 1

for k, v in lang_profiles.items():
    print(f"  {k}: {v} ({100*v/len(transcriptions):.0f}%)")
print()

# ── 9. Vocabulaire médical d'urgence ──
print("═══ VOCABULAIRE MÉDICAL/URGENCE ═══\n")
medical_vocab = [
    (r'\bl.?ma[3l](?:ad|de|ade)\b', 'l\'malade'),
    (r'\bl.?ambulance\b', "l'ambulance"),
    (r'\bsbitar\b', 'sbitar (hôpital)'),
    (r'\bl.?(?:h|7)(?:o|u)pital\b', "l'hôpital"),
    (r'\b(?:crise|la\s+crise)\b', 'crise'),
    (r'\bl.?(?:h|7)émorr?agie\b', "l'hémorragie"),
    (r'\btension\b', 'tension'),
    (r'\bsat(?:u)?ration\b', 'saturation'),
    (r'\boxyg[eè]ne\b', 'oxygène'),
    (r'\bconvuls[eé]\b', 'convulsé'),
    (r'\b(?:i|y|t)?-?(?:nuffes|respir)\w*\b', 'respirer/nuffes'),
    (r'\bcanc[eé]r(?:eu)?s?e?\b', 'cancer/cancéreuse'),
    (r'\b(?:i|y|t)?-?(?:7waj|7oaj)\b', '7waj (avoir besoin)'),
    (r'\binconscient\b', 'inconscient'),
    (r'\b(?:malaise)\b', 'malaise'),
    (r'\b(?:épilep(?:tique|sie))\b', 'épileptique'),
    (r'\btmess?th?\b', 'thmesth/tmess (feu)'),
    (r'\bn.?nar\b', 'n-nar (feu)'),
]
for pat, name in medical_vocab:
    count = sum(len(re.findall(pat, t, re.I)) for t in transcriptions)
    if count > 0:
        print(f"  {name}: {count}")
print()

# ── 10. Noms de lieux kabylisés ──
print("═══ TOPONYMES KABYLISÉS ═══\n")
place_names = Counter()
for r in rows:
    lieu = r.get("lieu", "").strip()
    commune = r.get("commune", "").strip()
    if lieu:
        place_names[lieu] += 1
    if commune:
        place_names[f"COMMUNE:{commune}"] += 1

print("Lieux les plus fréquents:")
for k, v in place_names.most_common(20):
    print(f"  {k}: {v}")
print()

# ── 11. Structure dialogique (Operator/Caller turns) ──
print("═══ STRUCTURE DIALOGIQUE ═══\n")
has_operator_tag = sum(1 for t in transcriptions if re.search(r'\b(?:Operator|Agent|Receiver)\s*:', t, re.I))
has_caller_tag = sum(1 for t in transcriptions if re.search(r'\b(?:Caller|Appelant)\s*:', t, re.I))
has_dash_turns = sum(1 for t in transcriptions if ' - ' in t or ' — ' in t)
print(f"  Avec étiquettes Operator/Caller: {has_operator_tag}")
print(f"  Avec tirets (tours de parole): {has_dash_turns}")
print(f"  Sans marquage explicite: {len(transcriptions) - has_operator_tag - has_dash_turns}")
print()

# ── 12. Numéros de téléphone donnés ──
print("═══ NUMÉROS DE TÉLÉPHONE ═══\n")
phone_count = sum(1 for t in transcriptions if re.search(r'0\d{2}\s*\d{2}\s*\d{2}\s*\d{2}', t))
print(f"  Appels contenant un numéro de tél.: {phone_count}/{len(transcriptions)}")
print()

# ── 13. Particules et connecteurs kabyles ──
print("═══ PARTICULES & CONNECTEURS ═══\n")
particles = [
    (r'\bdayi\b', 'dayi (ici)'),
    (r'\bdagi\b', 'dagi (ici)'),
    (r'\bdinna\b', 'dinna (là-bas)'),
    (r'\btura\b', 'tura (maintenant)'),
    (r'\bchwi?ya\b', 'chwiya (un peu)'),
    (r'\bnes3a\b', "nes3a (nous avons)"),
    (r'\biss?3a\b', "iss3a / is3a (il a)"),
    (r'\btes3a\b', "tes3a (elle a)"),
    (r'\byiw(?:e)?th\b', 'yiweth (une — fém.)'),
    (r'\byiwen\b', 'yiwen (un — masc.)'),
    (r'\bamek\b', 'amek (comment)'),
    (r'\banda\b', 'anda (où)'),
    (r'\banida\b', 'anida (où)'),
    (r'\banwa\b', 'anwa (lequel)'),
    (r'\bdachu\b', 'dachu (quoi)'),
    (r'\bachou?\b', 'achu/achou (quoi)'),
    (r'\bagma\b', 'agma (frère)'),
    (r'\bkhouya\b', 'khouya (frère — arabe)'),
    (r'\ba\s*madame\b', 'a Madame'),
    (r'\ba\s*sidi?\b', 'a sidi (monsieur)'),
    (r'\b7bbib\b', '7bib (ami/cher)'),
    (r'\bla3(?:na)?y(?:a|e)k\b', "la3nayek (s'il te plaît)"),
    (r'\bma3lich(?:e)?\b', "ma3lich (s'il vous plaît / excusez)"),
]
for pat, name in particles:
    count = sum(len(re.findall(pat, t, re.I)) for t in transcriptions)
    if count > 0:
        print(f"  {name}: {count}")
print()

# ── 14. Système d'écriture (romanisation) ──
print("═══ CONVENTIONS D'ÉCRITURE ═══\n")
conventions = [
    (r'3', "'3' pour 'ع' (ayn)"),
    (r'7', "'7' pour 'ح' (ha emphatique)"),
    (r'9', "'9' pour 'ق' (qaf)"),
    (r'gh', "'gh' pour 'غ' (ghayn)"),
    (r'th', "'th' pour 'ث' (tha)"),
    (r'ch', "'ch' pour 'ش' (shin)"),
    (r'ɣ', "'ɣ' (gamma kabyle standard)"),
]
for pat, name in conventions:
    count = sum(len(re.findall(pat, t, re.I)) for t in transcriptions)
    print(f"  {name}: {count} occurrences")

print(f"\n{'='*70}")
print("ANALYSE TERMINÉE")
print(f"{'='*70}")
