# main.py
import os
import sys
import time
import logging
import shutil
import argparse
from typing import Optional
from .config import PipelineConfig
from .pipeline import CrateDataPipeline

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
    
    parser.add_argument(
        '--log-level',
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
    level = getattr(logging, log_level.upper())
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"crate_enrichment_{time.strftime('%Y%m%d-%H%M%S')}.log")
        ]
    )

def check_disk_space():
    if shutil.disk_usage(".").free < 1_000_000_000:  # 1GB
        logging.warning("Low disk space! This may affect performance.")

def main():
    args = parse_arguments()
    configure_logging(args.log_level)
    check_disk_space()
    
    try:
        # Create config from command line arguments
        config_kwargs = {}
        
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
            
        pipeline = CrateDataPipeline(config, **pipeline_kwargs)
        
        logging.info(f"Starting pipeline with {len(vars(args))} arguments")
        pipeline.run()
        
    except Exception as e:
        logging.critical(f"Pipeline failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()