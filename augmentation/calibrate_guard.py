"""Calibrate guard recognition threshold from real corpus."""
import csv
import re
from pathlib import Path

# Recognized words set — all words the guard considers "known"
REC = {
    # Greetings + panic
    "allo", "salam", "azul", "arwa7", "azlem", "khouya", "l7imaya",
    "himaya", "pompiers", "secours", "urgent",
    # Closings
    "saha", "sahit", "daccord", "dakur", "merci", "bslama",
    # Kabyle particles
    "dayi", "dagi", "tura", "chwiya", "an3am", "amek", "anda", "anwa",
    "dachu", "yiwen", "yiweth", "thella", "yella", "ulach", "wlach",
    "khati", "machi", "la3nayak", "meskin", "dachou", "illa",
    # Kabyle verbs (all forms)
    "ighli", "ghli", "eghli", "theghli", "doukh", "idukh", "yugh",
    "ithyughen", "nuffes", "che3l", "ich3el", "thech3el", "tkard",
    "iterteq", "iblessi", "irez", "teddu", "activiw", "arwah",
    "iwthit", "thewthit", "teqleb", "tfit",
    # Darija verbs
    "drab", "dharb", "ta7", "wqa3",
    # Medical/fire terms
    "tmess", "tmes", "thmesth", "incendie", "feu", "fumee", "gaz",
    "crise", "malaise", "tension", "malade", "marid",
    # French common (articles, prepositions, etc)
    "le", "la", "les", "un", "une", "de", "du", "des", "et", "ou",
    "il", "elle", "on", "je", "tu", "nous", "vous", "ce", "est",
    "pas", "dans", "pour", "sur", "avec", "qui", "que", "ne", "se",
    "en", "au", "son", "sa", "par", "oui", "non", "bonjour",
    "monsieur", "madame", "ambulance", "accident", "urgence", "bloc",
    "etage", "rue", "route", "cite", "quartier", "docteur", "hopital",
    "protection", "civile", "svp", "numero", "exact", "poste",
    "victime", "conscient", "voiture", "maison", "logement",
    "telephone", "famille", "voisin", "mari", "femme", "fille",
    "homme", "commune", "adresse", "blessure", "envoyez",
    # Darija markers
    "kayen", "wesh", "rani", "rana", "kifach", "bghit", "win",
    "hna", "wa7ed", "bezaf", "3endna", "temma",
    # Additional from real corpus
    "netcherrek", "zerb", "vite", "respir", "sbitar", "sbitar",
}

csv_path = Path("dataset/400annotations_local.csv")
ratios = []

with open(csv_path, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        text = (row.get("Transcription") or "").strip().lower()
        if len(text) < 10:
            continue
        words = re.findall(r"[a-z0-9']+", text)
        if len(words) < 3:
            continue
        recognized = 0
        for w in words:
            if len(w) <= 2 or w.isdigit():
                recognized += 1
            elif w in REC:
                recognized += 1
        ratio = recognized / len(words)
        ratios.append((ratio, len(words), text[:80]))

ratios.sort(key=lambda x: x[0])
n = len(ratios)
print(f"Real calls analyzed: {n}")
print(f"{'Percentile':<12} {'Ratio':>6}")
print(f"{'Min':<12} {ratios[0][0]:>5.0%}")
print(f"{'P5':<12} {ratios[max(0,int(n*0.05))][0]:>5.0%}")
print(f"{'P10':<12} {ratios[int(n*0.10)][0]:>5.0%}")
print(f"{'P25':<12} {ratios[int(n*0.25)][0]:>5.0%}")
print(f"{'Median':<12} {ratios[n//2][0]:>5.0%}")
print(f"{'Mean':<12} {sum(r[0] for r in ratios)/n:>5.0%}")
print()
print("=== CALIBRATION ===")
real_p5 = ratios[max(0, int(n * 0.05))][0]
# Whisper margin: -20% below P5 of real data
whisper_threshold = max(0.10, real_p5 - 0.20)
print(f"Real P5:              {real_p5:.0%}")
print(f"Whisper margin:       -20%")
print(f"RECOMMENDED THRESHOLD: {whisper_threshold:.0%}")
print()
print("5 lowest-recognition real calls:")
for ratio, wc, text in ratios[:5]:
    print(f"  {ratio:.0%} ({wc}w) {text}")
