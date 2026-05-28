
📦 Installation Guide for TOWER-CORE (TOWER-SAFETY-01)

Quick Install (PyPI)

```bash
pip install tower-core-engine
```

Install from Source

```bash
git clone https://github.com/gitdeeper12/TOWER-CORE.git
cd TOWER-CORE
pip install -e .
```

Verify Installation

```python
import tower_core
print(tower_core.__version__)  # 1.0.0
print(tower_core.__doi__)      # 10.5281/zenodo.20394041
```

```bash
python -c "from tower_core import TowerCoreAssessor; print('TOWER-CORE ready')"
```

Requirements

Package Version Required
Python ≥ 3.9
numpy ≥ 1.21.0
scipy ≥ 1.7.0
streamlit ≥ 1.28.0
plotly ≥ 5.17.0

Launch Dashboard

```bash
streamlit run examples/streamlit_dashboard.py
```

Dashboard: http://localhost:8501
