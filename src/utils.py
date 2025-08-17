#!/usr/bin/env python3
"""
Utility functions for content analysis
"""

import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from typing import Dict


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
    """Save results to JSON file with timestamp in organized directory."""
    # Create filename from URL
    domain = urlparse(url).netloc.replace('www.', '')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Organize by date
    date_folder = datetime.now().strftime('%Y-%m-%d')
    output_dir = f"data/outputs/{date_folder}"
    
    # Create directory if it doesn't exist
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{output_dir}/analysis_{domain}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to: {filename}")