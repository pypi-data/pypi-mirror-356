# ai_processing.py
import re
import time
import logging
import tiktoken
from typing import Callable, Optional
from llama_cpp import Llama
from .config import PipelineConfig, CrateMetadata, EnrichedCrate

class LLMEnricher:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.model = self._load_model()
        
    def _load_model(self):
        return Llama(
            model_path=self.config.model_path,
            n_ctx=1024,
            n_batch=512,
            n_gpu_layers=32
        )

    def estimate_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def truncate_content(self, content: str, max_tokens: int = 1000) -> str:
        """Truncate content to fit within token limit"""
        paragraphs = content.split("\n\n")
        result, current_tokens = "", 0
        
        for para in paragraphs:
            tokens = len(self.tokenizer.encode(para))
            if current_tokens + tokens <= max_tokens:
                result += para + "\n\n"
                current_tokens += tokens
            else:
                break
        return result.strip()

    def smart_truncate(self, content: str, max_tokens: int = 1000) -> str:
        """Intelligently truncate content to preserve the most important parts"""
        if not content:
            return ""
            
        # If content is short enough, return it all
        if len(self.tokenizer.encode(content)) <= max_tokens:
            return content
            
        # Split into sections based on markdown headers
        sections = []
        current_section = {"heading": "Introduction", "content": "", "priority": 10}
        
        for line in content.splitlines():
            if re.match(r'^#+\s+', line):  # It's a header
                # Save previous section if not empty
                if current_section["content"].strip():
                    sections.append(current_section)
                    
                # Create new section with appropriate priority
                heading = re.sub(r'^#+\s+', '', line)
                priority = 5  # Default priority
                
                # Assign priority based on content type
                if re.search(r'\b(usage|example|getting started)\b', heading, re.I):
                    priority = 10
                elif re.search(r'\b(feature|overview|about)\b', heading, re.I):
                    priority = 9
                elif re.search(r'\b(install|setup|config)\b', heading, re.I):
                    priority = 8
                elif re.search(r'\b(api|interface)\b', heading, re.I):
                    priority = 7
                    
                current_section = {"heading": heading, "content": line + "\n", "priority": priority}
            else:
                current_section["content"] += line + "\n"
                
                # Boost priority if code block is found
                if "```rust" in line or "```no_run" in line:
                    current_section["priority"] = max(current_section["priority"], 8)
        
        # Add the last section
        if current_section["content"].strip():
            sections.append(current_section)
        
        # Sort sections by priority (highest first)
        sections.sort(key=lambda x: x["priority"], reverse=True)
        
        # Build the result, respecting token limits
        result = ""
        tokens_used = 0
        
        for section in sections:
            section_text = f"## {section['heading']}\n{section['content']}\n"
            section_tokens = len(self.tokenizer.encode(section_text))
            
            if tokens_used + section_tokens <= max_tokens:
                result += section_text
                tokens_used += section_tokens
            elif tokens_used < max_tokens - 100:  # If we can fit a truncated version
                # Take what we can
                remaining_tokens = max_tokens - tokens_used
                truncated_text = self.tokenizer.decode(self.tokenizer.encode(section_text)[:remaining_tokens])
                result += truncated_text
                break
        
        return result

    def clean_output(self, output: str, task: str = "general") -> str:
        """Task-specific output cleaning"""
        if not output:
            return ""
        
        # Remove any remaining prompt artifacts
        output = output.split("<|end|>")[0].strip()
        
        if task == "classification":
            # For classification tasks, extract just the category
            categories = ["AI", "Database", "Web Framework", "Networking", "Serialization", 
                         "Utilities", "DevTools", "ML", "Cryptography", "Unknown"]
            for category in categories:
                if re.search(r'\b' + re.escape(category) + r'\b', output, re.IGNORECASE):
                    return category
            return "Unknown"
        
        elif task == "factual_pairs":
            # For factual pairs, ensure proper formatting
            pairs = []
            facts = re.findall(r'✅\s*Factual:?\s*(.*?)(?=❌|\Z)', output, re.DOTALL)
            counterfacts = re.findall(r'❌\s*Counterfactual:?\s*(.*?)(?=✅|\Z)', output, re.DOTALL)
            
            # Pair them up
            for i in range(min(len(facts), len(counterfacts))):
                pairs.append(f"✅ Factual: {facts[i].strip()}\n❌ Counterfactual: {counterfacts[i].strip()}")
            
            return "\n\n".join(pairs)
        
        else:
            # General cleaning - more permissive than before
            lines = [line.strip() for line in output.splitlines() if line.strip()]
            return "\n".join(lines)

    def run_llama(self, prompt: str, temp: float = 0.2, max_tokens: int = 256) -> Optional[str]:
        """Run the LLM with customizable parameters per task"""
        try:
            token_count = self.estimate_tokens(prompt)
            if token_count > self.config.prompt_token_margin:
                logging.warning(f"Prompt too long ({token_count} tokens). Truncating.")
                prompt = self.truncate_content(prompt, self.config.prompt_token_margin - 100)
            
            output = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=temp,
                stop=["<|end|>", "<|user|>", "<|system|>"]  # Stop at these tokens
            )
            
            raw_text = output["choices"][0]["text"]
            return self.clean_output(raw_text)
        except Exception as e:
            logging.error(f"Model inference failed: {str(e)}")
            raise

    def validate_and_retry(
        self,
        prompt: str,
        validation_func: Callable[[str], bool],
        temp: float = 0.2,
        max_tokens: int = 256,
        retries: int = 3
    ) -> Optional[str]:
        """Run LLM with validation and automatic retry on failure"""
        for attempt in range(retries):
            try:
                # Adjust temperature slightly upward on retries to get different results
                adjusted_temp = temp * (1 + (attempt * 0.1))
                result = self.run_llama(prompt, temp=adjusted_temp, max_tokens=max_tokens)
                
                # Validate the result
                if result and validation_func(result):
                    return result
                
                # If we get here, validation failed
                logging.warning(f"Validation failed on attempt {attempt+1}/{retries}. Retrying with modified parameters.")
                
                # For the last attempt, simplify the prompt
                if attempt == retries - 2:
                    prompt = self.simplify_prompt(prompt)
                    
            except Exception as e:
                logging.error(f"Generation error on attempt {attempt+1}: {str(e)}")
            
            # Backoff before retry
            time.sleep(1.5 * (2 ** attempt))
        
        # If we exhaust all retries, return None
        return None

    def simplify_prompt(self, prompt: str) -> str:
        """Simplify a prompt by removing examples and reducing context"""
        # Remove few-shot examples
        prompt = re.sub(r'# Example [0-9].*?(?=# Crate to Classify|\Z)', '', prompt, flags=re.DOTALL)
        
        # Make instructions more direct
        prompt = re.sub(r'<\|system\|>.*?<\|user\|>', '<|system|>Be concise.\n<|user|>', prompt, flags=re.DOTALL)
        
        return prompt

    def validate_classification(self, result: str) -> bool:
        """Ensure a valid category was returned"""
        if not result:
            return False
        valid_categories = ["AI", "Database", "Web Framework", "Networking", "Serialization", 
                          "Utilities", "DevTools", "ML", "Cryptography", "Unknown"]
        return any(category.lower() == result.strip().lower() for category in valid_categories)

    def validate_factual_pairs(self, result: str) -> bool:
        """Ensure exactly 5 factual/counterfactual pairs exist"""
        if not result:
            return False
            
        facts = re.findall(r'✅\s*Factual:?\s*(.*?)(?=❌|\Z)', result, re.DOTALL)
        counterfacts = re.findall(r'❌\s*Counterfactual:?\s*(.*?)(?=✅|\Z)', result, re.DOTALL)
        
        return len(facts) >= 3 and len(counterfacts) >= 3  # At least 3 pairs

    def enrich_crate(self, crate: CrateMetadata) -> EnrichedCrate:
        """Apply all AI enrichments to a crate"""
        # Convert CrateMetadata to EnrichedCrate
        enriched_dict = crate.__dict__.copy()
        enriched = EnrichedCrate(**enriched_dict)
        
        try:
            # Generate README summary first
            if crate.readme:
                readme_content = self.smart_truncate(crate.readme, 2000)
                prompt = (
                    f"<|system|>Extract key features from README.\n"
                    f"<|user|>Summarize key aspects of this Rust crate from its README:\n{readme_content}\n"
                    f"<|end|>"
                )
                enriched.readme_summary = self.validate_and_retry(
                    prompt, 
                    lambda x: len(x) > 50, 
                    temp=0.3, 
                    max_tokens=300
                )
            
            # Extract key dependencies for context
            key_deps = [dep.get("crate_id") for dep in crate.dependencies[:5] if dep.get("kind") == "normal"]
            
            # Generate other enrichments
            enriched.feature_summary = self.summarize_features(crate)
            enriched.use_case = self.classify_use_case(
                crate, 
                enriched.readme_summary or ""
            )
            enriched.score = self.score_crate(crate)
            enriched.factual_counterfactual = self.generate_factual_pairs(crate)
            
            return enriched
        except Exception as e:
            logging.error(f"Failed to enrich {crate.name}: {str(e)}")
            return enriched

    def summarize_features(self, crate: CrateMetadata) -> str:
        """Generate summaries for crate features with better prompting"""
        try:
            if not crate.features:
                return "No features documented for this crate."
            
            # Format features with their dependencies
            feature_text = ""
            for f in crate.features[:8]:  # Limit to 8 features for context size
                feature_name = f.get("name", "")
                deps = f.get("dependencies", [])
                deps_str = ", ".join(deps) if deps else "none"
                feature_text += f"- {feature_name} (dependencies: {deps_str})\n"
            
            prompt = (
                f"<|system|>You are a Rust programming expert analyzing crate features.\n"
                f"<|user|>For the Rust crate `{crate.name}`, explain these features and what functionality they provide:\n\n"
                f"{feature_text}\n\n"
                f"Provide a concise explanation of each feature's purpose and when a developer would enable it.\n"
                f"<|end|>"
            )
            
            # Use moderate temperature for informative but natural explanation
            result = self.run_llama(prompt, temp=0.2, max_tokens=350)
            return result or "Feature summary not available."
        except Exception as e:
            logging.warning(f"Feature summarization failed for {crate.name}: {str(e)}")
            return "Feature summary not available."

    def classify_use_case(self, crate: CrateMetadata, readme_summary: str) -> str:
        """Classify the use case of a crate with rich context"""
        try:
            # Calculate available tokens for prompt (classification usually needs ~20 response tokens)
            available_prompt_tokens = self.config.model_token_limit - 200  # Reserve for response
            
            joined = ", ".join(crate.keywords[:10]) if crate.keywords else "None"
            key_deps = [dep.get("crate_id") for dep in crate.dependencies[:5] if dep.get("kind") == "normal"]
            key_deps_str = ", ".join(key_deps) if key_deps else "None"
            
            # Adaptively truncate different sections based on importance
            token_budget = available_prompt_tokens - 400  # Reserve tokens for prompt template
            
            # Allocate different percentages to each section
            desc_tokens = int(token_budget * 0.2)
            readme_tokens = int(token_budget * 0.6)
            
            desc = self.truncate_content(crate.description, desc_tokens)
            readme_summary = self.smart_truncate(readme_summary, readme_tokens)
            
            # Few-shot prompting with examples
            prompt = (
                f"<|system|>You are a Rust expert classifying crates into the most appropriate category.\n"
                f"<|user|>\n"
                f"# Example 1\n"
                f"Crate: `tokio`\n"
                f"Description: An asynchronous runtime for the Rust programming language\n"
                f"Keywords: async, runtime, futures\n"
                f"Key Dependencies: mio, bytes, parking_lot\n"
                f"Category: Networking\n\n"
                
                f"# Example 2\n"
                f"Crate: `serde`\n"
                f"Description: A generic serialization/deserialization framework\n"
                f"Keywords: serde, serialization\n"
                f"Key Dependencies: serde_derive\n"
                f"Category: Serialization\n\n"
                
                f"# Crate to Classify\n"
                f"Crate: `{crate.name}`\n"
                f"Description: {desc}\n"
                f"Keywords: {joined}\n"
                f"README Summary: {readme_summary}\n"
                f"Key Dependencies: {key_deps_str}\n\n"
                f"Category (pick only one): [AI, Database, Web Framework, Networking, Serialization, Utilities, DevTools, ML, Cryptography, Unknown]\n"
                f"<|end|>"
            )
            
            # Validate classification with retry
            result = self.validate_and_retry(
                prompt, 
                validation_func=self.validate_classification,
                temp=0.1, 
                max_tokens=20
            )
            
            return result or "Unknown"
        except Exception as e:
            logging.error(f"Classification failed for {crate.name}: {str(e)}")
            return "Unknown"

    def generate_factual_pairs(self, crate: CrateMetadata) -> str:
        """Generate factual/counterfactual pairs with retry and validation"""
        try:
            desc = self.truncate_content(crate.description, 300)
            readme_summary = self.truncate_content(getattr(crate, 'readme_summary', '') or '', 300)
            
            prompt = (
                f"<|system|>Create exactly 5 factual/counterfactual pairs for the Rust crate. "
                f"Factual statements must be true. Counterfactuals should be plausible but incorrect - "
                f"make them subtle and convincing rather than simple negations.\n"
                f"<|user|>\n"
                f"Crate: {crate.name}\n"
                f"Description: {desc}\n"
                f"Repo: {crate.repository}\n"
                f"README Summary: {readme_summary}\n"
                f"Key Features: {', '.join([f.get('name', '') for f in crate.features[:5]])}\n\n"
                f"Format each pair as:\n"
                f"✅ Factual: [true statement about the crate]\n"
                f"❌ Counterfactual: [plausible but false statement]\n\n"
                f"Create exactly 5 pairs.\n"
                f"<|end|>"
            )
            
            # Use validation for retry
            result = self.validate_and_retry(
                prompt, 
                validation_func=self.validate_factual_pairs, 
                temp=0.6, 
                max_tokens=500
            )
            
            return result or "Factual pairs generation failed."
        except Exception as e:
            logging.error(f"Exception in factual_pairs for {crate.name}: {str(e)}")
            return "Factual pairs generation failed."

    def score_crate(self, crate: CrateMetadata) -> float:
        """Calculate a score for the crate based on various metrics"""
        score = (crate.downloads / 1000) + (crate.github_stars * 10)
        score += len(self.truncate_content(crate.readme, 1000)) / 500
        return round(score, 2)
