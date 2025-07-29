# production_config.py
"""
Production configuration to reduce runtime warnings and optimize performance.
This file contains settings that can be imported to minimize verbose logging
and improve the user experience in production environments.
"""

import logging
import os

# Production logging configuration
def configure_production_logging():
    """Configure logging for production to reduce verbose warnings"""
    
    # Set up logging format
    logging.basicConfig(
        level=logging.INFO,  # Default to INFO level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set specific loggers to less verbose levels
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests_cache').setLevel(logging.WARNING)
    
    # If PRODUCTION environment variable is set, be even quieter
    if os.getenv('PRODUCTION', 'false').lower() == 'true':
        logging.getLogger().setLevel(logging.WARNING)
        logging.getLogger('rust_crate_pipeline').setLevel(logging.INFO)

# Production-optimized settings
PRODUCTION_SETTINGS = {
    # Reduced retries to minimize warnings
    'max_retries': 2,
    'validation_retries': 2,
    
    # GitHub API management
    'github_rate_limit_threshold': 100,
    'github_critical_threshold': 50,
    
    # LLM settings  
    'llm_timeout': 30,
    'llm_max_attempts': 2,
    
    # Logging preferences
    'quiet_mode': True,
    'log_level': 'INFO',
    
    # Performance settings
    'batch_size': 10,
    'checkpoint_interval': 10,
    'cache_ttl': 3600,
}

def get_production_config():
    """Get production configuration dictionary"""
    return PRODUCTION_SETTINGS.copy()

def is_production():
    """Check if running in production mode"""
    return os.getenv('PRODUCTION', 'false').lower() == 'true'

def setup_production_environment():
    """Set up the complete production environment"""
    configure_production_logging()
    
    # Set environment variables for quieter operation
    os.environ.setdefault('PYTHONWARNINGS', 'ignore::UserWarning')
    
    if is_production():
        print("🚀 Production mode enabled - optimized for minimal warnings")
        return get_production_config()
    else:
        print("🔧 Development mode - full logging enabled")
        return {}
