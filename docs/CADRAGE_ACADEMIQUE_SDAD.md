# Cadrage Académique — PFE M2 SDAD × Projet ASR Urgences DGPC
> Dernière mise à jour : 9 février 2026  
> Auteur : Rayan T. — M2 Science de Données et Aide à la Décision  
> Établissement : Université A. MIRA de Béjaïa — Faculté Sciences Exactes — Département RO

---

## 1. Positionnement du Master

### 1.1 Identité du programme
| Champ | Valeur |
|-------|--------|
| **Domaine** | Mathématiques et Informatique |
| **Filière** | Mathématiques Appliquées |
| **Spécialité** | Science de Données et Aide à la Décision (SDAD) |
| **Département** | Recherche Opérationnelle |
| **Faculté** | Sciences Exactes |

### 1.2 Compétences visées par le programme
Le master SDAD forme des spécialistes capables de :
- Extraire et traiter l'information depuis n'importe quel support (texte, image, audio)
- Modéliser et résoudre des problèmes complexes d'aide à la décision
- Fournir une analyse de données adéquate pour les problèmes de prise de décision
- Combiner science des données appliquée et cadres décisionnels
- Développer une compréhension approfondie corrélation vs causalité

### 1.3 Débouchés cités dans le programme
1. Data Scientists, Data Miners
2. Chefs de projets en informatique décisionnelle
3. Concepteurs d'outils logiciels spécialisés
4. Ingénieurs de recherche et développement
5. Consultants experts en décisionnel

> **Notre projet couvre les débouchés 1, 2, 3 et 4 simultanément.**

---

## 2. Alignement Projet ↔ Programme SDAD

### 2.1 Cartographie modules → composantes du projet

| Module SDAD (Semestre) | Composante du projet | Correspondance |
|---|---|---|
| **Fondement de data sciences** (S1) | Pipeline bout-en-bout Audio→JSON→Décision | Collecte, préparation, nettoyage, deep learning, classification |
| **Python pour data science** (S1) | Tout le pipeline (Python, Streamlit, PyTorch, Pydantic) | NumPy, Pandas, scikit-learn, ML, visualisation |
| **Management de projets** (S1) | 7 sprints planifiés, diagramme de Gantt, gestion risques | PERT, MPM, Gantt, gestion des ressources |
| **Entreprenariat** (S1) | Label Startup "Data Algérie", business model | Business plan, analyse de marché |
| **Optimisation discrète** (S1) | `compute_dispatch()` = affectation optimale des moyens | Problèmes classiques de RO |
| **Machine Learning pour big data** (S2) | Whisper V3 fine-tuning, Qwen 2.5 QLoRA | Algorithmes ML, feature engineering, surapprentissage |
| **Système d'info. décisionnel & entrepôt** (S2) | 234K enregistrements legacy → plateforme décisionnelle | Architecture SID, ETL, datamarts |
| **Techniques d'optimisation avancées** (S2) | `compute_urgency()` = optimisation multicritère | Optimisation multi-objectif, Pareto |
| **Génie logiciel** (S2) | Architecture pipeline modulaire, tests, CI | Cycle de vie logiciel, UML |
| **Apprentissage & optimisation statistiques** (S3) | Fine-tuning Whisper/Qwen, hyperparamètres, benchmarks | Qualité de prévision, risque, régression PLS |
| **Business Intelligence** (S3) | Tableau de bord DGPC, KPIs, visualisation | Entrepôts, visualisation, intelligence prédictive |
| **Data mining et applications** (S3) | Extraction d'information depuis appels d'urgence | Application en sécurité civile (cf. applications en santé) |
| **Optimisation chaîne logistique** (S3) | Dispatch = routage des moyens d'intervention | Problèmes de transport, localisation |
| **Théorie des jeux** (S3) | Allocation de ressources entre équipes A/B/C | Jeux coopératifs, allocation de ressources |
| **Modèles linéaires généralisés** (S2) | Baselines logistic regression pour benchmark | Régression logistique, modèle log-linéaire |
| **Rédaction scientifique** (S3) | Le mémoire lui-même | Structure, méthodologie, communication |

### 2.2 Taux de couverture
- **15 modules sur 17** du programme sont directement mobilisés par le projet
- Seuls "Cryptographie" (S1) et "Analyse de survie" (S1) ne sont pas directement concernés
- **Taux de couverture ≈ 88%** — exceptionnel pour un PFE

---

## 3. Formalisation Mathématique pour le Jury RO/SDAD

Le jury attend des **mathématiques** et de l'**aide à la décision**, pas uniquement du code. Voici comment traduire chaque composante dans leur langage.

### 3.1 ASR = Problème d'estimation statistique

*Module concerné : Apprentissage et optimisation statistiques (S3)*

$$\hat{T} = \arg\max_{T} P(T \mid A; \theta)$$

où :
- $A$ = signal audio d'entrée
- $T$ = transcription textuelle
- $\theta$ = paramètres du modèle Whisper V3
- $\hat{T}$ = transcription optimale

**Fine-tuning kabyle** : On cherche $\theta^*$ tel que :

$$\theta^* = \arg\min_{\theta} \mathcal{L}(\theta) = -\sum_{i=1}^{N} \log P(T_i \mid A_i; \theta)$$

avec $N$ = taille du corpus d'entraînement kabyle.

**Métrique d'évaluation** — Word Error Rate (WER) :

$$\text{WER} = \frac{S + D + I}{N_{ref}}$$

où $S$ = substitutions, $D$ = suppressions, $I$ = insertions, $N_{ref}$ = mots de référence.

### 3.2 Extraction structurée = Problème de classification multi-tâches

*Module concerné : Machine Learning pour big data (S2), Data mining (S3)*

Soit $T$ la transcription. Le LLM (Qwen 2.5 7B) réalise une extraction multi-tâches :

$$f: T \mapsto (y_1, y_2, \ldots, y_k)$$

où chaque $y_j$ est une variable catégorielle ou numérique :

| Variable $y_j$ | Type | Domaine |
|---|---|---|
| $y_1$ : `incident_type` | Catégoriel (14 classes) | $\{$FIRE, ACCIDENT, MEDICAL, ...$\}$ |
| $y_2$ : `injury_severity` | Ordinal (5 niveaux) | $\{$NONE, MINOR, MODERATE, SEVERE, CRITICAL$\}$ |
| $y_3$ : `victims_count` | Entier | $\mathbb{N}$ |
| $y_4$ : `fire_present` | Ternaire | $\{$YES, NO, UNKNOWN$\}$ |
| $y_5$ : `trapped_persons` | Ternaire | $\{$YES, NO, UNKNOWN$\}$ |
| $y_6$ : `weapons_involved` | Ternaire | $\{$YES, NO, UNKNOWN$\}$ |
| $y_7$ : `hazmat_involved` | Ternaire | $\{$YES, NO, UNKNOWN$\}$ |
| $y_8$ : `location_description` | Texte structuré | Commune × Daïra × Lieu |

**Contrainte de décodage** (Outlines) : La sortie est contrainte à un schéma JSON-Schema valide :

$$\hat{y} \in \mathcal{Y}_{valid} \subset \mathcal{Y}_{all}$$

Cela élimine les hallucinations structurelles et garantit la conformité ontologique.

### 3.3 Urgence = Problème d'optimisation multicritère (arbre de décision)

*Module concerné : Techniques d'optimisation avancées (S2), Optimisation discrète (S1)*

$$u^* = \arg\max_{u \in \{U1, U2, U3, U4, U5\}} f(x_1, x_2, \ldots, x_8)$$

La fonction $f$ est un **arbre de décision déterministe** à 16 règles, implémenté dans `compute_urgency()` :

```
Règle 1 : SI weapons_involved = YES  → U5 (CRITIQUE)
Règle 2 : SI hazmat_involved = YES   → U5 (CRITIQUE)
Règle 3 : SI trapped_persons = YES ∧ injury_severity ∈ {SEVERE, CRITICAL} → U5
Règle 4 : SI fire_present = YES ∧ incident_type = FIRE → U4 (TRÈS ÉLEVÉE)
...
Règle 16 : SINON → U1 (FAIBLE)
```

**Propriétés formelles** de l'arbre :
- **Complétude** : $\forall x \in \mathcal{X}, \exists!\ u : f(x) = u$ (toute entrée produit exactement une sortie)
- **Déterminisme** : même entrée → même sortie (pas de stochasticité)
- **Monotonicité** : si la gravité d'un facteur augmente, l'urgence ne diminue jamais
- **Transparence** : chaque décision est traçable et explicable (pas de boîte noire)

> **Séparation critique** : Le LLM extrait les **FAITS** ($x_1, \ldots, x_8$). Le CODE calcule la **DÉCISION** ($u^*$). Cela garantit reproductibilité et auditabilité — essentiel en contexte d'urgence.

### 3.4 Dispatch = Problème de transport / affectation

*Module concerné : Optimisation chaîne logistique (S3), Optimisation discrète (S1)*

$$\min \sum_{i,j} c_{ij} \cdot x_{ij}$$

sous contraintes :

$$\sum_j x_{ij} \geq d_i \quad \forall i \quad \text{(satisfaction des besoins)}$$
$$\sum_i x_{ij} \leq s_j \quad \forall j \quad \text{(capacité des unités)}$$
$$x_{ij} \in \{0, 1\} \quad \text{(affectation binaire)}$$

où :
- $d_i$ = besoins calculés par `compute_dispatch()` (ambulances, camions, etc.)
- $s_j$ = capacité de l'unité d'intervention $j$
- $c_{ij}$ = coût d'affectation (distance, temps de trajet)
- $x_{ij}$ = 1 si l'unité $j$ est affectée au besoin $i$

### 3.5 Fusion texte × prosodie = Combinaison convexe de scores

*Module concerné : Apprentissage et optimisation statistiques (S3), Analyse discriminante*

$$U_{final} = \alpha \cdot U_{texte} + (1 - \alpha) \cdot U_{prosodie}$$

où :
- $U_{texte} \in [0, 1]$ = score d'urgence issu de l'extraction textuelle
- $U_{prosodie} \in [0, 1]$ = score de stress issu de openSMILE (features acoustiques : F0, jitter, shimmer, HNR, énergie)
- $\alpha \in [0, 1]$ = poids de fusion

**Optimisation du poids** par validation croisée :

$$\alpha^* = \arg\min_{\alpha \in [0,1]} \frac{1}{K} \sum_{k=1}^{K} \mathcal{L}_{k}(\alpha)$$

où $K$ = nombre de folds, $\mathcal{L}_k$ = erreur de classification sur le fold $k$.

---

## 4. Stratégie de Benchmark — Baselines classiques vs Pipeline avancé

### 4.1 Pourquoi des baselines classiques ?

Le jury SDAD a enseigné SVM, régression logistique, arbres de décision, k-NN, Naïve Bayes, Random Forest. Il faut **montrer qu'on maîtrise ces méthodes** (validation des acquis) **puis démontrer que le pipeline avancé fait mieux** (contribution).

### 4.2 Design expérimental

```
┌─────────────────────────────────────────────────┐
│                DONNÉES (320 appels)              │
├───────────┬──────────────┬──────────────────────┤
│ Train 70% │ Validation   │ Test 15%             │
│ (224)     │ 15% (48)     │ (48)                 │
│ réel +    │ réel SEUL    │ réel SEUL            │
│ synthétique│              │ (JAMAIS touché)      │
└───────────┴──────────────┴──────────────────────┘
```

**Règle absolue** : données synthétiques JAMAIS dans eval/test.

### 4.3 Tableau comparatif des méthodes

| Méthode | Type | Features | Module SDAD |
|---|---|---|---|
| **TF-IDF + SVM** | Baseline 1 | Bag-of-words | ML big data (S2) |
| **TF-IDF + Logistic Regression** | Baseline 2 | Bag-of-words | Modèles linéaires (S2) |
| **TF-IDF + Random Forest** | Baseline 3 | Bag-of-words | ML big data (S2) |
| **TF-IDF + Decision Tree** | Baseline 4 | Bag-of-words | ML big data (S2) |
| **Word2Vec + k-NN** | Baseline 5 | Embeddings | ML big data (S2) |
| **BERT fine-tuné** | Méthode intermédiaire | Contextual embeddings | Apprentissage stat (S3) |
| **Qwen 2.5 7B QLoRA + Outlines** | Notre pipeline | Constrained LLM decoding | — (contribution) |

### 4.4 Métriques d'évaluation

Pour chaque méthode, on rapporte :

| Métrique | Formule | Usage |
|---|---|---|
| **Accuracy** | $\frac{TP + TN}{N}$ | Vue globale |
| **Precision** | $\frac{TP}{TP + FP}$ | Faux positifs critiques (dispatch inutile) |
| **Recall** | $\frac{TP}{TP + FN}$ | Faux négatifs critiques (urgence manquée) |
| **F1-score** | $\frac{2 \cdot P \cdot R}{P + R}$ | Compromis P/R |
| **F1-macro** | $\frac{1}{C}\sum_{c=1}^{C} F1_c$ | Équilibre entre classes |
| **Matrice de confusion** | $M_{ij}$ = nb de $i$ prédits $j$ | Analyse des erreurs |
| **WER** (ASR) | $\frac{S+D+I}{N_{ref}}$ | Qualité transcription |
| **Temps d'inférence** | $t$ (secondes) | Contrainte temps réel |

> **En contexte d'urgence, le Recall est prioritaire sur la Precision** : mieux vaut envoyer une ambulance de trop que rater un blessé.

### 4.5 Résultat attendu

```
                    Accuracy   F1-macro   Recall
TF-IDF + SVM         0.65       0.58      0.52
TF-IDF + LogReg      0.63       0.55      0.49
TF-IDF + RF          0.68       0.61      0.55
BERT fine-tuné        0.78       0.73      0.71
Qwen QLoRA+Outlines   0.89       0.86      0.91  ← notre pipeline
```

> Ces chiffres sont des **estimations préliminaires** à valider expérimentalement.

---

## 5. Structure du Mémoire — Recalibrée pour SDAD

### 5.1 Plan détaillé

| Chapitre | Titre | Contenu | Modules SDAD mobilisés |
|---|---|---|---|
| **Introduction** | Contexte, problématique, objectifs | Présentation DGPC, enjeux multilingues, questions de recherche | — |
| **Ch1** | État de l'art | ASR multilingue, NLP pour l'urgence, systèmes décisionnels d'urgence, revue des architectures existantes | Fondement data sciences, BI |
| **Ch2** | Données & Méthodologie | Analyse statistique des 234K appels legacy, ontologie (14 types, 5 urgences), protocole d'annotation (320 appels), knowledge base géographique | Data mining, Entrepôt de données |
| **Ch3** | Pipeline & Modélisation | ASR (Whisper V3 FT) → Extraction (Qwen QLoRA) → Post-traitement (`compute_urgency`, `compute_dispatch`), formalisé mathématiquement | ML, Apprentissage stat, Optimisation |
| **Ch4** | Résultats & Benchmarks | WER, F1, matrice confusion, comparaison 6 baselines vs pipeline, courbes d'apprentissage, ablation study, temps d'inférence | Modèles linéaires, Classification |
| **Conclusion** | Synthèse & Perspectives | Prototype déployable, limites, perspectives plateforme décisionnelle, roadmap | BI, Aide à la décision |
| **Annexe A** | Volet Entrepreneurial | Business model canvas, analyse de marché, KPIs DGPC (preuve du besoin), roadmap startup | Entreprenariat, Management projets |
| **Annexe B** | Détails techniques | Schémas JSON, prompts, configuration fine-tuning, code key functions | Python pour data science |
| **Annexe C** | Planning projet | Diagramme de Gantt (7 sprints), PERT, gestion des risques | Management de projets |

### 5.2 Comment chaque chapitre sert les deux diplômes

```
                    Jury M2 SDAD          Comité Startup Label
                    ─────────────         ──────────────────
Introduction        ✓ Problématique       ✓ Contexte marché
Ch1 État de l'art   ✓✓ Rigueur biblio     · (peu pertinent)
Ch2 Données         ✓✓ Méthodologie       ✓ Preuve du besoin (234K)
Ch3 Pipeline        ✓✓ Formalisation      ✓ Innovation technique
Ch4 Résultats       ✓✓ Benchmarks         ✓✓ Preuves de performance
Conclusion          ✓ Synthèse            ✓✓ Vision produit
Annexe A            · (bonus)             ✓✓ Business model
Annexe B            ✓ Détails techniques  · (peu pertinent)
Annexe C            ✓ Gestion de projet   ✓ Planning réaliste
```

---

## 6. Avantage Compétitif devant le Jury

### 6.1 Comparaison avec un PFE SDAD typique

| Critère | PFE SDAD typique | Notre projet |
|---|---|---|
| **Données** | Dataset Kaggle (public, nettoyé) | 234K appels réels DGPC + 320 appels annotés manuellement |
| **Client** | Fictif ou académique | DGPC Béjaïa (Protection Civile — vrai client institutionnel) |
| **Problème** | Classification standard | Aide à la décision en temps réel pour urgences vitales |
| **Pipeline** | Un notebook Jupyter isolé | Pipeline bout-en-bout Audio → JSON → Décision |
| **Méthodes** | SVM vs Random Forest | Baselines classiques + LLM + ASR + prosodie (state-of-the-art) |
| **Langues** | Français ou anglais | Kabyle + arabe dialectal + français (trilinguisme — rare) |
| **Entrepreneuriat** | Aucun | Label startup "Data Algérie" (double diplôme) |
| **Déploiement** | Aucun | Prototype déployable avec interface Streamlit |
| **Impact social** | Faible | Sauver des vies — optimisation des temps de réponse |

### 6.2 Les 5 arguments massue

1. **Données réelles d'un vrai client** — le jury voit trop de projets sur des données Kaggle. Des données réelles de la Protection Civile, c'est du concret.

2. **Aide à la décision littérale** — « Quelle équipe envoyer ? Quelle urgence ? » C'est **exactement** le titre du master.

3. **Pipeline complet, pas un notebook** — conception logicielle modulaire, tests, ontologie formelle, gestion de projet en sprints.

4. **Formalisation mathématique** — on parle le langage du jury : optimisation multicritère, problème d'affectation, estimation statistique, validation croisée.

5. **Double valorisation** — diplôme académique + label startup. Le module "Entreprenariat" (S1) n'est plus un cours abstrait, il est appliqué.

---

## 7. Méthodologie Expérimentale

### 7.1 Protocole de validation

```
┌─────────────────────────────────────────────────────────┐
│ 1. COLLECTE                                              │
│    320 appels réels → annotation manuelle (2 annotateurs)│
│    Inter-annotator agreement (Cohen's κ)                 │
├─────────────────────────────────────────────────────────┤
│ 2. PRÉTRAITEMENT                                         │
│    Audio : normalisation, VAD, segmentation              │
│    Texte : tokenisation, nettoyage                       │
├─────────────────────────────────────────────────────────┤
│ 3. SPLIT STRATIFIÉ                                       │
│    Train (70%) + Val (15%) + Test (15%)                  │
│    Stratifié par incident_type (min 50/type)             │
│    Synthétique → Train UNIQUEMENT                        │
├─────────────────────────────────────────────────────────┤
│ 4. ENTRAÎNEMENT                                          │
│    Whisper V3 fine-tuning (ASR kabyle)                   │
│    Qwen 2.5 7B QLoRA (extraction structurée)             │
│    Baselines classiques (SVM, LogReg, RF, DT, k-NN)     │
├─────────────────────────────────────────────────────────┤
│ 5. ÉVALUATION                                            │
│    Validation set → sélection modèle + hyperparamètres  │
│    Test set → métriques finales (JAMAIS utilisé avant)   │
│    Cross-validation K=5 sur les baselines                │
├─────────────────────────────────────────────────────────┤
│ 6. ANALYSE                                               │
│    Matrice de confusion, courbes ROC/PR                  │
│    Ablation study (ASR seul, extraction seule, fusion)   │
│    Analyse d'erreurs qualitative                         │
│    Test de significativité statistique (McNemar)          │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Critères de qualité scientifique

| Critère | Comment on le satisfait |
|---|---|
| **Reproductibilité** | Code versionné (Git), seeds fixés, configs documentées |
| **Validité interne** | Split stratifié, pas de data leakage, cross-validation |
| **Validité externe** | Données réelles DGPC (pas synthétiques dans eval/test) |
| **Significativité** | Tests statistiques (McNemar, bootstrap CI) |
| **Transparence** | Décisions déterministes, prompts versionnés, logs |
| **Éthique** | Anonymisation des données, convention avec DGPC |

---

## 8. Analyse Statistique des Données Legacy (234K appels)

### 8.1 Ce qu'on peut montrer dans le Ch2

À partir des 234K enregistrements du système 0666 (2018-2025) :

| Analyse | Méthode | Module SDAD |
|---|---|---|
| Distribution temporelle des appels | Séries temporelles, saisonnalité | Fondement data sciences |
| Répartition géographique (52 communes) | Visualisation, cartes de chaleur | Data mining applications |
| Corrélation type d'intervention × saison | Test du χ², V de Cramér | Modèles linéaires |
| Durée moyenne d'intervention par type | ANOVA, boxplots | Apprentissage stat |
| Prédiction de la charge (nb appels/jour) | Régression, ARIMA | Apprentissage stat |
| Clustering des communes par profil d'appel | K-means, CAH | ML big data |
| Mapping 35 types legacy → 14 IncidentType | Analyse qualitative | Data mining |

> Ces analyses ne nécessitent **aucun ASR** — ce sont des données tabulaires du système existant. Elles démontrent le besoin et la faisabilité.

### 8.2 KPIs pour le label startup

| KPI | Source | Valeur attendue |
|---|---|---|
| Nb appels/an | Legacy 234K / 7 ans | ~33K appels/an |
| Temps moyen de traitement | Legacy | À mesurer |
| Taux de mauvaise catégorisation | Audit DGPC | À estimer |
| Gain potentiel (temps) | Pipeline vs manuel | Objectif : -40% |
| Couverture linguistique | Kabyle + arabe + français | 95% des appelants |

---

## 9. Architecture du Pipeline — Formalisation

### 9.1 Diagramme formel

```
                    ┌──────────┐
                    │  Audio   │
                    │   A(t)   │
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              ▼                     ▼
    ┌───────────────┐     ┌───────────────┐
    │  Whisper V3   │     │  openSMILE    │
    │  θ* fine-tuné │     │  Prosodie     │
    │  P(T|A;θ*)    │     │  φ(A) → s    │
    └───────┬───────┘     └───────┬───────┘
            │                     │
            ▼                     │
    ┌───────────────┐             │
    │  Qwen 2.5 7B  │             │
    │  QLoRA+Outlines│            │
    │  f(T) → Y     │             │
    └───────┬───────┘             │
            │                     │
            ▼                     │
    ┌───────────────┐             │
    │ Post-traitement│            │
    │ déterministe   │◄───────────┘
    │ g(Y,s) → D    │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │ EmergencyCall │
    │ (output final)│
    └───────────────┘
```

### 9.2 Définitions formelles

| Symbole | Signification | Domaine |
|---|---|---|
| $A(t)$ | Signal audio | $\mathbb{R}^T$ (T échantillons) |
| $\theta^*$ | Paramètres Whisper fine-tunés | $\mathbb{R}^p$ |
| $T$ | Transcription | Séquence de tokens |
| $s$ | Score de stress (prosodie) | $[0, 1]$ |
| $Y = (y_1, \ldots, y_k)$ | Faits extraits | $\mathcal{Y}_1 \times \cdots \times \mathcal{Y}_k$ |
| $u^*$ | Niveau d'urgence | $\{U1, U2, U3, U4, U5\}$ |
| $D$ | Décision de dispatch | $\{$moyens, personnel$\}$ |

### 9.3 Propriété de séparation LLM / Code

**Théorème (informel)** : La séparation extraction (LLM) / décision (code déterministe) garantit :
1. **Reproductibilité** : $g(Y, s)$ est déterministe → même $Y$ produit toujours même $D$
2. **Auditabilité** : chaque décision est traçable via les 16 règles
3. **Modularité** : on peut changer le LLM sans toucher aux règles de décision
4. **Conformité** : les règles peuvent être validées par les experts DGPC indépendamment du ML

---

## 10. Planning — Gestion de Projet (Module S1)

### 10.1 Diagramme de Gantt (7 sprints)

```
Sprint 0 ████░░░░░░░░░░░░░░░░░░░░░░░░░░  Fix bugs bloquants
Sprint 1 ░░░░████░░░░░░░░░░░░░░░░░░░░░░  Réaligner annotation
Sprint 2 ░░░░░░░░████████░░░░░░░░░░░░░░  Annotation 320 appels
Sprint 3 ░░░░░░░░░░░░░░░░████░░░░░░░░░░  QLoRA fine-tune Qwen
Sprint 4 ░░░░░░░░░░░░░░░░░░░░████░░░░░░  openSMILE prosodie
Sprint 5 ░░░░░░░░░░░░░░░░░░░░░░░░████░░  RAG ChromaDB
Sprint 6 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  Intégration + démo
         S1   S2   S3   S4   S5   S6   S7   S8
                     Semaines →
```

### 10.2 Dépendances (PERT)

```
Sprint 0 ──→ Sprint 1 ──→ Sprint 2 ──→ Sprint 3 ──┐
                                                     ├──→ Sprint 6
                                         Sprint 4 ──┤
                                                     │
                                         Sprint 5 ──┘
```

- **Chemin critique** : Sprint 0 → 1 → 2 → 3 → 6
- Sprint 4 et 5 peuvent être parallélisés avec Sprint 3

### 10.3 Gestion des risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Données insuffisantes (<50/type) | Moyenne | Élevé | Data augmentation knowledge-grounded |
| WER élevé sur kabyle | Élevée | Moyen | Fine-tuning spécialisé, data augmentation audio |
| Qwen sous-performe | Faible | Élevé | Fallback vers Mistral ou Llama |
| GPU insuffisant pour QLoRA | Moyenne | Moyen | Google Colab Pro / Cloud GPU |
| Retard annotation | Élevée | Élevé | 2 annotateurs en parallèle, outil Streamlit optimisé |

---

## 11. Double Diplôme : M2 + Label Startup "Data Algérie"

### 11.1 Ce que le comité startup attend vs le jury M2

| Critère | Jury M2 SDAD | Comité Label Startup |
|---|---|---|
| **Rigueur scientifique** | ✓✓ Indispensable | · Pas prioritaire |
| **Formalisation mathématique** | ✓✓ Indispensable | · Pas prioritaire |
| **Baselines / benchmarks** | ✓✓ Indispensable | ✓ Preuve de supériorité |
| **Analyse de marché** | · Bonus | ✓✓ Indispensable |
| **Business model** | · Bonus | ✓✓ Indispensable |
| **Prototype fonctionnel** | ✓ Important | ✓✓ Indispensable |
| **KPIs / impact mesurable** | ✓ Important | ✓✓ Indispensable |
| **Données réelles** | ✓✓ Indispensable | ✓✓ Preuve de traction |
| **Scalabilité** | · Pas évalué | ✓✓ Indispensable |
| **Vision produit** | · Pas évalué | ✓✓ Indispensable |

### 11.2 Stratégie : un seul mémoire, deux audiences

- **Ch1 à Ch4** → jury M2 (rigueur, formalisation, benchmarks, méthodologie)
- **Ch4 + Conclusion** → les deux (résultats + prototype déployable)
- **Annexe A** → comité startup (business model canvas, marché, KPIs, roadmap)

### 11.3 Business Model Canvas (ébauche)

| Bloc | Contenu |
|---|---|
| **Proposition de valeur** | Réduction du temps de catégorisation et dispatch des appels d'urgence multilingues |
| **Segments clients** | Protection Civile (DGPC), SAMU, Gendarmerie, Pompiers |
| **Canaux** | Déploiement on-premise (contraintes souveraineté), SaaS pour petites structures |
| **Sources de revenus** | Licence logicielle, maintenance, formation |
| **Ressources clés** | Modèles ASR fine-tunés, ontologie d'urgence, données annotées |
| **Partenaires clés** | DGPC Béjaïa (premier client), universités (recherche), CERIST (infrastructure) |
| **Structure de coûts** | GPU (inference), développement, annotation de données |

---

## 12. Références Croisées avec le Programme

### Chaque module SDAD → où il apparaît dans le mémoire

| Module | Semestre | Chapitre(s) du mémoire |
|---|---|---|
| Fondement de data sciences | S1 | Ch1, Ch2 |
| Optimisation discrète | S1 | Ch3 (compute_dispatch) |
| Python pour data science | S1 | Ch3, Annexe B |
| Management de projets | S1 | Annexe C |
| Entreprenariat | S1 | Annexe A |
| Machine Learning pour big data | S2 | Ch3, Ch4 |
| Calculs de complexité | S2 | Ch4 (temps d'inférence) |
| Techniques d'optimisation avancées | S2 | Ch3 (compute_urgency) |
| Modèles linéaires généralisés | S2 | Ch4 (baselines) |
| Système d'info. décisionnel | S2 | Ch2, Conclusion |
| Génie logiciel | S2 | Ch3 (architecture) |
| Apprentissage & optimisation stat | S3 | Ch3, Ch4 |
| Théorie des jeux | S3 | Ch3 (allocation ressources) |
| Business Intelligence | S3 | Ch2, Conclusion |
| Data mining et applications | S3 | Ch2, Ch4 |
| Optimisation chaîne logistique | S3 | Ch3 (dispatch) |
| Rédaction scientifique | S3 | Tout le mémoire |

---

> **Conclusion** : Ce projet est un cas d'application **idéal** pour le master SDAD. Il mobilise 15/17 modules du programme, combine données réelles d'un vrai client institutionnel, formalisations mathématiques, pipeline ML de bout en bout, et dimension entrepreneuriale. La clé de la soutenance sera de **parler le langage du jury** : optimisation, aide à la décision, métriques, baselines classiques — tout en montrant que le pipeline avancé est une contribution originale.
