# pipeline.py
import os
import time
import logging
import json
import asyncio
from typing import List, Dict, Optional
from .config import PipelineConfig, CrateMetadata, EnrichedCrate
from .network import CrateAPIClient, GitHubBatchClient
from .ai_processing import LLMEnricher
from .analysis import SourceAnalyzer, SecurityAnalyzer, UserBehaviorAnalyzer, DependencyAnalyzer

# Import enhanced scraping capabilities
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from enhanced_scraping import CrateDocumentationScraper, EnhancedScrapingResult
    enhanced_scraping_available = True
except ImportError:
    enhanced_scraping_available = False
    CrateDocumentationScraper = None
    EnhancedScrapingResult = None
    logging.warning("Enhanced scraping not available - using basic methods")


class CrateDataPipeline:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.api_client = CrateAPIClient(config)
        self.github_client = GitHubBatchClient(config)
        self.enricher = LLMEnricher(config)
        self.crates = self.get_crate_list()
        self.output_dir = self._create_output_dir()        # Initialize enhanced scraping if available
        self.enhanced_scraper = None
        if enhanced_scraping_available and CrateDocumentationScraper is not None and hasattr(config, 'enable_crawl4ai'):
            try:
                self.enhanced_scraper = CrateDocumentationScraper(
                    enable_crawl4ai=config.enable_crawl4ai)
                logging.info("✅ Enhanced scraping with Crawl4AI enabled")
            except Exception as e:
                logging.warning(
                    f"❌ Failed to initialize enhanced scraping: {e}")
        elif enhanced_scraping_available and CrateDocumentationScraper is not None:
            try:
                self.enhanced_scraper = CrateDocumentationScraper(
                    enable_crawl4ai=True)
                logging.info(
                    "✅ Enhanced scraping with Crawl4AI enabled (default)")
            except Exception as e:
                logging.warning(
                    f"❌ Failed to initialize enhanced scraping: {e}")

    def _create_output_dir(self) -> str:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_dir = f"crate_data_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def get_crate_list(self, limit: Optional[int] = None) -> List[str]:
        """Return a comprehensive list of all high-value crates to process"""
        crates = [
            # Web frameworks and servers
            "actix-web", "rocket", "axum", "warp", "tower", "tide", "gotham", "iron",
            "nickel", "rouille", "thruster", "poem", "salvo", "viz", "ntex", "may-minihttp",
            "tiny_http", "httptest", "mockito", "wiremock",

            # Async runtimes and utilities
            "tokio", "tokio-stream", "async-trait", "futures", "async-std", "smol",
            "embassy", "embassy-executor", "embassy-time", "embassy-sync", "async-channel",
            "async-broadcast", "async-lock", "async-once", "async-recursion", "futures-util",
            "futures-channel", "futures-timer", "futures-test", "pin-project", "pin-project-lite",

            # Serialization/deserialization
            "serde", "serde_json", "serde_yaml", "bincode", "toml", "ron", "postcard",
            "ciborium", "rmp-serde", "quick-xml", "roxmltree", "serde_cbor", "serde_derive",
            "serde_repr", "serde_with", "serde_bytes", "flexbuffers", "bson", "avro-rs",

            # Error handling and debugging
            "anyhow", "thiserror", "eyre", "color-eyre", "miette", "fehler", "snafu",
            "failure", "quick-error", "derive_more", "displaydoc", "backtrace", "better-panic",
            # Command line and terminal
            "clap", "structopt", "argh", "gumdrop", "docopt", "getopts", "pico-args",
            "crossterm", "termion", "console", "indicati", "dialoguer", "termcolor",
            "colored", "yansi", "owo-colors", "nu-ansi-term", "terminal_size",
            # Utilities and general purpose
            "rand", "uuid", "itertools", "num", "cfg-i", "bytes", "mime",
            "form_urlencoded", "csv", "once_cell", "base64", "flate2", "tar", "dirs",
            "walkdir", "glob", "bitflags", "indexmap", "smallvec", "arrayvec", "tinyvec",
            "ahash", "fxhash", "rustc-hash", "seahash", "siphasher", "wyhash", "xxhash-rust",
            "getrandom", "fastrand", "nanorand", "url", "percent-encoding", "unicode-segmentation",
            "unicode-normalization", "unicode-width", "memchr", "aho-corasick", "bstr",
            # HTTP clients and servers
            "reqwest", "hyper", "sur", "ureq", "attohttpc", "isahc", "curl", "libcurl-sys",
            "http", "http-body", "httparse", "hyper-tls", "hyper-rustls", "native-tls",
            "webpki", "webpki-roots",

            # Database and storage
            "sqlx", "diesel", "postgres", "rusqlite", "mysql", "mongodb", "redis",
            "tokio-postgres", "deadpool-postgres", "bb8", "r2d2", "sea-orm", "rbatis",
            "sled", "rocksdb", "lmdb", "redb", "pickledb", "persy", "heed", "fjall",
            # Concurrency and parallelism
            "rayon", "crossbeam", "crossbeam-channel", "crossbeam-utils", "crossbeam-epoch",
            "crossbeam-deque", "parking_lot", "spin", "atomic", "arc-swap", "dashmap",
            "flume", "kanal", "tokio-util", "futures-concurrency",
            # Protocol buffers, gRPC, and messaging
            "prost", "tonic", "protobu", "grpcio", "tarpc", "capnp", "rmp",
            "zmq", "nanomsg", "nats", "rdkafka", "pulsar", "lapin", "amqp", "rumqttc",
            # Procedural macros and metaprogramming
            "syn", "quote", "proc-macro2", "proc-macro-crate", "proc-macro-error",
            "darling", "derive_builder", "strum", "strum_macros",
            "enum-iterator", "num-derive", "num-traits", "paste", "lazy_static",

            # Cryptography and security
            "ring", "rustls", "openssl", "sha2", "sha3", "blake2", "blake3", "md5",
            "hmac", "pbkdf2", "scrypt", "argon2", "bcrypt", "chacha20poly1305",
            "aes-gcm", "rsa", "ed25519-dalek", "x25519-dalek", "curve25519-dalek",
            "secp256k1", "k256", "p256", "ecdsa", "signature", "rand_core",

            # Game development and graphics
            "bevy", "macroquad", "ggez", "piston", "winit", "wgpu", "vulkano", "glium",
            "three-d", "kiss3d", "nalgebra", "cgmath", "glam", "ultraviolet", "mint",
            "image", "imageproc", "resvg", "tiny-skia", "lyon", "femtovg", "skulpin",
            # Networking and protocols
            "socket2", "mio", "polling", "async-io", "calloop", "quinn",
            "rustls-pemfile", "trust-dns", "hickory-dns", "async-h1", "h2", "h3",
            "websocket", "tokio-tungstenite", "tungstenite", "ws", "warp-ws",

            # Text processing and parsing
            "regex", "regex-syntax", "pest", "pest_derive", "nom", "combine", "winnow",
            "lalrpop", "chumsky", "logos", "lex", "yacc", "tree-sitter", "syntect",
            "pulldown-cmark", "comrak", "markdown", "ammonia", "scraper", "kuchiki",

            # System programming and OS interfaces
            "libc", "winapi", "windows", "nix", "users", "sysinfo", "procfs", "psutil",
            "notify", "inotify", "hotwatch", "signal-hook", "ctrlc", "daemonize",
            "fork", "shared_memory", "memmap2", "mlock", "caps", "uzers",
            # Testing and development tools
            "criterion", "proptest", "quickcheck", "rstest", "serial_test", "mockall",
            "httpmock", "assert_cmd", "assert_fs", "predicates", "tempfile",
            "insta", "goldenfile", "similar", "difference", "pretty_assertions",

            # Configuration and environment
            "config", "figment", "envy", "dotenv", "confy", "directories", "app_dirs",
            "etcetera", "platform-dirs", "home", "which", "dunce", "normpath",

            # Logging and observability
            "log", "env_logger", "tracing", "tracing-subscriber", "tracing-futures",
            "tracing-actix-web", "tracing-log", "slog", "fern", "flexi_logger",
            "log4rs", "simplelog", "stderrlog", "pretty_env_logger", "fast_log",

            # Time and date
            "chrono", "time", "humantime", "chrono-tz", "chrono-english", "ical",
            "cron", "tokio-cron-scheduler", "job_scheduler", "delay_timer",

            # Machine Learning & AI
            "tokenizers", "safetensors", "linfa", "ndarray", "smartcore", "burn",
            "tract-core", "tract-onnx", "tract-hir", "tract-linalg", "tract-data",
            "tract-nne", "tract-onnx-opl", "tract-pulse", "tract-pulse-opl",
            "tract-nnef-resources", "tch", "torch-sys", "ort", "ort-sys", "candle-core",
            "candle-nn", "candle-transformers", "candle-kernels", "candle-onnx",
            "candle-metal-kernels", "tiktoken-rs", "tensorflow", "tensorflow-sys",
            "onnxruntime", "onnxruntime-sys", "onnx-protobu", "llama-cpp-2",
            "llama-cpp-sys-2", "llm", "llm-samplers", "llm-chain", "llm-chain-openai", "llama-core", "llamaedge", "openai", "openai-api-rs", "openai_dive",
            "genai", "aleph-alpha-client", "llm_api_access", "ollama-rs",
            "rust-bert", "fastembed", "hf-hub", "whisper-rs-sys", "toktrie",
            "toktrie_hf_tokenizers", "toktrie_hf_downloader", "rust_tokenizers",
        ]

        if limit is not None:
            return crates[:limit]
        return crates

    async def fetch_metadata_batch(
            self,
            crate_names: List[str]) -> List[CrateMetadata]:
        """Fetch metadata for a batch of crates using asyncio-based parallel processing

        Each coroutine processes completely independent crate data, ensuring safety.
        No shared state is modified - each coroutine only reads from self.api_client and
        returns independent results.
        """
        results = []

        async def fetch_single_crate_safe(crate_name: str) -> Optional[CrateMetadata]:
            try:
                # If api_client has an async method, use it; otherwise, run in executor
                if hasattr(self.api_client, 'fetch_crate_metadata_async'):
                    data = await self.api_client.fetch_crate_metadata_async(crate_name)
                else:
                    loop = asyncio.get_running_loop()
                    data = await loop.run_in_executor(None, self.api_client.fetch_crate_metadata, crate_name)
                if data:
                    return CrateMetadata(
                        name=data.get("name", ""),
                        version=data.get("version", ""),
                        description=data.get("description", ""),
                        repository=data.get("repository", ""),
                        keywords=data.get("keywords", []),
                        categories=data.get("categories", []),
                        readme=data.get("readme", ""),
                        downloads=data.get("downloads", 0),
                        github_stars=data.get("github_stars", 0),
                        dependencies=data.get("dependencies", []),
                        features=data.get("features", []),
                        code_snippets=data.get("code_snippets", []),
                        readme_sections=data.get("readme_sections", {}),
                        librs_downloads=data.get("librs_downloads"),
                        source=data.get("source", "crates.io")
                    )
                return None
            except Exception as e:
                logging.error(f"Error fetching {crate_name}: {e}")
                return None

        # Use asyncio.gather for parallel async processing
        tasks = [fetch_single_crate_safe(name) for name in crate_names]
        results_raw = await asyncio.gather(*tasks)
        results = [r for r in results_raw if r is not None]
        for crate in results:
            logging.info(f"Fetched metadata for {crate.name}")
        return results

    # Remove the async methods that are no longer needed
    # async def _fetch_single_crate_async(self, crate_name: str) ->
    # Optional[Dict]:

    async def enrich_batch(
            self,
            batch: List[CrateMetadata]) -> List[EnrichedCrate]:
        """Enrich a batch of crates with GitHub stats, enhanced scraping, and AI"""
        # Add GitHub stats first
        github_repos = [
            c.repository for c in batch if "github.com" in c.repository]
        repo_stats = self.github_client.batch_get_repo_stats(github_repos)

        # Update crates with GitHub info
        for crate in batch:
            repo_url = crate.repository
            if repo_url in repo_stats:
                stats = repo_stats[repo_url]
                crate.github_stars = stats.get("stargazers_count", 0)

        # Enhanced scraping if available
        if self.enhanced_scraper:
            batch = asyncio.run(self._enhance_with_scraping(batch))

        # Now enrich with AI
        enriched_batch = []
        for crate in batch:
            try:
                enriched = self.enricher.enrich_crate(crate)
                enriched_batch.append(enriched)
                logging.info(f"Enriched {crate.name}")
            except Exception as e:
                logging.error(f"Failed to enrich {crate.name}: {str(e)}")
                # Add the crate with just the fields we have
                enriched_dict = crate.__dict__.copy()
                enriched_batch.append(EnrichedCrate(**enriched_dict))

        return enriched_batch

    async def _enhance_with_scraping(
            self, batch: List[CrateMetadata]) -> List[CrateMetadata]:
        """Enhance crates with advanced web scraping data"""
        enhanced_batch = []

        for crate in batch:
            try:                # Scrape comprehensive documentation
                scraping_results = await self.enhanced_scraper.scrape_crate_info(crate.name)

                # Integrate scraping results into crate metadata
                enhanced_crate = self._integrate_scraping_results(
                    crate, scraping_results)
                enhanced_batch.append(enhanced_crate)

                logging.info(
                    f"Enhanced scraping for {crate.name}: {len(scraping_results)} sources")

            except Exception as e:
                logging.warning(
                    f"Enhanced scraping failed for {crate.name}: {e}")
                enhanced_batch.append(crate)

        return enhanced_batch

    def _integrate_scraping_results(self,
                                    crate: CrateMetadata,
                                    scraping_results: Dict[str,
                                                           EnhancedScrapingResult]) -> CrateMetadata:
        """Integrate enhanced scraping results into crate metadata"""
        # Create a copy of the crate to avoid modifying the original
        enhanced_crate = CrateMetadata(**crate.__dict__)

        # Add enhanced scraping data
        enhanced_crate.enhanced_scraping = {}

        for source, result in scraping_results.items():
            if result.error:
                continue

            enhanced_crate.enhanced_scraping[source] = {
                'title': result.title,
                'quality_score': result.quality_score,
                'extraction_method': result.extraction_method,
                'structured_data': result.structured_data,
                'content_length': len(result.content)
            }            # Update README if we got better content
            if source == 'docs_rs' and result.quality_score > 0.7:
                if not enhanced_crate.readme or len(
                        result.content) > len(
                        enhanced_crate.readme):
                    enhanced_crate.readme = result.content
                    logging.info(
                        f"Updated README for {crate.name} from {source}")

            # Extract additional metadata from structured data
            if result.structured_data:
                if 'features' in result.structured_data and isinstance(
                        result.structured_data['features'], list):
                    enhanced_crate.enhanced_features = result.structured_data['features']

                if 'dependencies' in result.structured_data and isinstance(
                        result.structured_data['dependencies'], list):
                    enhanced_crate.enhanced_dependencies = result.structured_data['dependencies']

                if 'examples' in result.structured_data and isinstance(
                        result.structured_data['examples'], list):
                    enhanced_crate.code_snippets.extend(
                        result.structured_data['examples'])

        return enhanced_crate

    def analyze_dependencies(self, crates: List[EnrichedCrate]) -> Dict:
        """Analyze dependencies between crates"""
        return DependencyAnalyzer.analyze_dependencies(crates)

    def save_checkpoint(self, data: List[EnrichedCrate], prefix: str):
        """Save processing checkpoint with status metadata"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(self.output_dir, f"{prefix}_{timestamp}.jsonl")

        with open(filename, "w") as f:
            for item in data:
                # Convert to dict for serialization
                item_dict = item.__dict__.copy()
                f.write(json.dumps(item_dict) + "\n")

        # Save status metadata
        status = {
            "timestamp": timestamp,
            "total_crates": len(data),
            "processed_crates": sum(
                1 for c in data if c.use_case is not None),
            "advanced_analysis": sum(
                1 for c in data if c.source_analysis is not None),
            "checkpoint_file": filename}

        status_file = os.path.join(
            self.output_dir,
            f"{prefix}_status_{timestamp}.json")
        with open(status_file, "w") as f:
            json.dump(status, f, indent=2)

        logging.info(f"Saved checkpoint to {filename}")
        return filename

    def save_final_output(
            self,
            data: List[EnrichedCrate],
            dependency_data: Dict):
        """Save final enriched data and analysis"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")

        # Save main enriched data
        final_output = os.path.join(
            self.output_dir,
            f"enriched_crate_metadata_{timestamp}.jsonl")
        with open(final_output, "w") as f:
            for item in data:
                item_dict = item.__dict__.copy()
                f.write(json.dumps(item_dict) + "\n")

        # Save dependency analysis
        dep_file = os.path.join(
            self.output_dir,
            f"dependency_analysis_{timestamp}.json")
        with open(dep_file, "w") as f:
            json.dump(dependency_data, f, indent=2)

        # Generate summary report
        summary = {
            "total_crates": len(data),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "most_popular": sorted([{
                "name": c.name,
                "score": c.score or 0,
                "downloads": c.downloads,
                "github_stars": c.github_stars
            } for c in data], key=lambda x: x["score"], reverse=True)[:5],
            "most_depended_upon": dependency_data.get("most_depended", [])[:5]
        }

        summary_file = os.path.join(
            self.output_dir,
            f"summary_report_{timestamp}.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        logging.info(f"Results saved to {self.output_dir}/")

    async def run(self):
        """Main pipeline execution flow (async)"""
        start_time = time.time()
        logging.info(f"Processing {len(self.crates)} crates...")

        # Process in batches
        all_enriched = []
        crate_batches = [self.crates[i:i + self.config.batch_size]
                         for i in range(0, len(self.crates), self.config.batch_size)]

        for batch_num, batch in enumerate(crate_batches):
            logging.info(
                f"Processing batch {batch_num + 1}/{len(crate_batches)} ({len(batch)} crates)")

            # Fetch metadata (async)
            batch_data = await self.fetch_metadata_batch(batch)

            # Enrich the batch (async)
            enriched_batch = await self.enrich_batch(batch_data)
            all_enriched.extend(enriched_batch)

            # Save checkpoint after each batch
            self.save_checkpoint(all_enriched, "batch_checkpoint")
            logging.info(
                f"Completed batch {batch_num + 1}, processed {len(all_enriched)}/{len(self.crates)} crates so far")

            # Optional: Add source analysis for some crates
            if batch_num < 2:  # Only do detailed analysis for first 2 batches
                for crate in enriched_batch:
                    try:
                        crate.source_analysis = SourceAnalyzer.analyze_crate_source(
                            crate)
                        crate.security = SecurityAnalyzer.check_security_metrics(
                            crate)
                        crate.user_behavior = UserBehaviorAnalyzer.fetch_user_behavior_data(
                            crate)
                        logging.info(
                            f"Advanced analysis completed for {crate.name}")
                    except Exception as e:
                        logging.warning(
                            f"Advanced analysis failed for {crate.name}: {str(e)}")

        # Step 3: Perform dependency analysis
        logging.info("Analyzing crate dependencies...")
        dependency_analysis = self.analyze_dependencies(all_enriched)

        # Save final results
        self.save_final_output(all_enriched, dependency_analysis)

        # Final summary
        duration = time.time() - start_time
        logging.info(
            f"✅ Done. Enriched {len(all_enriched)} crates in {duration:.2f}s")

        return all_enriched, dependency_analysis
