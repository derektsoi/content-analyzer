# Content Analyzer with Auto-Tagging

A professional content analysis tool for cross-border e-commerce businesses, featuring AI-powered region detection and comprehensive text analysis.

## Features

- **Content Analysis**: Word count, readability scores, keyword extraction
- **AI-Powered Tagging**: Automatic extraction of brands, product categories, source regions, and target markets
- **Cross-Border E-commerce Focus**: Specialized for international shopping and shipping content
- **Professional Structure**: Modular, maintainable, and scalable codebase

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Setup

1. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

2. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

### Usage

**AI-powered analysis** (recommended):
```bash
python scripts/run_analysis.py --auto-tag https://example.com/blog-post
```

**Basic text analysis**:
```bash
python scripts/run_analysis.py https://example.com/blog-post
python scripts/run_analysis.py path/to/textfile.txt
```

**Demo mode**:
```bash
python scripts/run_analysis.py
```

## Project Structure

```
content-analyzer/
├── src/                         # Source code
│   ├── content_analyzer.py      # Core text analysis
│   ├── auto_tagger.py          # AI tagging system
│   └── utils.py                # Helper functions
├── tests/                       # Test data and testing
│   └── ground_truth_regions.json
├── data/                        # Data organization
│   └── outputs/                # Analysis results by date
├── config/                      # Configuration files
│   └── prompts/                # AI prompts
└── scripts/                     # Entry points
    └── run_analysis.py         # Main CLI
```

## AI Tagging Categories

The system extracts tags in these categories:

- **Brands**: Product brand names (Amazon, Lululemon, etc.)
- **Product Categories**: Product types (Electronics, Athleisure, etc.)
- **Product Source Regions**: Where products originate (US, UK, Japan, etc.)
- **Target User Regions**: Intended market (Singapore, Malaysia, etc.)
- **Shopping Intent**: Cross-border shopping themes (Price-comparison, How-to-buy, etc.)

## Chain of Thought Analysis

The AI follows a systematic 5-step process:

1. Read content and identify mentioned countries/regions
2. Distinguish between product sources vs target markets
3. Extract brands, categories, and shopping intents
4. Assign confidence scores based on textual evidence
5. Review and validate findings

## Output

Results are saved in `data/outputs/YYYY-MM-DD/` with detailed JSON including:
- Content analysis (word count, readability, keywords)
- AI-generated tags with confidence scores
- Metadata (URL, timestamp, content length)

## Ground Truth Testing

Test data and expected results are maintained in `tests/ground_truth_regions.json` for systematic validation of region detection accuracy.

## Development

The codebase follows professional Python standards:
- Modular architecture for easy maintenance
- Proper error handling and logging
- Comprehensive documentation
- Git-friendly structure with organized outputs