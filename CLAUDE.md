# Content Analyzer Project Context

## Project Overview
This is a professional content analysis tool for cross-border e-commerce businesses, featuring AI-powered region detection and comprehensive text analysis capabilities.

## Key Features
- **Content Analysis**: Word count, readability scores (Flesch Reading Ease), keyword extraction
- **AI-Powered Tagging**: Automatic extraction of brands, product categories, source regions, target markets
- **Cross-Border E-commerce Focus**: Specialized for international shopping and shipping content
- **Chain of Thought Analysis**: 5-step systematic AI analysis process

## Project Structure
```
content-analyzer/
├── src/                         # Core source code
│   ├── content_analyzer.py      # Text analysis engine (ContentAnalyzer class)
│   ├── auto_tagger.py          # AI tagging system (AutoTagger class)  
│   └── utils.py                # Helper functions (URL fetching, display, file I/O)
├── tests/                       # Test data and validation
│   └── ground_truth_regions.json # Expected results for region detection testing
├── data/                        # Data organization
│   ├── cache/                  # Temporary data storage
│   └── outputs/                # Analysis results organized by date (YYYY-MM-DD/)
├── config/                      # Configuration files
│   └── prompts/                # AI prompt templates
│       └── ecommerce_content_analysis.txt
├── scripts/                     # Entry points and executables
│   └── run_analysis.py         # Main CLI interface
└── requirements.txt            # Python dependencies
```

## Dependencies
- **Core**: requests, beautifulsoup4, openai, python-dotenv
- **Analysis**: Built-in Python libraries for text processing and statistics
- **Requirements**: Python 3.7+ with OpenAI API key

## Usage Patterns
1. **AI Analysis** (recommended): `python scripts/run_analysis.py --auto-tag <url>`
2. **Basic Analysis**: `python scripts/run_analysis.py <file_or_url>`  
3. **Demo Mode**: `python scripts/run_analysis.py`

## Development Commands
- **Install**: `pip install -r requirements.txt`
- **Run Tests**: No automated test framework configured yet
- **Main Entry**: `python scripts/run_analysis.py`

## Configuration
- Requires `.env` file with `OPENAI_API_KEY=your-api-key-here`
- AI prompts stored in `config/prompts/`
- Results automatically saved to `data/outputs/YYYY-MM-DD/`

## Code Architecture
- **Modular Design**: Separate classes for content analysis and AI tagging
- **Professional Standards**: Proper error handling, logging, documentation
- **Clean Separation**: Core logic in src/, entry points in scripts/
- **Data Organization**: Structured outputs with timestamps and metadata

## AI Tagging Categories
- **Brands**: Product brand names (Amazon, Lululemon, etc.)
- **Product Categories**: Product types (Electronics, Athleisure, etc.)
- **Product Source Regions**: Origin countries (US, UK, Japan, etc.)
- **Target User Regions**: Market destinations (Singapore, Malaysia, etc.)
- **Shopping Intent**: Cross-border themes (Price-comparison, How-to-buy, etc.)

## Output Format
- JSON structure with content analysis + AI tags
- Confidence scores for AI-generated tags
- Metadata including URL, timestamp, content length
- Organized by date in `data/outputs/YYYY-MM-DD/`

## Testing Strategy
- Ground truth data in `tests/ground_truth_regions.json`
- Manual validation against known content samples
- No automated testing framework currently implemented