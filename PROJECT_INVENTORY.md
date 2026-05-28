# LOAD-SPAN v1.0.0 - Project Inventory

## Project Information

| Field | Value |
|-------|-------|
| Project Name | LOAD-SPAN |
| Version | 1.0.0 |
| Release Date | May 28, 2026 |
| Author | Samir Baladi |
| Email | gitdeeper@gmail.com |
| ORCID | 0009-0003-8903-0029 |
| License | MIT |
| DOI (Zenodo) | 10.5281/zenodo.20422430 |
| DOI (OSF) | 10.17605/OSF.IO/H35FU |

## Repository Links

| Platform | URL |
|----------|-----|
| GitHub | https://github.com/gitdeeper12/LOAD-SPAN |
| GitLab | https://gitlab.com/gitdeeper12/LOAD-SPAN |
| Bitbucket | https://bitbucket.org/gitdeeper-12/LOAD-SPAN |
| Codeberg | https://codeberg.org/gitdeeper12/LOAD-SPAN |
| PyPI | https://pypi.org/project/load-span-engine |
| Zenodo | https://doi.org/10.5281/zenodo.20422430 |
| OSF Project | https://osf.io/H35FU |
| OSF Registration | https://doi.org/10.17605/OSF.IO/H35FU |
| Internet Archive | https://archive.org/details/osf-registrations-H35FU |
| Website | https://load-span.netlify.app |

## Documentation

| Page | URL |
|------|-----|
| Homepage | https://load-span.netlify.app |
| Dashboard | https://load-span.netlify.app/dashboard |
| Results | https://load-span.netlify.app/results |
| Documentation | https://load-span.netlify.app/documentation |

## PyPI Package

| Field | Value |
|-------|-------|
| Package Name | load-span-engine |
| Version | 1.0.0 |
| Release Date | May 28, 2026 |
| Python Version | >=3.9 |
| License | MIT |
| Install Command | `pip install load-span-engine` |

## Project Structure

```

LOAD-SPAN/
│
├── load_span/                              # Core Python package (84 files)
│   ├── init.py
│   ├── pipeline.py
│   ├── lsii.py
│   │
│   ├── modules/                            # Four analytical modules
│   │   ├── dlrm.py                         # Dynamic Load Redistribution Module
│   │   ├── lssam.py                        # Long-Span Stability Assessment Module
│   │   ├── farm.py                         # Fatigue Accumulation and Reliability Module
│   │   └── aisl.py                         # AI-Assisted Support Layer
│   │
│   ├── stiffness/                          # Direct stiffness method subsystem
│   ├── stability/                          # Buckling and geometric stability
│   ├── fatigue/                            # Fatigue and reliability subsystem
│   ├── reliability/                        # Structural reliability analysis
│   ├── collapse/                           # Progressive collapse analysis
│   ├── ai_support/                         # AI-assisted analytical support layer
│   ├── degradation/                        # Member capacity degradation modeling
│   ├── loading/                            # Load modeling subsystem
│   ├── sensors/                            # Sensor integration and fusion
│   ├── monitoring/                         # Real-time monitoring dashboard
│   ├── archival/                           # Operational data archival
│   ├── simulation/                         # Validation and benchmark environment
│   └── utils/                              # Shared utilities
│
├── tests/                                  # Unit and validation tests
├── examples/                               # Usage examples
├── docs/                                   # Documentation source
├── configs/                                # YAML configuration files
├── paper/                                  # Research paper (PDF/DOCX)
│   ├── LOAD-SPAN_Research_Paper.pdf
│   ├── LOAD-SPAN_Research_Paper.docx
│   └── figures/
│
├── data/                                   # Data directories
│   ├── raw/
│   ├── processed/
│   └── archival/
│
├── logs/                                   # Log files
├── scripts/                                # Helper scripts
│
├── requirements.txt                        # Production dependencies
├── requirements-dev.txt                    # Development dependencies
├── pyproject.toml                          # Project configuration
├── setup.py                                # Setup script
├── setup.cfg                               # Setup configuration
├── Makefile                                # Make commands
├── Dockerfile                              # Docker container
│
├── README.md                               # Main documentation
├── CHANGELOG.md                            # Version history
├── CONTRIBUTING.md                         # Contribution guidelines
├── CODE_OF_CONDUCT.md                      # Code of conduct
├── AUTHORS.md                              # Authors list
├── LICENSE                                 # MIT License
├── NOTICE                                  # Notices
├── SECURITY.md                             # Security policy
├── CITATION.cff                            # Citation metadata
├── .env.example                            # Environment variables
├── .gitignore                              # Git ignore rules
├── .gitlab-ci.yml                          # CI/CD pipeline
├── .pre-commit-config.yaml                 # Pre-commit hooks
└── .readthedocs.yaml                       # ReadTheDocs config

```

## Modules Summary

| # | Module | Name | Core Method | Output |
|---|--------|------|-------------|--------|
| 1 | DLRM | Dynamic Load Redistribution Module | Direct stiffness assembly | ΔF_member(t), R_struct(t) |
| 2 | LSSAM | Long-Span Stability Assessment Module | Euler–Riks + Hasofer-Lind | λ_cr(t), β(t) |
| 3 | FARM | Fatigue Accumulation and Reliability Module | Rainflow + Palmgren-Miner | D_fatigue(x,t) |
| 4 | AISL | AI-Assisted Support Layer | XGBoost + LSTM | LSII_forecast(t+48h) |

## Governing Equations

| Eq | Name | Formula |
|----|------|---------|
| 1 | Global Stiffness | K·u = f → ΔF_member = K_member·Δu_member |
| 2 | Euler Critical Load | P_cr = π²·E·I / (K·L)² |
| 3 | Fatigue Accumulation | D_fatigue(t) = Σ [n_i(t) / N_i(Δσ_i)] |
| 4 | Reliability Index | β = (μ_R - μ_S) / √(σ_R² + σ_S²) |
| 5 | Capacity Degradation | R(t) = R₀·(1 - D_corr - D_fatigue) |
| 6 | LSII | LSII = 0.35·(β/β_target) + 0.30·(1-D_fatigue) + 0.20·R_struct + 0.15·(λ_cr/λ_target) |

## Safety Thresholds

| Signal | LSII Range | β Threshold | Action |
|--------|------------|-------------|--------|
| 🟢 STEADY_STATE | LSII ≥ 0.90 | β ≥ 3.8 | Continuous monitoring |
| 🟠 MONITORING_PHASE_1 | 0.75 ≤ LSII < 0.90 | 2.5 ≤ β < 3.8 | Enhanced monitoring |
| 🟠 MITIGATION_PHASE_2 | 0.65 ≤ LSII < 0.75 | 1.5 ≤ β < 2.5 | Load restriction |
| 🔴 CRITICAL_BREACH | LSII < 0.65 | β < 1.5 | Immediate closure |

## Validation Results

| Case | Structure | LSII Accuracy | Anomaly Detection | Fatigue MAE |
|------|-----------|---------------|-------------------|-------------|
| V1 | Cable-stayed bridge | ±2.9% | 93.8% | 2.8% |
| V2 | Roof truss (forensic) | ±3.1% | 91.2% | 3.4% |
| V3 | Scale model | ±2.6% | 95.1% | 2.1% |
| **Mean** | - | **±2.87%** | **93.4%** | **2.77%** |

## Test Results

| Test Type | Results |
|-----------|---------|
| Unit Tests | 10/10 passed |
| Model Validation | 8/8 passed |
| Import Tests | All passed |
| Coverage | Core modules fully tested |

## Dependencies

### Production
- numpy >= 1.21.0
- scipy >= 1.7.0
- pandas >= 1.3.0
- matplotlib >= 3.4.0
- scikit-learn >= 1.0.0
- xgboost >= 1.5.0
- streamlit >= 1.12.0
- plotly >= 5.5.0
- pyyaml >= 5.4.0
- pydantic >= 1.9.0

### Development
- pytest >= 7.0.0
- black >= 22.0.0
- flake8 >= 5.0.0
- mypy >= 0.990
- sphinx >= 5.0.0

## File Statistics

| Type | Count |
|------|-------|
| Python Files | 84 |
| Configuration Files | 15 |
| Documentation Files | 10 |
| Test Files | 8 |
| Example Files | 7 |
| Total Files | ~124 |

## Commands

### Installation
```bash
pip install load-span-engine
```

Development

```bash
git clone https://github.com/gitdeeper12/LOAD-SPAN.git
cd LOAD-SPAN
pip install -e .
make install-dev
```

Testing

```bash
make test
python tests/test_model_validation.py
```

Dashboard

```bash
streamlit run load_span/monitoring/app.py
```

Build & Publish

```bash
python -m build
twine upload dist/*
```

Citation Formats

BibTeX (Zenodo)

```bibtex
@dataset{baladi2026loadspan_zenodo,
  author = {Baladi, Samir},
  title = {{LOAD-SPAN}: Research Paper and Simulation Data},
  year = {2026},
  doi = {10.5281/zenodo.20422430}
}
```

BibTeX (OSF)

```bibtex
@misc{baladi2026loadspan_osf,
  author = {Baladi, Samir},
  title = {{LOAD-SPAN} Framework: Pre-registered Study Protocol},
  year = {2026},
  doi = {10.17605/OSF.IO/H35FU}
}
```

APA

```
Baladi, S. (2026). LOAD-SPAN: Dynamic Load Redistribution Analysis 
and Long-Span Structural Stability Assessment with AI-Assisted 
Analytical Support (Version 1.0.0). Zenodo. 
https://doi.org/10.5281/zenodo.20422430
```

---

Last Updated: May 28, 2026
Version: 1.0.0
SPAN-SAFETY-01
