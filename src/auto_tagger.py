#!/usr/bin/env python3
"""
Auto-tagging system for e-commerce blog content using OpenAI API
"""

import os
import json
from datetime import datetime
from typing import Dict, Optional
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai

from content_analyzer import ContentAnalyzer
from utils import fetch_url_content


class AutoTagger:
    """Auto-tagging system for e-commerce blog content using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API key from parameter, env var, or .env file."""
        load_dotenv()  # Load .env file if it exists
        
        self.api_key = (
            api_key or 
            os.getenv('OPENAI_API_KEY') or 
            os.getenv('OPENAI_KEY')
        )
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please:\n"
                "1. Create a .env file with: OPENAI_API_KEY=your-key\n"
                "2. Or set environment variable: export OPENAI_API_KEY=your-key\n"
                "3. Or pass api_key parameter to AutoTagger(api_key='your-key')\n"
                "Get your API key from: https://platform.openai.com/api-keys"
            )
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.confidence_threshold = 0.5
        self.max_tags_per_category = 5
    
    def _load_prompt(self, prompt_name: str) -> str:
        """Load prompt from config file."""
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'config', 'prompts', f'{prompt_name}.txt'
        )
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    
    def generate_tags(self, content: str, url: str = "", title: str = "") -> Dict:
        """Generate tags for content using OpenAI API with zero-shot prompting."""
        
        system_prompt = self._load_prompt('region_detection')

        user_prompt = f"""Content to analyze:
URL: {url}
Title: {title}
Content: {content[:3000]}{'...' if len(content) > 3000 else ''}"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective model good for structured tasks
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.3,  # Lower temperature for more consistent tagging
                response_format={"type": "json_object"}  # Force JSON response
            )
            
            # Extract JSON from response
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            tags_data = json.loads(response_text)
            
            # Filter by confidence threshold and limit per category
            filtered_tags = {}
            for category, tags in tags_data.items():
                if isinstance(tags, list):
                    filtered_tags[category] = [
                        tag for tag in tags 
                        if isinstance(tag, dict) and tag.get('confidence', 0) >= self.confidence_threshold
                    ][:self.max_tags_per_category]
                else:
                    filtered_tags[category] = []
            
            return filtered_tags
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse OpenAI response as JSON: {e}")
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {e}")
    
    def analyze_url(self, url: str) -> Dict:
        """Analyze a URL and return both content analysis and auto-tags."""
        print(f"Fetching content from: {url}")
        
        # Get content
        content = fetch_url_content(url)
        
        # Extract title from content (basic approach)
        soup = BeautifulSoup(content, 'html.parser') if '<' in content else None
        title = ""
        if soup:
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else ""
        
        # Generate tags
        print("Generating tags with OpenAI API...")
        tags = self.generate_tags(content, url, title)
        
        # Basic content analysis
        analyzer = ContentAnalyzer(content)
        content_stats = analyzer.analyze_all()
        
        return {
            'url': url,
            'title': title,
            'timestamp': datetime.now().isoformat(),
            'content_analysis': content_stats,
            'auto_tags': tags,
            'content_length': len(content)
        }