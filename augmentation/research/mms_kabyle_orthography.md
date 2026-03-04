# MMS Kabyle TTS — Guide d'orthographe et adaptation des données

## 1. Modèle : `facebook/mms-tts-kab`

- **Architecture** : VITS (Variational Inference + adversarial TTS)
- **Données d'entraînement** : Bible Kabyle (Nouveau Testament) en alphabet latin — source : Faith Comes By Hearing, bible.com
- **Pas de voice cloning** — voix unique synthétique
- **Sample rate** : 16000 Hz
- **Le tokenizer normalise** : lowercased, sans ponctuation

## 2. Vocabulaire du tokenizer (38 caractères)

```
Acceptés : a b c d e f g h i j k l m n q r s t u w x y z
           ɛ ḥ ɣ ṛ ṭ ẓ ṣ č ǧ ḍ
           (espace) ' - |

Refusés  : o  p  v  ḏ  ṯ
```

### Règles de remplacement pour les lettres refusées

| Refusé | → Remplacé par | Justification |
|--------|---------------|---------------|
| `o` | `u` | Le Kabyle officiel n'a pas de /o/, utilise /u/ |
| `p` | `b` | Pas de /p/ en Kabyle natif, le plus proche est /b/ |
| `v` | `b` | Bien que le Kabyle parlé utilise /v/ (ex: vava), le tokenizer MMS ne l'a pas (Bible utilise `b`) |
| `ḏ` | `d` | Spirantisé — pas dans le vocab MMS, utiliser `d` simple |
| `ṯ` | `t` | Spirantisé — pas dans le vocab MMS, utiliser `t` simple |

> **Note importante** : Le Kabyle parlé utilise `v` (ex: vava = père), mais la Bible Kabyle d'entraînement MMS utilise `b` à la place. Donc on doit écrire `baba` pour que MMS le prononce.

## 3. Exemples réels de la Bible Kabyle (données MMS)

### Matta (Matthieu) chapitre 13
```
Ass-nni kan, Sidna Ɛisa yeffeɣ-ed seg wexxam, iṛuḥ ad iqqim ṛṛif n lebḥeṛ.
Aṭas n lɣaci i d-yessnejmaɛen ɣuṛ-es.
Ițmeslay-asen s lemtul, yeqqaṛ-asen: Yiwen umusaw yeffeɣ ad izzeṛɛ.
Mi gella yeẓẓu, kṛa n zzeṛṛiɛa yeɣli ɣef yiṛi n webṛid.
```

### Yuhenna (Jean) chapitre 1
```
Di tazwaṛa yella Wawal, Wawal yella ɣeṛ Ṛebbi, Wawal yella d Ṛebbi.
Netta yella ɣeṛ Ṛebbi si tazwaṛa.
Kṛa yellan, yexdem-it s Wawal.
Deg-s i tella tudeṛt, tudeṛt-agi tella d tafat n yemdanen.
```

### Déclaration des droits de l'homme (Kabyle)
```
Imdanen, akken ma llan ttlalen d ilelliyen msawan di lḥweṛma d yizeṛfan.
Ɣuṛ-sen tamsakwit d lɛaquel u yessefk ad-tili tegmatt gaṛ-asen.
```

### Patterns orthographiques clés observés

| Pattern | Exemples | Signification |
|---------|----------|---------------|
| Lettres doublées | `yeffeɣ`, `wexxam`, `yeqqaṛ`, `ttlalen` | Consonnes emphatiques/longues |
| Particule `-d`/`-ed` | `yeffeɣ-ed`, `ǧǧan-d`, `d-yuli` | Particule de direction (vers ici) |
| Particule `ɣuṛ-` | `ɣuṛ-es`, `ɣuṛ-sen` | "chez" + pronom |
| `ṛ` (r emphatique) | `Ṛebbi`, `lebḥeṛ`, `webṛid`, `ṛṛif` | Très fréquent en Kabyle |
| `ɛ` (ayin) | `Ɛisa`, `lɛaquel`, `izzeṛɛ` | Son pharyngal |
| `ɣ` (gamma) | `yeffeɣ`, `ɣeṛ`, `yeɣli` | Son vélaire |
| `ḥ` (ha emphatique) | `Lmasiḥ`, `lḥweṛma`, `acḥal` | Pharyngal sourd |
| `ṭ` (t emphatique) | `aṭas` (beaucoup), `ṭṭlam` | Consonne emphatique |
| Négation `ur...ara` | `ur yesɛi ara`, `ur tt-yessin ara` | Structure de négation |

## 4. Mapping arabizi → orthographe MMS

### Digrammes (traiter d'abord, ordre important)

| Arabizi | → MMS | Son |
|---------|-------|-----|
| `gh` | `ɣ` | gamma — iɣli, ɣef |
| `ch` | `c` | affriquée — acemma |
| `kh` | `x` | fricatif — axxam |

### Chiffres arabizi (dans les mots uniquement)

| Arabizi | → MMS | Exemple |
|---------|-------|---------|
| `7` | `ḥ` | 7imaya → ḥimaya |
| `3` | `ɛ` | an3am → anɛam |
| `9` | `q` | ta9aryeth → taqaryeth |

### Protection des numéros

Les numéros de téléphone (034 86 07 80) et les chiffres seuls (bloc 5, cité 200) doivent être **protégés** avant la conversion arabizi pour ne pas transformer le `7` de `07` en `ḥ`.

## 5. Problème du code-switching (Kabyle + Français)

### Le défi
Nos transcriptions mélangent Kabyle, français et arabe. MMS ne sait prononcer **que le Kabyle**. Les mots français sont mal prononcés car MMS lit chaque lettre comme du Kabyle (ex: `exact` → il prononce le `x` comme /x/ kabyle au lieu de /gz/).

### Solution : kabyliser les mots français
Écrire les mots français avec la **phonétique Kabyle** pour que MMS les prononce naturellement avec un accent Kabyle :

| Français | → Kabyle phonétique | Justification |
|----------|-------------------|---------------|
| exact | igzakt | prononciation réelle |
| ambulance | ambilans | pas de o ni p |
| pompiers | bumbiyi | p→b, o→u, ier→iyi |
| accident | aksidan | cc→ks, en→an |
| protection | bruteksyun | p→b, o→u |
| envoyez | anfwayi | v→f... ou garder comme mot Kabyle `aznem` |
| voiture | tumubil | terme Kabyle réel |
| maison | axxam | terme Kabyle réel |
| oui | ih | terme Kabyle réel |
| merci | tanemmirt | terme Kabyle réel |
| vite | deɣya | terme Kabyle réel |
| maintenant | tura | terme Kabyle réel |

> **Stratégie recommandée** : privilégier les **vrais mots Kabyle** quand ils existent (axxam, tumubil, deɣya, tanemmirt, ih) plutôt que de "kabyliser" le français. Les mots français sans équivalent Kabyle courant peuvent être kabylisés phonétiquement.

## 6. Adaptation de la génération de données

### Pipeline actuel
```
Transcription arabizi → arabizi_normalizer.py (IPA) → F5-TTS/XTTS-v2
```

### Pipeline adapté pour MMS Kabyle
```
Transcription arabizi → to_mms() converter → MMS Kabyle TTS → filtre téléphonique 8kHz
```

### Étapes du convertisseur `to_mms()`
1. Lowercase + strip
2. Protéger les numéros de téléphone
3. Remplacer les mots français par leurs équivalents Kabyle (dictionnaire)
4. Convertir les digrammes arabizi (`gh`→`ɣ`, `ch`→`c`, `kh`→`x`)
5. Convertir les chiffres arabizi (`7`→`ḥ`, `3`→`ɛ`, `9`→`q`)
6. Remplacer les lettres hors vocab (`o`→`u`, `p`→`b`, `v`→`b`)
7. Retirer toute ponctuation + caractères non-MMS
8. Restaurer les numéros

### Post-processing audio
- Bandpass 300-3400 Hz (bande téléphonique)
- Resample 16kHz → 8kHz (G.711)
- Optionnel : injection de bruit à SNR variable (8-20 dB)

## 7. Limites et alternatives

| Aspect | MMS Kabyle | F5-TTS | XTTS-v2 |
|--------|-----------|--------|---------|
| Kabyle natif | ✅ Oui | ❌ Non | ❌ Non (arabe/FR) |
| Voice cloning | ❌ Non | ✅ Oui | ✅ Oui |
| Code-switching | ❌ Kabyle seul | ✅ Bon | ✅ Bon |
| Qualité voix | Robotique | Naturelle | Naturelle |
| VRAM | ~1 GB | ~8 GB | ~4 GB |
| Vitesse | Très rapide | Moyen | Moyen |
| Colab gratuit | ✅ T4 OK | ⚠️ wandb bug | ❌ pip install fail (Py 3.12) |

### Stratégie hybride (à explorer)
1. **MMS Kabyle** pour les mots/phrases en Kabyle pur
2. **F5-TTS** pour les parties en français (avec voice cloning)
3. Concaténer les segments par tour de parole

## 8. Prochaines étapes

- [ ] Faire valider le scénario démo par un locuteur Kabyle natif
- [ ] Enrichir le dictionnaire français → Kabyle avec les mots fréquents du corpus (362× la, 126× pompiers, 108× ambulance...)
- [ ] Tester la qualité MMS sur 10 scénarios variés
- [ ] Explorer le pipeline hybride MMS + F5-TTS
- [ ] Ajuster le `SPEED_FACTOR` pour un débit naturel
- [ ] Tester si le fine-tuning MMS est possible pour ajouter `v` au vocabulaire
