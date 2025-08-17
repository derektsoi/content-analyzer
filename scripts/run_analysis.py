#!/usr/bin/env python3
"""
Content Analyzer with Auto-Tagging - Main Entry Point
Features: word count, readability analysis, keyword extraction, AI-powered tagging
"""

import sys
import time
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_analyzer import ContentAnalyzer
from auto_tagger import AutoTagger
from utils import fetch_url_content, is_url, display_results, save_results_json


def main():
    """Main function with auto-tagging support."""
    # Check for auto-tagging mode
    if len(sys.argv) > 1 and sys.argv[1] == '--auto-tag':
        if len(sys.argv) < 3:
            print("Usage: python scripts/run_analysis.py --auto-tag <url>")
            print("   or: python scripts/run_analysis.py <file_path_or_url> (basic analysis)")
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
                print("Usage: python scripts/run_analysis.py <file_path_or_url>")
                print("   or: python scripts/run_analysis.py --auto-tag <url>")
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
        print("  python scripts/run_analysis.py --auto-tag <url>     # AI-powered tagging")
        print("  python scripts/run_analysis.py <file_or_url>        # Basic analysis")
        print("  python scripts/run_analysis.py                      # Demo mode")
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