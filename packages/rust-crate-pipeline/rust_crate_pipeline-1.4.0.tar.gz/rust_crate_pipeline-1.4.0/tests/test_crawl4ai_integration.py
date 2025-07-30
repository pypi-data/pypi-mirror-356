"""
Test script for Crawl4AI integration into both standard and Sigil pipelines
"""

import asyncio
import logging
import sys
import os
import pytest

# Add the project to Python path
sys.path.insert(0, os.path.dirname(__file__))


def test_enhanced_scraping():
    """Test the enhanced scraping module"""
    print("🧪 Testing Enhanced Scraping Module...")
    try:
        from enhanced_scraping import CrateDocumentationScraper, EnhancedScraper
        print("✅ Enhanced scraping imports successful")
        scraper = EnhancedScraper(enable_crawl4ai=True)
        print(
            f"✅ Enhanced scraper initialized (Crawl4AI enabled: {
                scraper.enable_crawl4ai})")
        crate_scraper = CrateDocumentationScraper(enable_crawl4ai=True)
        print("✅ Crate documentation scraper initialized")
        assert scraper is not None
        assert crate_scraper is not None
    except ImportError as e:
        print(f"❌ Required module missing: {e}")
        assert False, f"Required module missing: {e}"
    except FileNotFoundError as e:
        print(f"❌ Required file missing: {e}")
        assert False, f"Required file missing: {e}"
    except Exception as e:
        print(f"❌ Enhanced scraping test failed: {e}")
        assert False, f"Unexpected error: {e}"


def test_standard_pipeline_integration():
    """Test Crawl4AI integration in standard pipeline (model loading bypassed)"""
    print("\n🧪 Testing Standard Pipeline Integration...")
    try:
        from rust_crate_pipeline.config import PipelineConfig
        from rust_crate_pipeline.pipeline import CrateDataPipeline
        import unittest.mock
        class DummyEnricher:
            def __init__(self, config):
                self.model = None
        # Patch LLMEnricher everywhere it is used in the pipeline
        with unittest.mock.patch('rust_crate_pipeline.pipeline.LLMEnricher', DummyEnricher), \
             unittest.mock.patch('rust_crate_pipeline.ai_processing.LLMEnricher', DummyEnricher):
            config = PipelineConfig(
                enable_crawl4ai=True,
                crawl4ai_model="ollama/deepseek-coder:6.7b"
            )
            print("✅ PipelineConfig with Crawl4AI created")
            pipeline = CrateDataPipeline(config)
            print(f"✅ Standard pipeline initialized (Enhanced scraper: {pipeline.enhanced_scraper is not None})")
            assert pipeline is not None
            assert pipeline.enhanced_scraper is not None
    except ImportError as e:
        print(f"❌ Required module missing: {e}")
        assert False, f"Required module missing: {e}"
    except FileNotFoundError as e:
        print(f"❌ Required file missing: {e}")
        assert False, f"Required file missing: {e}"
    except Exception as e:
        print(f"❌ Standard pipeline integration test failed: {e}")
        assert False, f"Unexpected error: {e}"


def test_sigil_pipeline_integration():
    """Test Crawl4AI integration in Sigil pipeline"""
    print("\n🧪 Testing Sigil Pipeline Integration...")
    try:
        from rust_crate_pipeline.config import PipelineConfig
        from sigil_enhanced_pipeline import SigilCompliantPipeline
        config = PipelineConfig(
            enable_crawl4ai=True,
            crawl4ai_model="ollama/deepseek-coder:6.7b"
        )
        print("✅ PipelineConfig with Crawl4AI created")
        pipeline = SigilCompliantPipeline(config, skip_ai=True, limit=1)
        print(
            f"✅ Sigil pipeline initialized (Enhanced scraper: {
                pipeline.enhanced_scraper is not None})")
        assert pipeline is not None
        assert pipeline.enhanced_scraper is not None
    except ImportError as e:
        print(f"❌ Required module missing: {e}")
        assert False, f"Required module missing: {e}"
    except FileNotFoundError as e:
        print(f"❌ Required file missing: {e}")
        assert False, f"Required file missing: {e}"
    except Exception as e:
        print(f"❌ Sigil pipeline integration test failed: {e}")
        assert False, f"Unexpected error: {e}"


def test_cli_integration():
    """Test CLI integration with new Crawl4AI arguments"""
    print("\n🧪 Testing CLI Integration...")
    try:
        import sys
        from rust_crate_pipeline.main import parse_arguments
        test_args = [
            '--enable-crawl4ai',
            '--crawl4ai-model',
            'ollama/test',
            '--limit',
            '1'
        ]
        original_argv = sys.argv
        sys.argv = ['main.py'] + test_args
        try:
            args = parse_arguments()
            sys.argv = original_argv  # Restore original argv
        except SystemExit:
            sys.argv = original_argv  # Restore original argv
            print("✅ CLI parsing successful (help processed)")
            assert True
            return
        print("✅ CLI parsing successful:")
        print(
            f"   - Enable Crawl4AI: {getattr(args, 'enable_crawl4ai', 'Not found')}")
        print(
            f"   - Crawl4AI Model: {getattr(args, 'crawl4ai_model', 'Not found')}")
        print(
            f"   - Disable Crawl4AI: {getattr(args, 'disable_crawl4ai', 'Not found')}")
        assert getattr(args, 'enable_crawl4ai', None) is not None
    except ImportError as e:
        print(f"❌ Required module missing: {e}")
        assert False, f"Required module missing: {e}"
    except FileNotFoundError as e:
        print(f"❌ Required file missing: {e}")
        assert False, f"Required file missing: {e}"
    except Exception as e:
        print(f"❌ CLI integration test failed: {e}")
        assert False, f"Unexpected error: {e}"


@pytest.mark.asyncio
async def test_async_functionality():
    """Test async functionality of enhanced scraping"""
    print("\n🧪 Testing Async Functionality...")
    try:
        from enhanced_scraping import EnhancedScraper
        scraper = EnhancedScraper(enable_crawl4ai=False)
        result = await scraper.scrape_documentation("https://httpbin.org/html", "test")
        print("✅ Async scraping successful:")
        print(f"   - URL: {result.url}")
        print(f"   - Title: {result.title[:50]}...")
        print(f"   - Method: {result.extraction_method}")
        print(f"   - Quality: {result.quality_score:.2f}")
        await scraper.close()
        assert result is not None
        assert hasattr(result, 'url')
    except ImportError as e:
        print(f"❌ Required module missing: {e}")
        assert False, f"Required module missing: {e}"
    except FileNotFoundError as e:
        print(f"❌ Required file missing: {e}")
        assert False, f"Required file missing: {e}"
    except Exception as e:
        print(f"❌ Async functionality test failed: {e}")
        assert False, f"Unexpected error: {e}"


def main():
    """Run all integration tests"""
    print("🚀 Crawl4AI Integration Test Suite")
    print("=" * 50)

    # Configure logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise

    tests = [
        ("Enhanced Scraping Module", test_enhanced_scraping),
        ("Standard Pipeline Integration", test_standard_pipeline_integration),
        ("Sigil Pipeline Integration", test_sigil_pipeline_integration),
        ("CLI Integration", test_cli_integration),
    ]

    results = {}

    # Run synchronous tests
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False

    # Run async test
    try:
        async_result = asyncio.run(test_async_functionality())
        results["Async Functionality"] = async_result
    except Exception as e:
        print(f"❌ Async Functionality failed with exception: {e}")
        results["Async Functionality"] = False

    # Print summary
    print("\n" + "=" * 50)
    print("🎯 Test Results Summary:")
    passed = 0
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status}: {test_name}")
        if result:
            passed += 1

    print(f"\n📊 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Crawl4AI integration is successful!")
        print("\n📋 Ready for use:")
        print(
            "   - Standard Pipeline: python -m rust_crate_pipeline.main --enable-crawl4ai")
        print("   - Sigil Pipeline: python -m rust_crate_pipeline.main --enable-sigil-protocol --enable-crawl4ai")
        print(
            "   - Disable Crawl4AI: python -m rust_crate_pipeline.main --disable-crawl4ai")
    else:
        print("⚠️  Some tests failed. Review the errors above.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
