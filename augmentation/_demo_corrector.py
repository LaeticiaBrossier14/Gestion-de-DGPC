"""
PREUVE : le correcteur fonctionne bien.
Simule un output Gemini avec des erreurs typiques → montre les corrections.
"""
import sys, os
sys.path.insert(0, os.path.abspath('.'))
from augmentation.engine.corrector import KabyleCorrector

c = KabyleCorrector()

# Simuler un output Gemini AVEC erreurs (comme avant le prompt amélioré)
gemini_output = "Allo, awi-d l'ambulance! Yella n argaz i-ɣli deg uxxam, la tension teɛla, ur yezmir. Machi i-teddu gher ṣbitar."

print("=" * 65)
print("DEMO DU CORRECTEUR KABYLE")
print("=" * 65)
print()
print(f"GEMINI (avant correction):")
print(f"  {gemini_output}")
print()

result = c.correct(gemini_output, "medical_emergency")

print(f"CORRIGE (apres correction):")
print(f"  {result.corrected_text}")
print()
print(f"BILAN: {result.summary}")
print()

if result.corrections:
    print("DETAILS DES CORRECTIONS:")
    for x in result.corrections:
        print(f"  {x.icon} [{x.rule}] '{x.original}' -> '{x.replacement}'")
        print(f"     Explication: {x.explanation}")
        print()
else:
    print("Aucune correction necessaire.")
