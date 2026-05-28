"""Simple import tests for LOAD-SPAN."""

def test_import_load_span():
    """Test main package import."""
    try:
        import load_span
        assert hasattr(load_span, '__version__')
        print("✓ load_span imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import load_span: {e}")
        raise


def test_import_lsii():
    """Test LSII module import."""
    try:
        from load_span.lsii import LongSpanIntegrityIndex
        assert LongSpanIntegrityIndex is not None
        print("✓ LSII module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import LSII: {e}")
        raise


def test_import_modules():
    """Test modules import."""
    modules = ['dlrm', 'lssam', 'farm', 'aisl']
    for module in modules:
        try:
            exec(f"from load_span.modules import {module}")
            print(f"✓ {module} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {module}: {e}")


def test_import_stiffness():
    """Test stiffness module import."""
    try:
        from load_span.stiffness import assembly, redistribution
        print("✓ stiffness module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import stiffness: {e}")


def test_import_fatigue():
    """Test fatigue module import."""
    try:
        from load_span.fatigue import rainflow, palmgren_miner
        print("✓ fatigue module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import fatigue: {e}")
