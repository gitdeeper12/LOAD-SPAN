"""Model validation tests for LOAD-SPAN."""

import sys
import numpy as np

sys.path.insert(0, '.')

from load_span.modules.dlrm import DynamicLoadRedistributionModule
from load_span.modules.lssam import LongSpanStabilityModule
from load_span.modules.farm import FatigueAndReliabilityModule
from load_span.modules.aisl import AISupportLayer
from load_span.lsii import LongSpanIntegrityIndex


def test_dlrm_cable_loss_scenario():
    """Test DLRM with simulated cable loss in cable-stayed bridge."""
    print("\n=== DLRM TEST: Cable Loss ===")
    
    dlrm = DynamicLoadRedistributionModule()
    dlrm.configure(redundancy_min=0.70, redistribution_warn=0.20)
    
    result = dlrm.analyze()
    
    print(f"  Structural Redundancy R_struct: {result['r_struct']:.3f}")
    print(f"  Max DCR: {result['max_dcr']:.3f}")
    print(f"  Redistribution Magnitude: {result['redistribution_magnitude']:.3f}")
    
    assert 0.0 <= result['r_struct'] <= 1.0, "R_struct out of range"
    assert result['max_dcr'] >= 0.0, "DCR must be non-negative"
    
    if result['max_dcr'] > 1.0:
        print("  WARNING: DCR > 1.0 - Potential collapse risk")
    else:
        print("  Structure stable after redistribution")
    
    return result


def test_lssam_buckling_scenario():
    """Test LSSAM with compression member buckling analysis."""
    print("\n=== LSSAM TEST: Buckling Analysis ===")
    
    lssam = LongSpanStabilityModule()
    lssam.configure(lambda_cr_min=2.0, beta_min=3.5)
    
    result = lssam.assess()
    
    print(f"  Euler Critical Load P_cr: {result['p_cr_euler']/1e6:.2f} MN")
    print(f"  Critical Load Factor λ_cr: {result['lambda_cr']:.3f}")
    print(f"  Reliability Index β: {result['beta']:.3f}")
    print(f"  Imperfection Coefficient γ: {result['gamma_ml']:.3f}")
    
    assert result['lambda_cr'] > 0, "λ_cr must be positive"
    assert result['beta'] > 0, "β must be positive"
    
    if result['lambda_cr'] >= 2.0:
        print("  Adequate buckling safety margin")
    else:
        print(f"  WARNING: λ_cr = {result['lambda_cr']:.2f} below target (2.0)")
    
    return result


def test_farm_fatigue_scenario():
    """Test FARM with fatigue accumulation analysis."""
    print("\n=== FARM TEST: Fatigue Accumulation ===")
    
    farm = FatigueAndReliabilityModule()
    farm.configure(d_limit=0.80, d_crit=1.00, sn_class="FAT90")
    
    result = farm.compute()
    
    print(f"  Miner Fatigue Damage: {result['d_fatigue_max']:.4f}")
    print(f"  Augmented Reliability Index β: {result['beta_augmented']:.3f}")
    print(f"  Remaining Life: {result['remaining_life_days']:.0f} days")
    print(f"  Hot-Spot Stress: {result['hot_spot_stress']/1e6:.1f} MPa")
    
    assert 0.0 <= result['d_fatigue_max'] <= 1.5, "Fatigue damage out of range"
    
    if result['d_fatigue_max'] >= 0.80:
        print("  WARNING: Fatigue damage exceeded limit (0.80)")
    else:
        print("  Fatigue damage within safe limits")
    
    return result


def test_aisl_anomaly_detection():
    """Test AISL with anomaly detection simulation."""
    print("\n=== AISL TEST: Anomaly Detection ===")
    
    aisl = AISupportLayer()
    aisl.configure(physics_constrained=True, forecast_horizon=48)
    
    alerts = aisl.detect_anomalies()
    
    print(f"  Number of alerts: {len(alerts)}")
    
    for alert in alerts[:3]:
        print(f"    - Location: {alert.location}, Index: {alert.index:.3f}, Confidence: {alert.confidence:.2f}")
    
    # Fixed: Check forecast structure correctly
    forecast = aisl.forecast_lsii(horizon_hours=48)
    
    if forecast and len(forecast) > 0:
        last = forecast[-1]
        if 'lsii' in last:
            print(f"  LSII forecast after 48h: {last['lsii']:.3f}")
        if 'upper_bound' in last and 'lsii' in last:
            print(f"  Uncertainty: ±{last['upper_bound'] - last['lsii']:.3f}")
        elif 'upper' in last and 'lsii' in last:
            print(f"  Uncertainty: ±{last['upper'] - last['lsii']:.3f}")
    
    return alerts


def test_lsii_scenarios():
    """Test LSII with multiple operational scenarios."""
    print("\n=== LSII TEST: Operational Scenarios ===")
    
    lsii = LongSpanIntegrityIndex()
    
    scenarios = [
        ("Perfect", 4.5, 0.10, 0.95, 2.8),
        ("Normal", 3.8, 0.35, 0.85, 2.2),
        ("Light Degradation", 3.0, 0.55, 0.75, 1.8),
        ("Moderate Degradation", 2.2, 0.70, 0.65, 1.4),
        ("Critical", 1.5, 0.85, 0.50, 1.0),
        ("Imminent Failure", 0.8, 0.95, 0.35, 0.6),
    ]
    
    for name, beta, d_fat, r_struct, lam in scenarios:
        result = lsii.compute(beta, d_fat, r_struct, lam)
        print(f"  {name}: LSII={result.lsii:.3f} - {result.signal.value}")
        
        if name == "Perfect":
            assert result.signal.value == "🟢 STEADY_STATE"
        elif name == "Imminent Failure":
            assert result.signal.value == "🔴 CRITICAL_BREACH"
    
    return True


def test_progressive_collapse():
    """Test progressive collapse assessment."""
    print("\n=== PROGRESSIVE COLLAPSE TEST ===")
    
    from load_span.collapse.collapse_sequence import ProgressiveCollapseAnalyzer
    
    elements = [
        {'id': i, 'capacity': 1e6, 'connectivity': [i, i+1]} 
        for i in range(10)
    ]
    
    analyzer = ProgressiveCollapseAnalyzer(max_iterations=5)
    loads = np.ones(100) * 1e5
    
    result = analyzer.analyze_sequence(elements, initial_failure_id=0, loads=loads)
    
    print(f"  Collapse Propagation Distance C_prop: {result['propagation_distance']}")
    print(f"  Final State: {result['final_state']}")
    print(f"  Vulnerable to Disproportionate Collapse: {result['vulnerable_to_disproportionate_collapse']}")
    
    return result


def test_stress_hotspot():
    """Test hot-spot stress calculation."""
    print("\n=== HOT-SPOT STRESS TEST ===")
    
    def compute_hot_spot_stress(strain_04t, strain_10t, E=200e9):
        epsilon_hotspot = strain_04t + (strain_04t - strain_10t) * 0.4 / 0.6
        return epsilon_hotspot * E
    
    strain_04t = 250e-6
    strain_10t = 200e-6
    
    stress = compute_hot_spot_stress(strain_04t, strain_10t)
    print(f"  Hot-spot stress: {stress/1e6:.1f} MPa")
    assert stress > 0
    print("  Hot-spot stress test passed")
    
    return stress


def test_rainflow_cycle_counting():
    """Test rainflow cycle counting algorithm."""
    print("\n=== RAINFLOW CYCLE COUNTING TEST ===")
    
    from load_span.fatigue.rainflow import RainflowCounter
    
    t = np.linspace(0, 10, 1000)
    stress = 100e6 * np.sin(2 * np.pi * t)
    
    counter = RainflowCounter()
    cycles = counter.count(stress)
    
    print(f"  Number of cycles detected: {len(cycles)}")
    assert len(cycles) > 0
    
    if cycles:
        print(f"  Max amplitude: {max(c[0] for c in cycles)/1e6:.1f} MPa")
    
    print("  Rainflow test passed")
    
    return cycles


def run_full_model_validation():
    """Run all model validation tests."""
    print("=" * 60)
    print("LOAD-SPAN MODEL VALIDATION SUITE")
    print("=" * 60)
    
    results = {}
    passed = 0
    failed = 0
    
    tests = [
        ("DLRM Cable Loss", test_dlrm_cable_loss_scenario),
        ("LSSAM Buckling", test_lssam_buckling_scenario),
        ("FARM Fatigue", test_farm_fatigue_scenario),
        ("AISL Anomaly Detection", test_aisl_anomaly_detection),
        ("LSII Scenarios", test_lsii_scenarios),
        ("Progressive Collapse", test_progressive_collapse),
        ("Hot-Spot Stress", test_stress_hotspot),
        ("Rainflow Counting", test_rainflow_cycle_counting),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"  FAILED: {name} - {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_full_model_validation()
    sys.exit(0 if success else 1)
