#!/bin/bash
# LOAD-SPAN Validation Script

echo "Running LOAD-SPAN Validation Suite..."

# Run unit tests
echo "=== Unit Tests ==="
python -c "import sys; sys.path.insert(0, '.'); import pytest; pytest.main(['tests/', '-v'])"

# Run model validation
echo ""
echo "=== Model Validation ==="
python tests/test_model_validation.py

echo ""
echo "Validation complete!"
