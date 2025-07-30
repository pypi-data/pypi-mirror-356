# rust_crate_pipeline/__init__.py
"""
Rust Crate Data Processing Pipeline

A comprehensive system for gathering, enriching, and analyzing metadata for Rust crates.
Includes AI-powered enrichment using local LLMs and dependency analysis.

Example usage:
    from rust_crate_pipeline import CrateDataPipeline
    from rust_crate_pipeline.main import main
    
    # Run the main pipeline
    main()
    
    # Or use the pipeline class directly
    config = PipelineConfig()
    pipeline = CrateDataPipeline(config)
    pipeline.run()
    
Components:
    - CrateDataPipeline: Main orchestration class
    - PipelineConfig: Configuration management
    - Various analyzers for AI, security, and dependency analysis
"""

from .version import __version__

__author__ = "SuperUser666-Sigil"
__email__ = "miragemodularframework@gmail.com"
__license__ = "MIT"

# Import main components for easy access (only if dependencies are available)
try:
    from .pipeline import CrateDataPipeline
    from .config import PipelineConfig
    
    __all__ = [
        "CrateDataPipeline",
        "PipelineConfig", 
        "__version__",
        "__author__",
        "__email__",
        "__license__"
    ]
except ImportError:
    # Handle case where dependencies aren't installed yet
    __all__ = [
        "__version__",
        "__author__",
        "__email__",
        "__license__"
    ]