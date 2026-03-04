# 🛡️ DGPC — Guide de Collaboration

> **Document de travail** — Explique comment les deux binômes travaillent ensemble sur le projet d'annotation et de vérification des transcriptions audio Kabyle.

---

## 📌 Contexte du projet

Nous travaillons sur un pipeline de traitement de la parole en **Kabyle** pour la **Protection Civile de Béjaïa**.  
Le but est de constituer un dataset d'appels d'urgence avec leurs transcriptions corrigées.

### Ce qu'on a déjà

- **505 appels annotés** (Appelle 1 → Appelle 505) dans `dataset/500annotations_local.csv`
- Les transcriptions ont été faites automatiquement par l'IA (Gemini), mais certaines sont incorrectes
- Il faut donc **vérifier et corriger** ces transcriptions

### Ce qu'il reste à faire

- **Annoter les nouveaux appels** (Appelle 506 → Appelle 811) → rôle de la binôme
- **Vérifier et corriger les anciennes transcriptions** (Appelle 1 → 505) → rôle de l'autre binôme
- Ensuite **vérifier les nouvelles transcriptions** au fur et à mesure

---

## 🗂️ Structure des dossiers importants

```
dgpc_pipeline_ready/
│
├── annotation_app/              ← Application pour ANNOTER les nouveaux appels
│   ├── audio_raw/               ← Mettre les audios à annoter ici (506 → 811)
│   ├── audio_processed/         ← Conversions automatiques (ne pas toucher)
│   ├── dataset/
│   │   └── annotations_local.csv  ← CSV généré automatiquement par l'annotation
│   └── dgpc_annotation_local.py
│
├── verification_tool/           ← Application pour VÉRIFIER et CORRIGER les transcriptions
│   ├── audio/                   ← Audios pour la vérification (1 → 811 déjà dedans)
│   ├── index.html
│   ├── server.py
│   └── verification_progress.json  ← Sauvegarde de la progression
│
└── dataset/
    └── 500annotations_local.csv   ← Les 505 premières annotations (originales)
```

---

## 🔄 Comment les deux applications se synchronisent

```
ANNOTATION APP                         VERIFICATION TOOL
──────────────────────────             ──────────────────────────
Binôme annote Appelle 506              
  ↓ sauvegarde dans CSV                
git push ────────────────────────────► git pull
                                         ↓
                                       clic "🔄 Recharger"
                                         ↓
                                       Appelle 506 apparaît
                                       avec sa transcription ✅
                                       + audio déjà disponible ✅
                                         ↓
                                       Correction si nécessaire
                                         ↓
                                       git push ──────────────► git pull (binôme)
```

---

## 👩‍💻 Rôle 1 — Annoter les nouveaux appels (Binôme A)

### Étape 1 — Mettre les audios dans le bon dossier

Mets **tous tes fichiers audio** (Appelle 506 → 811) dans :

```
f:\dgpc_pipeline_ready\annotation_app\audio_raw\
```

> ✅ Tu mets **tous les audios d'un coup** dès le départ.  
> L'application reprend automatiquement là où tu t'es arrêtée.

---

### Étape 2 — Lancer l'application d'annotation

Ouvre un terminal PowerShell et tape :

```powershell
cd f:\dgpc_pipeline_ready\annotation_app
streamlit run dgpc_annotation_local.py
```

L'application s'ouvre dans le navigateur automatiquement.

---

### Étape 3 — Annoter

Dans l'application :

1. Elle démarre au **premier appel non annoté** automatiquement
2. Clique sur **"DÉMARRER ANALYSE IA"** → l'IA transcrit l'audio
3. **Vérifie** la transcription, corrige si besoin
4. Clique **"APPROUVER ET ENREGISTRER LE DOSSIER"**
5. Passe automatiquement à l'appel suivant → répète

---

### Étape 4 — Partager son travail via Git

**À chaque pause**, ouvre un terminal et tape ces commandes dans l'ordre :

```bash
cd f:\dgpc_pipeline_ready
git add -A
git commit -m "annotations session"
git push
```

> 💡 Fais ça régulièrement (toutes les 20-30 annotations).  
> L'autre binôme peut ainsi vérifier ton travail au fur et à mesure.

---

### Étape 5 — Recevoir les mises à jour de l'autre

```bash
cd f:\dgpc_pipeline_ready
git pull
```

Puis continue simplement à annoter.

---

## 👩‍💻 Rôle 2 — Vérifier et corriger les transcriptions (Binôme B)

### Étape 1 — Lancer la verification_tool

```powershell
cd f:\dgpc_pipeline_ready
.\verification_tool\.venv\Scripts\python.exe verification_tool/server.py
```

Puis ouvre dans le navigateur : **http://localhost:5000**

---

### Étape 2 — Vérifier les transcriptions

| Touche clavier | Action |
|---|---|
| `V` | ✅ Valider (la transcription est correcte) |
| `C` | ✏️ Corriger (ouvre un champ pour modifier le texte) |
| `S` | ⏭️ Passer (audio incompréhensible) |
| `Espace` | ▶️ Play / Pause l'audio |
| `→` / `←` | Appel suivant / précédent |

> 💾 La progression est **sauvegardée automatiquement**.  
> Tu peux fermer et revenir, l'app reprend où tu t'es arrêtée.

---

### Étape 3 — Recevoir les nouvelles annotations de la binôme

Quand la binôme a fait `git push` :

```bash
cd f:\dgpc_pipeline_ready
git pull
```

Puis dans l'application, clique sur **"🔄 Recharger (après git pull)"**  
→ Les nouveaux appels annotés apparaissent automatiquement dans la liste !

---

### Étape 4 — Envoyer ses corrections

```bash
cd f:\dgpc_pipeline_ready
git add -A
git commit -m "verification session"
git push
```

---

### Étape 5 — Exporter le CSV final (quand tout est fini)

Dans l'application, clique sur **"📥 Exporter CSV vérifié"**  
→ Télécharge le fichier final avec toutes les corrections appliquées.  
→ C'est ce fichier qui servira à entraîner le modèle IA.

---

## 📡 Ce qui passe par Git et ce qui ne passe pas

| Élément | Via Git ? | Raison |
|---|---|---|
| Transcriptions CSV ✍️ | ✅ OUI | Petit fichier texte |
| Progression vérification 💾 | ✅ OUI | Petit fichier JSON |
| Fichiers audio .wav 🎵 | ❌ NON | Trop lourds pour GitHub |

> **Bonne nouvelle :** Les deux binômes ont déjà les audios 506-811 sur leurs machines localement.  
> Donc pas besoin de les partager via Git ou clé USB.

---

## ⚠️ Règles importantes

| ✅ À faire | ❌ À ne pas faire |
|---|---|
| `git pull` avant de commencer | Commencer sans faire `git pull` d'abord |
| `git push` après chaque session | Oublier de push en fin de session |
| Mettre les audios dans `audio_raw` | Modifier les CSV manuellement |
| Vérifier la transcription IA avant de valider | Valider sans écouter l'audio |
| Dire à l'autre "je suis à Appelle N" | Travailler sur les mêmes appels en même temps |

---

## 🔁 Coordination entre les deux binômes

### Règle principale

> **"Je dis où j'en suis, l'autre continue à partir de là."**

**Exemple :**
- Binôme A annote jusqu'à Appelle 620 → elle le dit
- Binôme B prend le relai à partir de Appelle 621
- Pendant ce temps, Binôme B vérifie les transcriptions 506-620

### Comment savoir où s'est arrêtée l'autre ?

Dans l'`annotation_app`, la sidebar montre :
- ✅ `[CORRIGÉ]` → appel annoté
- 📝 `[À TRAITER]` → appel pas encore annoté

---

## 📋 Résumé rapide (aide-mémoire)

```
Avant de commencer   →  git pull
Pendant le travail   →  annoter OU vérifier
Après chaque session →  git add -A && git commit -m "..." && git push
Nouvelles annotations de l'autre →  git pull puis "🔄 Recharger" dans l'app
Tout est fini        →  "📥 Exporter CSV vérifié" dans verification_tool
```

---

*Document créé le 04/03/2026 — Projet DGPC Béjaïa*
