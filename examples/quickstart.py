"""LOAD-SPAN Quick Start Example."""

from load_span import LoadSpanAssessor

def main():
    # Initialize assessor
    assessor = LoadSpanAssessor()
    
    # Run assessment
    result = assessor.evaluate()
    
    # Print results
    print(f"LSII Score: {result.lsii_result.lsii:.3f}")
    print(f"Safety Signal: {result.lsii_result.signal.value}")
    print(f"Reliability Index β: {result.lsii_result.beta:.3f}")
    print(f"Fatigue Damage: {result.lsii_result.d_fatigue_max:.4f}")
    print(f"Collapse Risk: {result.collapse_risk:.3f}")

if __name__ == "__main__":
    main()
