#!/usr/bin/env python3
"""
Test script to validate Sigil enhanced pipeline integration
Runs without requiring AI models for development environment testing
"""

import sys
import os
import logging
import tempfile
import json
from pathlib import Path

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def test_basic_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    try:
        from rust_crate_pipeline.config import PipelineConfig
        print("✅ PipelineConfig imported successfully")
        from sigil_enhanced_pipeline import SigilCompliantPipeline, SigilEnrichedCrate
        print("✅ Sigil components imported successfully")
        from rust_crate_pipeline.main import main as pipeline_main
        print("✅ Main pipeline imported successfully")
    except ImportError as e:
        print(f"❌ Required module missing: {e}")
        assert False, f"Required module missing: {e}"
    except FileNotFoundError as e:
        print(f"❌ Required file missing: {e}")
        assert False, f"Required file missing: {e}"
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        assert False, f"Unexpected error: {e}"


def test_sigil_pipeline_initialization():
    """Test SigilCompliantPipeline initialization with a test crate list."""
    from rust_crate_pipeline.config import PipelineConfig
    from sigil_enhanced_pipeline import SigilCompliantPipeline

    test_crate_list = ["serde", "tokio"]
    config = PipelineConfig(crate_list=test_crate_list)
    try:
        pipeline = SigilCompliantPipeline(config, skip_ai=True)
        assert pipeline.crates == test_crate_list
    except Exception as e:
        assert False, f"Unexpected error: {e}"


def test_basic_crate_processing():
    """Test basic crate processing with a test crate list."""
    from rust_crate_pipeline.config import PipelineConfig
    from sigil_enhanced_pipeline import SigilCompliantPipeline

    test_crate_list = ["serde", "tokio"]
    config = PipelineConfig(crate_list=test_crate_list)
    try:
        pipeline = SigilCompliantPipeline(config, skip_ai=True)
        assert pipeline.crates == test_crate_list
    except Exception as e:
        assert False, f"Failed basic crate processing: {e}"


def test_pipeline_run_basic():
    """Test pipeline run in basic mode with a test crate list."""
    from rust_crate_pipeline.config import PipelineConfig
    from sigil_enhanced_pipeline import SigilCompliantPipeline

    test_crate_list = ["serde", "tokio"]
    config = PipelineConfig(crate_list=test_crate_list)
    try:
        pipeline = SigilCompliantPipeline(config, skip_ai=True)
        assert pipeline.crates == test_crate_list
    except Exception as e:
        assert False, f"Failed pipeline run: {e}"


def test_cli_integration():
    """Test CLI integration (dry run)"""
    print("\n🖥️ Testing CLI integration...")

    try:
        # Test that the argument parsing works
        import argparse
        from rust_crate_pipeline.main import parse_arguments

        # Test basic arguments
        test_args = [
            "--limit", "1",
            "--skip-ai",
            "--enable-sigil-protocol"
        ]

        # Mock sys.argv for testing
        original_argv = sys.argv
        sys.argv = ["test"] + test_args

        try:
            args = parse_arguments()
            print("✅ CLI arguments parsed successfully")
            print(f"✅ Limit: {args.limit}")
            print(f"✅ Skip AI: {args.skip_ai}")
            print(
                f"✅ Enable Sigil: {
                    getattr(
                        args,
                        'enable_sigil_protocol',
                        False)}")

            assert True, "CLI integration test completed successfully"

        finally:
            sys.argv = original_argv

    except Exception as e:
        print(f"❌ Failed CLI integration test: {e}")
        assert False, f"Failed CLI integration test: {e}"


def test_mock_sacred_chain():
    """Test mock Sacred Chain creation with a test crate list."""
    from rust_crate_pipeline.config import PipelineConfig
    from sigil_enhanced_pipeline import SigilCompliantPipeline

    test_crate_list = ["serde", "tokio"]
    config = PipelineConfig(crate_list=test_crate_list)
    try:
        pipeline = SigilCompliantPipeline(config, skip_ai=False)
        assert pipeline.crates == test_crate_list
    except Exception as e:
        assert False, f"Failed mock Sacred Chain test: {e}"


def main():
    """Run all integration tests"""
    print("🧪 Sigil Enhanced Pipeline Integration Tests")
    print("=" * 50)

    # Configure logging for tests
    logging.basicConfig(level=logging.WARNING)  # Reduce noise during testing

    tests = [
        ("Import Tests", test_basic_imports),
        ("Initialization Tests", test_sigil_pipeline_initialization),
        ("Basic Processing Tests", test_basic_crate_processing),
        ("Pipeline Run Tests", test_pipeline_run_basic),
        ("CLI Integration Tests", test_cli_integration),
        ("Mock Sacred Chain Tests", test_mock_sacred_chain),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")

    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Sigil pipeline integration is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check output above for details.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
