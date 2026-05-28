"""Basic LSII Calculation Example."""

from load_span.lsii import LongSpanIntegrityIndex

def main():
    lsii = LongSpanIntegrityIndex()
    
    # Example 1: Healthy structure
    result = lsii.compute(
        beta=4.2,
        d_fatigue=0.25,
        r_struct=0.88,
        lambda_cr=2.4
    )
    print(f"Healthy: LSII={result.lsii:.3f} - {result.signal.value}")
    
    # Example 2: Degraded structure
    result = lsii.compute(
        beta=2.5,
        d_fatigue=0.70,
        r_struct=0.62,
        lambda_cr=1.6
    )
    print(f"Degraded: LSII={result.lsii:.3f} - {result.signal.value}")
    
    # Example 3: Critical structure
    result = lsii.compute(
        beta=1.2,
        d_fatigue=0.88,
        r_struct=0.45,
        lambda_cr=0.9
    )
    print(f"Critical: LSII={result.lsii:.3f} - {result.signal.value}")

if __name__ == "__main__":
    main()
