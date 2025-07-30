# config.py
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class PipelineConfig:
    model_path: str = os.path.expanduser("~/models/deepseek/deepseek-coder-6.7b-instruct.Q4_K_M.gguf")
    max_tokens: int = 256
    model_token_limit: int = 4096
    prompt_token_margin: int = 3000
    checkpoint_interval: int = 10
    max_retries: int = 3
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    cache_ttl: int = 3600  # 1 hour
    batch_size: int = 10
    n_workers: int = 4

@dataclass
class CrateMetadata:
    name: str
    version: str
    description: str
    repository: str
    keywords: List[str]
    categories: List[str]
    readme: str
    downloads: int
    github_stars: int = 0
    dependencies: List[Dict[str, Any]] = field(default_factory=list)
    features: List[Dict[str, Any]] = field(default_factory=list)
    code_snippets: List[str] = field(default_factory=list)
    readme_sections: Dict[str, str] = field(default_factory=dict)
    librs_downloads: Optional[int] = None
    source: str = "crates.io"

@dataclass
class EnrichedCrate(CrateMetadata):
    readme_summary: Optional[str] = None
    feature_summary: Optional[str] = None
    use_case: Optional[str] = None
    score: Optional[float] = None
    factual_counterfactual: Optional[str] = None
    source_analysis: Optional[Dict[str, Any]] = None
    user_behavior: Optional[Dict[str, Any]] = None
    security: Optional[Dict[str, Any]] = None