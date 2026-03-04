"""
Kabyle Assembler — Transform French scenarios into Kabyle transcriptions.

Takes a structured French scenario (from Gemini) and assembles an authentic
Kabyle-French-Arabic code-switched emergency call transcription using:
  - Template bank (templates.yaml)
  - Grammar rules (rules.yaml + morphology.py)
  - Geography data (geography.yaml)

This module NEVER calls an LLM. All Kabyle text is rule-assembled.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from augmentation.engine.morphology import (
    EMERGENCY_VERBS,
    KEEP_FRENCH,
    NegationType,
    Person,
    Tense,
    add_future_particle,
    add_now,
    add_progressive,
    conjugate,
    construct_state,
    kabylise_article,
    make_hybrid_verb,
    negate,
    victim_expression,
)

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


# ── Config Loading ──────────────────────────────────────────

def _load_yaml(name: str) -> Dict[str, Any]:
    path = CONFIG_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_templates() -> Dict[str, Any]:
    return _load_yaml("templates.yaml")


def load_rules() -> Dict[str, Any]:
    return _load_yaml("rules.yaml")


def load_geography() -> Dict[str, Any]:
    return _load_yaml("geography.yaml")


# ── Weighted Random Selection ───────────────────────────────

def weighted_choice(items: List[Dict[str, Any]], key: str = "text", weight_key: str = "weight") -> str:
    """Select from weighted list, returning the text value."""
    texts = [item[key] for item in items]
    weights = [item.get(weight_key, 1) for item in items]
    return random.choices(texts, weights=weights, k=1)[0]


# ── Geography Sampling ──────────────────────────────────────

@dataclass
class LocationSample:
    """A sampled location from geography.yaml."""
    daira: str
    commune: str
    lieu: str
    repere: str

    def format_location_phrase(self) -> str:
        """Generate a location phrase in Kabyle style."""
        patterns = [
            f"g {self.lieu}, {self.commune}",
            f"deg {self.lieu}, g {self.commune}",
            f"athan g {self.lieu}, hedha {self.repere}",
            f"dayi g {self.lieu}",
            f"g {self.lieu}, {self.repere}",
        ]
        return random.choice(patterns)


def sample_location(geo: Dict[str, Any], *, daira_hint: str = "") -> LocationSample:
    """Sample a random location from geography, weighted by real distribution."""
    dairas = geo.get("dairas", [])
    if not dairas:
        return LocationSample("Béjaïa", "Béjaïa", "Centre-ville", "l'APC")

    # Pick daira
    if daira_hint:
        matching = [d for d in dairas if d["name"].lower() == daira_hint.lower()]
        daira = matching[0] if matching else random.choices(
            dairas, weights=[d.get("weight", 1) for d in dairas], k=1
        )[0]
    else:
        daira = random.choices(
            dairas, weights=[d.get("weight", 1) for d in dairas], k=1
        )[0]

    # Pick commune within daira
    communes = daira.get("communes", [])
    if not communes:
        return LocationSample(daira["name"], daira["name"], "Centre-ville", "l'APC")

    commune = random.choices(
        communes, weights=[c.get("weight", 1) for c in communes], k=1
    )[0]

    # Pick lieu and repere
    lieux = commune.get("lieux", ["Centre-ville"])
    reperes = commune.get("reperes", ["l'APC"])

    return LocationSample(
        daira=daira["name"],
        commune=commune["name"],
        lieu=random.choice(lieux),
        repere=random.choice(reperes),
    )


def sample_water_body(geo: Dict[str, Any]) -> Tuple[str, str]:
    """Sample a water body for drowning scenarios. Returns (name, kabyle_name)."""
    water = geo.get("water_bodies", {})
    all_bodies = []
    for category in ("rivers", "beaches", "dams"):
        for body in water.get(category, []):
            all_bodies.append((body.get("name", ""), body.get("kabyle_name", body.get("name", ""))))
    if not all_bodies:
        return ("Oued Soummam", "asif n Soummam")
    return random.choice(all_bodies)


# ── Dialogue Turn Assembler ─────────────────────────────────

@dataclass
class ScenarioInput:
    """Input from the French scenario generator (Stage 1)."""
    incident_type: str
    urgency: str = "high"
    # Location
    daira: str = ""
    commune: str = ""
    lieu: str = ""
    repere: str = ""
    # Victim
    victim_gender: str = "masc"
    victim_age: str = "adult"
    victim_count: int = 1
    victim_state: str = "conscious"
    medical_detail: str = ""
    # Fire
    fire_source: str = ""
    # Accident
    vehicle_type: str = ""
    accident_detail: str = ""
    # Drowning
    water_body: str = ""
    # Caller
    caller_emotion: str = "calm"
    caller_relation: str = "témoin"
    # Dialogue structure hints (from LLM)
    dialogue_turns: List[Dict[str, str]] = field(default_factory=list)


class KabyleAssembler:
    """Assembles Kabyle emergency call transcriptions from scenarios + rules."""

    def __init__(self):
        self.templates = load_templates()
        self.rules = load_rules()
        self.geo = load_geography()

    def assemble(self, scenario: ScenarioInput) -> str:
        """Assemble a full Kabyle transcription from a scenario.

        Returns a multi-turn dialogue string matching real corpus format:
          "Operator: ... Caller: ... Operator: ..."
        """
        turns: List[str] = []

        # Resolve location
        if scenario.lieu:
            loc = LocationSample(
                daira=scenario.daira or "Béjaïa",
                commune=scenario.commune or "Béjaïa",
                lieu=scenario.lieu,
                repere=scenario.repere or "l'APC",
            )
        else:
            loc = sample_location(self.geo, daira_hint=scenario.daira)

        # ── Turn 1: Caller greeting + service identification ──
        greeting = weighted_choice(self.templates["greetings"])
        greeting = greeting.replace("{service}", self._pick_service(scenario))
        greeting = greeting.replace("{commune}", loc.commune)

        # Some callers also identify service in greeting
        if "{" not in greeting and random.random() < 0.4:
            svc = self._pick_service_phrase(scenario, loc)
            greeting = f"{greeting} {svc}"

        turns.append(f"Caller: {greeting}")

        # ── Turn 2: Operator acknowledgment ──
        op_ack = random.choice([
            "An3am.",
            "Allo, an3am.",
            "Oui.",
            f"les pompiers n {loc.commune}, an3am.",
        ])
        turns.append(f"Operator: {op_ack}")

        # ── Turn 3: Caller describes incident ──
        description = self._assemble_incident_description(scenario, loc)
        turns.append(f"Caller: {description}")

        # ── Turn 4: Operator asks for location / details ──
        op_question = self._pick_operator_question(scenario)
        turns.append(f"Operator: {op_question}")

        # ── Turn 5: Caller gives location details ──
        loc_detail = self._assemble_location_detail(scenario, loc)
        turns.append(f"Caller: {loc_detail}")

        # ── Turn 6: Operator confirms location ──
        loc_confirm = self._operator_confirm_location(loc)
        turns.append(f"Operator: {loc_confirm}")

        # ── Turn 7: Caller confirms ──
        confirm = random.choice(["an3am.", "ih.", "oui.", "iyeh."])
        turns.append(f"Caller: {confirm}")

        # ── Turn 8+: Additional detail turns (for rich scenarios) ──
        extra_turns = self._generate_extra_turns(scenario, loc)
        turns.extend(extra_turns)

        # ── Final turns: Operator dispatch + closing ──
        dispatch = self._operator_dispatch(scenario, loc)
        turns.append(f"Operator: {dispatch}")

        # Caller closing
        closing = weighted_choice(self.templates["closings"])
        turns.append(f"Caller: {closing}")

        # Final operator closing
        op_close = random.choice(["Saha.", "D'accord, sahit.", "Sa7a."])
        turns.append(f"Operator: {op_close}")

        # Join as single transcription (matching real format)
        return " ".join(turns)

    # ── Incident Description Assembly ───────────────────────

    def _assemble_incident_description(
        self, scenario: ScenarioInput, loc: LocationSample
    ) -> str:
        """Build the core incident description in Kabyle."""
        itype = scenario.incident_type

        if itype in ("medical_emergency",):
            return self._describe_medical(scenario, loc)
        elif itype in ("accident_vehicular", "accident_pedestrian"):
            return self._describe_accident(scenario, loc)
        elif itype in ("fire_building", "fire_vehicle", "fire_forest"):
            return self._describe_fire(scenario, loc)
        elif itype == "drowning":
            return self._describe_drowning(scenario, loc)
        elif itype in ("assault_violence",):
            return self._describe_assault(scenario, loc)
        elif itype == "structural_collapse":
            return self._describe_collapse(scenario, loc)
        else:
            return self._describe_generic(scenario, loc)

    def _describe_medical(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Medical emergency: use ghli/doukh/yugh/hlek verbs."""
        victim = victim_expression(s.victim_gender, s.victim_count, s.victim_age)
        verb_key = random.choice(["ghli", "hlek", "doukh"])
        person = Person.SG3F if s.victim_gender == "fem" else Person.SG3M
        verb = conjugate(verb_key, person, Tense.PRETERITE)

        location_phrase = loc.format_location_phrase()
        medical = s.medical_detail or random.choice([
            "crise n'wul", "l'tension sighlin", "il est inconscient",
            "idoukh", "ihlek mlih",
        ])

        # Pattern: "nes3a {victim} dayi g {loc}, {medical}"
        patterns = [
            f"nes3a {victim} dayi {location_phrase}, {medical}.",
            f"{victim} {verb} {location_phrase}.",
            f"attan {victim} dayi, {verb}, {medical}.",
            f"yella {victim} dayi {location_phrase}, {medical}.",
        ]
        base = random.choice(patterns)

        # Emotional intensifiers for urgent/panicked callers
        if s.caller_emotion in ("paniqué", "urgent"):
            base += random.choice([
                " Urgent mlih mlih!",
                f" {kabylise_article('ambulance')} s'il vous plaît!",
                " arwa7-d! arwa7-d!",
            ])

        return base

    def _describe_accident(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Vehicular/pedestrian accident description."""
        vehicle = s.vehicle_type or random.choice(["tomobil", "moto", "l'camion"])
        location_phrase = loc.format_location_phrase()
        detail = s.accident_detail or random.choice([
            "t-déraper", "t-qleb", "yewwet-it",
        ])

        patterns = [
            f"thella une accident {location_phrase}, {vehicle} {detail}.",
            f"nes3a un accident {location_phrase}.",
            f"yiwen {vehicle} {detail} {location_phrase}.",
            f"une accident {vehicle} {location_phrase}, {detail}.",
        ]
        base = random.choice(patterns)

        # Add victim state if available
        if s.victim_state == "unconscious":
            base += " Il est inconscient."
        elif s.victim_state == "bleeding":
            base += " Iddem i-ttazal."

        return base

    def _describe_fire(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Fire description: use che3l/cha3l verbs."""
        source = s.fire_source or random.choice([
            "l'tomobil", "l'appartement", "lekhyout n l'triciti",
            "l'forêt", "l'bâtiment",
        ])
        verb = conjugate("che3l", Person.SG3M, Tense.PRETERITE)
        location_phrase = loc.format_location_phrase()

        patterns = [
            f"tche3l {source} {location_phrase}.",
            f"{verb} l'nar g {source}, {location_phrase}.",
            f"nes3a un incendie {location_phrase}, {source} cha3let.",
        ]
        return random.choice(patterns)

    def _describe_drowning(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Drowning: use ghleq verb + water body."""
        water_name, water_kab = sample_water_body(self.geo)
        if s.water_body:
            water_kab = s.water_body

        victim = victim_expression(s.victim_gender, s.victim_count, s.victim_age)
        verb = conjugate("ghleq", Person.SG3M if s.victim_gender == "masc" else Person.SG3F, Tense.PRETERITE)
        location_phrase = loc.format_location_phrase()

        patterns = [
            f"{victim} {verb} deg waman g {water_kab}, {location_phrase}.",
            f"nes3a {victim} {verb} g {water_kab}. Urgent!",
            f"{victim} yeghli g {water_kab}, {verb}, {location_phrase}.",
        ]
        base = random.choice(patterns)

        # Drowning is always urgent
        base += f" Arwa7-d s'il vous plaît, {kabylise_article('ambulance')}!"
        return base

    def _describe_assault(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Assault / violence description."""
        victim = victim_expression(s.victim_gender, s.victim_count, s.victim_age)
        location_phrase = loc.format_location_phrase()
        detail = s.accident_detail or random.choice([
            "yewwet-it s l'couteau", "yella l'bagarre",
            "yewwet-it", "3arku-t",
        ])

        patterns = [
            f"yella {victim} {detail} {location_phrase}.",
            f"nes3a l'bagarre {location_phrase}, {victim} blessé.",
            f"{victim} yewwet-it {location_phrase}.",
        ]
        return random.choice(patterns)

    def _describe_collapse(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Structural collapse description."""
        structure = s.fire_source or random.choice([
            "l'7iḍ", "l'bâtiment", "l'plafond", "l'balcon",
        ])
        location_phrase = loc.format_location_phrase()

        patterns = [
            f"yeghli {structure} {location_phrase}.",
            f"nes3a un effondrement {location_phrase}, {structure} yeghli.",
        ]
        base = random.choice(patterns)

        if s.victim_count > 0:
            victim = victim_expression(s.victim_gender, s.victim_count, s.victim_age)
            base += f" {victim} t7et-as."
        return base

    def _describe_generic(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Generic incident for unknown/other types."""
        location_phrase = loc.format_location_phrase()
        return f"nes3a l'urgence dayi {location_phrase}. S'il vous plaît, cheye3-ed."

    # ── Service Identification ──────────────────────────────

    def _pick_service(self, s: ScenarioInput) -> str:
        """Pick the emergency service name based on incident type."""
        if s.incident_type in ("fire_building", "fire_vehicle", "fire_forest"):
            return random.choice(["les pompiers", "l'pompiers"])
        elif s.incident_type == "medical_emergency":
            return random.choice(["l'ambulance", "les pompiers", "l'7imaya"])
        else:
            return random.choice(["les pompiers", "l'7imaya", "protection civile"])

    def _pick_service_phrase(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Full service identification phrase."""
        svc = self._pick_service(s)
        if random.random() < 0.3:
            return f"{svc} n {loc.commune}?"
        return f"{svc}?"

    # ── Operator Questions ──────────────────────────────────

    def _pick_operator_question(self, s: ScenarioInput) -> str:
        """Pick appropriate operator question based on context."""
        questions_by_type = {
            "location": [
                "Anda?", "Anwa amkan?", "Anida?",
                "Wash-n la commune?",
            ],
            "nature": [
                "Dachu i-yuɣen?", "Dachu yellan?",
                "Achu gellan?",
            ],
            "victim": [
                "Sh7al i gellan?", "Amek l'état-ines?",
            ],
        }

        # Usually ask location first
        pool = questions_by_type["location"]
        if random.random() < 0.3:
            pool = questions_by_type["nature"]
        return random.choice(pool)

    # ── Location Detail Assembly ────────────────────────────

    def _assemble_location_detail(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Caller gives location details."""
        parts = []

        # Name the place
        parts.append(loc.lieu)

        # Add commune if different from default
        if random.random() < 0.6:
            parts.append(loc.commune)

        # Add landmark
        if random.random() < 0.5:
            parts.append(loc.repere)

        return ", ".join(parts) + "."

    def _operator_confirm_location(self, loc: LocationSample) -> str:
        """Operator confirms location."""
        patterns = [
            f"{loc.lieu}?",
            f"D'accord, {loc.commune}.",
            f"{loc.lieu}, {loc.commune}?",
            f"Eh, {loc.lieu}.",
        ]
        return random.choice(patterns)

    # ── Extra Turns ─────────────────────────────────────────

    def _generate_extra_turns(self, s: ScenarioInput, loc: LocationSample) -> List[str]:
        """Generate additional dialogue turns for richer scenarios."""
        extras: List[str] = []

        # ── Operator asks about victim state ──
        if s.incident_type in ("medical_emergency", "accident_vehicular", "drowning"):
            if random.random() < 0.6:
                q = random.choice([
                    "Dachu i-yuɣen?",
                    "Amek l'état-ines?",
                    "T-nuffes? Machi?",
                ])
                extras.append(f"Operator: {q}")

                # Caller responds with medical details
                state = self._victim_state_phrase(s)
                extras.append(f"Caller: {state}")

        # ── Bloc / apartment details for urban calls ──
        if "logements" in loc.lieu.lower() or "cité" in loc.lieu.lower():
            if random.random() < 0.5:
                bloc = random.randint(1, 30)
                extras.append(f"Operator: Wacho l'bloc?")
                extras.append(f"Caller: L'bloc {bloc}.")

        # ── Family name (real pattern) ──
        if random.random() < 0.2:
            names = ["Benoudiba", "Afia", "Wannoughène", "Hakimi", "Berqouqi"]
            extras.append(f"Operator: Dachu la famille?")
            extras.append(f"Caller: {random.choice(names)}.")

        # ── Identity of caller ──
        if s.caller_relation == "médecin" and random.random() < 0.7:
            extras.append(f"Caller: C'est docteur {random.choice(['Hakimi', 'Benali', 'Mohand'])}. "
                         f"{s.medical_detail or 'il est dans un état grave'}.")

        # ── Redirect to local unit (real pattern: 20% of calls) ──
        if random.random() < 0.15:
            phone = self._pick_phone_number(loc)
            extras.append(f"Operator: Ak-d-fka l'numéro n {loc.commune}. "
                         f"Marki ghorek: {phone}.")
            extras.append(f"Caller: {phone}?")
            extras.append(f"Operator: An3am.")

        return extras

    def _victim_state_phrase(self, s: ScenarioInput) -> str:
        """Generate victim state description."""
        states = self.templates.get("victim_state", {})
        state_key = s.victim_state or "conscious"

        pool = states.get(state_key, states.get("conscious", ["mazal-it"]))
        base = random.choice(pool) if isinstance(pool, list) else str(pool)

        # Add medical detail
        if s.medical_detail:
            base += f", {s.medical_detail}"

        return base + "."

    # ── Operator Dispatch ───────────────────────────────────

    def _operator_dispatch(self, s: ScenarioInput, loc: LocationSample) -> str:
        """Operator confirms dispatch."""
        patterns = [
            f"D'accord, atura at-le7qed {kabylise_article('ambulance')}.",
            f"D'accord, aqla-gh n-teddu-d.",
            f"D'accord, sensiwlegh i {loc.commune}.",
            f"Khalas, d'accord. Tout de suite.",
            f"D'accord agma, tura at-ncheye3.",
        ]
        return random.choice(patterns)

    # ── Phone Numbers ───────────────────────────────────────

    def _pick_phone_number(self, loc: LocationSample) -> str:
        """Pick a plausible phone number for the location."""
        phones = self.geo.get("phone_patterns", {})
        key = loc.commune.lower().replace(" ", "_").replace("é", "e").replace("ï", "i")

        if key in phones:
            return phones[key]

        # Generate plausible number
        prefix = phones.get("bejaia_prefix", "034")
        return f"{prefix} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}"


# ── Convenience Function ────────────────────────────────────

def assemble_transcription(scenario: ScenarioInput) -> str:
    """One-shot assembly: scenario → Kabyle transcription."""
    assembler = KabyleAssembler()
    return assembler.assemble(scenario)
