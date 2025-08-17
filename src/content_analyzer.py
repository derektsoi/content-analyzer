#!/usr/bin/env python3
"""
Content Analyzer - Core text analysis functionality
Features: word count, readability analysis, keyword extraction
"""

import re
from collections import Counter
from typing import Dict, List, Tuple


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