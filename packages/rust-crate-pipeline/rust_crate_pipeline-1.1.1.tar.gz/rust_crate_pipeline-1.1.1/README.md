# Rust Crate Data Processing Pipeline

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive system for gathering, enriching, and analyzing metadata for Rust crates using AI-powered insights and dependency analysis.

## 🚀 Features

### 📊 **Comprehensive Data Collection**
- **Multi-source metadata fetching**: Pulls data from crates.io, GitHub, and lib.rs
- **Dependency analysis**: Complete dependency graphs and reverse dependency mapping
- **Code snippet extraction**: Automatically extracts Rust code examples from READMEs
- **Feature analysis**: Detailed breakdown of crate features and their dependencies

### 🤖 **AI-Powered Enrichment**
- **Use case classification**: Automatically categorizes crates (Web Framework, ML, Database, etc.)
- **Feature summarization**: AI-generated explanations of crate features
- **Factual/counterfactual pairs**: Generates training data for fact verification
- **Smart content truncation**: Intelligently preserves important README sections

### 🔍 **Advanced Analysis**
- **Source code metrics**: Lines of code, complexity analysis, API surface area
- **Security scanning**: Vulnerability checks and security pattern analysis
- **Community metrics**: GitHub activity, issue tracking, version adoption
- **Performance optimization**: Batch processing, caching, and retry logic

### ⚡ **Production-Ready Features**
- **Robust error handling**: Graceful degradation and comprehensive logging
- **Rate limiting**: Respects GitHub API limits with intelligent backoff
- **Checkpointing**: Automatic progress saving for long-running processes
- **Configurable processing**: Extensive CLI and config file options

## 📋 Prerequisites

### Required Dependencies
```bash
pip install requests requests-cache beautifulsoup4 tqdm llama-cpp-python tiktoken psutil
```

### Optional Dependencies
```bash
pip install radon rustworkx  # For advanced code analysis
```

### System Requirements
- **Python 3.8+**
- **Local LLM Model**: Deepseek Coder or compatible GGUF model
- **GitHub Token**: For enhanced GitHub API access (optional but recommended)
- **Disk Space**: ~1GB free space for processing and caching

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd enrichment-flow2
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download LLM Model
```bash
# Example: Download Deepseek Coder model
mkdir -p ~/models/deepseek/
wget https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF/resolve/main/deepseek-coder-6.7b-instruct.Q4_K_M.gguf \
     -O ~/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf
```

### 4. Set Environment Variables (Optional)
```bash
export GITHUB_TOKEN="your_github_token_here"
```

## 🚀 Quick Start

### Installation

#### From PyPI (Recommended)
```bash
pip install rust-crate-pipeline
```

#### From Source
```bash
git clone https://github.com/DaveTmire85/SigilDERG-Data_Production.git
cd SigilDERG-Data_Production
pip install -e .
```

#### Development Installation
```bash
git clone https://github.com/DaveTmire85/SigilDERG-Data_Production.git
cd SigilDERG-Data_Production
pip install -e ".[dev]"
```

### Basic Usage
```bash
# Run with default settings
python -m rust_crate_pipeline

# Process only 20 crates for testing
python -m rust_crate_pipeline --limit 20

# Skip AI processing for faster metadata-only collection
python -m rust_crate_pipeline --skip-ai --limit 50
```

### Advanced Usage
```bash
# Custom configuration
python -m rust_crate_pipeline \
    --limit 100 \
    --batch-size 5 \
    --workers 2 \
    --log-level DEBUG \
    --output-dir ./results

# Process specific crates
python -m rust_crate_pipeline \
    --crate-list serde tokio actix-web reqwest \
    --output-dir ./specific_crates

# Use custom model and config
python -m rust_crate_pipeline \
    --model-path ./my-model.gguf \
    --config-file ./custom_config.json
```

## 📁 Project Structure

```
enrichment-flow2/
├── __init__.py              # Package initialization and public API
├── __main__.py              # Entry point for python -m execution
├── main.py                  # CLI interface and main execution logic
├── config.py                # Configuration classes and data models
├── pipeline.py              # Main orchestration and workflow management
├── ai_processing.py         # LLM integration and AI-powered enrichment
├── network.py               # API clients and HTTP request handling
├── analysis.py              # Source code, security, and dependency analysis
└── utils/                   # Utility functions
    ├── logging_utils.py     # Logging configuration and decorators
    └── file_utils.py        # File operations and disk management
```

## ⚙️ Configuration

### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--limit` | int | None | Limit number of crates to process |
| `--batch-size` | int | 10 | Crates processed per batch |
| `--workers` | int | 4 | Parallel workers for API requests |
| `--output-dir` | str | auto | Custom output directory |
| `--model-path` | str | default | Path to LLM model file |
| `--max-tokens` | int | 256 | Maximum tokens for LLM generation |
| `--checkpoint-interval` | int | 10 | Save progress every N crates |
| `--log-level` | str | INFO | Logging verbosity |
| `--skip-ai` | flag | False | Skip AI enrichment |
| `--skip-source-analysis` | flag | False | Skip source code analysis |
| `--crate-list` | list | None | Specific crates to process |
| `--config-file` | str | None | JSON configuration file |

### Configuration File Example
```json
{
    "model_path": "/path/to/your/model.gguf",
    "batch_size": 5,
    "n_workers": 2,
    "max_tokens": 512,
    "checkpoint_interval": 5,
    "github_token": "ghp_your_token_here",
    "cache_ttl": 7200
}
```

## 📊 Output Format

The pipeline generates several output files:

### 1. **Enriched Metadata** (`enriched_crate_metadata_TIMESTAMP.jsonl`)
```json
{
    "name": "serde",
    "version": "1.0.193",
    "description": "A generic serialization/deserialization framework",
    "use_case": "Serialization",
    "score": 8542.3,
    "feature_summary": "Provides derive macros for automatic serialization...",
    "factual_counterfactual": "✅ Factual: Serde supports JSON serialization...",
    "source_analysis": {
        "file_count": 45,
        "loc": 12500,
        "functions": ["serialize", "deserialize", ...],
        "has_tests": true
    }
}
```

### 2. **Dependency Analysis** (`dependency_analysis_TIMESTAMP.json`)
```json
{
    "dependency_graph": {
        "actix-web": ["tokio", "serde", "futures"],
        "tokio": ["mio", "parking_lot"]
    },
    "reverse_dependencies": {
        "serde": ["actix-web", "reqwest", "clap"],
        "tokio": ["actix-web", "reqwest"]
    },
    "most_depended": [
        ["serde", 156],
        ["tokio", 98]
    ]
}
```

### 3. **Summary Report** (`summary_report_TIMESTAMP.json`)
```json
{
    "total_crates": 150,
    "total_time": "1247.32s",
    "timestamp": "2025-06-18T10:30:00",
    "most_popular": [
        {"name": "serde", "score": 8542.3},
        {"name": "tokio", "score": 7234.1}
    ]
}
```

## 🔧 Advanced Features

### Custom Crate Lists
Process specific crates by providing a custom list:
```bash
python -m rust_crate_pipeline --crate-list \
    serde tokio actix-web reqwest clap \
    --output-dir ./web_framework_analysis
```

### Performance Tuning
Optimize for your system:
```bash
# High-performance setup (good internet, powerful machine)
python -m rust_crate_pipeline --batch-size 20 --workers 8

# Conservative setup (limited resources)
python -m rust_crate_pipeline --batch-size 3 --workers 1
```

### Development Mode
Quick testing with minimal processing:
```bash
python -m rust_crate_pipeline \
    --limit 5 \
    --skip-ai \
    --skip-source-analysis \
    --log-level DEBUG
```

## 🏗️ Architecture

### Core Components

1. **CrateDataPipeline**: Main orchestration class that coordinates all processing
2. **LLMEnricher**: Handles AI-powered enrichment using local LLM models
3. **CrateAPIClient**: Manages API interactions with crates.io and fallback sources
4. **GitHubBatchClient**: Optimized GitHub API client with rate limiting
5. **SourceAnalyzer**: Analyzes source code metrics and complexity
6. **SecurityAnalyzer**: Checks for security vulnerabilities and patterns
7. **UserBehaviorAnalyzer**: Tracks community engagement and version adoption
8. **DependencyAnalyzer**: Builds and analyzes dependency relationships

### Processing Flow

```
1. Crate Discovery → 2. Metadata Fetching → 3. AI Enrichment
        ↓                      ↓                    ↓
4. Source Analysis → 5. Security Scanning → 6. Community Analysis
        ↓                      ↓                    ↓
7. Dependency Mapping → 8. Data Aggregation → 9. Report Generation
```

## 🧪 API Usage

### Programmatic Usage
```python
from rust_crate_pipeline import CrateDataPipeline, PipelineConfig

# Create custom configuration
config = PipelineConfig(
    batch_size=5,
    max_tokens=512,
    model_path="/path/to/model.gguf"
)

# Initialize and run pipeline
pipeline = CrateDataPipeline(config)
pipeline.run()

# Or use individual components
from rust_crate_pipeline import LLMEnricher, SourceAnalyzer

enricher = LLMEnricher(config)
analyzer = SourceAnalyzer()
```

### Custom Processing
```python
# Process specific crates with custom options
pipeline = CrateDataPipeline(
    config,
    limit=50,
    crate_list=["serde", "tokio", "actix-web"],
    skip_ai=False,
    output_dir="./custom_analysis"
)
```

## 🐛 Troubleshooting

### Common Issues

**🔴 Model Loading Errors**
```bash
# Verify model path
ls -la ~/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf

# Check model format compatibility
python -c "from llama_cpp import Llama; print('Model loading OK')"
```

**🔴 API Rate Limiting**
```bash
# Set GitHub token for higher rate limits
export GITHUB_TOKEN="your_token_here"

# Reduce batch size and workers
python -m rust_crate_pipeline --batch-size 3 --workers 1
```

**🔴 Memory Issues**
```bash
# Reduce token limits and batch size
python -m rust_crate_pipeline --max-tokens 128 --batch-size 2
```

**🔴 Network Timeouts**
```bash
# Enable debug logging to identify issues
python -m rust_crate_pipeline --log-level DEBUG --limit 10
```

### Performance Optimization

1. **Use SSD storage** for faster caching and temporary file operations
2. **Increase RAM** if processing large batches (recommended: 8GB+)
3. **Set GITHUB_TOKEN** for 5000 req/hour instead of 60 req/hour
4. **Use appropriate batch sizes** based on your internet connection
5. **Monitor disk space** - processing can generate several GB of data

## 📈 Performance Metrics

### Typical Processing Times
- **Metadata only**: ~2-3 seconds per crate
- **With AI enrichment**: ~15-30 seconds per crate
- **Full analysis**: ~45-60 seconds per crate

### Resource Usage
- **Memory**: 2-4GB during processing
- **Disk**: 10-50MB per crate (temporary files)
- **Network**: ~1-5MB per crate (API calls)

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd enrichment-flow2

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black . && isort .
```

### Adding New Analysis Features
1. Implement new analyzer in `analysis.py`
2. Add configuration options to `config.py`
3. Integrate with pipeline in `pipeline.py`
4. Add CLI arguments in `main.py`
5. Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Rust Community** for the excellent crates ecosystem
- **crates.io** for providing comprehensive API access
- **GitHub** for repository metadata and community data
- **Deepseek** for the powerful code-focused language model
- **llama.cpp** team for efficient local inference capabilities

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)

---

**Happy crate analyzing! 🦀✨**
