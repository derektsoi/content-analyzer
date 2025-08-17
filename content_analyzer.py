#!/usr/bin/env python3
"""
Content Analyzer - A tool for analyzing text content
Features: word count, readability analysis, keyword extraction
"""

import re
import sys
import time
import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from collections import Counter
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse
from dotenv import load_dotenv
import openai


class ContentAnalyzer:
    def __init__(self, text: str):
        self.text = text
        self.sentences = self._split_sentences()
        self.words = self._extract_words()
    
    def _split_sentences(self) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+', self.text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_words(self) -> List[str]:
        """Extract words from text, removing punctuation."""
        words = re.findall(r'\b[a-zA-Z]+\b', self.text.lower())
        return words
    
    def word_count(self) -> Dict[str, int]:
        """Calculate basic word statistics."""
        return {
            'total_words': len(self.words),
            'unique_words': len(set(self.words)),
            'sentences': len(self.sentences),
            'characters': len(self.text),
            'characters_no_spaces': len(self.text.replace(' ', ''))
        }
    
    def readability_score(self) -> Dict[str, float]:
        """Calculate readability metrics using Flesch Reading Ease."""
        if not self.sentences or not self.words:
            return {'flesch_reading_ease': 0, 'grade_level': 'N/A'}
        
        avg_sentence_length = len(self.words) / len(self.sentences)
        syllable_count = sum(self._count_syllables(word) for word in self.words)
        avg_syllables_per_word = syllable_count / len(self.words)
        
        # Flesch Reading Ease Score
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, flesch_score))  # Clamp between 0-100
        
        # Grade level interpretation
        if flesch_score >= 90:
            grade_level = "5th grade"
        elif flesch_score >= 80:
            grade_level = "6th grade"
        elif flesch_score >= 70:
            grade_level = "7th grade"
        elif flesch_score >= 60:
            grade_level = "8th-9th grade"
        elif flesch_score >= 50:
            grade_level = "10th-12th grade"
        elif flesch_score >= 30:
            grade_level = "College level"
        else:
            grade_level = "Graduate level"
        
        return {
            'flesch_reading_ease': round(flesch_score, 2),
            'grade_level': grade_level,
            'avg_sentence_length': round(avg_sentence_length, 2),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2)
        }
    
    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count for a word."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)  # Every word has at least 1 syllable
    
    def keyword_extraction(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Extract most frequent keywords, excluding common stop words."""
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        # Filter out stop words and short words
        filtered_words = [word for word in self.words 
                         if word not in stop_words and len(word) > 2]
        
        word_freq = Counter(filtered_words)
        return word_freq.most_common(top_n)
    
    def analyze_all(self) -> Dict:
        """Perform complete content analysis."""
        return {
            'word_count': self.word_count(),
            'readability': self.readability_score(),
            'keywords': self.keyword_extraction()
        }


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
    
    def generate_tags(self, content: str, url: str = "", title: str = "") -> Dict:
        """Generate tags for content using OpenAI API with zero-shot prompting."""
        
        system_prompt = """You are an expert content analyst for a cross-border e-commerce company specializing in global shopping and shipping services. 

Analyze blog content and extract relevant tags in these categories:
1. **Brands**: Specific brand names mentioned (e.g., Lululemon, Amazon, Nike)
2. **Product Categories**: Product types and categories (e.g., Activewear, Electronics, Books)  
3. **Source Regions**: Countries/regions where products originate or can be purchased (e.g., UK, US, Japan, Canada)
4. **Shopping Intent**: Shopping-related themes and purposes (e.g., Price-comparison, How-to-buy, Cross-border-shipping)

Instructions:
- Extract maximum 5 tags per category
- Assign confidence scores from 0.0 to 1.0 based on relevance and clarity
- Only include tags with confidence ≥ 0.3
- Focus on e-commerce and cross-border shopping context
- Use consistent, SEO-friendly tag formats (capitalize properly)

Respond with ONLY valid JSON in this exact format:
{
  "brands": [{"tag": "Brand Name", "confidence": 0.95}],
  "product_categories": [{"tag": "Category Name", "confidence": 0.90}],
  "source_regions": [{"tag": "Country/Region", "confidence": 0.85}],
  "shopping_intent": [{"tag": "Shopping Theme", "confidence": 0.80}]
}"""

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
        print("Generating tags with Claude API...")
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


def fetch_url_content(url: str) -> str:
    """
    Fetch and extract text content from a URL using professional scraping practices.
    
    Professional practices implemented:
    1. User-Agent header to identify as a legitimate client
    2. Timeout to prevent hanging requests
    3. Proper error handling for various HTTP issues
    4. Rate limiting with delay
    5. Content-type checking
    6. Text extraction from HTML while preserving structure
    """
    
    # Professional Practice #1: Always set a proper User-Agent
    # This identifies your scraper and is more respectful to servers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Content-Analyzer/1.0) AppleWebKit/537.36'
    }
    
    try:
        # Professional Practice #2: Set timeouts to prevent hanging
        # 10 seconds connection timeout, 30 seconds read timeout
        response = requests.get(url, headers=headers, timeout=(10, 30))
        
        # Professional Practice #3: Check status code
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        
        # Professional Practice #4: Check content type
        content_type = response.headers.get('content-type', '').lower()
        if 'text/html' not in content_type:
            raise ValueError(f"URL does not contain HTML content. Content-Type: {content_type}")
        
        # Professional Practice #5: Handle encoding properly
        response.encoding = response.apparent_encoding or 'utf-8'
        
        # Professional Practice #6: Parse HTML robustly with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Professional Practice #7: Remove unwanted elements
        # Remove script, style, and navigation elements that don't contain main content
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Professional Practice #8: Extract meaningful text
        # Get text while preserving paragraph structure
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        if not text:
            raise ValueError("No readable text content found in the webpage")
        
        return text
        
    except requests.exceptions.Timeout:
        raise Exception("Request timed out. The website may be slow or unresponsive.")
    except requests.exceptions.ConnectionError:
        raise Exception("Failed to connect to the website. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except Exception as e:
        raise Exception(f"Error processing webpage: {e}")


def is_url(string: str) -> bool:
    """Check if a string is a valid URL."""
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False


def display_results(results: Dict):
    """Display analysis results in console format."""
    print("=== Content Analysis Results ===\n")
    
    if 'content_analysis' in results:
        content_stats = results['content_analysis']
        print("Word Count Statistics:")
        for key, value in content_stats['word_count'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print("\nReadability Analysis:")
        for key, value in content_stats['readability'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print("\nTop Keywords:")
        for i, (word, count) in enumerate(content_stats['keywords'], 1):
            print(f"  {i}. {word} ({count} occurrences)")
    
    if 'auto_tags' in results:
        print("\n=== Auto-Generated Tags ===\n")
        tags = results['auto_tags']
        
        for category, tag_list in tags.items():
            if tag_list:  # Only show categories with tags
                print(f"{category.replace('_', ' ').title()}:")
                for tag_data in tag_list:
                    tag_name = tag_data['tag']
                    confidence = tag_data['confidence']
                    print(f"  • {tag_name} (confidence: {confidence:.2f})")
                print()


def save_results_json(results: Dict, url: str):
    """Save results to JSON file with timestamp."""
    # Create filename from URL
    domain = urlparse(url).netloc.replace('www.', '')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"analysis_{domain}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to: {filename}")


def main():
    """Main function with auto-tagging support."""
    # Check for auto-tagging mode
    if len(sys.argv) > 1 and sys.argv[1] == '--auto-tag':
        if len(sys.argv) < 3:
            print("Usage: python content_analyzer.py --auto-tag <url>")
            print("   or: python content_analyzer.py <file_path_or_url> (basic analysis)")
            return
        
        url = sys.argv[2]
        if not is_url(url):
            print("Error: Auto-tagging requires a valid URL")
            return
        
        try:
            # Initialize auto-tagger
            tagger = AutoTagger()
            
            # Analyze URL with auto-tagging
            results = tagger.analyze_url(url)
            
            # Display results
            display_results(results)
            
            # Save to JSON
            save_results_json(results, url)
            
        except Exception as e:
            print(f"Error in auto-tagging: {e}")
            return
    
    elif len(sys.argv) > 1:
        input_source = sys.argv[1]
        
        # Check if input is a URL
        if is_url(input_source):
            print(f"Fetching content from URL: {input_source}")
            print("Note: Use --auto-tag flag for AI-powered tagging")
            
            # Professional Practice #9: Rate limiting - be respectful to servers
            print("Please wait, fetching content...")
            time.sleep(1)  # Small delay to be respectful
            
            try:
                text = fetch_url_content(input_source)
                print(f"Successfully extracted {len(text)} characters from the webpage.\n")
            except Exception as e:
                print(f"Error fetching URL: {e}")
                return
        else:
            # Try to read as a file
            try:
                with open(input_source, 'r', encoding='utf-8') as file:
                    text = file.read()
                print(f"Analyzing content from file: {input_source}\n")
            except FileNotFoundError:
                print(f"Error: File '{input_source}' not found.")
                print("Usage: python content_analyzer.py <file_path_or_url>")
                print("   or: python content_analyzer.py --auto-tag <url>")
                return
            except Exception as e:
                print(f"Error reading file: {e}")
                return
        
        # Basic content analysis
        analyzer = ContentAnalyzer(text)
        results = {'content_analysis': analyzer.analyze_all()}
        display_results(results)
    
    else:
        # Usage information
        print("Content Analyzer with Auto-Tagging")
        print("Usage:")
        print("  python content_analyzer.py --auto-tag <url>     # AI-powered tagging")
        print("  python content_analyzer.py <file_or_url>        # Basic analysis")
        print("  python content_analyzer.py                      # Demo mode")
        print()
        
        # Use sample text for demonstration
        print("No input provided. Using sample text for demonstration.\n")
        text = """
        The quick brown fox jumps over the lazy dog. This is a sample text for 
        demonstrating the content analyzer. It includes multiple sentences with 
        varying complexity. The analyzer can calculate word counts, readability 
        scores, and extract keywords from any given text. This tool is useful 
        for writers, editors, and content creators who want to understand the 
        characteristics of their text.
        """
        
        analyzer = ContentAnalyzer(text)
        results = {'content_analysis': analyzer.analyze_all()}
        display_results(results)


if __name__ == "__main__":
    main()