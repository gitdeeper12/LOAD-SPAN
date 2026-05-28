#!/usr/bin/env python3

"""LOAD-SPAN v1.0.0 Upload - PyPI"""

import requests
import hashlib
import os
import glob

TOKEN = "YOUR_PYPI_TOKEN_HERE"

print("="*60)
print("🏗️ LOAD-SPAN v1.0.0 Upload - PyPI")
print("="*60)
print("Dynamic Load Redistribution Analysis")
print("Long-Span Structural Stability Assessment")
print("with AI-Assisted Analytical Support")
print("="*60)

# Read README.md
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    print(f"\n📄 README.md: {len(readme)} characters")
except FileNotFoundError:
    print("\n⚠️ README.md not found, using fallback description")
    readme = """LOAD-SPAN: Dynamic Load Redistribution Analysis and Long-Span Structural Stability Assessment with AI-Assisted Analytical Support.

A structural mechanics framework for dynamic load redistribution analysis and stability assessment in long-span structures, incorporating an AI-assisted analytical support layer as a bounded auxiliary tool for monitoring, anomaly detection, and predictive maintenance assistance.

Features:
- DLRM: Dynamic Load Redistribution Module with direct stiffness method
- LSSAM: Long-Span Stability Assessment Module with Euler-Riks buckling
- FARM: Fatigue Accumulation and Reliability Module with Palmgren-Miner rule
- AISL: AI-Assisted Support Layer with XGBoost anomaly detection
- LSII: Long-Span Structural Integrity Index composite metric
- Four-level governance decision logic (Steady/Monitoring/Mitigation/Critical)
"""

# Find distribution files
wheel_files = glob.glob("dist/*.whl")
tar_files = glob.glob("dist/*.tar.gz")

if not wheel_files and not tar_files:
    print("\n❌ No distribution files found. Building package...")
    os.system("python -m build")
    
    wheel_files = glob.glob("dist/*.whl")
    tar_files = glob.glob("dist/*.tar.gz")

print(f"\n📦 Distribution files:")
for f in wheel_files + tar_files:
    print(f"   • {os.path.basename(f)}")

upload_success = False

for filepath in wheel_files + tar_files:
    filename = os.path.basename(filepath)
    print(f"\n📤 Uploading: {filename}")

    # Determine file type
    if filename.endswith('.tar.gz'):
        filetype = 'sdist'
        pyversion = 'source'
    else:
        filetype = 'bdist_wheel'
        pyversion = 'py3'

    # Calculate hashes
    with open(filepath, 'rb') as f:
        content = f.read()
    md5_hash = hashlib.md5(content).hexdigest()
    sha256_hash = hashlib.sha256(content).hexdigest()

    # Upload data for LOAD-SPAN
    data = {
        ':action': 'file_upload',
        'metadata_version': '2.1',
        'name': 'load-span-engine',
        'version': '1.0.0',
        'filetype': filetype,
        'pyversion': pyversion,
        'md5_digest': md5_hash,
        'sha256_digest': sha256_hash,
        'description': readme,
        'description_content_type': 'text/markdown',
        'author': 'Samir Baladi',
        'author_email': 'gitdeeper@gmail.com',
        'license': 'MIT',
        'summary': 'LOAD-SPAN: Dynamic Load Redistribution Analysis and Long-Span Structural Stability Assessment with AI-Assisted Analytical Support',
        'home_page': 'https://load-span.netlify.app',
        'requires_python': '>=3.9',
        'keywords': 'structural-engineering, reliability-analysis, fatigue-analysis, buckling-analysis, structural-health-monitoring, ai-assisted, long-span-structures, bridges, progressive-collapse'
    }

    # Upload file
    try:
        with open(filepath, 'rb') as f:
            response = requests.post(
                'https://upload.pypi.org/legacy/',
                files={'content': (filename, f, 'application/octet-stream')},
                data=data,
                auth=('__token__', TOKEN),
                timeout=90,
                headers={'User-Agent': 'LOAD-SPAN-Uploader/1.0.0'}
            )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            print("   ✅✅✅ SUCCESS!")
            upload_success = True
        else:
            print(f"   ❌ Error: {response.text[:300]}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")

print("\n" + "="*60)
if upload_success:
    print("✅ LOAD-SPAN v1.0.0 uploaded successfully!")
    print("🔗 https://pypi.org/project/load-span-engine/1.0.0/")
else:
    print("⚠️ Upload completed with some issues.")
    print("🔗 https://pypi.org/project/load-span-engine/")
print("="*60)

print("\n📦 Install LOAD-SPAN:")
print("   pip install load-span-engine")
print("")
print("📖 Documentation:")
print("   https://load-span.netlify.app")
print("")
print("📊 Governance Dashboard:")
print("   https://load-span.netlify.app/dashboard")
print("")
print("🔬 Cite:")
print("   DOI: 10.5281/zenodo.20422430")
print("   OSF: 10.17605/OSF.IO/H35FU")
