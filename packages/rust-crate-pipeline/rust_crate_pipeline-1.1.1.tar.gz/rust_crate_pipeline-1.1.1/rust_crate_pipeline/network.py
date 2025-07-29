# network.py
import os
import re
import time
import logging
import requests
from requests_cache import CachedSession
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from .config import PipelineConfig

class GitHubBatchClient:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if config.github_token:
            self.headers["Authorization"] = f"token {config.github_token}"
        
        self.session = CachedSession(
            'github_cache', 
            expire_after=config.cache_ttl * 2  # Longer cache for GitHub
        )
        self.remaining_calls = 5000
        self.reset_time = 0

    def check_rate_limit(self):
        """Check and update current rate limit status"""
        try:
            response = self.session.get("https://api.github.com/rate_limit", headers=self.headers)
            if response.ok:
                data = response.json()
                self.remaining_calls = data["resources"]["core"]["remaining"]
                self.reset_time = data["resources"]["core"]["reset"]
                
                if self.remaining_calls < 100:
                    reset_in = self.reset_time - time.time()
                    logging.warning(f"GitHub API rate limit low: {self.remaining_calls} remaining. Resets in {reset_in/60:.1f} minutes")
        except Exception:
            pass

    def get_repo_stats(self, owner: str, repo: str) -> Dict:
        """Get repository statistics"""
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}"
            response = self.session.get(url, headers=self.headers)
            if response.ok:
                return response.json()
            else:
                logging.warning(f"Failed to get repo stats for {owner}/{repo}: {response.status_code}")
                return {}
        except Exception as e:
            logging.error(f"Error fetching repo stats: {str(e)}")
            return {}

    def batch_get_repo_stats(self, repo_list: List[str]) -> Dict[str, Dict]:
        """Get statistics for multiple repositories in a batch"""
        self.check_rate_limit()
        
        results = {}
        for repo_url in repo_list:
            # Extract owner/repo from URL
            match = re.search(r"github\.com/([^/]+)/([^/\.]+)", repo_url)
            if not match:
                continue
                
            owner, repo = match.groups()
            repo = repo.split('.')[0]  # Remove .git extension if present
            
            # Get stats
            stats = self.get_repo_stats(owner, repo)
            results[repo_url] = stats
            
            # Be nice to GitHub API
            time.sleep(0.1)
        
        return results

class CrateAPIClient:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.session = CachedSession('crate_cache', expire_after=config.cache_ttl)
        
    def fetch_crate_metadata(self, crate_name: str) -> Optional[Dict]:
        """Fetch metadata with retry logic"""
        for attempt in range(self.config.max_retries):
            try:
                return self._fetch_metadata(crate_name)
            except Exception as e:
                logging.warning(f"Attempt {attempt+1} failed for {crate_name}: {str(e)}")
                wait = 2 ** attempt
                time.sleep(wait)
        return None

    def _fetch_metadata(self, crate_name: str) -> Optional[Dict]:
        """Enhanced metadata fetching that tries multiple sources"""
        # First try crates.io (primary source)
        try:
            r = self.session.get(f"https://crates.io/api/v1/crates/{crate_name}")
            if r.ok:
                data = r.json()
                crate_data = data["crate"]
                latest = crate_data["newest_version"]
                
                # Get readme
                readme_response = self.session.get(f"https://crates.io/api/v1/crates/{crate_name}/readme")
                readme = readme_response.text if readme_response.ok else ""
                
                # Get dependencies
                deps_response = self.session.get(f"https://crates.io/api/v1/crates/{crate_name}/{latest}/dependencies")
                deps = deps_response.json().get("dependencies", []) if deps_response.ok else []
                
                # Get features - using the versions endpoint
                features = []
                versions_response = self.session.get(f"https://crates.io/api/v1/crates/{crate_name}/{latest}")
                if versions_response.ok:
                    version_data = versions_response.json().get("version", {})
                    features_dict = version_data.get("features", {})
                    features = [{"name": k, "dependencies": v} for k, v in features_dict.items()]
                
                # Repository info and GitHub stars
                repo = crate_data.get("repository", "")
                gh_stars = 0
                
                # Check if it's a GitHub repo
                if "github.com" in repo and self.config.github_token:
                    match = re.search(r"github.com/([^/]+)/([^/]+)", repo)
                    if match:
                        owner, repo_name = match.groups()
                        repo_name = repo_name.split('.')[0]  # Handle .git extensions
                        gh_url = f"https://api.github.com/repos/{owner}/{repo_name}"
                        gh_headers = {"Authorization": f"token {self.config.github_token}"} if self.config.github_token else {}
                        gh = self.session.get(gh_url, headers=gh_headers)
                        if gh.ok:
                            gh_data = gh.json()
                            gh_stars = gh_data.get("stargazers_count", 0)
                
                # Check if it's hosted on lib.rs
                lib_rs_data = {}
                if "lib.rs" in repo:
                    lib_rs_url = f"https://lib.rs/crates/{crate_name}"
                    lib_rs_response = self.session.get(lib_rs_url)
                    if lib_rs_response.ok:
                        soup = BeautifulSoup(lib_rs_response.text, 'html.parser')
                        # Get README from lib.rs if not already available
                        if not readme:
                            readme_div = soup.find('div', class_='readme')
                            if readme_div:
                                readme = readme_div.get_text(strip=True)
                        
                        # Get lib.rs specific stats
                        stats_div = soup.find('div', class_='crate-stats')
                        if stats_div:
                            downloads_text = stats_div.find(string=re.compile(r'[\d,]+ downloads'))
                            if downloads_text:
                                lib_rs_data["librs_downloads"] = int(re.sub(r'[^\d]', '', downloads_text))
                
                # Extract code snippets from readme
                code_snippets = self.extract_code_snippets(readme)
                
                # Extract sections from readme
                readme_sections = self.extract_readme_sections(readme) if readme else {}
                
                result = {
                    "name": crate_name,
                    "version": latest,
                    "description": crate_data.get("description", ""),
                    "repository": repo,
                    "keywords": crate_data.get("keywords", []),
                    "categories": crate_data.get("categories", []),
                    "readme": readme,
                    "downloads": crate_data.get("downloads", 0),
                    "github_stars": gh_stars,
                    "dependencies": deps,
                    "code_snippets": code_snippets,
                    "features": features,
                    "readme_sections": readme_sections,
                    **lib_rs_data
                }
                
                return result
                
        except Exception as e:
            logging.error(f"Failed fetching metadata for {crate_name}: {str(e)}")
            raise
        
        # If crates.io fails, try lib.rs
        try:
            r = self.session.get(f"https://lib.rs/crates/{crate_name}")
            if r.ok:
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Extract metadata from lib.rs page
                name = soup.select_one('h1').text.strip() if soup.select_one('h1') else crate_name
                
                # Find description
                desc_elem = soup.select_one('.description')
                description = desc_elem.text.strip() if desc_elem else ""
                
                # Find repository link
                repo_link = None
                for a in soup.select('a'):
                    if 'github.com' in a.get('href', ''):
                        repo_link = a['href']
                        break
                
                # Basic metadata from lib.rs
                return {
                    "name": name,
                    "version": "latest",  # lib.rs doesn't easily expose version
                    "description": description,
                    "repository": repo_link or "",
                    "keywords": [],
                    "categories": [],
                    "readme": "",
                    "downloads": 0,
                    "github_stars": 0,
                    "dependencies": [],
                    "code_snippets": [],
                    "features": [],
                    "readme_sections": {},
                    "source": "lib.rs",
                }
        except Exception:
            pass
        
        # Finally, try GitHub search
        try:
            # This is a simplification - GitHub's search API requires authentication
            headers = {}
            if self.config.github_token:
                headers["Authorization"] = f"token {self.config.github_token}"
                
            search_url = f"https://api.github.com/search/repositories?q={crate_name}+language:rust"
            r = requests.get(search_url, headers=headers)
            
            if r.ok:
                results = r.json().get("items", [])
                if results:
                    repo = results[0]  # Take first match
                    
                    # Basic metadata from GitHub
                    return {
                        "name": crate_name,
                        "version": "unknown",
                        "description": repo.get("description", ""),
                        "repository": repo.get("html_url", ""),
                        "keywords": [],
                        "categories": [],
                        "readme": "",
                        "downloads": 0,
                        "github_stars": repo.get("stargazers_count", 0),
                        "dependencies": [],
                        "code_snippets": [],
                        "features": [],
                        "readme_sections": {},
                        "source": "github",
                    }
        except Exception:
            pass
        
        # If all sources fail
        return None

    def extract_code_snippets(self, readme: str) -> List[str]:
        """Extract code snippets from markdown README"""
        snippets = []
        if not readme:
            return snippets
            
        # Find Rust code blocks
        pattern = r"```(?:rust|(?:no_run|ignore|compile_fail|mdbook-runnable)?)\s*([\s\S]*?)```"
        matches = re.findall(pattern, readme)
        
        for code in matches:
            if len(code.strip()) > 10:  # Only include non-trivial snippets
                snippets.append(code.strip())
        
        return snippets[:5]  # Limit to 5 snippets

    def extract_readme_sections(self, readme: str) -> Dict[str, str]:
        """Extract sections from README based on markdown headers"""
        if not readme:
            return {}
            
        sections = {}
        lines = readme.split('\n')
        current_section = ""
        current_content = []
        
        for line in lines:
            if re.match(r'^#+\s+', line):  # It's a header
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = re.sub(r'^#+\s+', '', line).strip()
                current_content = []
            else:
                if current_section:  # Only collect content if we have a section
                    current_content.append(line)
        
        # Don't forget the last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
