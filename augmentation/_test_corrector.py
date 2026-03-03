"""Quick test: verify corrector imports and works."""
import sys, os
sys.path.insert(0, os.path.abspath('.'))
from augmentation.engine.corrector import KabyleCorrector

c = KabyleCorrector()

# Test 1: combined fix
r = c.correct("ɣer yiwen n argaz, ur yezmir, la ambulance dagi")
print(f"IN:  ɣer yiwen n argaz, ur yezmir, la ambulance dagi")
print(f"OUT: {r.corrected_text}")
print(f"{r.summary}")
for x in r.corrections:
    print(f"  {x.icon} {x.rule}: {x.original} -> {x.replacement}")

# Test 2: clean text (should have 0 corrections)
r2 = c.correct("Allo, salam alaykoum, yella l'accident dagi g Bgayet")
print(f"\nClean text corrections: {r2.summary}")
assert r2.n_autofixes == 0, f"Expected 0 autofixes, got {r2.n_autofixes}"

print("\nALL TESTS PASSED")
