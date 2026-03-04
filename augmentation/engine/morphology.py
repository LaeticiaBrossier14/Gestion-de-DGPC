"""
Kabyle morphology engine — Verb conjugation, construct state, negation.

Applies Béjaïa dialect (Tasahlit / EOR) rules to produce grammatically
correct Kabyle word-forms from root + person + tense specifications.

Sources:
  - PROFIL_LINGUISTIQUE_BEJAIA.md (97 real emergency calls)
  - Thèse ASSOU (19 parlers, eastern Béjaïa)
  - rules.yaml config
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ── Enums ───────────────────────────────────────────────────

class Person(Enum):
    SG1 = "1sg"       # I
    SG2M = "2sg_masc" # you (masc)
    SG2F = "2sg_fem"  # you (fem)
    SG3M = "3sg_masc" # he
    SG3F = "3sg_fem"  # she
    PL1 = "1pl"       # we
    PL2 = "2pl"       # you (pl)
    PL3M = "3pl_masc" # they (masc)
    PL3F = "3pl_fem"  # they (fem)


class Tense(Enum):
    PRETERITE = "preterite"         # past/completed
    AORIST = "aorist"               # future/irrealis
    INTENSIVE = "intensive_aorist"  # habitual/progressive
    IMPERATIVE = "imperative"       # command


class NegationType(Enum):
    VERBAL_BEJAIA = "ul_ula"       # ul + verb + ula (Béjaïa)
    VERBAL_STD = "ur_ara"          # ur + verb + ara (standard)
    NOMINAL = "ulach"              # ulach (there is not)
    IDENTITY = "machi"             # machi + noun (it's not)
    REFUSAL = "khati"              # simple no


# ── Verb Root Registry ──────────────────────────────────────

@dataclass
class VerbRoot:
    """A Kabyle verb root with all its inflected forms."""
    root: str
    meaning: str
    # Preterite (past) forms per person
    preterite: Dict[Person, str] = field(default_factory=dict)
    # Aorist (future) forms per person
    aorist: Dict[Person, str] = field(default_factory=dict)
    # Intensive aorist forms
    intensive: Dict[Person, str] = field(default_factory=dict)
    # Imperative
    imperative_sg: str = ""
    imperative_pl: str = ""


def _build_emergency_verbs() -> Dict[str, VerbRoot]:
    """Build the emergency verb registry from attested corpus forms."""
    verbs: Dict[str, VerbRoot] = {}

    # ── ghli (fall / faint) — 19 occurrences ──
    v = VerbRoot(root="ghli", meaning="fall / faint")
    v.preterite = {
        Person.SG1: "ghli-gh",
        Person.SG3M: "i-ghli",
        Person.SG3F: "t-eghli",
        Person.PL1: "n-ghli",
        Person.PL3M: "ghli-n",
    }
    v.aorist = {
        Person.SG1: "ad-eghli-gh",
        Person.SG3M: "ad-yeghli",
        Person.SG3F: "ad-teghli",
        Person.PL1: "ad-neghli",
    }
    v.intensive = {
        Person.SG3M: "i-ghellib",
        Person.SG3F: "t-ghellib",
    }
    v.imperative_sg = "eghli"
    verbs["ghli"] = v

    # ── che3l (burn / catch fire) — 5 occurrences ──
    v = VerbRoot(root="che3l", meaning="burn / catch fire")
    v.preterite = {
        Person.SG3M: "ich3el",
        Person.SG3F: "cha3let",
        Person.PL3M: "ch3el-n",
    }
    v.aorist = {
        Person.SG3M: "ad-yeche3l",
        Person.SG3F: "ad-teche3l",
    }
    v.imperative_sg = "che3l"
    verbs["che3l"] = v

    # ── doukh (feel dizzy / sick) — 2 occurrences ──
    v = VerbRoot(root="doukh", meaning="feel dizzy / sick")
    v.preterite = {
        Person.SG3M: "i-doukh",
        Person.SG3F: "t-doukh",
    }
    v.aorist = {
        Person.SG3M: "ad-yedoukh",
        Person.SG3F: "ad-tedoukh",
    }
    verbs["doukh"] = v

    # ── yugh (hurt / be painful) — 5 occurrences ──
    v = VerbRoot(root="yugh", meaning="hurt")
    v.preterite = {
        Person.SG3M: "i-yugh",
        Person.SG3F: "t-yugh",
    }
    v.intensive = {
        Person.SG3M: "i-thyugh",
        Person.SG3F: "t-thyugh",
    }
    verbs["yugh"] = v

    # ── nuffes (breathe) — 3 occurrences ──
    v = VerbRoot(root="nuffes", meaning="breathe")
    v.preterite = {
        Person.SG3M: "i-nuffes",
        Person.SG3F: "t-nuffes",
    }
    v.aorist = {
        Person.SG3M: "ad-yenuffes",
        Person.SG3F: "ad-tnuffes",
    }
    verbs["nuffes"] = v

    # ── teddu (go / move) — 5 occurrences ──
    v = VerbRoot(root="teddu", meaning="go / move")
    v.preterite = {
        Person.SG1: "ddi-gh",
        Person.SG3M: "i-dda",
        Person.SG3F: "t-dda",
        Person.PL1: "n-dda",
    }
    v.aorist = {
        Person.SG1: "ad-eddu-gh",
        Person.SG2M: "ad-teddud",
        Person.SG3M: "ad-yeddu",
        Person.PL1: "ad-neddu",
    }
    v.intensive = {
        Person.SG3M: "i-tteddu",
        Person.SG3F: "t-tteddu",
        Person.PL3M: "tteddu-n",
        Person.PL1: "n-tteddu",
    }
    v.imperative_sg = "eddu"
    verbs["teddu"] = v

    # ── ttawi (carry / transport) — 4 occurrences ──
    v = VerbRoot(root="ttawi", meaning="carry / transport")
    v.preterite = {
        Person.SG3M: "i-wwin",
        Person.SG3F: "t-wwin",
        Person.PL3M: "wwin-n",
    }
    v.aorist = {
        Person.SG3M: "ad-yawi",
        Person.SG3F: "ad-tawi",
        Person.PL1: "ad-nawi",
        Person.PL3M: "ad-awin",
    }
    v.imperative_sg = "awi-d"
    v.imperative_pl = "awi-t-id"
    verbs["ttawi"] = v

    # ── ghleq (drown / suffocate) ──
    v = VerbRoot(root="ghleq", meaning="drown / suffocate")
    v.preterite = {
        Person.SG3M: "i-ghleq",
        Person.SG3F: "t-ghleq",
        Person.PL3M: "ghleq-n",
    }
    v.aorist = {
        Person.SG3M: "ad-yeghleq",
        Person.SG3F: "ad-teghleq",
    }
    verbs["ghleq"] = v

    # ── hlek (be sick / suffer) — 2 occurrences ──
    v = VerbRoot(root="hlek", meaning="be sick / suffer")
    v.preterite = {
        Person.SG3M: "ihlek",
        Person.SG3F: "thehlek",
    }
    v.aorist = {
        Person.SG3M: "ad-yehlek",
        Person.SG3F: "ad-thehlek",
    }
    verbs["hlek"] = v

    # ── 3awed (repeat / call again) ──
    v = VerbRoot(root="3awed", meaning="repeat / call again")
    v.preterite = {
        Person.SG1: "3awed-egh",
        Person.SG3M: "i-3awed",
    }
    v.aorist = {
        Person.SG1: "ad-3awed-egh",
        Person.SG3M: "ad-y3awed",
    }
    v.imperative_sg = "3awed"
    verbs["3awed"] = v

    # ── arwa7 (come — imperative only, very common) ──
    v = VerbRoot(root="arwa7", meaning="come")
    v.imperative_sg = "arwa7-d"
    v.imperative_pl = "arwa7-d"
    verbs["arwa7"] = v

    # ── ssiwel (call / phone) ──
    v = VerbRoot(root="ssiwel", meaning="call / phone")
    v.preterite = {
        Person.SG1: "ssiwel-gh",
        Person.SG3M: "i-ssiwel",
    }
    v.aorist = {
        Person.SG1: "ad-ssiwl-egh",
        Person.SG3M: "ad-yessiwel",
    }
    v.imperative_sg = "ssiwel"
    verbs["ssiwel"] = v

    return verbs


EMERGENCY_VERBS = _build_emergency_verbs()


# ── Conjugation ─────────────────────────────────────────────

def conjugate(
    verb_key: str,
    person: Person,
    tense: Tense,
    *,
    negative: bool = False,
    neg_type: NegationType = NegationType.VERBAL_BEJAIA,
) -> str:
    """Conjugate a verb root for person + tense, optionally negated.

    Returns the full verb phrase as a string.
    Falls back to the root key if the form is not registered.
    """
    verb = EMERGENCY_VERBS.get(verb_key)
    if verb is None:
        # Unknown verb — return root unchanged
        form = verb_key
    elif tense == Tense.IMPERATIVE:
        form = verb.imperative_sg or verb.root
    elif tense == Tense.PRETERITE:
        form = verb.preterite.get(person, verb.root)
    elif tense == Tense.AORIST:
        form = verb.aorist.get(person, verb.root)
    elif tense == Tense.INTENSIVE:
        form = verb.intensive.get(person, verb.root)
    else:
        form = verb.root

    if negative:
        return negate(form, neg_type)
    return form


# ── Negation ────────────────────────────────────────────────

def negate(verb_form: str, neg_type: NegationType = NegationType.VERBAL_BEJAIA) -> str:
    """Apply negation to a verb form.

    Béjaïa default: ul {verb} ula
    Standard:       ur {verb} ara
    """
    if neg_type == NegationType.VERBAL_BEJAIA:
        return f"ul {verb_form} ula"
    elif neg_type == NegationType.VERBAL_STD:
        return f"ur {verb_form} ara"
    elif neg_type == NegationType.NOMINAL:
        return "ulach"
    elif neg_type == NegationType.IDENTITY:
        return "machi"
    elif neg_type == NegationType.REFUSAL:
        return random.choice(["khati", "xati"])
    return verb_form


# ── Construct State ─────────────────────────────────────────

# Mappings: free state → annexed/construct state
_CONSTRUCT_STATE_MAP: Dict[str, str] = {
    # Common nouns from corpus
    "argaz": "urgaz",
    "axxam": "uxxam",
    "adrar": "udrar",
    "asif": "wasif",
    "aman": "waman",
    "akal": "wakal",
    "avrid": "uvrid",
    "amkan": "umkan",
    "abrid": "ubrid",
    # Feminine nouns
    "tamurt": "tmurt",
    "tameṭṭut": "tmeṭṭut",
    "tamghart": "tmghart",
    "taqchichth": "teqchichth",
    "tamettut": "tmettut",
    "taddart": "teddart",
    # Emergency-specific
    "ambulance": "ambulance",   # French loanwords: no change
    "accident": "accident",
    "tomobil": "tomobil",
}


def construct_state(noun: str) -> str:
    """Convert a noun from free state to construct (annexed) state.

    Rules:
    1. Known mappings → direct lookup.
    2. Initial 'a' → 'u'  (masculine nouns starting with a-).
    3. Initial 'ta' → 't' (feminine nouns starting with ta-).
    4. Otherwise → unchanged (loanwords, already in construct state).
    """
    lower = noun.lower()

    # Known mapping?
    if lower in _CONSTRUCT_STATE_MAP:
        mapped = _CONSTRUCT_STATE_MAP[lower]
        # Preserve original casing of first char
        if noun[0].isupper():
            return mapped[0].upper() + mapped[1:]
        return mapped

    # Rule: initial 'a' → 'u' (masculine)
    if lower.startswith("a") and len(noun) > 2:
        return "u" + noun[1:]

    # Rule: initial 'ta' → 't' (feminine)
    if lower.startswith("ta") and len(noun) > 3:
        return "t" + noun[2:]

    # No change (loanwords, already construct)
    return noun


# ── Code-Switching ──────────────────────────────────────────

# French terms that are NEVER translated — always kept as-is
KEEP_FRENCH: set = {
    "ambulance", "accident", "pompiers", "protection civile",
    "bloc", "étage", "logements", "crise", "tension",
    "oxygène", "inconscient", "blessé", "blessée", "hémorragie",
    "enceinte", "numéro", "route", "nationale", "d'accord",
    "urgent", "camion", "moto", "véhicule", "voiture",
    "bus", "fourgon", "brancard", "fracture", "brûlures",
}

# Arabic social formulas — always kept
KEEP_ARABIC: set = {
    "salam alaykoum", "wa alaykoum assalam",
    "inchallah", "wallah", "barak allah",
    "ya3tik sa7a", "ma3lich", "rebbi i3awn-ik",
}


def kabylise_article(french_term: str) -> str:
    """Add Kabyle-style article to a French technical term.

    Real patterns:
      ambulance → l'ambulance
      bloc      → l'bloc
      camion    → l'camion
      pompiers  → les pompiers / l'pompiers
    """
    if french_term.lower().startswith(("a", "e", "i", "o", "u", "h")):
        return f"l'{french_term}"
    elif french_term.lower() in ("pompiers", "blessés"):
        return random.choice([f"les {french_term}", f"l'{french_term}"])
    else:
        return f"l'{french_term}"


def make_hybrid_verb(french_verb: str, *, negative: bool = False) -> str:
    """Create a Kabyle-French hybrid verb form.

    Real corpus examples:
      it-respirerara    (il ne respire pas — FR verb + KAB negation)
      t-deplacer-ed     (venir se déplacer — FR verb + KAB direction)
      at-transporter-en (ils vont transporter)
    """
    if negative:
        return f"it-{french_verb}ara"
    return f"t-{french_verb}-ed"


# ── Victim / Subject Expressions ───────────────────────────

def victim_expression(
    gender: str = "masc",
    number: int = 1,
    age: str = "adult",
) -> str:
    """Generate a Kabyle victim expression.

    Returns expressions like:
      "yiwen" (one masc), "yiweth" (one fem),
      "thaqchichth" (little girl), "amghar" (old man)
    """
    if number == 1:
        if gender == "fem":
            if age == "child":
                return random.choice(["yiweth teqchichth", "thaqchichth"])
            elif age == "aged":
                return random.choice(["yiweth temghart", "thameghrath"])
            else:
                return random.choice(["yiweth tmetthuth", "yiweth"])
        else:
            if age == "child":
                return random.choice(["yiwen l'enfant", "aqchich"])
            elif age == "aged":
                return random.choice(["yiwen l'vieux", "amghar"])
            else:
                return random.choice(["yiwen", "yiwen urgaz"])
    else:
        if gender == "fem":
            return f"{number} n tlawin"
        return f"{number} n yergazen"


# ── Utility ─────────────────────────────────────────────────

# Future markers for Béjaïa dialect
FUTURE_PARTICLES = ["ad-", "at-", "di-", "da-"]
BEJAIA_FUTURE = ["di-", "da-"]  # Preferred in EOR


def add_future_particle(verb_form: str, *, bejaia_preferred: bool = True) -> str:
    """Add future/aorist particle to a verb form.

    Béjaïa dialect prefers di-/da- over standard ad-/at-.
    """
    pool = BEJAIA_FUTURE if bejaia_preferred else FUTURE_PARTICLES
    particle = random.choice(pool)
    # Remove existing particle if present
    for p in FUTURE_PARTICLES:
        if verb_form.startswith(p):
            verb_form = verb_form[len(p):]
            break
    return f"{particle}{verb_form}"


def add_progressive(verb_form: str) -> str:
    """Wrap a verb in progressive aspect: aqla-gh + verb."""
    return f"aqla-gh {verb_form}"


def add_now(verb_form: str) -> str:
    """Add 'now' adverb: tura + verb."""
    return f"tura {verb_form}"
