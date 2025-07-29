# analysis.py
import os
import re
import io
import json
import time
import tarfile
import tempfile
import subprocess
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
from .config import EnrichedCrate

class SourceAnalyzer:
    @staticmethod
    def analyze_crate_source(crate: EnrichedCrate) -> Dict:
        """Orchestrate source analysis from multiple sources"""
        crate_name = crate.name
        version = crate.version
        repo_url = crate.repository
        
        # Method 1: Try to download from crates.io
        try:
            url = f"https://crates.io/api/v1/crates/{crate_name}/{version}/download"
            response = requests.get(url, stream=True)
            
            if response.ok:
                # We got the tarball, analyze it
                return SourceAnalyzer.analyze_crate_tarball(response.content)
        except Exception as e:
            print(f"Failed to download from crates.io: {str(e)}")
        
        # Method 2: Try GitHub if we have a GitHub URL
        if "github.com" in repo_url:
            try:
                # Extract owner/repo from URL
                match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
                if match:
                    owner, repo_name = match.groups()
                    repo_name = repo_name.split('.')[0]  # Remove .git extension
                    
                    # Try to download tarball from GitHub
                    github_url = f"https://api.github.com/repos/{owner}/{repo_name}/tarball"
                    response = requests.get(github_url)
                    
                    if response.ok:
                        return SourceAnalyzer.analyze_github_tarball(response.content)
            except Exception as e:
                print(f"Failed to analyze from GitHub: {str(e)}")
        
        # Method 3: Try lib.rs
        try:
            # lib.rs doesn't have a direct download API, but redirects to crates.io or GitHub
            url = f"https://lib.rs/crates/{crate_name}"
            response = requests.get(url)
            
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for repository links
                repo_links = soup.select('a[href*="github.com"]')
                if repo_links:
                    repo_url = repo_links[0]['href']
                    
                    # We found a GitHub link, now analyze it
                    return SourceAnalyzer.analyze_crate_source_from_repo(crate_name, version, repo_url)
        except Exception as e:
            print(f"Failed to analyze from lib.rs: {str(e)}")
        
        # If we get here, we failed to analyze from any source
        return {
            "error": "Could not analyze crate from any source",
            "attempted_sources": ["crates.io", "github", "lib.rs"],
            "file_count": 0,
            "loc": 0
        }

    @staticmethod
    def analyze_crate_tarball(content: bytes) -> Dict:
        """Analyze a .crate tarball from crates.io"""
        metrics = {
            "file_count": 0,
            "loc": 0,
            "complexity": [],
            "types": [],
            "traits": [],
            "functions": [],
            "has_tests": False,
            "has_examples": False,
            "has_benchmarks": False
        }
        
        try:
            # Open the tar file from the content
            tar_content = io.BytesIO(content)
            with tarfile.open(fileobj=tar_content, mode='r:gz') as tar:
                # Get list of Rust files
                rust_files = [f for f in tar.getnames() if f.endswith('.rs')]
                metrics["file_count"] = len(rust_files)
                
                # Check for test/example/bench directories
                all_files = tar.getnames()
                metrics["has_tests"] = any('test' in f.lower() for f in all_files)
                metrics["has_examples"] = any('example' in f.lower() for f in all_files)
                metrics["has_benchmarks"] = any('bench' in f.lower() for f in all_files)
                
                # Analyze each Rust file
                for filename in rust_files:
                    try:
                        member = tar.getmember(filename)
                        if member.isfile():
                            file_content = tar.extractfile(member)
                            if file_content:
                                content_str = file_content.read().decode('utf-8', errors='ignore')
                                
                                # Count lines of code
                                metrics["loc"] += len(content_str.splitlines())
                                
                                # Extract code elements
                                fn_matches = re.findall(r'fn\s+([a-zA-Z0-9_]+)', content_str)
                                struct_matches = re.findall(r'struct\s+([a-zA-Z0-9_]+)', content_str)
                                trait_matches = re.findall(r'trait\s+([a-zA-Z0-9_]+)', content_str)
                                
                                metrics["functions"].extend(fn_matches)
                                metrics["types"].extend(struct_matches)
                                metrics["traits"].extend(trait_matches)
                    except Exception as e:
                        print(f"Error analyzing file {filename}: {str(e)}")
                        
        except Exception as e:
            metrics["error"] = str(e)
        
        return metrics

    @staticmethod
    def analyze_github_tarball(content: bytes) -> Dict:
        """Analyze a GitHub tarball (which has a different structure)"""
        metrics = {
            "file_count": 0,
            "loc": 0,
            "complexity": [],
            "types": [],
            "traits": [],
            "functions": [],
            "has_tests": False,
            "has_examples": False,
            "has_benchmarks": False
        }
        
        try:
            # GitHub tarballs are typically gzipped tar files
            tar_content = io.BytesIO(content)
            with tarfile.open(fileobj=tar_content, mode='r:gz') as tar:
                # GitHub tarballs include the repo name and commit as the top dir
                # So we need to handle the different structure
                rust_files = [f for f in tar.getnames() if f.endswith('.rs')]
                metrics["file_count"] = len(rust_files)
                
                # Check for test/example/bench directories
                all_files = tar.getnames()
                metrics["has_tests"] = any('test' in f.lower() for f in all_files)
                metrics["has_examples"] = any('example' in f.lower() for f in all_files)
                metrics["has_benchmarks"] = any('bench' in f.lower() for f in all_files)
                
                # Analyze each Rust file (same as crate tarball)
                for filename in rust_files:
                    try:
                        member = tar.getmember(filename)
                        if member.isfile():
                            file_content = tar.extractfile(member)
                            if file_content:
                                content_str = file_content.read().decode('utf-8', errors='ignore')
                                
                                # Count lines of code
                                metrics["loc"] += len(content_str.splitlines())
                                
                                # Extract code elements
                                fn_matches = re.findall(r'fn\s+([a-zA-Z0-9_]+)', content_str)
                                struct_matches = re.findall(r'struct\s+([a-zA-Z0-9_]+)', content_str)
                                trait_matches = re.findall(r'trait\s+([a-zA-Z0-9_]+)', content_str)
                                
                                metrics["functions"].extend(fn_matches)
                                metrics["types"].extend(struct_matches)
                                metrics["traits"].extend(trait_matches)
                    except Exception as e:
                        print(f"Error analyzing file {filename}: {str(e)}")
                        
        except Exception as e:
            metrics["error"] = str(e)
        
        return metrics

    @staticmethod
    def analyze_local_directory(directory: str) -> Dict:
        """Analyze source code from a local directory"""
        metrics = {
            "file_count": 0,
            "loc": 0,
            "complexity": [],
            "types": [],
            "traits": [],
            "functions": [],
            "has_tests": False,
            "has_examples": False,
            "has_benchmarks": False
        }
        
        try:
            # Find all Rust files
            rust_files = []
            for root, _, files in os.walk(directory):
                if "target" in root or ".git" in root:  # Skip build dirs and git
                    continue
                rust_files.extend([os.path.join(root, f) for f in files if f.endswith(".rs")])
                
            metrics["file_count"] = len(rust_files)
            
            # Check if the crate has tests/examples/benchmarks
            metrics["has_tests"] = any(os.path.exists(os.path.join(directory, d)) 
                                      for d in ["tests", "test"])
            metrics["has_examples"] = os.path.exists(os.path.join(directory, "examples"))
            metrics["has_benchmarks"] = os.path.exists(os.path.join(directory, "benches"))
            
            # Analyze each Rust file
            for file_path in rust_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Count lines of code
                    metrics["loc"] += len(content.splitlines())
                    
                    # Extract code elements
                    fn_matches = re.findall(r'fn\s+([a-zA-Z0-9_]+)', content)
                    struct_matches = re.findall(r'struct\s+([a-zA-Z0-9_]+)', content)
                    trait_matches = re.findall(r'trait\s+([a-zA-Z0-9_]+)', content)
                    
                    metrics["functions"].extend(fn_matches)
                    metrics["types"].extend(struct_matches)
                    metrics["traits"].extend(trait_matches)
                    
                except Exception as e:
                    print(f"Error analyzing file {file_path}: {str(e)}")
            
        except Exception as e:
            metrics["error"] = str(e)
        
        return metrics

    @staticmethod
    def analyze_crate_source_from_repo(crate_name: str, version: str, repo_url: str) -> Dict:
        """Clone and analyze a crate's source code from repository"""
        temp_dir = f"/tmp/rust_analysis/{crate_name}"
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Clone repository
            if not os.path.exists(f"{temp_dir}/.git"):
                subprocess.run(["git", "clone", "--depth=1", repo_url, temp_dir], 
                              capture_output=True, text=True, check=True)
            
            return SourceAnalyzer.analyze_local_directory(temp_dir)
            
        except Exception as e:
            return {
                "error": f"Failed to clone and analyze repository: {str(e)}",
                "file_count": 0,
                "loc": 0
            }
        finally:
            # Clean up (optional)
            # subprocess.run(["rm", "-rf", temp_dir], capture_output=True)
            pass

class SecurityAnalyzer:
    @staticmethod
    def check_security_metrics(crate: EnrichedCrate) -> Dict:
        """Check security metrics for a crate"""
        security_data = {
            "advisories": [],
            "vulnerability_count": 0,
            "cargo_audit": None,
            "clippy_warnings": 0,
            "test_coverage": None
        }
        
        crate_name = crate.name
        version = crate.version
        
        # Check RustSec Advisory Database
        try:
            # This would require the RustSec advisory database
            # For now, just return placeholder data
            advisories_url = f"https://rustsec.org/advisories/{crate_name}.json"
            response = requests.get(advisories_url)
            if response.ok:
                advisories = response.json()
                security_data["advisories"] = advisories
                security_data["vulnerability_count"] = len(advisories)
        except Exception:
            pass
        
        # Check for common security patterns in code
        try:
            # This would analyze the source code for unsafe blocks, etc.
            # Placeholder for now
            security_data["unsafe_blocks"] = 0
            security_data["security_patterns"] = []
        except Exception:
            pass
        
        return security_data

class UserBehaviorAnalyzer:
    @staticmethod
    def fetch_user_behavior_data(crate: EnrichedCrate) -> Dict:
        """Fetch user behavior data from GitHub and crates.io"""
        result = {
            "issues": [],
            "pull_requests": [],
            "version_adoption": {},
            "community_metrics": {}
        }
        
        crate_name = crate.name
        repo_url = crate.repository
        
        # Extract owner/repo from URL
        if not repo_url or "github.com" not in repo_url:
            return result
            
        parts = repo_url.rstrip('/').split('/')
        if len(parts) < 2:
            return result
        owner, repo = parts[-2], parts[-1]
        
        # Setup GitHub API access - use token if available
        headers = {"Accept": "application/vnd.github.v3+json"}
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"
        
        # Fetch recent issues and PRs
        try:
            # Get issues (last 30)
            issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=30"
            issues_resp = requests.get(issues_url, headers=headers)
            if issues_resp.ok:
                issues_data = issues_resp.json()
                
                # Process issue data
                for issue in issues_data:
                    if "pull_request" in issue:
                        # This is a PR, not an issue
                        result["pull_requests"].append({
                            "number": issue["number"],
                            "title": issue["title"],
                            "state": issue["state"],
                            "created_at": issue["created_at"],
                            "closed_at": issue["closed_at"],
                            "url": issue["html_url"]
                        })
                    else:
                        # Regular issue
                        result["issues"].append({
                            "number": issue["number"],
                            "title": issue["title"],
                            "state": issue["state"],
                            "created_at": issue["created_at"],
                            "closed_at": issue["closed_at"],
                            "url": issue["html_url"]
                        })
            
            # Fetch commit activity for the past year
            commits_url = f"https://api.github.com/repos/{owner}/{repo}/stats/commit_activity"
            commits_resp = requests.get(commits_url, headers=headers)
            if commits_resp.ok:
                result["community_metrics"]["commit_activity"] = commits_resp.json()
            
            # Rate limiting - be nice to GitHub API
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching GitHub data: {str(e)}")
        
        # Get version adoption data from crates.io
        try:
            versions_url = f"https://crates.io/api/v1/crates/{crate_name}/versions"
            versions_resp = requests.get(versions_url)
            if versions_resp.ok:
                versions_data = versions_resp.json()
                versions = versions_data.get("versions", [])
                
                # Process version data
                for version in versions[:10]:  # Top 10 versions
                    version_num = version["num"]
                    downloads = version["downloads"]
                    created_at = version["created_at"]
                    
                    result["version_adoption"][version_num] = {
                        "downloads": downloads,
                        "created_at": created_at
                    }
        except Exception as e:
            print(f"Error fetching crates.io version data: {str(e)}")
        
        return result

class DependencyAnalyzer:
    @staticmethod
    def analyze_dependencies(crates: List[EnrichedCrate]) -> Dict:
        """Analyze dependencies between crates"""
        dependency_graph = {}
        crate_names = {crate.name for crate in crates}
        
        for crate in crates:
            deps = []
            for dep in crate.dependencies:
                if dep.get("crate_id") in crate_names:
                    deps.append(dep.get("crate_id"))
            dependency_graph[crate.name] = deps
        
        # Find most depended-upon crates
        reverse_deps = {}
        for crate_name, deps in dependency_graph.items():
            for dep in deps:
                if dep not in reverse_deps:
                    reverse_deps[dep] = []
                reverse_deps[dep].append(crate_name)
        
        return {
            "dependency_graph": dependency_graph,
            "reverse_dependencies": reverse_deps,
            "most_depended": sorted(reverse_deps.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        }
