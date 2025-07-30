# main.py
import sys
import time
import logging
import shutil
import argparse
from .config import PipelineConfig
from .pipeline import CrateDataPipeline
from .production_config import setup_production_environment
from .github_token_checker import check_and_setup_github_token


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Rust Crate Data Processing Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m rust_crate_pipeline                    # Run with defaults
  python -m rust_crate_pipeline --limit 50         # Process only 50 crates
  python -m rust_crate_pipeline --batch-size 5     # Smaller batches
  python -m rust_crate_pipeline --output-dir ./data # Custom output directory
  python -m rust_crate_pipeline --log-level DEBUG   # Verbose logging
  PRODUCTION=true python -m rust_crate_pipeline     # Production mode (quieter)
        """
    )

    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=None,
        help='Limit the number of crates to process (default: process all)'
    )

    parser.add_argument(
        '--batch-size', '-b',
        type=int,
        default=10,
        help='Number of crates to process in each batch (default: 10)'
    )

    parser.add_argument(
        '--workers', '-w',
        type=int,
        default=4,
        help='Number of parallel workers for API requests (default: 4)'
    )

    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default=None,
        help='Output directory for results (default: auto-generated timestamped directory)'
    )

    parser.add_argument(
        '--model-path', '-m',
        type=str,
        default=None,
        help='Path to the LLM model file (default: ~/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf)'
    )

    parser.add_argument(
        '--max-tokens',
        type=int,
        default=256,
        help='Maximum tokens for LLM generation (default: 256)'
    )

    parser.add_argument(
        '--checkpoint-interval',
        type=int,
        default=10,
        help='Save checkpoint every N crates (default: 10)'
    )

    parser.add_argument('--log-level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default='INFO',
                        help='Logging level (default: INFO)'
                        )

    parser.add_argument(
        '--skip-ai',
        action='store_true',
        help='Skip AI enrichment (faster, metadata only)'
    )

    parser.add_argument(
        '--skip-source-analysis',
        action='store_true',
        help='Skip source code analysis'
    )

    # Enhanced scraping with Crawl4AI
    parser.add_argument(
        '--enable-crawl4ai',
        action='store_true',
        default=True,
        help='Enable enhanced web scraping with Crawl4AI (default: enabled)'
    )

    parser.add_argument(
        '--disable-crawl4ai',
        action='store_true',
        help='Disable Crawl4AI enhanced scraping (use basic scraping only)'    )

    parser.add_argument(
        '--crawl4ai-model',
        type=str,
        default='~/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf',
        help='GGUF model path for Crawl4AI content analysis (default: ~/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf)'
    )

    parser.add_argument(
        '--enable-sigil-protocol',
        action='store_true',
        help='Enable Sigil Protocol Sacred Chain processing (Rule Zero compliance)')

    parser.add_argument(
        '--sigil-mode',
        choices=['enhanced', 'direct-llm', 'hybrid'],
        default='enhanced',
        help='Sigil processing mode: enhanced (API-based), direct-llm (local), hybrid (both)'
    )

    parser.add_argument(
        '--crate-list',
        type=str,
        nargs='+',
        help='Specific crates to process (space-separated list)'
    )

    parser.add_argument(
        '--config-file',
        type=str,
        help='JSON config file to override default settings'
    )

    return parser.parse_args()


def configure_logging(log_level: str = 'INFO'):
    """Configure logging with both console and file output"""
    level = getattr(logging, log_level.upper())

    # Clear any existing handlers to avoid conflicts
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Set root logger level
    root_logger.setLevel(level)

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)

    # File handler with unique timestamp
    log_filename = f"crate_enrichment_{time.strftime('%Y%m%d-%H%M%S')}.log"
    try:
        file_handler = logging.FileHandler(
            log_filename, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Always capture DEBUG+ to file
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)

        # Log a test message to verify file handler works
        logging.info(f"Logging initialized - file: {log_filename}")

    except Exception as e:
        logging.error(f"Failed to create log file {log_filename}: {e}")
        print(f"Warning: Could not create log file: {e}")

    # Set library loggers to less verbose levels
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests_cache').setLevel(logging.WARNING)
    logging.getLogger('llama_cpp').setLevel(logging.WARNING)


def check_disk_space():
    if shutil.disk_usage(".").free < 1_000_000_000:  # 1GB
        logging.warning("Low disk space! This may affect performance.")


def main():
    # Setup production environment first for optimal logging
    prod_config = setup_production_environment()

    args = parse_arguments()
    configure_logging(args.log_level)
    check_disk_space()

    # Check GitHub token before proceeding
    if not check_and_setup_github_token():
        logging.error("GitHub token setup cancelled or failed. Exiting.")
        sys.exit(1)

    try:
        # Create config from command line arguments
        config_kwargs = {}

        # Apply production optimizations if available
        if prod_config:
            config_kwargs.update({
                'max_retries': prod_config.get('max_retries', 3),
                'batch_size': prod_config.get('batch_size', 10),
                'checkpoint_interval': prod_config.get('checkpoint_interval', 10),
                'cache_ttl': prod_config.get('cache_ttl', 3600),
            })

        if args.batch_size:
            config_kwargs['batch_size'] = args.batch_size
        if args.workers:
            config_kwargs['n_workers'] = args.workers
        if args.model_path:
            config_kwargs['model_path'] = args.model_path
        if args.max_tokens:
            config_kwargs['max_tokens'] = args.max_tokens
        if args.checkpoint_interval:
            config_kwargs['checkpoint_interval'] = args.checkpoint_interval
            # Load config file if provided
        if args.config_file:
            import json
            with open(args.config_file, 'r') as f:
                file_config = json.load(f)
                config_kwargs.update(file_config)

        # Handle Crawl4AI configuration
        enable_crawl4ai = args.enable_crawl4ai and not args.disable_crawl4ai if hasattr(
            args, 'disable_crawl4ai') else True
        config_kwargs.update({
            'enable_crawl4ai': enable_crawl4ai,
            'crawl4ai_model': getattr(args, 'crawl4ai_model', '~/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf')
        })

        config = PipelineConfig(**config_kwargs)

        # Pass additional arguments to pipeline
        pipeline_kwargs = {}
        if args.output_dir:
            pipeline_kwargs['output_dir'] = args.output_dir
        if args.limit:
            pipeline_kwargs['limit'] = args.limit
        if args.crate_list:
            pipeline_kwargs['crate_list'] = args.crate_list
        if args.skip_ai:
            pipeline_kwargs['skip_ai'] = True
        if args.skip_source_analysis:
            pipeline_kwargs['skip_source'] = True

        # Sigil Protocol integration
        if hasattr(
                args,
                'enable_sigil_protocol') and args.enable_sigil_protocol:
            # Import Sigil enhanced pipeline
            try:
                import sys
                sys.path.append('.')  # Add current directory to path
                from sigil_enhanced_pipeline import SigilCompliantPipeline

                pipeline = SigilCompliantPipeline(config, **pipeline_kwargs)
                logging.info(
                    "Starting Sigil Protocol compliant pipeline with Sacred Chain processing")
            except ImportError as e:
                logging.warning(f"Sigil enhanced pipeline not available: {e}")
                logging.info("Falling back to standard pipeline")
                pipeline = CrateDataPipeline(config, **pipeline_kwargs)
        else:
            pipeline = CrateDataPipeline(config, **pipeline_kwargs)
        logging.info(f"Starting pipeline with {len(vars(args))} arguments")

        # Run the pipeline asynchronously
        import asyncio
        asyncio.run(pipeline.run())

    except Exception as e:
        logging.critical(f"Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
