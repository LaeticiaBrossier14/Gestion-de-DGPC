"""
Scenario Generator — Stage 1: Generate rich French emergency scenarios via Gemini.

The LLM generates FRENCH scenarios only — no Kabyle.
The assembler (Stage 2) then translates them using rules.

Uses Pydantic structured output for guaranteed schema compliance.
"""

from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

# ── Pydantic Schemas for Gemini Structured Output ───────────


class LocationInfo(BaseModel):
    """Location data for the emergency scenario."""
    daira: str = Field(description="Daïra de Béjaïa (ex: Béjaïa, El Kseur, Kherrata)")
    commune: str = Field(description="Commune (ex: Béjaïa, Oued Ghir, Tichy)")
    lieu_dit: str = Field(description="Lieu-dit ou cité (ex: cité 3200 logements, Boulimat)")
    repere: str = Field(description="Point de repère (ex: zdat la poste, hedha l'mairie)")


class CallerProfile(BaseModel):
    """Profile of the person calling emergency services."""
    relation_victime: str = Field(description="Relation: lui-même, voisin, parent, témoin, médecin")
    etat_emotionnel: str = Field(description="État: paniqué, calme, en_colère, confus, pleurs")
    genre: str = Field(default="masc", description="Genre de l'appelant: masc ou fem")


class VictimInfo(BaseModel):
    """Information about the victim(s)."""
    nombre: int = Field(default=1, ge=0, le=20)
    age_approx: str = Field(description="Catégorie: enfant, adulte, agé")
    genre: str = Field(description="Genre: homme, femme, mixte")
    etat: str = Field(description="État: conscient, inconscient, blessé, critique, décédé")
    details_medicaux: str = Field(
        default="",
        description="Détails: crise cardiaque, chute de tension, noyade, brûlures, fracture"
    )


class IncidentDetails(BaseModel):
    """Details about the emergency incident."""
    description_fr: str = Field(
        description="Description détaillée en français (3-5 phrases)"
    )
    elements_sensoriels: List[str] = Field(
        default_factory=list,
        description="Éléments sensoriels: fumée, sang, cris, eau, feu"
    )
    facteurs_aggravants: List[str] = Field(
        default_factory=list,
        description="Facteurs: enceinte, handicapé, nuit, isolé, enfant seul"
    )
    services_demandes: List[str] = Field(
        default_factory=list,
        description="Services: ambulance, pompiers, police"
    )
    # Type-specific fields
    vehicle_type: str = Field(default="", description="Pour accidents: voiture, moto, camion")
    fire_source: str = Field(default="", description="Pour incendies: appartement, forêt, véhicule")
    water_body: str = Field(default="", description="Pour noyades: plage, oued, barrage")
    structure_type: str = Field(default="", description="Pour effondrements: mur, balcon, bâtiment")


class DialogueTurn(BaseModel):
    """A single turn in the emergency call dialogue."""
    speaker: Literal["caller", "operator"] = Field(description="Qui parle")
    intent: str = Field(
        description="Intent: greeting, identify_service, describe_incident, "
                    "give_location, ask_location, ask_details, confirm, "
                    "instruct, provide_number, dispatch, closing"
    )
    content_fr: str = Field(description="Contenu du tour de parole EN FRANÇAIS")
    emotion: str = Field(default="neutre", description="Émotion: urgent, calme, confus, paniqué")


class EmergencyScenario(BaseModel):
    """Complete emergency scenario — ALL in French."""
    incident_type: str = Field(
        description="Type: medical_emergency, accident_vehicular, fire_building, "
                    "fire_vehicle, fire_forest, drowning, assault_violence, "
                    "structural_collapse, hazmat, lost_person, other"
    )
    urgency: str = Field(description="Urgence: critical, high, medium, low")
    location: LocationInfo
    caller: CallerProfile
    victim: VictimInfo
    details: IncidentDetails
    dialogue: List[DialogueTurn] = Field(
        min_length=6, max_length=16,
        description="Dialogue de 6 à 16 tours entre appelant et opérateur"
    )


class ScenarioBatch(BaseModel):
    """Batch of scenarios for structured output."""
    scenarios: List[EmergencyScenario]


# ── Prompt Templates ────────────────────────────────────────

SYSTEM_PROMPT = """Tu es un expert en génération de scénarios d'appels d'urgence pour l'Algérie.

CONTEXTE:
- Protection Civile (l'Himaya) de Béjaïa, Algérie
- Numéros d'urgence: 14, 1021
- Zone: Wilaya de Béjaïa (Kabylie orientale)
- Les appels réels mélangent kabyle, français et arabe dialectal

RÈGLES:
1. Génère UNIQUEMENT en FRANÇAIS — jamais de kabyle, un moteur séparé s'en charge
2. Le dialogue doit suivre le flux réel: salutation → identification service → description incident → localisation → confirmation → dispatch → clôture
3. Utilise des lieux RÉELS de Béjaïa (cités, routes, villages)
4. Varie les profils appelants: paniqué, calme, confus, médecin, voisin, parent
5. Varie la longueur: 6-16 tours de dialogue
6. Sois RÉALISTE: les vrais appels ont des hésitations, des répétitions, des confusions
"""


def _build_scenario_prompt(
    incident_type: str,
    count: int,
    geography_context: str,
) -> str:
    """Build the generation prompt for Gemini."""
    type_descriptions = {
        "drowning": "Noyade dans un oued, plage ou barrage. La victime est souvent un enfant ou un nageur. "
                    "Urgence maximale. L'appelant est paniqué.",
        "assault_violence": "Agression physique, bagarre, ou violence. Peut impliquer des armes blanches. "
                           "L'appelant peut être la victime ou un témoin.",
        "hazmat": "Incident impliquant des matières dangereuses: fuite de gaz, produits chimiques, "
                 "pollution industrielle. Zone industrielle d'Akbou ou El Kseur.",
        "structural_collapse": "Effondrement d'un mur, balcon, plafond ou bâtiment. Souvent dans des "
                              "vieux bâtiments ou après de fortes pluies.",
        "fire_forest": "Feu de forêt dans les montagnes ou maquis autour de Béjaïa. "
                      "Souvent en été. Peut menacer des habitations.",
        "lost_person": "Personne perdue: enfant, personne âgée avec Alzheimer, randonneur. "
                      "L'appelant est un parent ou un voisin inquiet.",
        "medical_emergency": "Urgence médicale: crise cardiaque, AVC, chute, malaise, "
                            "femme enceinte, crise d'asthme, épilepsie.",
        "accident_vehicular": "Accident de la route: dérapage, collision, renversement. "
                             "Sur route nationale, autoroute, ou route de montagne.",
        "fire_building": "Incendie dans un bâtiment: appartement, local commercial. "
                        "Souvent causé par un court-circuit ou une fuite de gaz.",
        "fire_vehicle": "Véhicule en feu sur la route. Souvent après un accident ou "
                       "une surchauffe moteur.",
    }

    type_desc = type_descriptions.get(incident_type, "Incident d'urgence non spécifié.")

    return f"""{SYSTEM_PROMPT}

INCIDENT À GÉNÉRER: {incident_type}
DESCRIPTION: {type_desc}

GÉOGRAPHIE DISPONIBLE:
{geography_context}

Génère exactement {count} scénarios variés pour ce type d'incident.
Chaque scénario doit avoir un dialogue de 6 à 16 tours.
Varie les profils, les lieux, les niveaux d'urgence, et les émotions.
"""


# ── Gemini API Interface ───────────────────────────────────

class ScenarioGenerator:
    """Generates French emergency scenarios using Gemini API."""

    def __init__(self, api_key: str = "", model_name: str = "gemini-2.0-flash"):
        self._api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self._model_name = model_name
        self._model = None

    def _get_model(self) -> Any:
        if self._model is None:
            try:
                from google import genai
                client = genai.Client(api_key=self._api_key)
                self._model = client
            except ImportError:
                import google.generativeai as genai
                genai.configure(api_key=self._api_key)
                self._model = genai.GenerativeModel(self._model_name)
        return self._model

    def generate_scenarios(
        self,
        incident_type: str,
        count: int = 5,
        geography_context: str = "",
        *,
        temperature: float = 0.85,
        retries: int = 2,
    ) -> List[Dict[str, Any]]:
        """Generate French scenarios via Gemini structured output.

        Returns list of scenario dicts matching EmergencyScenario schema.
        """
        prompt = _build_scenario_prompt(incident_type, count, geography_context)
        model = self._get_model()

        for attempt in range(retries + 1):
            try:
                scenarios = self._call_gemini(model, prompt, count, temperature)
                if scenarios:
                    return scenarios
            except Exception as exc:
                print(f"  [Attempt {attempt+1}/{retries+1}] Generation error: {exc}")
                if attempt < retries:
                    time.sleep(2 * (attempt + 1))

        print(f"  ⚠ All retries failed for {incident_type}. Using local fallback.")
        return self._local_fallback(incident_type, count)

    def _call_gemini(
        self, model: Any, prompt: str, count: int, temperature: float
    ) -> List[Dict[str, Any]]:
        """Call Gemini with structured output."""
        try:
            # Try google-genai (new SDK) first
            from google import genai
            from google.genai import types

            response = model.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    response_mime_type="application/json",
                    response_schema=ScenarioBatch,
                ),
            )
            if response and response.text:
                import json
                data = json.loads(response.text)
                return data.get("scenarios", [data] if "incident_type" in data else [])
        except ImportError:
            pass

        # Fallback to google-generativeai (old SDK)
        generation_config = {
            "temperature": temperature,
            "response_mime_type": "application/json",
            "response_schema": ScenarioBatch,
        }
        response = model.generate_content(prompt, generation_config=generation_config)
        if response and response.text:
            import json
            data = json.loads(response.text)
            return data.get("scenarios", [data] if "incident_type" in data else [])

        return []

    def _local_fallback(
        self, incident_type: str, count: int
    ) -> List[Dict[str, Any]]:
        """Generate minimal scenarios locally when Gemini is unavailable.

        These are less rich but structurally valid, enough for the assembler.
        """
        scenarios = []
        for _ in range(count):
            scenario = {
                "incident_type": incident_type,
                "urgency": random.choice(["critical", "high", "medium"]),
                "location": {
                    "daira": "Béjaïa",
                    "commune": random.choice(["Béjaïa", "El Kseur", "Seddouk", "Tichy"]),
                    "lieu_dit": random.choice([
                        "Centre-ville", "cité 1000 logements", "Ihaddaden",
                        "Boulimat", "Route Nationale 12",
                    ]),
                    "repere": random.choice(["l'APC", "la poste", "la mosquée"]),
                },
                "caller": {
                    "relation_victime": random.choice(["témoin", "voisin", "parent"]),
                    "etat_emotionnel": random.choice(["paniqué", "calme", "confus"]),
                    "genre": random.choice(["masc", "fem"]),
                },
                "victim": {
                    "nombre": random.choice([1, 1, 1, 2]),
                    "age_approx": random.choice(["adulte", "agé", "enfant"]),
                    "genre": random.choice(["homme", "femme"]),
                    "etat": random.choice(["conscient", "inconscient", "blessé"]),
                    "details_medicaux": "",
                },
                "details": {
                    "description_fr": f"Incident de type {incident_type} signalé.",
                    "elements_sensoriels": [],
                    "facteurs_aggravants": [],
                    "services_demandes": ["ambulance"],
                    "vehicle_type": "",
                    "fire_source": "",
                    "water_body": "",
                    "structure_type": "",
                },
                "dialogue": [],
            }
            scenarios.append(scenario)
        return scenarios


# ── Convenience ─────────────────────────────────────────────

def generate_geography_context(geo: Dict[str, Any]) -> str:
    """Format geography data as context for the LLM prompt."""
    lines = []
    for daira in geo.get("dairas", []):
        communes = [c["name"] for c in daira.get("communes", [])]
        lieux = []
        for c in daira.get("communes", []):
            lieux.extend(c.get("lieux", [])[:3])
        lines.append(
            f"- Daïra {daira['name']}: communes {', '.join(communes)}; "
            f"lieux-dits: {', '.join(lieux[:5])}"
        )

    # Water bodies
    water = geo.get("water_bodies", {})
    for cat in ("rivers", "beaches", "dams"):
        for body in water.get(cat, []):
            lines.append(f"- {cat.title()}: {body.get('name', '')} ({body.get('location', '')})")

    return "\n".join(lines)
