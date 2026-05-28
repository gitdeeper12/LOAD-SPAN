
🚀 Deployment Guide for TOWER-CORE (TOWER-SAFETY-01)

Package Deployment (PyPI)

```bash
pip install build twine
python -m build
twine upload dist/*
```

Docker Deployment

```bash
docker build -t tower-core:latest .
docker run -it --rm tower-core:latest --config configs/lattice_120m.yaml
```

CI/CD Pipeline (GitLab CI)

The .gitlab-ci.yml includes: test, build, deploy, mirror

Trigger Deployment:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Netlify Deployment

```bash
cd Netlify/
netlify deploy --prod
```

Verification

```bash
pip install tower-core-engine
curl https://doi.org/10.5281/zenodo.20394041
curl https://tower-core.netlify.app
```

