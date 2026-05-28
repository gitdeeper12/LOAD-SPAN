<div align="center">

# LOAD-SPAN

### Dynamic Load Redistribution Analysis and Long-Span Structural Stability Assessment with AI-Assisted Analytical Support

**Structural Mechanics · Reliability Engineering · Dynamic Loading · AI-Augmented Monitoring Support · Long-Span Infrastructure Safety**

---

[![PyPI version](https://img.shields.io/pypi/v/load-span-engine?color=14362A&label=PyPI&logo=pypi&logoColor=white)](https://pypi.org/project/load-span-engine)
[![PyPI downloads](https://img.shields.io/pypi/dm/load-span-engine?color=1A5C3A&label=Downloads&logo=pypi&logoColor=white)](https://pypi.org/project/load-span-engine/#files)
[![Python versions](https://img.shields.io/pypi/pyversions/load-span-engine?color=306998&logo=python&logoColor=white)](https://pypi.org/project/load-span-engine)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20422430-blue.svg)](https://doi.org/10.5281/zenodo.20422430)
[![OSF Preregistration](https://img.shields.io/badge/OSF-Preregistered-blue?logo=osf&logoColor=white)](https://doi.org/10.17605/OSF.IO/H35FU)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--8903--0029-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0003-8903-0029)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Domain](https://img.shields.io/badge/Domain-Structural%20Safety%20%26%20Reliability-14362A)](https://doi.org/10.5281/zenodo.20422430)
[![Series](https://img.shields.io/badge/Series-SPAN--SAFETY--01-7A4A0A)](https://doi.org/10.5281/zenodo.20422430)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](https://github.com/gitdeeper12/LOAD-SPAN)

</div>

---

## 📌 Overview

**LOAD-SPAN** is a dynamic load redistribution analysis and structural stability assessment framework for long-span systems — including cable-stayed and suspension bridges, large-span roof trusses, offshore platforms, and viaduct superstructures — grounded in classical structural mechanics, fracture mechanics, and reliability engineering, with an AI-assisted analytical support layer operating under strict physical constraints.

> *"A long-span structure under operational and environmental loading is not in static equilibrium — it is a dynamically evolving system continuously redistributing internal forces, accumulating fatigue damage at connections, and progressing toward or receding from its reliability index threshold in real time. LOAD-SPAN quantifies these changes continuously and governs the safety margin accordingly."*

Conventional periodic inspection of long-span structures cannot detect dynamic load redistribution patterns, assess fatigue damage accumulation at welded and bolted connections under variable amplitude stress histories, or evaluate the structural reliability index under the specific loading conditions of the next extreme event. LOAD-SPAN provides a continuous, quantitative, four-module analytical framework that classifies structural condition in real time as:

| Signal | Safety Status | Action |
|---|---|---|
| 🟢 **STEADY STATE** | `LSII ≥ 0.90` | All margins within safe bounds — continuous monitoring, standard schedule |
| 🟠 **MONITORING PHASE 1** | `0.75 ≤ LSII < 0.90` | Enhanced monitoring frequency; targeted inspection at flagged connections |
| 🟠 **MITIGATION PHASE 2** | `0.65 ≤ LSII < 0.75` | Operational load restriction; immediate structural review |
| 🔴 **CRITICAL BREACH** | `LSII < 0.65` | Immediate closure; exclusion zone enforcement; emergency structural assessment |

---

## 🗂️ Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [LOAD-SPAN Pipeline](#-load-span-pipeline)
- [Governing Equations](#-governing-equations)
- [Scoring & Safety Bounds](#-scoring--safety-bounds)
- [Platforms & Mirrors](#-platforms--mirrors)
- [Clone & Download](#-clone--download)
- [Citation](#-citation)
- [License](#-license)
- [Author](#-author)

---

## ✨ Key Features

- **Four-module coupled assessment pipeline** — DLRM (Dynamic Load Redistribution Module), LSSAM (Long-Span Structural Stability Assessment Module), FARM (Fatigue Accumulation and Reliability Module), AISL (AI-Assisted Support Layer)
- **Long-Span Structural Integrity Index (LSII)** — weighted composite safety metric with four-level governance decision logic
- **Direct stiffness method with member redundancy tracking** — global stiffness assembly K·u = f with real-time redistribution detection
- **Palmgren–Miner damage accumulation** — rainflow cycle counting + Goodman mean stress correction + IIW hot-spot stress approach
- **Cornell–Hasofer–Lind reliability index (β)** — first-order reliability method (FORM) with continuous β-to-P_f mapping
- **Euler–Riks buckling analysis** — critical load factor λ_cr with geometric nonlinearity (P-delta) correction
- **Progressive collapse assessment** — alternate load path (ALP) analysis + GSA/UFC robustness protocols
- **24–48 hour LSII trend projection** — warning lead time versus 0–4 hours for conventional monitoring
- **±2.94% LSII accuracy** — validated against 3 independent field and laboratory data sets
- **Full open-source distribution** — available across 11 platforms

---

## 📁 Project Structure

```
LOAD-SPAN/
│
├── load_span/                              # Core Python package
│   ├── __init__.py                         # Package entry point & public API
│   ├── pipeline.py                         # Main LOAD-SPAN assessment pipeline
│   ├── lsii.py                             # LSII composite index & governance logic
│   │
│   ├── modules/                            # Four analytical modules
│   │   ├── __init__.py
│   │   ├── dlrm.py                         # Module 1: Dynamic Load Redistribution Module
│   │   ├── lssam.py                        # Module 2: Long-Span Structural Stability Assessment Module
│   │   ├── farm.py                         # Module 3: Fatigue Accumulation and Reliability Module
│   │   └── aisl.py                         # Module 4: AI-Assisted Support Layer
│   │
│   ├── stiffness/                          # Direct stiffness method subsystem
│   │   ├── __init__.py
│   │   ├── assembly.py                     # Global stiffness matrix assembly K·u = f
│   │   ├── redistribution.py               # Internal force redistribution tracking
│   │   ├── member_forces.py                # Member axial, shear, moment extraction
│   │   ├── influence_lines.py              # Moving load influence line computation
│   │   └── redundancy.py                   # Structural redundancy index R_struct
│   │
│   ├── stability/                          # Buckling and geometric stability
│   │   ├── __init__.py
│   │   ├── euler_buckling.py               # Critical load P_cr = π²EI / (KL)²
│   │   ├── riks.py                         # Euler–Riks arc-length incremental solver
│   │   ├── pdelta.py                       # P-delta geometric stiffness K_G
│   │   ├── buckling_mode.py                # Mode shape extraction and λ_cr computation
│   │   └── lateral_torsional.py            # Lateral-torsional buckling assessment
│   │
│   ├── fatigue/                            # Fatigue and reliability subsystem
│   │   ├── __init__.py
│   │   ├── rainflow.py                     # ASTM E1049-85 rainflow cycle counting
│   │   ├── sn_curves.py                    # Eurocode FAT class S-N curve database
│   │   ├── palmgren_miner.py               # Miner linear damage accumulation D(t)
│   │   ├── goodman.py                      # Goodman mean stress correction σ_a,eq
│   │   ├── hot_spot_stress.py              # IIW hot-spot stress extrapolation
│   │   └── damage_map.py                   # Spatial fatigue damage distribution D(x,t)
│   │
│   ├── reliability/                        # Structural reliability analysis
│   │   ├── __init__.py
│   │   ├── cornell.py                      # Cornell reliability index β computation
│   │   ├── hasofer_lind.py                 # Hasofer–Lind FORM exact invariant β
│   │   ├── failure_probability.py          # P_f = Φ(−β) mapping
│   │   ├── limit_state.py                  # Limit state function g(X) = R − S
│   │   └── monte_carlo.py                  # Monte Carlo sampling for P_f verification
│   │
│   ├── collapse/                           # Progressive collapse analysis
│   │   ├── __init__.py
│   │   ├── alp.py                          # Alternate load path (ALP) analysis
│   │   ├── gsa_protocol.py                 # GSA 2003 robustness assessment
│   │   ├── ufc_protocol.py                 # UFC 4-023-03 tie force method
│   │   ├── demand_capacity.py              # DCR = Q_UD / Q_CE ratio computation
│   │   └── collapse_sequence.py            # Progressive failure sequence tracker
│   │
│   ├── ai_support/                         # AI-assisted analytical support layer
│   │   ├── __init__.py
│   │   ├── xgboost_load.py                 # XGBoost load pattern anomaly detection
│   │   ├── lstm_forecast.py                # LSTM 24–48h LSII trajectory forecast
│   │   ├── sensor_fusion.py                # Multi-sensor data fusion and QC
│   │   ├── physics_constraints.py          # Physical bounds enforcement on AI outputs
│   │   └── uncertainty.py                  # AI prediction uncertainty quantification
│   │
│   ├── degradation/                        # Member capacity degradation modeling
│   │   ├── __init__.py
│   │   ├── corrosion.py                    # ISO 9224 corrosion rate model
│   │   ├── remaining_life.py               # T_rem(e) = (A_rem − A_crit) / (dA/dt)
│   │   ├── capacity_reduction.py           # R(t) = R₀ · (1 − D_corr − D_fatigue)
│   │   └── chaboche.py                     # Chaboche continuum damage mechanics
│   │
│   ├── loading/                            # Load modeling subsystem
│   │   ├── __init__.py
│   │   ├── traffic_load.py                 # Moving load and traffic stream models
│   │   ├── wind_load.py                    # Dynamic wind pressure and buffeting
│   │   ├── thermal_load.py                 # Thermal expansion and restraint forces
│   │   └── seismic_load.py                 # Response spectrum seismic input
│   │
│   ├── sensors/                            # Sensor integration and fusion
│   │   ├── __init__.py
│   │   ├── accelerometer.py                # Tri-axial MEMS accelerometer parser
│   │   ├── strain_gauge.py                 # Vibrating-wire strain gauge processing
│   │   ├── displacement.py                 # Linear variable differential transformer
│   │   ├── load_cell.py                    # Cable force and bearing load cells
│   │   └── fusion.py                       # Multi-sensor data fusion and QC
│   │
│   └── utils/                              # Shared utilities
│       ├── __init__.py
│       ├── metrics.py                      # LSII, β, D_fatigue, R_struct computation
│       ├── validators.py                   # Input validation and safety bounds
│       └── constants.py                    # Material, code, and geometry parameters
│
├── monitoring/                             # Real-time monitoring dashboard
│   ├── __init__.py
│   ├── app.py                              # Streamlit application entry point
│   ├── dashboard.py                        # LSII governance dashboard layout
│   ├── redistribution_plot.py              # Internal force redistribution display
│   ├── fatigue_map.py                      # Spatial fatigue damage map renderer
│   ├── reliability_panel.py               # β index and P_f trend panel
│   └── components/
│       ├── lsii_gauge.py                   # LSII composite index gauge display
│       ├── signal_panel.py                 # 🔴🟠🟢 governance signal status
│       └── trend_forecast.py               # 24–48h LSII trajectory projection
│
├── archival/                               # Operational data archival
│   ├── __init__.py
│   ├── writer.py                           # Append-only JSON/CSV record writer
│   ├── checksum.py                         # SHA-256 tamper-evidence layer
│   └── partitioner.py                      # Per-module time-window CSV partitioner
│
├── simulation/                             # Validation and benchmark environment
│   ├── __init__.py
│   ├── span_configs.py                     # Span geometry and material definitions
│   ├── loading_scenarios.py                # Traffic, wind, and fatigue scenarios
│   ├── benchmarks.py                       # Three-case validation suite
│   ├── parameters.py                       # Canonical v1.0.0 parameter registry
│   └── results/                            # Pre-computed validation outputs
│       ├── V1_cable_stayed_bridge_traffic.json
│       ├── V2_roof_truss_fatigue_forensics.json
│       └── V3_suspension_span_wind.json
│
├── examples/                               # Usage examples and tutorials
│   ├── quickstart.py                       # Minimal working example
│   ├── basic_lsii.ipynb                    # Jupyter: single-span LSII assessment
│   ├── fatigue_accumulation.ipynb          # Jupyter: rainflow + Miner walkthrough
│   ├── buckling_analysis.ipynb             # Jupyter: Euler–Riks incremental analysis
│   ├── reliability_index.ipynb             # Jupyter: Cornell–Hasofer–Lind β computation
│   ├── streamlit_dashboard.py              # Launch real-time monitoring dashboard
│   └── corrosion_life_prediction.py        # Remaining life forecast demo
│
├── tests/                                  # Unit and integration tests
│   ├── test_dlrm.py
│   ├── test_lssam.py
│   ├── test_farm.py
│   ├── test_aisl.py
│   ├── test_lsii.py
│   ├── test_rainflow.py
│   ├── test_buckling.py
│   ├── test_reliability.py
│   └── test_pipeline.py
│
├── docs/                                   # Documentation source
│   ├── architecture.md                     # Module architecture reference
│   ├── mathematics.md                      # Governing equations documentation
│   ├── monitoring.md                       # Sensor system and data fusion guide
│   ├── governance.md                       # LSII threshold calibration reference
│   └── api_reference.md                    # Full Python API reference
│
├── paper/                                  # Research paper artifacts
│   ├── LOAD-SPAN_Research_Paper.pdf        # Published paper (PDF)
│   ├── LOAD-SPAN_Research_Paper.docx       # Editable Word version
│   └── figures/
│       ├── lsii_formulation.svg
│       ├── fatigue_damage_map.svg
│       ├── load_redistribution_example.svg
│       └── reliability_index_diagram.svg
│
├── .gitlab-ci.yml                          # GitLab CI/CD pipeline
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── publish.yml
├── pyproject.toml
├── setup.cfg
├── requirements.txt
├── requirements-dev.txt
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── AUTHORS.md
├── LICENSE
└── README.md                               # This file
```

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install load-span-engine

# Install from source
git clone https://github.com/gitdeeper12/LOAD-SPAN.git
cd LOAD-SPAN
pip install -e .
```

### Minimal Example

```python
from load_span import LoadSpanAssessor

# Initialize assessor with span configuration
assessor = LoadSpanAssessor(
    span_config="configs/cable_stayed_bridge.yaml",
    sensor_stream="live"   # or path to historical CSV
)

# Run full LOAD-SPAN assessment pipeline
result = assessor.evaluate()

print(result.lsii)               # Long-Span Structural Integrity Index ∈ [0, 1]
print(result.signal)             # "STEADY_STATE" | "MONITORING_1" | "MITIGATION_2" | "CRITICAL"
print(result.beta)               # Cornell–Hasofer–Lind reliability index β
print(result.d_fatigue_max)      # Maximum Palmgren–Miner damage across all connections
print(result.lambda_cr)          # Critical load factor (Euler–Riks)
print(result.r_struct)           # Structural redundancy index
```

### With Full Four-Module Configuration

```python
from load_span import LoadSpanAssessor
from load_span.modules import DLRM, LSSAM, FARM, AISL

assessor = LoadSpanAssessor(
    span_config="configs/cable_stayed_bridge.yaml",
    modules={
        "dlrm":  DLRM(redundancy_min=0.70, redistribution_warn=0.20),
        "lssam": LSSAM(lambda_cr_min=2.0, beta_min=3.5),
        "farm":  FARM(d_limit=0.80, d_crit=1.00, sn_class="FAT90"),
        "aisl":  AISL(physics_constrained=True, forecast_horizon=48),
    }
)

result = assessor.evaluate()
print(result.breakdown)
# {"redistribution": 0.88, "stability": 0.92, "fatigue": 0.95, "reliability": 0.90}
```

### Fatigue Damage Accumulation Analysis

```python
from load_span.fatigue import RainflowCounter, PalmgrenMiner
from load_span.fatigue import SNcurve

# Load strain time series from instrumented connection detail
strain_ts = load_csv("sensors/connection_C12_strain.csv")

counter = RainflowCounter()
cycles = counter.count(strain_ts)          # ASTM E1049-85 rainflow

sn = SNcurve(fat_class=90, m=3)           # Eurocode FAT90
miner = PalmgrenMiner(sn_curve=sn)
D = miner.accumulate(cycles)              # D(t) = Σ n_i / N_i

print(f"Fatigue damage: {D:.4f} (limit: 0.80, failure: 1.00)")
```

### Launch Real-Time Monitoring Dashboard

```bash
# Start Streamlit LSII governance dashboard
streamlit run examples/streamlit_dashboard.py

# Dashboard at: http://localhost:8501
# Panels:
#   · LSII composite gauge with 4-level signal
#   · Internal force redistribution trend
#   · Fatigue damage map (spatial connection display)
#   · Reliability index β with P_f trend
#   · 24–48h LSII trajectory forecast
```

---

## 🧩 LOAD-SPAN Pipeline

```
┌────────────────────────────────────────────────────────────────────────┐
│  Sensor Input: Strain Gauges · Load Cells · Accelerometers · LVDT      │
└──────────────────────────┬─────────────────────────────────────────────┘
                           │
       ┌───────────────────┼──────────────────┬──────────────────┐
       │                   │                  │                  │
       ▼                   ▼                  ▼                  ▼
    DLRM               LSSAM              FARM               AISL
    Direct Stiffness   Euler–Riks         Rainflow           XGBoost
    K·u = f            Arc-length         Cycle Counting     Anomaly Detection
    Redistribution     λ_cr buckling      D_fatigue(t)       LSTM Forecast
    R_struct tracking  P-delta K_G        Hot-spot stress    Physics Bounds
    Influence lines    β reliability      Goodman corr.      Uncertainty QC
       │                   │                  │                  │
       └───────────────────┼──────────────────┴──────────────────┘
                           │
                 Capacity Degradation
                 R(t) = R₀·(1 − D_corr − D_fatigue)
                 ISO 9224 corrosion + Chaboche CDM
                           │
                           ▼
            Long-Span Structural Integrity Index
            LSII = 0.35·(β/β_target) + 0.30·(1−D_fatigue)
                       + 0.20·R_struct + 0.15·(λ_cr/λ_target)
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
           Safety Signal       Archival
           🟢🟠🔴             JSON/CSV + SHA-256
           4-level LSII       Streamlit dashboard
```

### Module Summary

| # | Module | Governing Output | Core Method |
|---|--------|-----------------|-------------|
| 1 | **DLRM** | `ΔF_member(t), R_struct(t)` | Direct stiffness assembly + redistribution tracking |
| 2 | **LSSAM** | `λ_cr(t), β(t)` | Euler–Riks arc-length + Hasofer–Lind FORM |
| 3 | **FARM** | `D_fatigue(x,t)` | Rainflow + Palmgren–Miner + IIW hot-spot |
| 4 | **AISL** | `LSII_forecast(t+48h)` | XGBoost anomaly + LSTM trajectory (physics-constrained) |
| — | **R(t)** | `R_struct,global(t)` | Chaboche damage + ISO 9224 corrosion |
| — | **LSII** | `LSII(t) ∈ [0,1]` | Weighted composite of all four modules |

---

## ⚙️ Governing Equations

```
Eq. 1 — Global Stiffness and Force Redistribution:
  K · u = f   →   ΔF_member = K_member · Δu_member

Eq. 2 — Euler Critical Load (Buckling):
  P_cr = π² · E · I / (K · L)²

Eq. 3 — Structural Joint Fatigue Accumulation:
  D_fatigue(t) = Σᵢ [ nᵢ(t) / Nᵢ(Δσᵢ) ] ≤ D_limit

Eq. 4 — Cornell–Hasofer–Lind Reliability Index:
  β = (μ_R − μ_S) / √(σ_R² + σ_S²)   →   P_f = Φ(−β)

Eq. 5 — Member Capacity Degradation:
  R(t) = R₀ · (1 − D_corrosion(t) − D_fatigue(t))

Eq. 6 — Long-Span Structural Integrity Index:
  LSII = [0.35 · (β / β_target)] + [0.30 · (1 − D_fatigue)]
             + [0.20 · R_struct] + [0.15 · (λ_cr / λ_target)]
```

---

## 📊 Scoring & Safety Bounds

```
LSII governance certification thresholds:
  LSII ≥ 0.90   →   🟢 Steady State
  0.75 ≤ LSII < 0.90   →   🟠 Monitoring Phase 1
  0.65 ≤ LSII < 0.75   →   🟠 Mitigation Phase 2
  LSII < 0.65   →   🔴 Critical Breach

Additional safety bounds:
  β (reliability index)  ≥  3.50   (target reliability)
  λ_cr (buckling factor) ≥  2.00   (critical load margin)
  D_fatigue,max          <  0.80   (Miner damage warning threshold)
  R_struct               ≥  0.70   (structural redundancy index)
  DCR (collapse demand)  ≤  2.00   (GSA demand-capacity ratio)
```

**Validation results (LOAD-SPAN v1.0.0):**

| Case | Span Type | LSII Accuracy | β Detection | Fatigue MAE | λ_cr Error |
|---|---|---|---|---|---|
| V1 | Cable-stayed bridge — traffic loading | ±2.9% | 94.7% (β threshold) | 2.6% | ±4.3% |
| V2 | Roof truss — fatigue forensics | ±3.1% | 94.2% (post-hoc) | 3.1% | N/A |
| V3 | Suspension span — wind dynamic | ±2.8% | 95.8% (2% threshold) | 1.9% | ±3.5% |
| **Mean** | — | **±2.94%** | **94.9%** | **2.53%** | **±3.9%** |

---

## 🌐 Platforms & Mirrors

| Platform | URL | Role |
|---|---|---|
| 🐙 **GitHub** (Primary) | [github.com/gitdeeper12/LOAD-SPAN](https://github.com/gitdeeper12/LOAD-SPAN) | Source code, issues, PRs |
| 🦊 **GitLab** (Mirror) | [gitlab.com/gitdeeper12/LOAD-SPAN](https://gitlab.com/gitdeeper12/LOAD-SPAN) | CI/CD mirror |
| 🪣 **Bitbucket** (Mirror) | [bitbucket.org/gitdeeper-12/LOAD-SPAN](https://bitbucket.org/gitdeeper-12/LOAD-SPAN) | Enterprise mirror |
| 🏔️ **Codeberg** (Mirror) | [codeberg.org/gitdeeper12/LOAD-SPAN](https://codeberg.org/gitdeeper12/LOAD-SPAN) | Open-source community |
| 📦 **PyPI** | [pypi.org/project/load-span-engine](https://pypi.org/project/load-span-engine) | Python package distribution |
| 🔬 **Zenodo** | [doi.org/10.5281/zenodo.20422430](https://doi.org/10.5281/zenodo.20422430) | Citable DOI, paper & data |
| 📋 **OSF Project** | [osf.io/H35FU](https://osf.io/H35FU) | Research project registry |
| 📝 **OSF Preregistration** | [doi.org/10.17605/OSF.IO/H35FU](https://doi.org/10.17605/OSF.IO/H35FU) | Pre-registered study protocol |
| 🌐 **Website** | [load-span.netlify.app](https://load-span.netlify.app) | Live documentation & dashboard |
| 🧑‍🔬 **ORCID** | [orcid.org/0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) | Researcher identity |
| 🗄️ **Internet Archive** | [archive.org/details/osf-registrations-H35FU](https://archive.org/details/osf-registrations-H35FU) | Permanent archival copy |

### 🌐 Official Website Pages

| Page | URL |
|---|---|
| Homepage | [load-span.netlify.app](https://load-span.netlify.app) |
| Dashboard | [load-span.netlify.app/dashboard](https://load-span.netlify.app/dashboard) |
| Results | [load-span.netlify.app/results](https://load-span.netlify.app/results) |
| Documentation | [load-span.netlify.app/documentation](https://load-span.netlify.app/documentation) |

---

## 🔄 Clone & Download

### Git Clone

```bash
# GitHub (Primary)
git clone https://github.com/gitdeeper12/LOAD-SPAN.git

# GitLab (Mirror)
git clone https://gitlab.com/gitdeeper12/LOAD-SPAN.git

# Bitbucket (Mirror)
git clone https://bitbucket.org/gitdeeper-12/LOAD-SPAN.git

# Codeberg (Mirror)
git clone https://codeberg.org/gitdeeper12/LOAD-SPAN.git
```

### Direct ZIP Download

| Source | Link |
|---|---|
| GitHub | [LOAD-SPAN-main.zip](https://github.com/gitdeeper12/LOAD-SPAN/archive/refs/heads/main.zip) |
| GitLab | [LOAD-SPAN-main.zip](https://gitlab.com/gitdeeper12/LOAD-SPAN/-/archive/main/LOAD-SPAN-main.zip) |
| Bitbucket | [LOAD-SPAN-main.zip](https://bitbucket.org/gitdeeper-12/LOAD-SPAN/get/main.zip) |
| Codeberg | [LOAD-SPAN-main.zip](https://codeberg.org/gitdeeper12/LOAD-SPAN/archive/main.zip) |
| PyPI files | [pypi.org/project/load-span-engine/#files](https://pypi.org/project/load-span-engine/#files) |
| Zenodo record | [doi.org/10.5281/zenodo.20422430](https://doi.org/10.5281/zenodo.20422430) |

---

## 📖 Citation

If LOAD-SPAN contributes to your research, please cite using one of the following formats.

### 📦 PyPI Package

```bibtex
@software{baladi2026loadspan_pypi,
  author       = {Baladi, Samir},
  title        = {{LOAD-SPAN}: Dynamic Load Redistribution Analysis and
                  Long-Span Structural Stability Assessment with
                  AI-Assisted Analytical Support},
  year         = {2026},
  version      = {1.0.0},
  publisher    = {Python Package Index},
  url          = {https://pypi.org/project/load-span-engine},
  note         = {Python package, MIT License, Series SPAN-SAFETY-01}
}
```

### 🔬 Zenodo Archive (Paper & Data)

```bibtex
@dataset{baladi2026loadspan_zenodo,
  author       = {Baladi, Samir},
  title        = {{LOAD-SPAN}: Dynamic Load Redistribution Analysis and
                  Long-Span Structural Stability Assessment with
                  AI-Assisted Analytical Support —
                  Research Paper and Simulation Data},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.20422430},
  url          = {https://doi.org/10.5281/zenodo.20422430},
  note         = {Structural Safety \& Reliability Engineering · SPAN-SAFETY-01}
}
```

### 📝 OSF Preregistration

```bibtex
@misc{baladi2026loadspan_osf,
  author       = {Baladi, Samir},
  title        = {{LOAD-SPAN} Framework: Pre-registered Study Protocol for
                  Dynamic Load Redistribution Analysis and Structural
                  Stability Assessment in Long-Span Systems},
  year         = {2026},
  publisher    = {Open Science Framework},
  doi          = {10.17605/OSF.IO/H35FU},
  url          = {https://doi.org/10.17605/OSF.IO/H35FU},
  note         = {OSF Preregistration}
}
```

### 📄 Research Paper

```bibtex
@article{baladi2026loadspan,
  author       = {Baladi, Samir},
  title        = {{LOAD-SPAN}: Dynamic Load Redistribution Analysis and
                  Long-Span Structural Stability Assessment with
                  AI-Assisted Analytical Support},
  year         = {2026},
  month        = {May},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.20422430},
  url          = {https://doi.org/10.5281/zenodo.20422430},
  note         = {Ronin Institute / Rite of Renaissance,
                  Series SPAN-SAFETY-01}
}
```

### APA (inline)

> Baladi, S. (2026). *LOAD-SPAN: Dynamic Load Redistribution Analysis and Long-Span Structural Stability Assessment with AI-Assisted Analytical Support* (Version 1.0.0, Series SPAN-SAFETY-01). Zenodo. https://doi.org/10.5281/zenodo.20422430

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Samir Baladi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
```

---

## 👤 Author

**Samir Baladi**
Interdisciplinary Researcher — Structural Reliability Engineering & Computational Safety Analysis
Ronin Institute / Rite of Renaissance

| Contact | Link |
|---|---|
| 📧 Email | [gitdeeper@gmail.com](mailto:gitdeeper@gmail.com) |
| 🧑‍🔬 ORCID | [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) |
| 🐙 GitHub | [github.com/gitdeeper12](https://github.com/gitdeeper12) |
| 🔬 Zenodo | [doi.org/10.5281/zenodo.20422430](https://doi.org/10.5281/zenodo.20422430) |

---

<div align="center">

**SPAN-SAFETY-01 · Version 1.0.0 · May 2026**

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20422430-blue.svg)](https://doi.org/10.5281/zenodo.20422430)
[![PyPI](https://img.shields.io/pypi/v/load-span-engine?color=14362A)](https://pypi.org/project/load-span-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Domain](https://img.shields.io/badge/Domain-Structural%20Safety%20%26%20Reliability-14362A)](https://doi.org/10.5281/zenodo.20422430)

*"Structural integrity in a long-span system is not a property frozen at commissioning — it is a continuously evolving state of internal force redistribution requiring continuous quantitative assessment."*

</div>
