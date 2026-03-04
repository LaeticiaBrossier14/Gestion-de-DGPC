# Présentation NASDA — Data Algérie IA
> **Dossier de labellisation Startup — Ministère de l'Économie de la Connaissance, des Startups et des Micro-entreprises**
>
> Février 2026

---

## SLIDE 1 — اسم الشركة / قطاع المشروع

| | |
|---|---|
| **اسم الشركة** | **Data Algérie IA** |
| **قطاع المشروع** | Intelligence Artificielle — Infrastructure de Données Locales Multilingues |
| **الفئة** | Deep-Tech / GovTech / Économie de la Connaissance |
| **Logo / علامة** | [À concevoir — symbolique : réseau neuronal + drapeau algérien + ondes sonores] |

**Slogan :**
> « Transformer les données algériennes en intelligence qui sauve des vies et éclaire des décisions. »

---

## SLIDE 2 — تحديد المهمة (Définition de la Mission)

### المهمة / Mission

> **Construire la première infrastructure algérienne de compréhension et de valorisation des données locales multilingues (kabyle, darija, français, arabe) par l'intelligence artificielle, pour transformer des données brutes inexploitées en outils d'aide à la décision dans les secteurs critiques.**

### السوق المستهدف / Marché cible

| Horizon | Segment | Volume estimé |
|---------|---------|---------------|
| **Court terme** (0–18 mois) | Protection Civile (DGPC) — traitement automatisé des appels d'urgence multilingues | 58 directions de wilaya, ~1,2 M interventions/an, 70 000 agents¹ |
| **Moyen terme** (18–36 mois) | Santé publique (épidémiologie prédictive via données pharmacies) + Agriculture (prédiction rendement/prix) | 11 000+ pharmacies², 350+ hôpitaux, 8,5 M hectares de terres agricoles³ |
| **Long terme** (3–5 ans) | Plateforme nationale « Data Factory » + expansion Maghreb | Marché IA en Afrique : projeté à 6,5 Mds $ d'ici 2030⁴ |

### وسائل الإنتاج / Moyens de production

| Ressource | Description | Coût estimé An 1 |
|-----------|-------------|------------------|
| Infrastructure GPU | ENSIA (cluster H100/L40S opérationnel⁵), Ooredoo Cloud DZ, Colab Pro en complément | 2 400 000 DZD (~15 500 €) |
| Serveurs API & hébergement souverain | VPS ICOSNET ou Octenium (données sensibles restent en Algérie) | 480 000 DZD (~3 100 €) |
| Stack logiciel | 100% open-source (Whisper, Qwen, FastAPI, Streamlit, ChromaDB) | **0 DZD** en licences |
| Postes de travail | 2 stations de développement (existants, amortis) | 0 DZD |
| **Total infrastructure An 1** | | **~2 880 000 DZD (~18 600 €)** |

### مناصب الشغل / Emplois à créer

| Année | Postes | Profils |
|-------|--------|---------|
| An 1 | 3 | CTO/IA (fondateur), Développeur Full-stack, Linguiste/Annotateur kabyle |
| An 2 | +2 → 5 | Ingénieur IA, Business Developer |
| An 3 | +3–5 → 8–10 | Data Scientists, Commercial, Support technique 24/7 |

> ¹ Wikipedia — Protection civile en Algérie : 70 000 agents, 58 DPC de wilaya
> ² Ministère de la Santé, 2024
> ³ Ministère de l'Agriculture, 2023
> ⁴ Statista Market Insights, AI Market Africa, Oct 2025
> ⁵ ENSIA — École Nationale Supérieure en Intelligence Artificielle, cluster GPU inauguré 2024

---

## SLIDE 3 — فريق العمل (Équipe)

### المسيّر / Fondateur — [TON NOM]

| | |
|---|---|
| **Formation** | Master 2 — Science de Données et Aide à la Décision (SDAD), Département Recherche Opérationnelle, Université A. MIRA de Béjaïa |
| **Compétences** | Fine-tuning de grands modèles de langage (Whisper, Qwen), pipelines NLP/ASR, optimisation et aide à la décision multicritère, Python avancé |
| **Langues** | Kabyle (natif), Français, Arabe, Anglais — avantage stratégique unique pour le NLP multilingue algérien |
| **Réalisations** | • Prototype fonctionnel de pipeline IA urgences multilingues (PFE, code sur GitHub) |
| | • Analyse de 234 933 enregistrements d'appels réels de la DGPC Béjaïa |
| | • Ontologie de 14 types d'incidents, 5 niveaux d'urgence, système de dispatch déterministe |
| | • Outils d'annotation (Streamlit + Google Colab) en production |
| **Expertise terrain** | Collaboration directe avec la DGPC Béjaïa (accès aux données, compréhension des processus opérationnels) |

### Co-fondateur recherché — Profil Dev Full-Stack / Infra Cloud

| Compétence | Besoin |
|---|---|
| Backend API (FastAPI, Docker) | Déploiement des modèles IA en production |
| Infra cloud souverain | Conformité données sensibles (hébergement DZ) |
| Sécurité | Chiffrement, gestion des accès, RGPD/loi DZ |

### Comité consultatif (Advisory Board — à construire)

| Rôle | Objectif |
|---|---|
| Mentor académique NLP | Université de Béjaïa / USTHB — caution scientifique |
| Contact institutionnel DGPC | Faciliter le déploiement pilote et l'accès aux données |
| Mentor entrepreneur | Réseau Algeria Venture / incubateur — stratégie de croissance |

---

## SLIDE 4 — ملخص السوق (Résumé du Marché)

### الماضي / Passé (avant 2020)

- **Zéro** solution IA commerciale pour les langues algériennes (kabyle, darija)
- Les systèmes de traitement d'appels d'urgence en Algérie sont **100% manuels** : un opérateur décroche, écoute, catégorise mentalement, rédige manuellement
- La Protection Civile utilise le système « 0666 » (base Access/VB6, années 2000) — aucune transcription vocale, aucune aide à la décision automatisée
- Google, Meta et les géants tech **ne couvrent pas** le kabyle ni la darija algérienne

### الحاضر / Présent (2024–2026)

| Indicateur | Valeur | Source |
|---|---|---|
| Startups labellisées en Algérie | 1 300+ (objectif 20 000 d'ici 2029) | startup.dz, 2025 |
| Fonds gouvernementaux startups tech | Algeria Startup Fund (ASF) — 6 banques publiques | Décret 2022 |
| Infrastructure GPU nationale | ENSIA (cluster NVIDIA H100/L40S), Ooredoo Cloud | Inauguré 2024 |
| Startups NLP algériennes | Fentech/Hadretna (traduction dialectale), Symloop (NLP arabe) | — |
| Couverture IA du kabyle | **0%** — aucun service commercial | Vérifié Google, Meta, 2025 |
| Protection civile algérienne | 70 000 agents, 58 DPC, ~1,2 M interventions/an, numéros 14 et 1021 | Wikipedia, DGPC |

**Chiffres clés de notre étude terrain (DGPC Béjaïa) :**

| KPI | Valeur | Signification |
|---|---|---|
| Appels enregistrés (2018–2025) | **234 933** | Volume massif, exploitable |
| Taux de perte (rejetés + manqués) | **42,19%** | Près de la moitié des appels perdus → besoin critique |
| Appels/jour en moyenne | 426 | Charge opérationnelle élevée |
| Jour de pointe | 1 108 appels (19/04/2025) | Pics lors de catastrophes |
| Délai médian de réponse | 6 secondes | Performant mais 42% jamais traités |

### المستقبل / Futur (2027–2030)

- Marché IA en Afrique : croissance annuelle estimée à 25–30% (CAGR) → 6,5+ Mds $ d'ici 2030
- Demande mondiale croissante en données multilingues authentiques (Google, Meta = acheteurs potentiels de corpus)
- Transformation numérique du secteur public algérien (e-gouvernement, villes intelligentes, Loi 2023 sur l'économie de la connaissance)
- **Fenêtre d'opportunité : 2–4 ans** avant que les géants couvrent le kabyle/darija

---

## SLIDE 5 — المفهوم التجاري للمنتج (Concept Produit)

### Le concept central

> **Données chaotiques algériennes (audio, texte, tout secteur, toute langue) → Moteur de compréhension linguistique IA → Intelligence actionnable pour l'aide à la décision**

```
┌──────────────────────┐        ┌──────────────────────┐        ┌──────────────────────┐
│  DONNÉES BRUTES      │        │  CLÉ LINGUISTIQUE    │        │  INTELLIGENCE        │
│  (kabyle, darija,    │───────▶│  Moteur IA           │───────▶│  Outils d'aide       │
│  français, mélangés) │        │  multilingue algérien│        │  à la décision       │
└──────────────────────┘        └──────────────────────┘        └──────────────────────┘
  Appels d'urgence                ASR (Whisper fine-tuné)         Dashboard temps réel
  Posts réseaux sociaux           Extraction (Qwen + Outlines)    Alertes automatiques
  Ventes pharmacies               Classification structurée       Dispatch optimisé
  Rapports agricoles              Analyse prosodique              Prédictions
```

### Pourquoi commencer par les appels d'urgence ?

C'est le **cas le plus exigeant** (bruit, stress, code-switching, temps réel, zéro tolérance d'erreur). **Si le moteur tient ici, il tient partout :**

| Défi | Appels d'urgence | Autres données |
|------|-----------------|----------------|
| Bruit audio | Sirènes, cris, vent | Texte propre |
| Code-switching | 3 langues dans une phrase, sous stress | Plus structuré |
| Tolérance d'erreur | 0% (vie humaine) | Plus souple |
| Latence requise | Secondes | Minutes/heures |

### Pipeline technologique (MVP fonctionnel)

```
Audio d'appel → Whisper V3 Fine-tuné (kabyle) → Transcription
                                                      ↓
Audio         → openSMILE (prosodie)          → Score de stress
                                                      ↓
Transcription → Qwen 2.5 7B QLoRA + Outlines → JSON structuré
                                                      ↓
JSON          → Post-traitement déterministe  → Urgence + Dispatch
                (compute_urgency, compute_dispatch)
                                                      ↓
                                              EmergencyCall (output)
```

### Produits planifiés (roadmap)

| # | Produit | Cible | Horizon |
|---|---------|-------|---------|
| 1 | **IA Urgence** (MVP) | DGPC — traitement automatisé appels multilingues | 0–12 mois |
| 2 | **HealthMap DZ** | Ministère Santé — détection épidémique via pharmacies | 12–24 mois |
| 3 | **AgriPredict** | Agriculteurs — prédiction rendement et prix optimaux | 18–30 mois |
| 4 | **Social Insights** | Gouvernance — analyse sentiment public en dialectes DZ | 24–36 mois |
| 5 | **Marketplace Données** | Google, Meta, HuggingFace — vente corpus multilingues | 30–48 mois |

### Preuve de concept existante

- ✅ Prototype pipeline fonctionnel (PFE M2 SDAD, code GitHub)
- ✅ 234 933 enregistrements d'appels réels analysés
- ✅ Ontologie de 14 types d'incidents validée avec la DGPC
- ✅ Outils d'annotation opérationnels (Streamlit + Colab)

---

## SLIDE 6 — المنافسة (Concurrence)

### Panorama concurrentiel

| Concurrent | Pays | Activité | Forces | Faiblesses vs nous |
|-----------|------|----------|--------|---------------------|
| **Fentech / Hadretna** | 🇩🇿 Algérie | LLM dialectes algériens, traduction | Premier entrant NLP DZ, corpus dialectal | Focus traduction, pas de vertical métier, pas d'audio, pas de kabyle |
| **Symloop** | 🇩🇿 Algérie | NLP arabe/darija, services IT | Équipe expérimentée | Services sur mesure (ESN), pas de plateforme SaaS scalable |
| **Corti** | 🇩🇰 Danemark | IA urgences médicales | Déployé dans 8 pays, levée 40M$ | Pas de kabyle/darija, prix prohibitif (~100K€/an), modèle propriétaire |
| **Vitr.ai** | 🇨🇦 Canada | IA analyse appels 911 | Partenariat police Montréal | Anglais/français uniquement, pas de marché DZ |
| **Google / Gemini** | 🇺🇸 USA | IA multilingue mondiale | 70+ langues, puissance de calcul illimitée | **Ne comprend pas le kabyle**, API only, pas de données locales |
| **Meta / Seamless** | 🇺🇸 USA | Traduction multilingue | 100+ langues | **Kabyle non supporté**, pas d'application métier |

### الميزة التنافسية / Notre avantage compétitif (moat)

| # | Avantage | Pourquoi c'est défendable |
|---|---------|--------------------------|
| 1 | **Seule entité kabyle + darija + FR + code-switching** | Aucun concurrent mondial ou local ne couvre ce spectre linguistique |
| 2 | **Accès aux données terrain** | Collaboration directe DGPC Béjaïa — données réelles inaccessibles aux géants |
| 3 | **Effet flywheel** | Chaque appel traité = nouvelle donnée → modèle s'améliore → meilleur service → plus de clients → plus de données |
| 4 | **Coût 10x inférieur** | Stack open-source + salaires DZ vs Corti/Vitr.ai en Europe/Amérique |
| 5 | **Hébergement souverain** | Données sensibles (urgences, santé) restent en Algérie — conformité réglementaire |
| 6 | **Expertise domaine + linguistique** | Fondateur natif kabyle + formation data science + terrain DGPC |

---

## SLIDE 7 — الأهداف (Objectifs Chiffrés)

### Objectifs à 3 ans

| Indicateur | An 1 | An 2 | An 3 |
|------------|------|------|------|
| **Clients** | 1 pilote (DGPC Béjaïa) | 3–5 clients payants (2–3 DPC + 1 santé) | 8–15 clients multi-secteurs |
| **Wilayas couvertes** | 1 (Béjaïa) | 3–5 (kabylophone : Tizi, Bouira, BGM) | 10–15 wilayas |
| **Appels traités/mois** | 3 000 (pilote) | 15 000–25 000 | 50 000–100 000 |
| **Corpus collecté** | 5 000 enregistrements annotés | 50 000+ | 200 000+ |
| **Précision pipeline (F1)** | ≥ 0.80 (MVP) | ≥ 0.88 | ≥ 0.92 |
| **Temps de traitement** | < 5 sec/appel | < 3 sec/appel | < 2 sec/appel |
| **Équipe** | 3 personnes | 5 personnes | 8–10 personnes |
| **Revenu annuel (DZD)** | 0 (subventions) | 8–15 M | 35–65 M |

### Comment atteindre ces objectifs

```
ANNÉE 1 — PROUVER (Phase pilote)
├── Déployer MVP chez DGPC Béjaïa (gratuit, convention PFE → pilote)
├── Annoter 500+ appels réels → entraîner modèles spécialisés
├── Mesurer : taux d'appels correctement catégorisés, temps gagné
├── Publier résultats (conférence IA, article scientifique)
└── Obtenir labellisation NASDA + financement amorce

ANNÉE 2 — VENDRE (Phase commerciale)
├── Convertir pilote DGPC en contrat payant (SaaS mensuel)
├── Déployer dans 2–4 DPC supplémentaires (wilayas kabylophones)
├── Lancer HealthMap DZ (détection épidémique) avec 1 partenaire santé
├── Recruter +2 (Ingénieur IA + Business Developer)
└── Lever 20–30 M DZD (Algeria Venture / ASF)

ANNÉE 3 — SCALER (Phase croissance)
├── 10–15 wilayas couvertes
├── Lancer AgriPredict (agriculture)
├── Vente de corpus linguistiques à des tiers (HuggingFace, chercheurs)
├── Distillation : modèles légers spécialisés (1.5B) déployables edge
└── Préparer Série A (50–100 M DZD)
```

---

## SLIDE 8 — الخطة المالية (Plan Financier)

### Hypothèses de pricing

| Produit | Modèle | Prix unitaire |
|---------|--------|---------------|
| **IA Urgence SaaS** | Abonnement mensuel par DPC | 150 000–300 000 DZD/mois/DPC (~970–1 940 €) |
| **HealthMap DZ** | Abonnement annuel par hôpital/DSP | 800 000–1 500 000 DZD/an |
| **Vente corpus** | Par lot de 10 000 enregistrements annotés | 500 000–2 000 000 DZD/lot |
| **Consulting intégration** | Journée homme | 50 000 DZD/jour |

> **Benchmark prix :** Corti (Danemark) facture ~100 000 €/an/client. Nous proposons un tarif **20x inférieur** adapté au marché algérien, tout en conservant des marges de 60–70% grâce au stack open-source et aux salaires locaux.

### Revenus prévisionnels (en milliers DZD)

| Source de revenus | An 1 | An 2 | An 3 |
|-------------------|------|------|------|
| SaaS IA Urgence (DPC) | 0 | 5 400–10 800 | 21 600–43 200 |
| SaaS HealthMap | 0 | 1 600–3 000 | 4 800–9 000 |
| Vente corpus / datasets | 0 | 1 000–2 000 | 3 000–6 000 |
| Licensing pipeline à tiers | 0 | 0 | 2 000–4 000 |
| Consulting / intégration | 0 | 500–1 000 | 1 500–3 000 |
| **Subventions (NASDA, ASF, grants)** | **10 000–15 000** | **3 000–5 000** | **0** |
| **TOTAL** | **10 000–15 000** | **11 500–21 800** | **32 900–65 200** |

### Charges prévisionnelles (en milliers DZD)

| Poste de charge | An 1 | An 2 | An 3 |
|-----------------|------|------|------|
| Salaires (3 → 5 → 8–10 pers.) | 2 880 | 5 760 | 10 560 |
| Infrastructure GPU & cloud | 2 400 | 3 600 | 4 800 |
| Bureau / coworking | 360 | 720 | 1 200 |
| Juridique / comptable / PI | 400 | 250 | 250 |
| Marketing / conférences | 200 | 500 | 1 200 |
| Déplacements (wilayas) | 300 | 600 | 900 |
| Imprévus (10%) | 654 | 1 143 | 1 891 |
| **TOTAL CHARGES** | **7 194** | **12 573** | **20 801** |

### Détail calcul salaires

| Poste | Salaire mensuel (DZD) | An 1 (×12) | An 2 | An 3 |
|-------|----------------------|------------|------|------|
| CTO/IA (fondateur) | 80 000 | 960 000 | 100 000 ×12 | 120 000 ×12 |
| Dev Full-stack | 70 000 | 840 000 | 80 000 ×12 | 90 000 ×12 |
| Linguiste/Annotateur | 50 000 | 600 000 | 60 000 ×12 | 70 000 ×12 |
| Ingénieur IA | — | — | 80 000 ×12 | 90 000 ×12 |
| Business Developer | — | — | 60 000 ×12 | 70 000 ×12 |
| Postes supplémentaires An 3 | — | — | — | ~3 × 70 000 ×12 |
| **TOTAL** | | **2 400 000** | **4 560 000** | **8 040 000** |

> *Note : charges patronales estimées à +20% → totaux ajustés dans le tableau des charges.*

### Résultat net prévisionnel

| | An 1 | An 2 | An 3 |
|---|------|------|------|
| **Revenus** | 10 000–15 000 | 11 500–21 800 | 32 900–65 200 |
| **Charges** | 7 194 | 12 573 | 20 801 |
| **Résultat net** | **+2 806 à +7 806** | **-1 073 à +9 227** | **+12 099 à +44 399** |
| **Marge nette** | 28–52% | -9% à +42% | 37–68% |

### Point mort (break-even)

- **Scénario optimiste (subventions + 3 clients An 2)** : point mort atteint **mi-An 2**
- **Scénario prudent (subventions seules An 1, 1 client An 2)** : point mort atteint **fin An 2**
- **An 3 : rentabilité structurelle** dans tous les scénarios

---

## SLIDE 9 — الاحتياجات من الموارد (Besoins en Ressources)

### طاقم عمل / Personnel

| Phase | Recrutement | Priorité |
|-------|-------------|----------|
| **Immédiat** (0–3 mois) | Co-fondateur Dev Full-stack/Infra | 🔴 Critique |
| **An 1** (3–12 mois) | Linguiste/Annotateur kabyle-darija | 🔴 Critique |
| **An 2** | Ingénieur IA + Business Developer | 🟡 Importante |
| **An 3** | Data Scientists (×2), Commercial, Support | 🟢 Croissance |

### أخبار التكنولوجيا / Technologie

| Composant | Solution | Statut |
|-----------|----------|--------|
| GPU entraînement | ENSIA (H100/L40S) + Google Colab Pro | Disponible |
| GPU inférence production | VPS GPU ICOSNET ou Ooredoo Cloud DZ | À contractualiser |
| Framework ML | PyTorch, HuggingFace Transformers, Outlines | Open-source, prêt |
| ASR multilingue | Whisper V3 (OpenAI, open-source) → fine-tuner sur kabyle | Base disponible |
| LLM extraction | Qwen 2.5 7B (Alibaba, open-source) → QLoRA fine-tuning | Base disponible |
| Prosodie/Stress | openSMILE (Munich, open-source) | Prêt à intégrer |
| RAG | ChromaDB + knowledge base DGPC (52 communes, 19 daïras) | Développé |
| Frontend | Streamlit (prototypage), React (production) | Streamlit en prod |
| API | FastAPI + Docker | À déployer |

### تمويل / Financement

| Phase | Montant (DZD) | Montant (€) | Source visée |
|-------|---------------|-------------|-------------|
| **Amorce An 1** | 10–15 M | 65K–97K € | NASDA label + ASF + Algeria Venture |
| **Croissance An 2** | 20–30 M | 130K–194K € | ASF + clients + grants internationaux |
| **Série A An 3** | 50–100 M | 323K–646K € | VC + ASF + revenus |

### توزيع / Distribution

| Canal | Stratégie |
|-------|-----------|
| **B2G direct** (gouvernement) | Pilote gratuit → démonstration de valeur → contrat payant |
| **Conférences / publications** | Crédibilité scientifique (articles, démos en conférence IA) |
| **Bouche-à-oreille institutionnel** | Un DPC satisfait → recommandation aux autres wilayas |

### ترقية / Promotion

| Action | Coût estimé | Impact |
|--------|-------------|--------|
| Présence LinkedIn / réseaux professionnels | 0 DZD | Visibilité startup DZ |
| Participation conférences IA (ENSIA, USTHB) | 50 000 DZD/an | Crédibilité technique |
| Publication article scientifique (open access) | 0 DZD | Référencement international |
| Démo vidéo du pipeline (YouTube/LinkedIn) | 0 DZD | Preuve de concept visible |

### منتجات / Produits (séquençage)

```
An 1 : IA Urgence (MVP) ──→ An 2 : + HealthMap DZ ──→ An 3 : + AgriPredict + Marketplace Données
```

### خدمات / Services

| Service | Description | Prix |
|---------|-------------|------|
| Intégration système | Connexion IA au système existant du client | 50 000 DZD/jour |
| Formation opérateurs | Prise en main du dashboard IA | Inclus dans SaaS |
| Support technique | 24/7 pour urgences, 8h–18h pour autres | Inclus dans SaaS (premium) |
| Annotation personnalisée | Création de corpus sur mesure pour un domaine | Sur devis |

---

## SLIDE 10 — المخاطر والأرباح (Risques et Bénéfices)

### المخاطر / Risques

| # | Risque | Probabilité | Impact | Mitigation |
|---|--------|-------------|--------|------------|
| 1 | **Bureaucratie bloque le contrat DGPC** | Élevée | Élevé | Pilote GRATUIT via convention PFE universitaire → preuve de valeur avant contrat. Aucun engagement financier demandé initialement |
| 2 | **Fentech pivote sur nos verticaux (urgences)** | Moyenne | Moyen | Premier entrant sur le terrain DGPC + données exclusives + corpus kabyle. Fentech n'a pas d'accès terrain ni d'audio |
| 3 | **Précision modèle insuffisante sur kabyle** | Moyenne | Élevé | Données synthétiques knowledge-grounded + curriculum learning + collaboration linguistes Université de Béjaïa. WER kabyle Whisper fine-tuné déjà prometteur |
| 4 | **Google/Meta couvrent le kabyle** | Faible (2–4 ans) | Élevé | Notre moat n'est pas le modèle, c'est l'accès aux données locales + l'intégration métier. Même si Google couvre le kabyle, il ne connaît pas le dispatch DGPC |
| 5 | **Difficulté à recruter (brain drain)** | Élevée | Moyen | Commencer petit (3 personnes), collaborer avec universités (stages), proposer equity + mission impactante |
| 6 | **Financement insuffisant An 1** | Moyenne | Élevé | Candidatures multiples (NASDA, ASF, Algeria Venture, ATRST). Infrastructure frugale (stack open-source, Colab Pro = 15 $/mois) |
| 7 | **Questions éthiques (données sensibles)** | Basse | Élevé | Hébergement souverain DZ, anonymisation systématique, charte éthique publiée, convention avec la DGPC encadrant l'usage |

### الأرباح / Bénéfices et impact

| # | Bénéfice | Mesure d'impact |
|---|----------|-----------------|
| 1 | **Vies sauvées** | Réduction du temps de catégorisation : objectif 2 min → 30 sec (−75%) |
| 2 | **Réduction du taux de perte d'appels** | De 42% (mesuré) → objectif < 20% avec aide IA |
| 3 | **Emplois qualifiés** | 3 → 10 emplois tech en 3 ans en Algérie (anti brain drain) |
| 4 | **Corpus national unique** | Actif stratégique : premières données annotées kabyle/darija pour l'IA (valeur internationale) |
| 5 | **Souveraineté numérique** | Données algériennes traitées en Algérie, pas exportées vers des clouds étrangers |
| 6 | **Revenus** | 33–65 M DZD/an à An 3 (rentabilité structurelle) |
| 7 | **Modèle réplicable** | Exportable vers Maroc (darija marocaine), Tunisie, Afrique subsaharienne |

### Comparable africain de référence

| Startup | Pays | Parcours | Résultat |
|---------|------|----------|----------|
| **InstaDeep** | 🇹🇳 Tunisie | Fondée 2014, IA décisionnelle, 1 fondateur polytechnicien | **Rachetée 636 M€ par BioNTech** (2023), 9 ans |
| **Lelapa AI** | 🇿🇦 Afrique du Sud | LLM langues africaines (InkubaLM) | Série A en cours, partenariat Google |
| **Data Algérie IA** | 🇩🇿 **Algérie** | IA multilingue données locales | **À construire** — même fenêtre qu'InstaDeep en 2014 |

---

## SLIDE 11 — العناصر المفتاحية (Éléments Clés)

### على المدى القصير / Court terme (0–6 mois) — Décisions urgentes

| Décision | Conséquence si retardée |
|----------|------------------------|
| **1. Obtenir le label NASDA** | Perte des avantages fiscaux, pas d'accès ASF, crédibilité réduite |
| **2. Trouver un co-fondateur tech** | Fondateur seul → risque de burnout, blocage sur l'infra de production |
| **3. Signer convention DGPC → pilote** | Sans convention formelle, pas d'accès légal aux données → prototype reste académique |
| **4. Clarifier la propriété intellectuelle (PFE vs startup)** | Risque juridique si l'université revendique le code du PFE |
| **5. Sécuriser le financement amorce (10–15 M DZD)** | Prototype reste à l'état de PFE, pas de transition vers produit commercial |

### على المدى طويل / Long terme (6–24 mois) — Décisions stratégiques

| Décision | Conséquence si retardée |
|----------|------------------------|
| **6. Choix du 2ème vertical (santé ou agriculture)** | Mauvais pivot = 6 mois perdus. Décision basée sur l'accès aux données réel |
| **7. Stratégie éthique et protection des données** | Risque réputationnel majeur si scandale de fuite de données d'urgence |
| **8. Timing de l'expansion inter-wilayas** | Trop tôt = dispersion, trop tard = concurrent s'installe |
| **9. Partenariats internationaux (HuggingFace, Google)** | Vente de corpus = revenu passif important, mais IP à protéger |

### Si financement NASDA obtenu — allocation

```
FINANCEMENT AMORCE : 10–15 M DZD
├── 40% → Recrutement (co-fondateur + linguiste)          = 4–6 M DZD
├── 25% → Infrastructure GPU & cloud An 1                 = 2,5–3,75 M DZD
├── 15% → Juridique (PI, convention DGPC, statut SPA)     = 1,5–2,25 M DZD
├── 10% → Bureau / coworking / déplacements               = 1–1,5 M DZD
└── 10% → Réserve de trésorerie                           = 1–1,5 M DZD
```

---

## SLIDE 12 — شكرا على الانتباه

> ### « On ne vend pas de l'IA. On vend l'accès structuré à des données algériennes que personne d'autre ne comprend. »

---

**[TON NOM]** — Fondateur, Data Algérie IA

Master 2 Science de Données et Aide à la Décision — Université A. MIRA de Béjaïa

📧 [email]  
📱 [téléphone]  
🔗 [LinkedIn]  
💻 [GitHub : github.com/rayantr06]

---

> *« La fenêtre est ouverte. InstaDeep a prouvé que le Maghreb peut produire des champions de l'IA. L'Algérie a les données, les langues et le besoin. Il ne manque que l'entreprise qui relie tout ça. »*

---

### Notes pour la présentation orale

1. **Slide 1** (30 sec) — Se présenter, nommer la startup et le secteur
2. **Slide 2** (2 min) — La mission : insister sur le marché multilingue algérien inexploité
3. **Slide 3** (1 min) — L'équipe : mettre en avant le double profil (data science + kabyle natif)
4. **Slide 4** (2 min) — Le marché : COMMENCER par le chiffre 42% d'appels perdus (choc)
5. **Slide 5** (3 min) — Le produit : FAIRE UNE DÉMO LIVE si possible (audio → JSON en 5 sec)
6. **Slide 6** (1 min 30) — La concurrence : insister sur « personne ne fait kabyle + urgences »
7. **Slide 7** (1 min 30) — Les objectifs : être précis et réaliste
8. **Slide 8** (2 min) — Le plan financier : insister sur le point mort mi-An 2
9. **Slide 9** (1 min) — Les ressources : montrer que le stack est frugal (open-source)
10. **Slide 10** (1 min 30) — Risques : être honnête, le comité apprécie la lucidité
11. **Slide 11** (1 min) — Les décisions clés : montrer l'urgence d'agir maintenant
12. **Slide 12** (30 sec) — Conclure avec la citation, remercier, ouvrir aux questions

**Durée totale : ~18 minutes** (sur 20 min allouées typiquement)
