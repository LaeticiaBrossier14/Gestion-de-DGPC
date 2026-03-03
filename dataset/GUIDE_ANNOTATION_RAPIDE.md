# GUIDE D'ANNOTATION RAPIDE — Appels DGPC Béjaïa
## Une décision en moins de 30 secondes par appel

---

## ÉTAPE 1 — La question principale

> **"Est-ce que cet appel nécessite qu'on envoie quelqu'un ?"**

```
OUI  → Vrai appel urgence     (tu en as déjà 400)
NON  → Continue vers Étape 2
```

---

## ÉTAPE 2 — Si NON, c'est lequel ?

### ❌ TYPE A — Faux appel
**Signal sonore :** rires, silence, enfant qui joue, raccroche vite  
**Signal texte :** très court, pas de lieu, pas de victime  
**Exemples terrain :**
- *"Allo allo..."* puis raccroche
- Enfant qui joue avec le téléphone
- Quelqu'un qui teste le numéro
- Insultes / provocation

```
intent        → false_alarm
urgency_human → low
incident_type → unknown
```

---

### 📞 TYPE B — Appel par erreur / mauvais numéro
**Signal :** cherche une autre administration  
**Exemples terrain :**
- *"C'est la gendarmerie ?"*
- *"C'est le 15 SAMU ?"*
- *"Allo la mairie ?"*
- L'opérateur redirige avec un autre numéro

```
intent        → other
urgency_human → low
incident_type → unknown
```

---

### 🔄 TYPE C — Mise à jour / suivi
**Signal :** l'appelant rappelle pour donner des nouvelles  
**Exemples terrain :**
- *"L'ambulance est arrivée, merci"*
- *"Finalement c'est bon"*
- *"Le blessé est décédé"*
- *"On a trouvé quelqu'un"*

```
intent        → update_info
urgency_human → low
incident_type → [même type que l'appel original]
```

---

### ❓ TYPE D — Question / renseignement
**Signal :** demande d'information, pas d'incident  
**Exemples terrain :**
- *"C'est quoi votre numéro ?"*
- *"Vous couvrez quelle zone ?"*
- *"C'est ouvert la nuit ?"*
- *"Comment ça marche pour faire une déclaration ?"*

```
intent        → other
urgency_human → low
incident_type → unknown
```

---

### 🔇 TYPE E — Inaudible / inutilisable
**Signal :** bruit, silence total, qualité audio nulle, 0 mot compréhensible  
**Action : NE PAS TRANSCRIRE — mettre de côté**

```
transcription → [INAUDIBLE]
intent        → other
urgency_human → unknown
incident_type → unknown
```

---

## ÉTAPE 3 — Tableau de décision rapide

| Ce que tu entends | Type | `intent` | `urgency_human` | `incident_type` |
|---|---|---|---|---|
| Rires / enfant / silence | ❌ Faux | `false_alarm` | `low` | `unknown` |
| "C'est la gendarmerie ?" | 📞 Erreur | `other` | `low` | `unknown` |
| "L'ambulance est arrivée" | 🔄 Màj | `update_info` | `low` | *[copier original]* |
| "Votre numéro svp ?" | ❓ Question | `other` | `low` | `unknown` |
| Rien compréhensible | 🔇 Inaudible | `other` | `unknown` | `unknown` |

---

## ÉTAPE 4 — Colonnes à remplir (minimum requis)

Pour les appels non-urgents, tu n'as besoin que de **5 colonnes** :

| Colonne dans l'app | Quoi mettre |
|---|---|
| `Transcription` (zone de texte) | Texte brut — même approximatif, même 1 phrase |
| `Intention appel` (selectbox) | 🚫 Faux appel / ❌ Autre / 🔄 Mise à jour |
| `Urgence (humain)` (selectbox) | 🟢 Faible ou ❓ Inconnu |
| `Type d'incident` (selectbox) | ❓ Inconnu (sauf mise à jour) |
| `Raisonnement` (zone de texte) | 1 phrase max — pourquoi tu as choisi ce label |

**Tout le reste** (victimes, feu, armes, localisation…) → laisser par défaut.

---

## Correspondance Guide ↔ App d'annotation

| Valeur guide | Bouton dans l'app |
|---|---|
| `false_alarm` | 🚫 Faux appel / Blague |
| `other` | ❌ Autre (erreur n°, test) |
| `update_info` | 🔄 Mise à jour |
| `report_incident` | 📞 Signalement d'incident |
| `request_help` | ❓ Demande d'aide |

---

## OBJECTIF PAR SESSION DE TRAVAIL

```
1 heure  →  écouter 30-40 appels
            annoter 20-25 utilisables
            écarter 5-10 inaudibles

Objectif total  →  200 appels non-urgents annotés
Temps estimé    →  8 à 10 heures de travail
```

---

## RÈGLE D'OR

> **En cas de doute entre faux appel et erreur → choisir "❌ Autre (erreur n°, test)".**  
> C'est plus honnête. Un faux appel intentionnel est rare.

> **En cas de doute sur la transcription → écrire ce que tu entends, même approximatif.**  
> Un texte imparfait vaut mieux qu'une ligne vide.

---

*Guide DGPC Béjaïa — Projet IA Protection Civile — Aligné avec l'app d'annotation v4.0*
