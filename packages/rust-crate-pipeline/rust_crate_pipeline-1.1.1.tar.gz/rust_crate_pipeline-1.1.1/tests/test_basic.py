"""Test package imports and basic functionality."""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_package_import():
    """Test that the package can be imported."""
    import rust_crate_pipeline
    assert rust_crate_pipeline.__version__ == "1.1.0"
    assert rust_crate_pipeline.__author__ == "SuperUser666-Sigil"


def test_main_components_import():
    """Test that main components can be imported."""
    try:
        from rust_crate_pipeline import CrateDataPipeline, PipelineConfig
        assert CrateDataPipeline is not None
        assert PipelineConfig is not None
    except ImportError as e:
        # This is expected if dependencies aren't installed
        pytest.skip(f"Dependencies not available: {e}")


def test_main_function_exists():
    """Test that the main function exists."""
    try:
        from rust_crate_pipeline import main
        assert callable(main)
    except ImportError as e:
        pytest.skip(f"Dependencies not available: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
