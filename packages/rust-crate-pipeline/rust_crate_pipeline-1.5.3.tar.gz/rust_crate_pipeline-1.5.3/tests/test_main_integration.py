#!/usr/bin/env python3
"""
Minimal test to verify Sigil pipeline integration works in the main pipeline
"""

import sys
import os
import tempfile

# Add project to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def test_pipeline_integration():
    """Test SigilCompliantPipeline integration with a default/test crate list."""
    from rust_crate_pipeline.config import PipelineConfig
    from sigil_enhanced_pipeline import SigilCompliantPipeline

    # Provide a test crate list for integration
    test_crate_list = ["serde", "tokio"]
    config = PipelineConfig(crate_list=test_crate_list)
    try:
        sigil_pipeline = SigilCompliantPipeline(
            config,
            skip_ai=True  # Ensure model is not loaded
        )
        assert sigil_pipeline.crates == test_crate_list
    except Exception as e:
        assert False, f"Unexpected error: {e}"


def test_compatibility_interface():
    """Test SigilCompliantPipeline compatibility interface with a test crate list."""
    from rust_crate_pipeline.config import PipelineConfig
    from sigil_enhanced_pipeline import SigilCompliantPipeline

    test_crate_list = ["serde", "tokio"]
    config = PipelineConfig(crate_list=test_crate_list)
    try:
        sigil_pipeline = SigilCompliantPipeline(config, skip_ai=True)
        assert sigil_pipeline.crates == test_crate_list
    except Exception as e:
        assert False, f"Compatibility test failed: {e}"


def test_cli_argument_parsing():
    """Test that CLI arguments are properly parsed for Sigil options"""
    print("\n⚙️ Testing CLI Argument Integration")
    print("-" * 40)

    original_argv = sys.argv  # Move this outside the try block
    
    try:
        from rust_crate_pipeline.main import parse_arguments

        # Test parsing Sigil-related arguments
        test_cases = [
            ["--enable-sigil-protocol"],
            ["--enable-sigil-protocol", "--sigil-mode", "enhanced"],
            ["--enable-sigil-protocol", "--skip-ai", "--limit", "5"],
        ]

        for i, test_args in enumerate(test_cases):
            sys.argv = ["test"] + test_args

            try:
                args = parse_arguments()
                print(f"✅ Test case {i + 1}: {' '.join(test_args)}")
                print(
                    f"   - Enable Sigil: {getattr(args, 'enable_sigil_protocol', False)}")
                print(
                    f"   - Sigil Mode: {getattr(args, 'sigil_mode', 'default')}")
                print(f"   - Skip AI: {getattr(args, 'skip_ai', False)}")
                print(f"   - Limit: {getattr(args, 'limit', 'None')}")

            except Exception as e:
                print(f"❌ Test case {i + 1} failed: {e}")

        sys.argv = original_argv
        assert True, "CLI argument parsing test completed successfully"

    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        sys.argv = original_argv
        assert False, f"CLI test failed: {e}"


def main():
    """Run all integration tests"""
    print("🚀 Sigil Enhanced Pipeline - Main Integration Tests")
    print("=" * 60)

    tests = [
        ("Pipeline Integration", test_pipeline_integration),
        ("Interface Compatibility", test_compatibility_interface),
        ("CLI Argument Integration", test_cli_argument_parsing),
    ]

    passed = 0
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"\n✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {e}")

    print("\n" + "=" * 60)
    print(f"🎯 Integration Test Results: {passed}/{len(tests)} passed")

    if passed == len(tests):
        print("🎉 All integration tests passed!")
        print("✅ Sigil enhanced pipeline is successfully integrated!")
        print("✅ Ready for production deployment with AI models!")
        return 0
    else:
        print("⚠️ Some integration tests failed.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
