# Profil Linguistique — Dialecte Kabyle de Béjaïa (Tasahlit)
## Corpus de Référence : 97 appels d'urgence réels annotés & corrigés
> Extrait automatiquement le 15 février 2026 — `dataset/annotations_local.csv`

---


## 1. Vue d'ensemble du corpus

| Métrique | Valeur |
|----------|--------|
| Total appels | 97 |
| Longueur moyenne (chars) | 475 |
| Longueur médiane (chars) | 387 |
| Min / Max (chars) | 33 — 1511 |
| Mots moyen | 72 |
| Mots médiane | 60 |
| Min / Max (mots) | 4 — 242 |

**Règle guard** : Toute transcription synthétique doit avoir **≥ 30 chars et ≥ 8 mots**. Les transcriptions < 30 chars sont suspectes (4 dans le corpus réel = appels coupés/silences).

---

## 2. Profil Linguistique — Mix de langues

| Profil | Appels | % |
|--------|--------|---|
| **Kabyle dominant** (< 5% marqueurs FR) | 62 | 64% |
| **Mixte Kabyle-Français** (5-15% FR) | 35 | 36% |
| **Darija dominant** | 0 | 0% |

### 2.1 Observation clé
Le dialecte de Béjaïa est un **kabyle fortement francisé** :
- Marqueurs français : **297 occurrences** (termes techniques, urbanisme, médical)
- Marqueurs arabe/darija : **90 occurrences** (formules religieuses, interjections)
- Le kabyle fournit la **structure grammaticale** (verbes, morphologie, négation)
- Le français fournit le **vocabulaire technique** (ambulance, accident, bloc, étage, urgence)
- L'arabe fournit les **formules sociales** (salam, wallah, inchallah, barak allah)

**Règle guard** : Un appel 100% français ou 100% arabe est **invalide**. Il doit contenir au minimum 3 marqueurs kabyles (particules, verbes conjugués, négation).

---

## 3. Salutations & Ouverture (obligatoire)

| Formule | Occurrences | % des appels |
|---------|-------------|--------------|
| **Allo** | 62 | 64% |
| **Salam / Salamou alaykoum** | 36 | 37% |
| **Azul** | 3 | 3% |
| **Sba7 lkhir / Msa lkhir** | 3 | 3% |

### Patterns d'ouverture typiques (premiers mots)
```
Allo? Salam alaykoum.
Allo l'pompiers?
Allo l'7imaya?
Salam alaykoum, les pompiers n Bgayet?
Allo, l'ambulance?
Azul fell-awen.
Allo, Hmayai oui?
```

### Identification du service (fréquent)
| Expression | Signification | Fréquence |
|-----------|---------------|-----------|
| `l'pompiers` / `les pompiers` | Les pompiers | 38 (39%) |
| `l'ambulance` | L'ambulance | 21 (22%) |
| `l'himaya` / `7imaya` / `Hmayai` | La Protection Civile | 10 (10%) |
| `protection civile` | Protection Civile (FR) | 9 (9%) |

**Règle guard** : Tout appel synthétique doit commencer par une salutation dans le top-4.

---

## 4. Négation Kabyle (CRITIQUE pour l'authenticité)

### 4.1 Formes attestées dans le corpus

| Forme | Signification | Occurrences | Exemple attesté |
|-------|---------------|-------------|-----------------|
| **khati / xati** | Non | 17 | `Khati, deg l'social uksar` |
| **machi** | Ce n'est pas | 14 | `Machi tin n Souq el-Tnayn` |
| **ur ... ara** | Négation circumfixe (standard) | 2 | `Ur teqlaq ara` |
| **ulach / wlach** | Il n'y a pas | 4 | `ulachithn` (il n'y en a pas) |
| **la la** | Non non (darija) | 2 | `La la, mor l'tunnel` |

### 4.2 Règles de négation

1. **Négation verbale** : `ur + VERBE + ara` (circumfixe)
   - `ur teqlaq ara` (ne t'inquiète pas)
   - `uzmirara` = `u-zmir-ara` (il ne peut pas)
   - `it-respirerara` = contracté, mélangé FR (ne respire pas)

2. **Négation nominale** : `ulach` / `wlach` (= il n'y a pas)
   - `wlachitt` (il n'y en a pas du tout — féminin)
   - `ulac` (il n'y a pas)

3. **Négation identitaire** : `machi` (= ce n'est pas)
   - `machi tin n Souq el-Tnayn` (ce n'est pas celle de Souq el-Tnayn)
   - `machi enceinte` (elle n'est pas enceinte)

4. **Refus simple** : `khati` / `xati` (= non)
   - Réponse directe à une question oui/non

**Règle guard** : 
- `ur` ne doit JAMAIS apparaître sans `ara` dans la même proposition.
- `machi` doit être suivi d'un nom/adjectif, jamais d'un verbe conjugué.
- `khati` et `xati` sont interchangeables (variantes graphiques).

---

## 5. Affirmation

| Forme | Signification | Occurrences |
|-------|---------------|-------------|
| **an3am** | Oui (kabyle formel) | 36 |
| **ih / iyeh** | Oui (kabyle informel) | 8 |
| **d'accord** | D'accord (français) | 97 (quasi-universel) |
| **saha / sahit** | Merci / au revoir | 45 |
| **ouais** | Oui (français familier) | 3 |

**Observation** : `d'accord` est la formule la plus utilisée (97 occurrences), elle sert à la fois de confirmation et de clôture. `an3am` est le "oui" kabyle formel, `ih` le informel.

---

## 6. Conjugaison Verbale Kabyle

### 6.1 Préfixes de personne

| Préfixe | Personne | Exemple |
|---------|----------|---------|
| `i-` / `y-` | 3ème masc. sing. (il) | `i-ghli` (il est tombé), `y-eghli` |
| `t-` | 2ème pers. / 3ème fém. | `t-nuffes` (elle respire), `t-sa3` (tu as / elle a) |
| `n-` | 1ère pers. plur. (nous) | `n-as-d` (on vient), `n-teddu` (on y va) |
| `–gh` | 1ère pers. sing. (suffixe) | `steqsi-gh` (j'ai demandé), `zri-gh` (j'ai vu) |

### 6.2 Temps / aspects

| Marqueur | Temps | Exemple |
|----------|-------|---------|
| `ad-` / `at-` | **Futur / aoriste** | `ad-teddud` (tu viendras), `at-t-as` (elle viendra) |
| `tura` | **Maintenant** (adverbe) | `tura t-le7qed l'ambulance` (l'ambulance arrive maintenant) |
| `dayen` / `aqla-gh` | **Progressif / en cours** | `aqla-gh n-teddu-d` (on est en route) |
| prétérit (sans marque) | **Passé** | `i-ghli` (il est tombé), `t-qleb` (elle s'est renversée) |

### 6.3 Verbes d'urgence les plus fréquents

| Verbe | Sens | Occurrences | Formes attestées |
|-------|------|-------------|------------------|
| **ghli** | tomber / s'évanouir | 20 | `i-ghli`, `t-eghli`, `ye-ghli`, `theghli` |
| **che3l** | brûler / prendre feu | 5 | `tche3l`, `ch3el`, `ich3el`, `cha3let` |
| **doukh** | être étourdi/mal | 2 | `i-doukh`, `t-hdukh` |
| **yugh** | faire mal | 4 | `i-yugh`, `t-yugh`, `thyughun` |
| **arwa7** | venir (impératif) | 2 | `arwa7`, `arwa7-en` |
| **nuffes** | respirer | 3 | `t-nuffes`, `it-respirerara` (hybride!) |
| **teddu** | aller/se déplacer | 5 | `n-teddu`, `at-teddud`, `ttedund` |
| **ttawi** | emmener/transporter | 4 | `at-tawi-t`, `n-awi`, `attawimt` |

**Règle guard** : Un appel médical synthétique DOIT contenir au moins 1 verbe d'urgence parmi {ghli, doukh, yugh, nuffes}.

---

## 7. Particules et Connecteurs Kabyles (marqueurs d'authenticité)

### 7.1 Déictiques (lieu)

| Particule | Sens | Occurrences |
|-----------|------|-------------|
| `dayi` | ici | 23 |
| `dagi` | ici (variante) | 21 |
| `dinna` | là-bas | 9 |
| `anda` | où | 22 |
| `anida` | où (variante) | 8 |

### 7.2 Possession / Existence

| Particule | Sens | Occurrences |
|-----------|------|-------------|
| `nes3a` | nous avons | 6 |
| `is3a` | il a | 5 |
| `tes3a` | elle a | 1 |
| `yella` | il y a | ~10 |

### 7.3 Numéraux et quantificateurs

| Forme | Sens | Exemples attestés |
|-------|------|-------------------|
| `yiwen` | un (masc.) | `yiwen l'accident` |
| `yiweth` | une (fém.) | `yiweth teqchichth` (une petite fille) |
| `sin` | deux | `sin i-berdan` (deux fois) |
| `chwiya` | un peu | 28 occurrences |

### 7.4 Interrogatifs

| Forme | Sens | Occurrences |
|-------|------|-------------|
| `amek` | comment | 13 |
| `anda` / `anida` | où | 30 |
| `anwa` | lequel | 11 |
| `dachu` / `achu` | quoi | 15 |

**Règle guard** : Un appel synthétique de **≥ 50 mots** doit contenir au minimum **5 particules kabyles** de cette liste. Si < 5, le texte est probablement trop "français".

---

## 8. Termes d'adresse

| Forme | Registre | Occurrences |
|-------|----------|-------------|
| `a Madame` | Poli-mixte | 14 |
| `agma` | Frère (kabyle) | 7 |
| `khouya` / `khoya` | Frère (arabe) | 5 |
| `a sidi` | Monsieur (kabyle) | 4 |
| `7bib` / `7bbib` | Ami/cher | 2 |
| `la3nayek` | S'il te plaît | 3 |
| `ma3lich(e)` | Excusez / SVP | 12 |

---

## 9. Vocabulaire Médical / Urgence

### 9.1 Termes médicaux (kabylisés)

| Terme | Sens | Fréq. | Note |
|-------|------|-------|------|
| `l'ambulance` | ambulance | 33 | Terme FR maintenu |
| `sbitar` | hôpital | 7 | Kabylisation de "hôpital" |
| `l'malade` | le malade | 4 | Article kabyle + FR |
| `crise` | crise | 7 | `crise n'wul` (crise cardiaque) |
| `tension` | tension artérielle | 4 | FR maintenu |
| `l'oxygène` | oxygène | 3 | FR |
| `saturation` | saturation O₂ | 2 | Terme technique FR |
| `inconscient` | inconscient | 2 | FR maintenu |
| `cancéreuse` | cancéreuse | 4 | FR |
| `blessé(e)` | blessé | 5 | FR ou `iblissi` (kabylisé) |
| `l'hémorragie` | hémorragie | 1 | FR |

### 9.2 Expressions composées kabyle-français

| Expression | Sens | Registre |
|-----------|------|----------|
| `crise n'wul` | Crise cardiaque | Kabyle + FR |
| `l'ma3da-as` | Son estomac | Arabe + suffixe kabyle |
| `l'douleurs n l'cancer` | Les douleurs du cancer | FR avec connecteur kabyle |
| `teffas s't-kuffa` | Il mousse par la bouche | Kabyle pur |
| `l'tension sighlin` | La tension est partie | FR + verbe kabyle |
| `it-respirerara` | Il ne respire pas | FR + négation kabyle! |
| `il arrive pas à respirer` | FR pur dans contexte kabyle | Code-switch complet |

---

## 10. Vocabulaire Incendie / Feu

| Terme | Sens | Formes attestées |
|-------|------|------------------|
| `thmesth` / `tmess` | feu | `tche3l thmesth` (le feu a pris) |
| `n-nar` | feu (arabe) | `cha3let fiha n-nar` |
| `che3l` | brûler | `tche3l`, `ch3el`, `ich3el` |
| `ddaxan` | fumée | `ddaxan d berkan` (fumée noire) |
| `l'gaz` | gaz | `explosion de gaz` |
| `lekhyout n l'tricity` | câbles électriques | Hybride kabyle+FR |

---

## 11. Géographie & Localisation

### 11.1 Structure typique de localisation
```
[commune] + [quartier/cité] + [repère] + [détail]
```

Exemples attestés :
- `Ighzer Ouzarif, 2550 logements, le bloc 20, appartement 4`
- `Sidi Ali Labhar, 140 logements, les blocs n-vrid`
- `Seddouk ville, centre-ville, l'cafétéria Hidra`
- `Cité Djamaa, à l'extérieur, au 3ème cartier`

### 11.2 Communes les plus représentées
| Commune | Appels |
|---------|--------|
| Béjaïa | 48 |
| El Kseur | 7 |
| Seddouk | 5 |
| Sidi Aïch | 5 |
| Oued Ghir | 4 |
| Kherrata | 4 |
| Souk El Tenine | 3 |
| Amizour | 3 |
| Akbou | 3 |

### 11.3 Vocabulaire géographique kabylisé
| Terme | Sens |
|-------|------|
| `l'qa3a` | en bas / plaine |
| `ufella` | en haut |
| `uksar` | en bas (partie basse d'une cité) |
| `assawen` | la montée |
| `avrid` | la route |
| `l'piste` | la piste (chemin non goudronné) |
| `taddart` | le village |
| `l'brid` | la route |
| `l'pont` | le pont |

---

## 12. Convention d'Écriture (Romanisation Arabizi-Kabyle)

### 12.1 Chiffres pour consonnes emphatiques (Arabizi)

| Chiffre | Son | Arabe | Fréquence |
|---------|-----|-------|-----------|
| **3** | ع (ayn) | عين | 455 |
| **7** | ح (ha emphatique) | حاء | 194 |
| **9** | ق (qaf) | قاف | 31 |

### 12.2 Digrammes

| Digramme | Son | Fréquence |
|----------|-----|-----------|
| **gh** | غ (ghayn) | 212 |
| **th** | θ (tha spirante) | 156 |
| **ch** | ش (shin) | 323 |

### 12.3 Caractère Unicode kabyle (rare)
- `ɣ` (gamma kabyle standard) : 11 occurrences seulement
- Le corpus utilise massivement **arabizi** (`3`, `7`, `gh`) plutôt que la notation officielle INALCO/HCA.

**Règle guard** : La romanisation synthétique doit utiliser le système **arabizi** (3, 7, gh, ch, th) et NON pas les caractères ɛ, ħ, ɣ, ʃ de la notation linguistique académique.

---

## 13. Structure Dialogique

| Format | Appels | % |
|--------|--------|---|
| Avec étiquettes `Operator:`/`Caller:` | 3 | 3% |
| Avec tirets `—` pour tours de parole | 31 | 32% |
| Sans marquage (flux continu) | 63 | 65% |

### 13.1 Pattern dominant : flux continu sans étiquettes
Le texte alterne les répliques sans marqueur explicite. L'opérateur et l'appelant sont distingués par le contexte (questions vs réponses, ton formel vs informel).

### 13.2 Numéros de téléphone
- **15 appels (15%)** contiennent un numéro de téléphone (l'opérateur redirige vers une caserne locale)
- Format : `034 XX XX XX` ou `030 16 XX XX`

**Règle guard** : Les formats de dialogue acceptés sont : flux continu (majorité), tirets, ou étiquettes. Un seul format par transcription.

---

## 14. Pattern de clôture

| Expression | Sens | Fréquence |
|-----------|------|-----------|
| `saha` / `sahit` | Merci / au revoir | 45 |
| `d'accord` | D'accord | fréquent |
| `ya3tik sa7a` | Que Dieu te donne la santé | 5 |
| `barak allah fik` | Que Dieu te bénisse | 4 |
| `tanmirt` | Merci (kabyle pur) | 1 |
| `ar thilamt` | À la prochaine | 1 |
| `Rebbi i3awn-ik` | Que Dieu t'aide | 1 |

**Observation** : `saha`/`sahit` est quasi-universel. `tanmirt` (kabyle pur) est très rare — le dialecte béjaoui préfère `saha` (emprunt arabe).

---

## 15. Récapitulatif des Règles pour `guard_kabyle_language`

### Règles BLOQUANTES (rejet si violation)
| # | Règle | Seuil |
|---|-------|-------|
| R1 | Longueur minimale | ≥ 30 chars ET ≥ 8 mots |
| R2 | Salutation obligatoire | Doit commencer par Allo/Salam/Azul/Sba7 lkhir |
| R3 | Marqueurs kabyles minimum | ≥ 3 particules kabyles (dayi, dagi, tura, chwiya, an3am, etc.) |
| R4 | Romanisation arabizi | Doit utiliser 3/7/gh/ch et NON ɛ/ħ/ɣ/ʃ |
| R5 | Pas 100% français | Au moins 1 verbe kabyle conjugué |
| R6 | Négation bien formée | `ur` doit être accompagné de `ara` dans ±10 mots |

### Règles QUALITÉ (score 0-1, pénalité si violation)
| # | Règle | Pénalité |
|---|-------|----------|
| Q1 | Verbe d'urgence médical | -0.2 si medical_emergency et aucun verbe {ghli, doukh, yugh, nuffes} |
| Q2 | Vocabulaire feu | -0.2 si fire_* et aucun terme {thmesth, tmess, che3l, n-nar, ddaxan} |
| Q3 | Localisation structurée | -0.1 si pas de commune/quartier identifiable |
| Q4 | Clôture | -0.1 si pas de formule de clôture (saha, d'accord, etc.) |
| Q5 | Longueur réaliste | -0.15 si < 30 mots (médiane corpus = 60) |
| Q6 | Code-switching naturel | -0.1 si > 40% de mots français (ratio corpus: ~10-15%) |
| Q7 | Genre grammatical | -0.1 si yiwen (masc.) avec nom féminin, ou yiweth (fém.) avec nom masc. |

### Score final
```
score = 1.0 - sum(pénalités)
if any(BLOQUANTE violée): score = 0.0
if score >= 0.80: PASS
if 0.65 <= score < 0.80: → CRITIC (LLM review)
if score < 0.65: REJECT
```

---

## 16. Annexe : Glossaire Kabyle Béjaïa (extrait du corpus)

| Kabyle | Français | Catégorie |
|--------|----------|-----------|
| an3am | oui | affirmation |
| ih / iyeh | oui (informel) | affirmation |
| khati / xati | non | négation |
| machi | ce n'est pas | négation |
| ulach / wlach | il n'y a pas | négation |
| dayi / dagi | ici | déictique |
| dinna | là-bas | déictique |
| tura | maintenant | temporel |
| chwiya | un peu | quantificateur |
| yiwen / yiweth | un / une | numéral |
| amek | comment | interrogatif |
| anda / anida | où | interrogatif |
| dachu / achu | quoi | interrogatif |
| anwa | lequel | interrogatif |
| agma | frère | adresse |
| a sidi | monsieur | adresse |
| ma3lich | SVP / excusez | politesse |
| saha / sahit | merci / au revoir | clôture |
| la3nayek | SVP (plus insistant) | politesse |
| sbitar | hôpital | médical |
| l'qa3a | en bas / plaine | géographie |
| ufella | en haut | géographie |
| avrid / l'brid | route | géographie |
| taddart | village | géographie |
| ghli | tomber / s'évanouir | verbe urgence |
| che3l | brûler | verbe urgence |
| doukh | être étourdi | verbe urgence |
| yugh | faire mal | verbe urgence |
| nuffes | respirer | verbe urgence |
| teddu | aller/venir | verbe mouvement |
| ttawi | emmener | verbe mouvement |
| arwa7 | viens (impératif) | verbe mouvement |
