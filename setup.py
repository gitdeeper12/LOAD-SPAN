from setuptools import setup, find_packages
import os

# Get all packages
packages = []
for root, dirs, files in os.walk('load_span'):
    if '__init__.py' in files:
        pkg = root.replace(os.sep, '.')
        packages.append(pkg)

setup(
    name="load-span-engine",
    version="1.0.0",
    author="Samir Baladi",
    author_email="gitdeeper@gmail.com",
    description="Dynamic Load Redistribution Analysis and Long-Span Structural Stability Assessment with AI-Assisted Analytical Support",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=packages,
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "scikit-learn>=1.0.0",
        "xgboost>=1.5.0",
        "streamlit>=1.12.0",
        "plotly>=5.5.0",
        "pyyaml>=5.4.0",
        "pydantic>=1.9.0",
    ],
    entry_points={
        "console_scripts": [
            "load-span=load_span.cli:main",
            "load-span-dashboard=load_span.monitoring.app:run",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
